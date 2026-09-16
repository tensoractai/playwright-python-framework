import allure
import pytest
from actions.action_factory import ActionFactory
from tests.files.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    password = action_factory.helpers.fetch_dotenv("company_Password")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
    diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
    diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")
    
    # Login & Setup
    action_factory.login_actions.perform_login(url=url, email=email, password=password)
    action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("Files")
@allure.story("Click Upload Files button on Files page")
@allure.title("Validate Upload Files modal tabs options")
def test_validate_upload_files_tabs(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        expected_tabs = test_data_inputs.upload_files_tabs

        # Click Files menu
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.ui_utils.smart_wait()

        # Click Upload Files button
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.upload_files_button)
        action_factory.ui_utils.smart_wait()

        # Grab all text from upload_files_tabs
        actual_tabs = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.files_page.upload_files_tabs)
        print(f"Actual Upload Files tabs: {actual_tabs}")

        # Validate expected tabs in actual tabs
        if actual_tabs == expected_tabs:
            status = "Pass"
            message = f"Upload Files modal tabs verified successfully: {actual_tabs}"
            action_factory.helpers.attach_screenshot(name="UploadFilesTabsVerified")
            action_factory.helpers.attach_allure(name="Validate Upload Files Tabs", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Expected tabs {expected_tabs}, but found {actual_tabs}"
            action_factory.helpers.attach_screenshot(name="UploadFilesTabsVerificationFailed")
            action_factory.helpers.attach_allure(name="Validate Upload Files Tabs", text=message)
            assert False, message

    except Exception as e:
        status = "Fail"
        message = str(e)
        action_factory.helpers.handle_failure(message=message)
        raise

    finally:
        action_factory.helpers.write_test_results(
            status=status,
            message=message
        )
