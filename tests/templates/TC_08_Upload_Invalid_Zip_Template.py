import allure
import pytest
from actions.action_factory import ActionFactory
from tests.templates.test_data_inputs import test_data_inputs

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

@allure.feature("Templates")
@allure.story("Invalid Zip File Upload")
@allure.title("Verify uploading a mixed files zip displays invalid zip file error message")
def test_upload_invalid_zip_template(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        template_name = test_data_inputs.invalid_zip_template_name
        description = test_data_inputs.valid_template_description
        mixed_zip_file = test_data_inputs.invalid_mixed_zip_file

        # Click Templates menu
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()

        # Click Upload New Template, enter name, description, and upload mixed files zip
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(mixed_zip_file)
        action_factory.ui_utils.smart_wait()

        # Validate error message "invalid Zip File"
        error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.templates_page.invalid_zip_error)

        if error_visible:
            status = "Pass"
            message = "Error message 'invalid Zip File' displayed as expected."
            action_factory.helpers.attach_screenshot(name="InvalidZipFileError")
            action_factory.helpers.attach_allure(name="Invalid Zip File Upload", text=message)
            assert True, message
        else:
            status = "Fail"
            message = "Error message 'invalid Zip File' was not displayed."
            action_factory.helpers.attach_screenshot(name="InvalidZipFileErrorFailed")
            action_factory.helpers.attach_allure(name="Invalid Zip File Upload", text=message)
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
