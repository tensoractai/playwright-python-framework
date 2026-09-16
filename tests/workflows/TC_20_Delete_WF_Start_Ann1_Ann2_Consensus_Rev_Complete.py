import allure
import pytest
from actions.action_factory import ActionFactory
from tests.workflows.test_data_inputs import test_data_inputs

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

@allure.feature("Workflows")
@allure.story("TC_20: Start -> Annotate 1 -> Annotate 2 Consensus -> Review -> Complete (Delete Linked)")
@allure.title("Verify attempting to delete a TC_20 workflow linked to an active project is blocked")
def test_tc20_delete_wf_start_ann1_ann2_consensus_rev_complete(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        dataset_name = test_data_inputs.common_dataset_name
        template_name = test_data_inputs.common_template_name_A
        workflow_name = test_data_inputs.tc19_edit_workflow_name
        project_name = test_data_inputs.tc20_project_name
        description = test_data_inputs.description
        nodes_list = ["Start", "Annotate", "Annotate", "Review", "Complete"]

        # Create Project linking dataset and workflow
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.projects_actions.create_project(
            project_name=project_name,
            dataset_name=dataset_name,
            workflow_name=workflow_name,
            description=description
        )
        action_factory.ui_utils.smart_wait()

        project_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        if project_name in project_name_list:
            status = "Pass"
            message = f"Project '{project_name}' was created."
            action_factory.helpers.attach_screenshot(name="TC20ProjectCreated")
            action_factory.helpers.attach_allure(name="TC_20 Project", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' was not created."
            action_factory.helpers.attach_screenshot(name="TC20ProjectNotCreated")
            action_factory.helpers.attach_allure(name="TC_20 Project", text=message)
            assert False, message
            
        # Attempt to delete linked workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.delete_workflow(workflow_name)
        action_factory.ui_utils.smart_wait()
        error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.workflow_delete_failed_popup)
        if error_visible:
            status = "Pass"
            message = f"Deletion of linked workflow '{workflow_name}' was blocked as expected."
            action_factory.helpers.attach_screenshot(name="TC20PreventDeleteLinkedWorkflowPass")
            action_factory.helpers.attach_allure(name="TC_20 Delete Linked Workflow", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Deletion of linked workflow '{workflow_name}' was not blocked."
            action_factory.helpers.attach_screenshot(name="TC20PreventDeleteLinkedWorkflowFailed")
            action_factory.helpers.attach_allure(name="TC_20 Delete Linked Workflow", text=message)
            assert False, message

        # Close the popup
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()
        workflow_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        if workflow_name in workflow_name_list:
            status = "Pass"
            message = f"Workflow '{workflow_name}' is still present after attempting to delete."
            action_factory.helpers.attach_screenshot(name="TC20WorkflowNotDeleted")
            action_factory.helpers.attach_allure(name="TC_20 Delete Workflow", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_name}' was deleted successfully."
            action_factory.helpers.attach_screenshot(name="TC20DeleteWorkflowFailed")
            action_factory.helpers.attach_allure(name="TC_20 Delete Workflow", text=message)
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
