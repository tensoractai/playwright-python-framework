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
@allure.story("Update Template Functionality")
@allure.title("Verify creating a template, clicking Update button, uploading a new zip file, and validating toast message")
def test_update_template_functionality(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        template_name = test_data_inputs.update_template_name
        description = test_data_inputs.valid_template_description
        initial_file = test_data_inputs.valid_template_file
        updated_file = test_data_inputs.updated_template_file

        # Click Templates menu
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()

        # Create template and validate creation
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(initial_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        template_names = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        if template_name in template_names:
            status = "Pass"
            message  = "Template updated successfully with new zip file."
            action_factory.helpers.attach_screenshot(name="TemplateUpdatedSuccessfully")
            action_factory.helpers.attach_allure(name="Update Template Functionality", text=message)
            assert True, message
        else:
            status = "Fail"
            message  = "Template not found after creation."
            action_factory.helpers.attach_screenshot(name="TemplateNotFoundAfterCreation")
            action_factory.helpers.attach_allure(name="Update Template Functionality", text=message)
            assert False, message
            
        # Click Update button and upload new Zip file
        action_factory.templates_actions.update_template(template_name, updated_file)

        # Validate toast message "Template updated successfully"
        action_factory.templates_actions.validate_template_toast_msg("Template updated successfully")
        action_factory.ui_utils.smart_wait()

        template_names = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        if template_name in template_names:
            status = "Pass"
            message  = "Template updated successfully after update button click."
            action_factory.helpers.attach_screenshot(name="TemplateUpdatedSuccessfullyAfterUpdate")
            action_factory.helpers.attach_allure(name="Update Template Functionality", text=message)
            assert True, message
        else:
            status = "Fail"
            message  = "Template not found after update."
            action_factory.helpers.attach_screenshot(name="TemplateNotFoundAfterUpdate")
            action_factory.helpers.attach_allure(name="Update Template Functionality", text=message)
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
