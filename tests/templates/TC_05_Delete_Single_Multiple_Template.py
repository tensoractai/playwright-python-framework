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
@allure.story("Delete Single and Multiple Templates Functionality")
@allure.title("Verify deletion of single and multiple template items")
def test_delete_single_multiple_templates(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        template_names = test_data_inputs.delete_template_names
        description = test_data_inputs.valid_template_description
        text_template_file = test_data_inputs.text_template_file

        # Click on Template menu
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()

        # Create 4 Templates
        for t_name in template_names:
            action_factory.templates_actions.upload_new_template(template_name=t_name, description=description)
            action_factory.templates_actions.upload_template_files(text_template_file)
            action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
            action_factory.ui_utils.smart_wait()

        # Delete first Template "AUT_Delete_Template_1"
        first_template = template_names[0]
        action_factory.templates_actions.delete_template(first_template)
        action_factory.ui_utils.smart_wait()
        popup_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.templates_page.template_delete_success_msg)
        if popup_visible:
            status = "Pass"
            message = f"Single template '{first_template}' deleted successfully."
            action_factory.helpers.attach_screenshot(name="SingleTemplateDeletedSuccessfully")
            action_factory.helpers.attach_allure(name="Delete Single Template", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Single template '{first_template}' was not deleted."
            action_factory.helpers.attach_screenshot(name="SingleTemplateDeletionFailed")
            action_factory.helpers.attach_allure(name="Delete Single Template", text=message)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        template_list = action_factory.ui_utils.grab_text_from_all(
            action_factory.page_factory.templates_page.template_names_list
        )
        if first_template not in template_list:
            status = "Pass"
            message = f"Single template '{first_template}' deleted successfully."
            action_factory.helpers.attach_screenshot(name="SingleTemplateDeletedSuccessfully")
            action_factory.helpers.attach_allure(name="Delete Single Template", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Single template '{first_template}' was not deleted."
            action_factory.helpers.attach_screenshot(name="SingleTemplateDeletionFailed")
            action_factory.helpers.attach_allure(name="Delete Single Template", text=message)
            assert False, message

        # Step 4: Delete remaining 3 Templates
        remaining_templates = template_names[1:]
        action_factory.templates_actions.delete_template(remaining_templates)
        action_factory.ui_utils.smart_wait()
        popup_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.templates_page.template_delete_success_msg)
        if popup_visible:
            status = "Pass"
            message = f"Single template '{first_template}' deleted successfully."
            action_factory.helpers.attach_screenshot(name="SingleTemplateDeletedSuccessfully")
            action_factory.helpers.attach_allure(name="Delete Single Template", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Single template '{first_template}' was not deleted."
            action_factory.helpers.attach_screenshot(name="SingleTemplateDeletionFailed")
            action_factory.helpers.attach_allure(name="Delete Single Template", text=message)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        final_template_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        deleted_present = [name for name in template_names if name in final_template_list]

        if not deleted_present:
            status = "Pass"
            message = "All 4 templates deleted successfully and verified."
            action_factory.helpers.attach_screenshot(name="AllTemplatesDeletedSuccessfully")
            action_factory.helpers.attach_allure(name="Delete Multiple Templates", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to delete templates: {deleted_present}"
            action_factory.helpers.attach_screenshot(name="MultipleTemplatesDeletionFailed")
            action_factory.helpers.attach_allure(name="Delete Multiple Templates", text=message)
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
