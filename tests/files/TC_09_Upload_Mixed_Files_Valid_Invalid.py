import allure
import pytest
from actions.action_factory import ActionFactory
from test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    password = action_factory.helpers.fetch_dotenv("company_Password")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
    diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
    diff_email_password = action_factory.helpers.fetch_dotenv(
        "different_email_for_otp_password"
    )
    # Login
    action_factory.login_actions.perform_login(
        url=url,
        email=email,
        password=password
    )
    action_factory.login_actions.use_different_email_OTP(
        diff_email,
        diff_email_password
    )
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("Files")
@allure.story("Upload Mixed Files Valid and Invalid Both Files")
@allure.title("Upload Mixed Files Valid and Invalid Both Files")
def test_Upload_Mixed_Files_Valid_Invalid(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        Mixed_Files = test_data_inputs.Mixed_Files

        # upload Mixed Files :: 
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.files_actions.upload_files_without_uploadbtn(*Mixed_Files)
        action_factory.ui_utils.smart_wait()
        invalid_error = action_factory.ui_utils.is_element_visible(action_factory.page_factory.files_page.invalid_file_error)
        if invalid_error:
            status = "Pass"
            message = f"Invalid file error is visible."
            action_factory.helpers.attach_screenshot(name="InvalidFileError")
            action_factory.helpers.attach_allure(name="Invalid File Error", text="Invalid file error is visible")
            assert True, message
        else:
            status = "Fail"
            message = f"Invalid file error is not visible."
            action_factory.helpers.attach_screenshot(name="InvalidFileErrorFailed")
            action_factory.helpers.attach_allure(name="Invalid File Error", text="Invalid file error is not visible")
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.upload_button.nth(1))
        action_factory.ui_utils.smart_wait()
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")


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



