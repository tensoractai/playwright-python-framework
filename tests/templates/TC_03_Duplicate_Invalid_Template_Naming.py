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
@allure.story("Duplicate and Invalid Template Naming Validation")
@allure.title("Verify prevention of creating templates with duplicate, invalid special character, and case-insensitive names")
def test_duplicate_invalid_template_naming(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        duplicate_name = test_data_inputs.duplicate_template_name
        special_char_name = test_data_inputs.special_char_template_name
        capital_duplicate_name = test_data_inputs.capital_duplicate_template_name
        description = test_data_inputs.valid_template_description
        valid_template_file = test_data_inputs.valid_template_file

        # Click on Template menu
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()

        # Create initial Template with Name "AUT_Template_Duplicate"
        action_factory.templates_actions.upload_new_template(template_name=duplicate_name, description=description)
        action_factory.templates_actions.upload_template_files(valid_template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()
        template_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        if duplicate_name in template_name_list:
            status = "Pass"
            message = f"Template '{duplicate_name}' created successfully."
            action_factory.helpers.attach_screenshot(name="TemplateCreatedSuccessfully")
            action_factory.helpers.attach_allure(name="Upload Valid Template", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template '{duplicate_name}' was not found in the templates list."
            action_factory.helpers.attach_screenshot(name="TemplateCreationValidationFailed")
            action_factory.helpers.attach_allure(name="Upload Valid Template", text=message)
            assert False, message

        # Attempt to create another Template with the exact same name "AUT_Template_Duplicate"
        action_factory.templates_actions.upload_new_template(template_name=duplicate_name, description=description)
        action_factory.templates_actions.upload_template_files(valid_template_file)
        action_factory.ui_utils.smart_wait()

        duplicate_error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.templates_page.template_exists_error)
        if duplicate_error_visible:
            status = "Pass"
            message = f"Error message for duplicate template name '{duplicate_name}' displayed properly."
            action_factory.helpers.attach_screenshot(name="DuplicateTemplateNameError")
            action_factory.helpers.attach_allure(name="Duplicate Template Name Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Error message for duplicate template name '{duplicate_name}' was not displayed."
            action_factory.helpers.attach_screenshot(name="DuplicateTemplateNameErrorFailed")
            action_factory.helpers.attach_allure(name="Duplicate Template Name Validation", text=message)
            assert False, message

        # Close/Cancel popup
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        # Attempt to create Template with Special Characters "AUT_@$%%$_Hello"
        action_factory.templates_actions.upload_new_template(template_name=special_char_name, description=description)
        action_factory.templates_actions.upload_template_files(valid_template_file)
        action_factory.ui_utils.smart_wait()

        special_char_error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.templates_page.template_invalid_name_error)
        if special_char_error_visible:
            status = "Pass"
            message = f"Error message for invalid special characters template name '{special_char_name}' displayed properly."
            action_factory.helpers.attach_screenshot(name="SpecialCharTemplateNameError")
            action_factory.helpers.attach_allure(name="Special Char Template Name Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Error message for invalid special characters template name '{special_char_name}' was not displayed."
            action_factory.helpers.attach_screenshot(name="SpecialCharTemplateNameErrorFailed")
            action_factory.helpers.attach_allure(name="Special Char Template Name Validation", text=message)
            assert False, message

        # Close/Cancel popup
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        # Attempt to create Template with Capitalized Duplicate Name "AUT_TEMPLATE_DUPLICATE"
        action_factory.templates_actions.upload_new_template(template_name=capital_duplicate_name, description=description)
        action_factory.ui_utils.smart_wait()

        capital_duplicate_error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.templates_page.template_exists_error)
        if capital_duplicate_error_visible:
            status = "Pass"
            message = f"Error message for case-insensitive duplicate template name '{capital_duplicate_name}' displayed properly."
            action_factory.helpers.attach_screenshot(name="CapitalDuplicateTemplateNameError")
            action_factory.helpers.attach_allure(name="Capital Duplicate Template Name Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Error message for case-insensitive duplicate template name '{capital_duplicate_name}' was not displayed."
            action_factory.helpers.attach_screenshot(name="CapitalDuplicateTemplateNameErrorFailed")
            action_factory.helpers.attach_allure(name="Capital Duplicate Template Name Validation", text=message)
            assert False, message

        # Close/Cancel popup
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

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
