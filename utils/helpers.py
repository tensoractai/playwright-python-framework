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
import requests
import msal

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

    def fetch_otp_from_microsoft(self, timeout=120):
        """
        Fetch OTP from the dedicated Microsoft 365 automation mailbox.

        Required in .env:
            MICROSOFT_TENANT_ID
            MICROSOFT_CLIENT_ID
            MICROSOFT_CLIENT_SECRET
            different_email_for_otp
        """

        tenant_id = self.fetch_dotenv("MICROSOFT_TENANT_ID")
        client_id = self.fetch_dotenv("MICROSOFT_CLIENT_ID")
        client_secret = self.fetch_dotenv("MICROSOFT_CLIENT_SECRET")
        otp_email = os.getenv("MICROSOFT_OTP_EMAIL") or os.getenv("different_email_for_otp")
        if not tenant_id: raise ValueError("MICROSOFT_TENANT_ID is not configured in .env")
        if not client_id: raise ValueError("MICROSOFT_CLIENT_ID is not configured in .env")
        if not client_secret: raise ValueError("MICROSOFT_CLIENT_SECRET is not configured in .env")
        if not otp_email: raise ValueError("MICROSOFT_OTP_EMAIL or different_email_for_otp is not configured in .env")

        authority = f"https://login.microsoftonline.com/{tenant_id}"
        scope = ["https://graph.microsoft.com/.default"]
        app = msal.ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_secret,
            authority=authority
        )
        start_time = time.time()
        min_received_time = start_time - 15
        while time.time() - start_time < timeout:
            print("Checking Microsoft mailbox for new OTP...")
            try:
                token_result = app.acquire_token_for_client(scopes=scope)
                if "access_token" not in token_result:
                    error = token_result.get("error")
                    description = token_result.get("error_description")
                    raise Exception(f"Microsoft authentication failed: {error} - {description}")
                access_token = token_result["access_token"]
                headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
                endpoint = f"https://graph.microsoft.com/v1.0/users/{otp_email}/mailFolders/inbox/messages"
                params = {
                    "$top": "10",
                    "$orderby": "receivedDateTime desc",
                    "$select": "id,subject,from,receivedDateTime,bodyPreview,body"
                }
                response = requests.get(endpoint, headers=headers, params=params, timeout=30)
                response.raise_for_status()
                messages = response.json().get("value", [])
                for message in messages:
                    received_time = message.get("receivedDateTime", "")
                    if received_time:
                        try:
                            received_dt = datetime.fromisoformat(
                                received_time.replace("Z", "+00:00")
                            )
                            if received_dt.timestamp() < min_received_time:
                                continue
                        except Exception as e:
                            print(f"Unable to parse received time: {e}")

                    subject = message.get("subject", "")
                    body_preview = message.get("bodyPreview", "")
                    body_content = message.get("body", {}).get("content", "")
                    clean_body = re.sub(r'<[^>]+>', ' ', body_content)
                    combined_text = f"{subject} {body_preview} {clean_body}"

                    otp_match = (
                        re.search(r"(?:one-time password|otp|verification code).*?\b(\d{4,8})\b", combined_text, re.IGNORECASE | re.DOTALL) or
                        re.search(r"\b(\d{6})\b", combined_text) or
                        re.search(r"\b(\d{4,8})\b", combined_text)
                    )
                    if otp_match:
                        otp_value = otp_match.group(1) if otp_match.groups() else otp_match.group(0)
                        print(f"NEW OTP received successfully: {otp_value}")
                        return otp_value
            except requests.RequestException as e:
                err_msg = str(e)
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        err_msg += f" | Details: {e.response.text}"
                    except Exception:
                        pass
                print(f"Microsoft Graph API error: {err_msg}")
            except Exception as e:
                print(f"Microsoft OTP fetch error: {e}")
            print("New OTP email not received yet. Waiting 5 seconds...")
            time.sleep(5)
        raise Exception(f"OTP not received within {timeout} seconds.")


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