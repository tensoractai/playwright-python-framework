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
@allure.story("Search Project Name")
@allure.title("Verify searching a project name returns the expected project in the list")
def test_Search_Project_Name(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        dataset_name = test_data_inputs.valid_dataset_Name
        workflow_name = test_data_inputs.valid_workflow_Name
        search_project_name = test_data_inputs.search_project_name

        # Navigate to Projects Menu
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()

        # Create project for search if not already present
        action_factory.projects_actions.create_project(
            project_name=search_project_name,
            dataset_name=dataset_name,
            workflow_name=workflow_name
        )
        action_factory.ui_utils.smart_wait()

        # Perform Search
        action_factory.ui_utils.fill_input(action_factory.page_factory.projects_page.search_input, search_project_name)
        action_factory.ui_utils.smart_wait()

        # Validate Search Results
        search_results = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        print(f"Search results for '{search_project_name}': {search_results}")

        if search_project_name in search_results:
            status = "Pass"
            message = f"Search returned the expected project '{search_project_name}' successfully."
            action_factory.helpers.attach_screenshot(name="SearchProjectSuccess")
            action_factory.helpers.attach_allure(name="Search Project Name", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Search failed to display expected project '{search_project_name}'. Found: {search_results}"
            action_factory.helpers.attach_screenshot(name="SearchProjectFailed")
            action_factory.helpers.attach_allure(name="Search Project Name", text=message)
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
