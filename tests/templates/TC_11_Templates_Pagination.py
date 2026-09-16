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
@allure.story("Templates Pagination Check")
@allure.title("Verify templates pagination control for limits 5, 10, 20, and 50 with creation and tab switching")
def test_templates_pagination(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        template_name = test_data_inputs.pagination_template_name
        description = test_data_inputs.valid_template_description
        template_file = test_data_inputs.valid_template_file

        # Click Templates menu
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()

        # Check pagination for 5
        action_factory.templates_actions.set_templates_pagination("5")
        template_count = action_factory.page_factory.templates_page.template_names_list.count()
        if template_count <= 5:
            status = "Pass"
            message = f"Template count ({template_count}) is within limit for pagination 5."
            action_factory.helpers.attach_screenshot(name="TemplatesPagination5Pass")
            action_factory.helpers.attach_allure(name="Templates Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template count ({template_count}) exceeds limit of 5."
            action_factory.helpers.attach_screenshot(name="TemplatesPagination5Failed")
            action_factory.helpers.attach_allure(name="Templates Pagination Check", text=message)
            assert False, message

        # After setting Pagination 5, create new template and verify pagination persistence
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        template_count_after_create = action_factory.page_factory.templates_page.template_names_list.count()
        if template_count_after_create <= 5:
            status = "Pass"
            message = f"Template count ({template_count_after_create}) remains <= 5 after creating a new template."
            action_factory.helpers.attach_screenshot(name="PaginationPreservedAfterTemplateCreation")
            action_factory.helpers.attach_allure(name="Templates Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template count ({template_count_after_create}) exceeded limit of 5 after template creation."
            action_factory.helpers.attach_screenshot(name="PaginationNotPreservedAfterCreation")
            action_factory.helpers.attach_allure(name="Templates Pagination Check", text=message)
            assert False, message

        # After setting pagination 5, switch to Datasets menu and come back to Templates page
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()

        template_count_after_switch = action_factory.page_factory.templates_page.template_names_list.count()
        if template_count_after_switch <= 5:
            status = "Pass"
            message = f"Template count ({template_count_after_switch}) remains <= 5 after switching menu and returning."
            action_factory.helpers.attach_screenshot(name="PaginationPreservedAfterMenuSwitch")
            action_factory.helpers.attach_allure(name="Templates Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template count ({template_count_after_switch}) exceeded limit of 5 after menu switch."
            action_factory.helpers.attach_screenshot(name="PaginationNotPreservedAfterSwitch")
            action_factory.helpers.attach_allure(name="Templates Pagination Check", text=message)
            assert False, message

        # Check pagination for 10
        action_factory.templates_actions.set_templates_pagination("10")
        template_count = action_factory.page_factory.templates_page.template_names_list.count()
        if template_count <= 10:
            status = "Pass"
            message = f"Template count ({template_count}) is within limit for pagination 10."
            action_factory.helpers.attach_screenshot(name="TemplatesPagination10Pass")
            action_factory.helpers.attach_allure(name="Templates Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template count ({template_count}) exceeds limit of 10."
            action_factory.helpers.attach_screenshot(name="TemplatesPagination10Failed")
            action_factory.helpers.attach_allure(name="Templates Pagination Check", text=message)
            assert False, message

        # Check pagination for 20
        action_factory.templates_actions.set_templates_pagination("20")
        template_count = action_factory.page_factory.templates_page.template_names_list.count()
        if template_count <= 20:
            status = "Pass"
            message = f"Template count ({template_count}) is within limit for pagination 20."
            action_factory.helpers.attach_screenshot(name="TemplatesPagination20Pass")
            action_factory.helpers.attach_allure(name="Templates Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template count ({template_count}) exceeds limit of 20."
            action_factory.helpers.attach_screenshot(name="TemplatesPagination20Failed")
            action_factory.helpers.attach_allure(name="Templates Pagination Check", text=message)
            assert False, message

        # Check pagination for 50
        action_factory.templates_actions.set_templates_pagination("50")
        template_count = action_factory.page_factory.templates_page.template_names_list.count()
        if template_count <= 50:
            status = "Pass"
            message = f"Template count ({template_count}) is within limit for pagination 50."
            action_factory.helpers.attach_screenshot(name="TemplatesPagination50Pass")
            action_factory.helpers.attach_allure(name="Templates Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template count ({template_count}) exceeds limit of 50."
            action_factory.helpers.attach_screenshot(name="TemplatesPagination50Failed")
            action_factory.helpers.attach_allure(name="Templates Pagination Check", text=message)
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
