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
@allure.story("Cancel File Upload Operation")
@allure.title("Verify cancelling file upload process while uploading multiple files")
def test_cancel_file_upload_operation(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        files_to_upload = test_data_inputs.Files_cancel_scenario

        # Click Files menu
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.ui_utils.smart_wait()
        # Select files to upload
        action_factory.datasets_actions.upload_files_with_uploadBtn(*files_to_upload)
        # Cancel the upload using files_actions method
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.uploading_btn)
        action_factory.files_actions.cancel_file_upload()

        # Validate upload was cancelled and popup/dialog is closed
        upload_button_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.datasets_page.upload_files_button)

        if upload_button_visible:
            status = "Pass"
            message = "File upload instance was cancelled successfully."
            action_factory.helpers.attach_screenshot(name="FileUploadCancelledSuccessfully")
            action_factory.helpers.attach_allure(name="Cancel File Upload Operation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = "File upload cancellation failed or UI did not reset."
            action_factory.helpers.attach_screenshot(name="FileUploadCancellationFailed")
            action_factory.helpers.attach_allure(name="Cancel File Upload Operation", text=message)
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
