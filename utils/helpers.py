from asyncio import timeout
import csv
from datetime import datetime
import inspect
import json
import os
import allure
import time
from dotenv import load_dotenv
import logging
import re
import pytest
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class Helpers:

    def __init__(self, page):
        self.page = page
        self.REPORT_FILE = f"reports/TestResults_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.logger = logging.getLogger(__name__)
        load_dotenv()

    def fetch_dotenv(self, key):
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"{key} not found in .env")
        if value.startswith("QA_"):
            referenced_value = os.getenv(value)
            if referenced_value is None:
                raise ValueError(f"Referenced variable '{value}' not found in .env")
            return referenced_value
        return value

    def write_test_results(self, status, message=""):
        test_name = inspect.stack()[1].function
        os.makedirs("reports", exist_ok=True)
        file_exists = os.path.exists(self.REPORT_FILE)
        with open(self.REPORT_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow([
                    "Test Name",
                    "Status",
                    "Execution Time",
                    "Message"
                ])
            writer.writerow([
                test_name,
                status,
                datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                message
            ])

    def handle_failure(self, message=""):
        self.logger.error(f"Test failed: {message}")

        try:
            self.attach_screenshot(
                name="Last Seen Screenshot",
                full_page=True
            )
        except Exception as screenshot_error:
            self.logger.error(f"Failed to capture failure screenshot: {screenshot_error}")
        try:
            self.attach_allure(
                name="Failure Stack Trace",
                text=message
            )
        except Exception as allure_error:
            self.logger.error(f"Failed to attach failure log to Allure: {allure_error}")

    def attach_screenshot(self, name="Screenshot", full_page=True):
        try:
            test_folder = getattr(pytest, "current_test_folder", "")
            test_file = getattr(pytest, "current_test_file", "")
            if test_folder and test_file:
                screenshot_dir = os.path.join("screenshots", test_folder, test_file)
            else:
                screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)

            safe_name = re.sub(r'[^\w\-_\. ]', '_', name)
            file_path = os.path.join(screenshot_dir, f"{safe_name}.png")

            screenshot_bytes = self.page.screenshot(path=file_path, full_page=full_page)
            allure.attach(
                screenshot_bytes,
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
            self.logger.info(f"Screenshot saved locally at: {file_path} and attached to Allure: {name}")
            return file_path
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot. Error: {e}")
            raise

    def attach_allure(self, name="Attachment", text=""):
        try:
            allure.attach(text, name=name,
                attachment_type=allure.attachment_type.TEXT
            )
            self.logger.info(f"Allure attachment added: {name}")
        except Exception as e:
            self.logger.error(f"Failed to attach text to Allure report. Error: {e}")
            raise


    def fetch_otp_from_gmail(self, timeout=120):
        """
        Fetch OTP from the dedicated Gmail automation account.
        Required in .env:
            GMAIL_CLIENT_ID
            GMAIL_CLIENT_SECRET
            GMAIL_REFRESH_TOKEN
        """
        client_id = self.fetch_dotenv("GMAIL_CLIENT_ID")
        client_secret = self.fetch_dotenv("GMAIL_CLIENT_SECRET")
        refresh_token = self.fetch_dotenv("GMAIL_REFRESH_TOKEN")

        if not client_id:
            raise ValueError("GMAIL_CLIENT_ID is not configured in .env")
        if not client_secret:
            raise ValueError("GMAIL_CLIENT_SECRET is not configured in .env")
        if not refresh_token:
            raise ValueError("GMAIL_REFRESH_TOKEN is not configured in .env")

        # Record start timestamp (in ms) to ignore any emails received before this function call
        # Give a 15-second buffer for slight clock skew
        start_time_epoch = int(time.time())
        min_internal_date_ms = int((start_time_epoch - 15) * 1000)

        # Create Gmail OAuth credentials
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=["https://www.googleapis.com/auth/gmail.readonly"]
        )

        # Connect to Gmail API
        service = build("gmail", "v1", credentials=creds)
        start = time.time()
        while time.time() - start < timeout:
            print("Checking Gmail for new OTP...")
            try:
                # Query recent emails received after function start time
                query = f'(from:no-reply@objectways.com OR subject:TensorAct OR subject:verification) after:{start_time_epoch - 15}'
                response = service.users().messages().list(
                    userId="me",
                    q=query,
                    maxResults=10
                ).execute()

                messages = response.get("messages", [])

                for message in messages:
                    message_id = message["id"]
                    message_data = service.users().messages().get(
                        userId="me",
                        id=message_id,
                        format="full"
                    ).execute()

                    # Check email received timestamp to ignore older emails
                    internal_date = int(message_data.get("internalDate", 0))
                    if internal_date < min_internal_date_ms:
                        continue

                    snippet = message_data.get("snippet", "")
                    payload = message_data.get("payload", {})
                    body = self._extract_gmail_body(payload)

                    combined_text = f"{snippet} {body}"

                    # Match 6-digit code or code after verification text
                    otp_match = (
                        re.search(r"verification code.*?\b(\d{4,8})\b", combined_text, re.IGNORECASE | re.DOTALL) or
                        re.search(r"\b(\d{6})\b", combined_text) or
                        re.search(r"\b(\d{4,8})\b", combined_text)
                    )

                    if otp_match:
                        otp_value = otp_match.group(1) if otp_match.groups() else otp_match.group(0)
                        print(f"NEW OTP received successfully: {otp_value}")
                        return otp_value

            except Exception as e:
                print(f"Gmail API error: {e}")

            # Wait before checking Gmail again
            print("New OTP email not received yet. Waiting 5 seconds...")
            time.sleep(5)

        raise Exception(f"OTP not received within {timeout} seconds.")

    def _extract_gmail_body(self, payload):
        """
        Extract text content from Gmail message payload.
        Handles single-part, multipart, and nested multipart messages.
        """
        body = ""
        parts = payload.get("parts", [])
        if parts:
            for part in parts:
                mime_type = part.get("mimeType", "")
                if mime_type in ["text/plain", "text/html"]:
                    data = part.get("body", {}).get("data")
                    if data:
                        try:
                            body += base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                        except Exception as e:
                            print(f"Failed to decode Gmail part body: {e}")
                if part.get("parts"):
                    body += self._extract_gmail_body(part)
        else:
            data = payload.get("body", {}).get("data")
            if data:
                try:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                except Exception as e:
                    print(f"Failed to decode Gmail body: {e}")
        return body

    def resolve_next_index(self, existing_list, pattern):
        if "{i}" not in pattern:
            return 1
        i = 1
        while pattern.format(i=i) in existing_list:
            i += 1
        return i

    def resolve_latest_index(self, existing_list, pattern):
        if "{i}" not in pattern:
            return 1
        matched_indices = []
        for name in existing_list:
            prefix, suffix_pat = pattern.split("{i}", 1)
            escaped_prefix = re.escape(prefix)
            escaped_suffix = re.escape(suffix_pat)
            match = re.match(rf"^{escaped_prefix}(\d+){escaped_suffix}$", name)
            if match:
                matched_indices.append(int(match.group(1)))
        if matched_indices:
            return max(matched_indices)
        return 1

    def save_runtime_data(self, key, value, filepath="reports/execution_state.json"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data = {}
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        data[key] = value
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def get_runtime_data(self, key, default=None, filepath="reports/execution_state.json"):
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get(key, default)
            except Exception:
                pass
        return default