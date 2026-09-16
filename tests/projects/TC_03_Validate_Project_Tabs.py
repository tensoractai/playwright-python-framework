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
@allure.story("Project Tabs Validation")
@allure.title("Verify project tabs [Overview, Tasks, Workflow, Taxonomies, Datasets, Teams] are present")
def test_Validate_Project_Tabs(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        dataset_name = test_data_inputs.valid_dataset_Name
        template_name = test_data_inputs.valid_template_Name
        workflow_name = test_data_inputs.valid_workflow_Name
        project_name = test_data_inputs.valid_project_Name
        dataset_type_name = test_data_inputs.dataset_type_name
        dataset_files_upload = test_data_inputs.dataset_files_upload
        template_files_upload = test_data_inputs.template_files_upload
        nodes_list = test_data_inputs.nodes_list
        expected_tabs = test_data_inputs.expected_project_tabs

        # Navigate to Projects Menu
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()

        # Click the project created for TC_01 Valid
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_name))
        action_factory.ui_utils.smart_wait()

        # Grab project tabs and validate presence
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.projects_page.project_tabs.first, state="visible", timeout=10000)
        actual_tabs = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_tabs)
        print(f"Actual project tabs found: {actual_tabs}")

        missing_tabs = []
        for expected in expected_tabs:
            if not any(expected.lower() in tab.lower() or tab.lower() in expected.lower() for tab in actual_tabs):
                missing_tabs.append(expected)

        if not missing_tabs:
            status = "Pass"
            message = f"All expected project tabs {expected_tabs} are present in project '{project_name}'. Actual tabs: {actual_tabs}"
            action_factory.helpers.attach_screenshot(name="ProjectTabsValidationPassed")
            action_factory.helpers.attach_allure(name="Project Tabs", text=", ".join(actual_tabs))
            assert True, message
        else:
            status = "Fail"
            message = f"Missing project tabs: {missing_tabs} for project '{project_name}'. Actual tabs: {actual_tabs}"
            action_factory.helpers.attach_screenshot(name="ProjectTabsValidationFailed")
            action_factory.helpers.attach_allure(name="Project Tabs", text=message)
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
