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
@allure.story("Search Template Functionality")
@allure.title("Verify searching for existing and non-existing template names")
def test_search_template_names(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        search_name = test_data_inputs.search_template_name
        non_existing_name = test_data_inputs.non_existing_template_name
        description = test_data_inputs.valid_template_description
        valid_template_file = test_data_inputs.valid_template_file

        # Click on Template menu
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()

        # Create a Template named "AUT_Search_Temp"
        action_factory.templates_actions.upload_new_template(template_name=search_name, description=description)
        action_factory.templates_actions.upload_template_files(valid_template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()
        template_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        if search_name in template_list:
            status = "Pass"
            message = f"Template '{search_name}' is visible in search results."
            action_factory.helpers.attach_screenshot(name="TemplateVisible")
            action_factory.helpers.attach_allure(name="Template Functionality", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template '{search_name}' was not found in search results."
            action_factory.helpers.attach_screenshot(name="TemplateNotFound")
            action_factory.helpers.attach_allure(name="Template Functionality", text=message)
            assert False, message

        # Search for existing template name "AUT_Search_Temp"
        action_factory.templates_actions.search_template_name(search_name)
        action_factory.ui_utils.smart_wait()

        template_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        print(f"Template search results list: {template_list}")

        if search_name in template_list:
            status = "Pass"
            message = f"Searched template '{search_name}' is visible in search results."
            action_factory.helpers.attach_screenshot(name="SearchedTemplateVisible")
            action_factory.helpers.attach_allure(name="Search Template Functionality", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Searched template '{search_name}' was not found in search results."
            action_factory.helpers.attach_screenshot(name="SearchedTemplateNotFound")
            action_factory.helpers.attach_allure(name="Search Template Functionality", text=message)
            assert False, message

        # Search for non-existing template name "Checking_Template_Not_There"
        action_factory.templates_actions.search_template_name(non_existing_name)
        action_factory.ui_utils.smart_wait()

        no_templates_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.templates_page.no_templates_found)
        updated_template_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)

        if no_templates_visible and non_existing_name not in updated_template_list:
            status = "Pass"
            message = f"Non-existing template '{non_existing_name}' is not visible and 'No templates found' message is verified."
            action_factory.helpers.attach_screenshot(name="NoTemplatesFoundVerified")
            action_factory.helpers.attach_allure(name="Search Template Functionality", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Non-existing template search for '{non_existing_name}' failed to show empty results."
            action_factory.helpers.attach_screenshot(name="NoTemplatesFoundVerificationFailed")
            action_factory.helpers.attach_allure(name="Search Template Functionality", text=message)
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
