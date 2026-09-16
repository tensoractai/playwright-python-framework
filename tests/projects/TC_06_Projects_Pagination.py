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
@allure.story("Projects Pagination Check")
@allure.title("Verify projects pagination control for limits 5, 10, 20, and 50 with creation and tab switching")
def test_projects_pagination(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        dataset_name = test_data_inputs.valid_dataset_Name
        workflow_name = test_data_inputs.valid_workflow_Name
        project_name = test_data_inputs.pagination_project_name

        # Navigate to Projects Menu
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()

        # Check pagination for 5
        action_factory.projects_actions.set_projects_pagination("5")
        project_count = action_factory.page_factory.projects_page.project_names_list.count()
        if project_count <= 5:
            status = "Pass"
            message = f"Project count ({project_count}) is <= 5."
            action_factory.helpers.attach_screenshot(name="ProjectsPagination5Pass")
            action_factory.helpers.attach_allure(name="Projects Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Project count ({project_count}) exceeds limit of 5."
            action_factory.helpers.attach_screenshot(name="ProjectsPagination5Failed")
            action_factory.helpers.attach_allure(name="Projects Pagination Check", text=message)
            assert False, message

        # Create new project and verify pagination persistence
        action_factory.projects_actions.create_project(
            project_name=project_name,
            dataset_name=dataset_name,
            workflow_name=workflow_name
        )

        project_count_after_create = action_factory.page_factory.projects_page.project_names_list.count()
        if project_count_after_create <= 5:
            status = "Pass"
            message = f"Project count ({project_count_after_create}) remains <= 5 after creating a new project."
            action_factory.helpers.attach_screenshot(name="PaginationPreservedAfterProjectCreation")
            action_factory.helpers.attach_allure(name="Projects Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Project count ({project_count_after_create}) exceeded limit of 5 after project creation."
            action_factory.helpers.attach_screenshot(name="PaginationNotPreservedAfterCreation")
            action_factory.helpers.attach_allure(name="Projects Pagination Check", text=message)
            assert False, message

        # Switch menu to Datasets and return to Projects page, verify count <= 5
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()

        project_count_after_switch = action_factory.page_factory.projects_page.project_names_list.count()
        if project_count_after_switch <= 5:
            status = "Pass"
            message = f"Project count ({project_count_after_switch}) remains <= 5 after switching menu and returning."
            action_factory.helpers.attach_screenshot(name="PaginationPreservedAfterTabSwitch")
            action_factory.helpers.attach_allure(name="Projects Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Project count ({project_count_after_switch}) exceeded limit of 5 after menu switch."
            action_factory.helpers.attach_screenshot(name="PaginationNotPreservedAfterSwitch")
            action_factory.helpers.attach_allure(name="Projects Pagination Check", text=message)
            assert False, message

        # Check pagination for 10
        action_factory.projects_actions.set_projects_pagination("10")
        project_count_10 = action_factory.page_factory.projects_page.project_names_list.count()
        if project_count_10 <= 10:
            status = "Pass"
            message = f"Project count ({project_count_10}) is <= 10."
            action_factory.helpers.attach_screenshot(name="ProjectsPagination10Pass")
            action_factory.helpers.attach_allure(name="Projects Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Project count ({project_count_10}) exceeds limit of 10."
            action_factory.helpers.attach_screenshot(name="ProjectsPagination10Failed")
            action_factory.helpers.attach_allure(name="Projects Pagination Check", text=message)
            assert False, message

        # Check pagination for 20
        action_factory.projects_actions.set_projects_pagination("20")
        project_count_20 = action_factory.page_factory.projects_page.project_names_list.count()
        if project_count_20 <= 20:
            status = "Pass"
            message = f"Project count ({project_count_20}) is <= 20."
            action_factory.helpers.attach_screenshot(name="ProjectsPagination20Pass")
            action_factory.helpers.attach_allure(name="Projects Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Project count ({project_count_20}) exceeds limit of 20."
            action_factory.helpers.attach_screenshot(name="ProjectsPagination20Failed")
            action_factory.helpers.attach_allure(name="Projects Pagination Check", text=message)
            assert False, message

        # Check pagination for 50
        action_factory.projects_actions.set_projects_pagination("50")
        project_count_50 = action_factory.page_factory.projects_page.project_names_list.count()
        if project_count_50 <= 50:
            status = "Pass"
            message = f"Pagination 5, 10, 20, 50 validated successfully. Final count at 50 limit: {project_count_50}"
            action_factory.helpers.attach_screenshot(name="ProjectsPagination50Pass")
            action_factory.helpers.attach_allure(name="Projects Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Project count ({project_count_50}) exceeds limit of 50."
            action_factory.helpers.attach_screenshot(name="ProjectsPagination50Failed")
            action_factory.helpers.attach_allure(name="Projects Pagination Check", text=message)
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
