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
@allure.story("Project Teams User Assignment")
@allure.title("Verify assigning Annotator and Reviewer to project Teams tab and removing assigned Annotator user")
def test_Add_And_Remove_Users_In_Project_Teams(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        dataset_name = test_data_inputs.valid_dataset_Name
        workflow_name = test_data_inputs.valid_workflow_Name
        project_name = test_data_inputs.teams_project_name
        annotator_email = action_factory.helpers.fetch_dotenv("annotator_Username")
        reviewer_email = action_factory.helpers.fetch_dotenv("reviewer_Username")

        # Navigate to Projects Menu
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()

        # Create project if not already present
        existing_projects = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        if project_name not in existing_projects:
            action_factory.projects_actions.create_project(
                project_name=project_name,
                dataset_name=dataset_name,
                workflow_name=workflow_name
            )
            action_factory.ui_utils.smart_wait()

        # Open Project
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_name))
        action_factory.ui_utils.smart_wait()

        # Navigate to Teams Tab
        action_factory.projects_actions.click_teams_tab()
        action_factory.ui_utils.smart_wait()

        # Assign Annotator and Reviewer Users
        action_factory.projects_actions.add_users(role="Annotator", email_address=annotator_email)
        action_factory.projects_actions.add_users(role="Reviewer", email_address=reviewer_email)
        action_factory.ui_utils.smart_wait()

        # Validate Annotator and Reviewer Users Assigned
        assigners = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.assigners_list)
        print(f"Assigned users list: {assigners}")

        if annotator_email in assigners and reviewer_email in assigners:
            status = "Pass"
            message = f"Annotator '{annotator_email}' and Reviewer '{reviewer_email}' assigned successfully."
            action_factory.helpers.attach_screenshot(name="AnnotatorAndReviewerAssignedSuccess")
            action_factory.helpers.attach_allure(name="Teams User Assignment", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to assign Annotator '{annotator_email}' and/or Reviewer '{reviewer_email}'. Current assigners: {assigners}"
            action_factory.helpers.attach_screenshot(name="UserAssignmentFailed")
            action_factory.helpers.attach_allure(name="Teams User Assignment", text=message)
            assert False, message

        # Select Annotator User Checkbox and Remove
        action_factory.projects_actions.remove_user(annotator_email)
        action_factory.ui_utils.smart_wait()
        # Validate Annotator User Removed
        assigners_after_remove = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.assigners_list)
        print(f"Assigned users after removal: {assigners_after_remove}")
        if annotator_email not in assigners_after_remove:
            status = "Pass"
            message = f"Annotator '{annotator_email}' removed successfully. Remaining users: {assigners_after_remove}"
            action_factory.helpers.attach_screenshot(name="AnnotatorUserRemovedSuccess")
            action_factory.helpers.attach_allure(name="Teams User Removal", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Annotator '{annotator_email}' was not removed from Teams. Current assigners: {assigners_after_remove}"
            action_factory.helpers.attach_screenshot(name="AnnotatorUserRemovalFailed")
            action_factory.helpers.attach_allure(name="Teams User Removal", text=message)
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
