import allure
import pytest
from actions.action_factory import ActionFactory
from tests.projects.test_data_inputs import test_data_inputs

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

@allure.feature("Projects")
@allure.story("Create Invalid Project")
@allure.title("Verify validation errors for duplicate project names, special characters, and DB queries")
def test_Create_Invalid_Project_Validation_Errors(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        existing_project_name = test_data_inputs.valid_project_Name
        existing_dataset_name = test_data_inputs.valid_dataset_Name
        existing_workflow_name = test_data_inputs.valid_workflow_Name
        special_char_name = test_data_inputs.special_char_project_name
        db_query_project_names = test_data_inputs.db_query_project_names

        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()

        # Duplicate Project Name Validation
        action_factory.projects_actions.create_project(project_name=existing_project_name, dataset_name=existing_dataset_name,workflow_name=existing_workflow_name)
        action_factory.ui_utils.smart_wait()
        duplicate_error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.projects_page.duplicate_project_warning, timeout=5000) 
        
        if duplicate_error_visible:
            status = "Pass"
            message = f"Error displayed when using duplicate project name: {existing_project_name}"
            action_factory.helpers.attach_screenshot(name="DuplicateProjectErrorVisible")
            action_factory.helpers.attach_allure(name="Duplicate Project Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Duplicate project error message not displayed for project name '{existing_project_name}'."
            action_factory.helpers.attach_screenshot(name="DuplicateProjectErrorMissing")
            action_factory.helpers.attach_allure(name="Duplicate Project Validation", text=message)
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        # Special Characters Validation
        action_factory.projects_actions.create_project(project_name=special_char_name,dataset_name=existing_dataset_name,workflow_name=existing_workflow_name)
        action_factory.ui_utils.smart_wait()

        special_char_error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.projects_page.invalid_name_error, timeout=5000)
        if special_char_error_visible:
            status = "Pass"
            message = f"Error displayed for special character name: {special_char_name}"
            action_factory.helpers.attach_screenshot(name="SpecialCharErrorVisible")
            action_factory.helpers.attach_allure(name="Special Characters Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Invalid character error message not displayed for project name '{special_char_name}'."
            action_factory.helpers.attach_screenshot(name="SpecialCharErrorMissing")
            action_factory.helpers.attach_allure(name="Special Characters Validation", text=message)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        # DB Query Names Validation ("DROP", "DELETE")
        action_factory.projects_actions.create_project(project_name=db_query_project_names,dataset_name=existing_dataset_name,workflow_name=existing_workflow_name)
        action_factory.ui_utils.smart_wait()
        db_query_error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.projects_page.invalid_name_error, timeout=5000)
        if db_query_error_visible:
            status = "Pass"
            message = f"Error displayed for DB query name: {db_query_project_names}"
            action_factory.helpers.attach_screenshot(name=f"DBQueryErrorVisible_{db_query_project_names}")
            action_factory.helpers.attach_allure(name="DB Query Name Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Invalid character/query error message not displayed for DB query name '{db_query_project_names}'."
            action_factory.helpers.attach_screenshot(name=f"DBQueryErrorMissing_{db_query_project_names}")
            action_factory.helpers.attach_allure(name="DB Query Name Validation", text=message)
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
