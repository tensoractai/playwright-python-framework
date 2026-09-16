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
@allure.story("Upload Valid Template")
@allure.title("Verify uploading a valid template file and toast message validation")
def test_upload_valid_template(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        template_name = test_data_inputs.valid_template_name
        description = test_data_inputs.valid_template_description
        template_file = test_data_inputs.valid_template_file

        # Click on Template menu
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()

        # Click Upload New Template, enter name, description, and upload template file
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Validate Template is present in the templates list
        template_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        
        if template_name in template_name_list:
            status = "Pass"
            message = f"Template '{template_name}' created and displayed successfully."
            action_factory.helpers.attach_screenshot(name="TemplateCreatedSuccessfully")
            action_factory.helpers.attach_allure(name="Upload Valid Template", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template '{template_name}' was not found in the templates list."
            action_factory.helpers.attach_screenshot(name="TemplateCreationValidationFailed")
            action_factory.helpers.attach_allure(name="Upload Valid Template", text=message)
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
