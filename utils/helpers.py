import csv
from datetime import datetime
import inspect
import json
import os
import allure
import time
from dotenv import load_dotenv
import logging
import requests
import re
import pytest

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


    def fetch_otp_from_mail_tm(self, email, password, timeout=120):
        # Login
        response = requests.post(
            "https://api.mail.tm/token",
            json={
                "address": email,
                "password": password
            }
        )
        time.sleep(3)
        response.raise_for_status()
        token = response.json()["token"]
        headers = {
            "Authorization": f"Bearer {token}"
        }
        start = time.time()
        while time.time() - start < timeout:
            response = requests.get(
                "https://api.mail.tm/messages",
                headers=headers
            )
            response.raise_for_status()
            messages = response.json()["hydra:member"]
            if messages:
                message_id = messages[0]["id"]
                response = requests.get(
                    f"https://api.mail.tm/messages/{message_id}",
                    headers=headers
                )
                response.raise_for_status()
                body = response.json()["text"]
                otp = re.search(r"\b\d{4,8}\b", body)
                if otp:
                    return otp.group()
            time.sleep(5)
        raise Exception("OTP not received within timeout.")

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