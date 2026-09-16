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
@allure.story("Save Button Disabled Without Template Configuration")
@allure.title("Verify save button is disabled when template is not configured on annotate node and workflow is not created when cancelled")
def test_workflow_save_disabled_without_template(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        workflow_name = test_data_inputs.tc21_workflow_name
        description = test_data_inputs.description
        nodes_list = ["Start", "Annotate", "Review", "Complete"]

        # Click Workflows menu and create workflow name
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description=description)
        action_factory.ui_utils.smart_wait()

        # Add nodes without configuring any template
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)

        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.ui_utils.smart_wait()

        # Connect Nodes
        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="review", node_index1=1, position1="right", index1=2,
            node_Name2="annotate", node_index2=1, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()

        # Validate Save button is in disabled mode
        save_disabled = action_factory.ui_utils.is_element_enabled(action_factory.page_factory.workflows_page.save_btn)
        print(f"Save button disabled state: {save_disabled}")

        if save_disabled == False:
            status = "Pass"
            message = "Save button is correctly disabled when template is not configured."
            action_factory.helpers.attach_screenshot(name="SaveButtonDisabledPass")
            action_factory.helpers.attach_allure(name="Workflow Save Disabled Without Template", text=message)
            assert True, message
        else:
            status = "Fail"
            message = "Save button was enabled even though template was not configured."
            action_factory.helpers.attach_screenshot(name="SaveButtonEnabledFailed")
            action_factory.helpers.attach_allure(name="Workflow Save Disabled Without Template", text=message)
            assert False, message

        # Cancel / Back out of the workflow creation page
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.close_btn)
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()

        # Verify Workflow is NOT created
        workflow_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        print(f"Workflows list after cancel: {workflow_list}")

        if workflow_name not in workflow_list:
            status = "Pass"
            message = f"Workflow '{workflow_name}' was not created after cancellation."
            action_factory.helpers.attach_screenshot(name="WorkflowNotCreatedOnCancel")
            action_factory.helpers.attach_allure(name="Workflow Save Disabled Without Template", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_name}' was unexpectedly created after cancellation."
            action_factory.helpers.attach_screenshot(name="WorkflowUnexpectedlyCreated")
            action_factory.helpers.attach_allure(name="Workflow Save Disabled Without Template", text=message)
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
