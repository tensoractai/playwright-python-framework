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
@allure.story("Delete Projects")
@allure.title("Verify deleting single project and bulk deleting multiple projects")
def test_Delete_Single_And_Bulk_Projects(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        dataset_name = test_data_inputs.valid_dataset_Name
        workflow_name = test_data_inputs.valid_workflow_Name
        delete_projects = test_data_inputs.delete_project_names

        # Navigate to Projects Menu
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()

        # Create 4 projects using dataset and workflow
        for p_name in delete_projects:
            existing_projects = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
            if p_name not in existing_projects:
                action_factory.projects_actions.create_project(
                    project_name=p_name,
                    dataset_name=dataset_name,
                    workflow_name=workflow_name
                )
                action_factory.ui_utils.smart_wait()

        # Single Project Deletion Validation
        single_project = delete_projects[0]
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.return_file_checkbox(single_project).first)
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.delete_toolbar_btn)
        action_factory.ui_utils.smart_wait()

        delete_popup = action_factory.ui_utils.wait_for_visible_if_exists(action_factory.page_factory.files_page.delete_confirmation)
        if delete_popup:
            action_factory.ui_utils.fill_input(action_factory.page_factory.files_page.delete_text, "DELETE")
            action_factory.ui_utils.click_element(action_factory.page_factory.files_page.delete_btn)
            action_factory.ui_utils.smart_wait()
        else:
            raise Exception("Deletion confirmation popup not displayed for single project deletion.")

        success_popup = action_factory.ui_utils.is_element_visible(action_factory.page_factory.projects_page.project_delete_success)
        if success_popup :
            status = "Pass"
            message = f"Project '{single_project}' was deleted successfully after removing dataset association."
            action_factory.helpers.attach_screenshot(name="SingleProjectDeletedSuccess")
            action_factory.helpers.attach_allure(name="Single Project Deletion", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{single_project}' was not deleted after removing dataset association."
            action_factory.helpers.attach_screenshot(name="SingleProjectDeleteFailed")
            action_factory.helpers.attach_allure(name="Single Project Deletion", text=message)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()
        
        projects_after_single_del = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        if single_project not in projects_after_single_del:
            status = "Pass"
            message = f"Single project '{single_project}' deleted successfully."
            action_factory.helpers.attach_screenshot(name="SingleProjectDeletedSuccess")
            action_factory.helpers.attach_allure(name="Single Project Deletion", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Single project '{single_project}' was not deleted."
            action_factory.helpers.attach_screenshot(name="SingleProjectDeleteFailed")
            action_factory.helpers.attach_allure(name="Single Project Deletion", text=message)
            assert False, message

        # Bulk 3 Projects Deletion Validation
        bulk_projects = delete_projects[1:]
        for b_name in bulk_projects:
            action_factory.ui_utils.click_element(action_factory.page_factory.files_page.return_file_checkbox(b_name).first)

        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.delete_toolbar_btn)
        action_factory.ui_utils.smart_wait()

        bulk_delete_popup = action_factory.ui_utils.wait_for_visible_if_exists(action_factory.page_factory.files_page.delete_confirmation)
        if bulk_delete_popup:
            action_factory.ui_utils.fill_input(action_factory.page_factory.files_page.delete_text, "DELETE")
            action_factory.ui_utils.click_element(action_factory.page_factory.files_page.delete_btn)
            action_factory.ui_utils.smart_wait()
        else:
            raise Exception("Deletion confirmation popup not displayed for bulk project deletion.")

        success_popup = action_factory.ui_utils.is_element_visible(action_factory.page_factory.projects_page.project_delete_success)
        if success_popup :
            status = "Pass"
            message = f"Project '{bulk_projects}' was deleted successfully after removing dataset association."
            action_factory.helpers.attach_screenshot(name="BulkProjectsDeletedSuccess")
            action_factory.helpers.attach_allure(name="Bulk Projects Deletion", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{bulk_projects}' was not deleted after removing dataset association."
            action_factory.helpers.attach_screenshot(name="BulkProjectsDeleteFailed")
            action_factory.helpers.attach_allure(name="Bulk Projects Deletion", text=message)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()
        
        projects_after_bulk_del = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        remaining_bulk_projects = [b for b in bulk_projects if b in projects_after_bulk_del]

        if not remaining_bulk_projects:
            status = "Pass"
            message = f"Single project '{single_project}' and bulk projects {bulk_projects} deleted successfully."
            action_factory.helpers.attach_screenshot(name="BulkProjectsDeletedSuccess")
            action_factory.helpers.attach_allure(name="Bulk Projects Deletion", text=f"Bulk projects deleted: {bulk_projects}")
            assert True, message
        else:
            status = "Fail"
            message = f"Bulk deletion failed. Projects still present: {remaining_bulk_projects}"
            action_factory.helpers.attach_screenshot(name="BulkProjectsDeleteFailed")
            action_factory.helpers.attach_allure(name="Bulk Projects Deletion", text=message)
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
