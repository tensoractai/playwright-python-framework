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
@allure.story("Template Name and Description Boundary Input Validation")
@allure.title("Verify creating a template with 50-character name and 2000-character description")
def test_template_boundary_input_validation(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        name_50_chars = test_data_inputs.template_name_50_chars
        desc_2000_chars = test_data_inputs.template_desc_2000_chars
        valid_template_file = test_data_inputs.valid_template_file

        # Click Templates menu
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()

        # Click Create New Template, enter 50-char name, 2000-char description, and upload file
        action_factory.templates_actions.upload_new_template(template_name=name_50_chars, description=desc_2000_chars)
        action_factory.templates_actions.upload_template_files(valid_template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Validate 50-char Template Name is accepted and visible in template list
        template_list = action_factory.ui_utils.grab_text_from_all(
            action_factory.page_factory.templates_page.template_names_list
        )
        print(f"Template names list: {template_list}")

        if name_50_chars in template_list:
            status = "Pass"
            message = f"Template with 50-char name '{name_50_chars}' and 2000-char description created successfully."
            action_factory.helpers.attach_screenshot(name="TemplateBoundaryInputAccepted")
            action_factory.helpers.attach_allure(name="Template Boundary Input Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template with 50-char name '{name_50_chars}' was not found in template list."
            action_factory.helpers.attach_screenshot(name="TemplateBoundaryInputFailed")
            action_factory.helpers.attach_allure(name="Template Boundary Input Validation", text=message)
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
