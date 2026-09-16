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
@allure.story("TC_30: Linked Workflow Edit Button Visibility Validation")
@allure.title("Verify that Edit button is not visible for a workflow linked to an active project")
def test_tc30_linked_workflow_edit_disabled(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        dataset_name = test_data_inputs.common_dataset_name
        template_name = test_data_inputs.common_template_name_A
        workflow_name = test_data_inputs.tc30_workflow_name
        project_name = test_data_inputs.tc30_project_name
        description = test_data_inputs.description
        nodes_list = ["Start", "Annotate", "Review", "Complete"]

        # Create Workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description=description)
        action_factory.ui_utils.smart_wait()
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name, position=0)
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="review", node_index1=1, position1="right", index1=2,
            node_Name2="annotate", node_index2=1, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

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

        # Open Workflow details and verify Edit button is not visible
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.click_workflow_name(workflow_name))
        action_factory.ui_utils.smart_wait()

        edit_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.edit_button, timeout=5000)
        if edit_visible:
            status = "Pass"
            message = f"Edit button is visible for workflow '{workflow_name}' linked to an active project as expected."
            action_factory.helpers.attach_screenshot(name="TC30EditButtonNotVisiblePass")
            action_factory.helpers.attach_allure(name="TC_30 Linked Workflow Edit Disabled", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Edit button is visible for workflow '{workflow_name}' linked to an active project."
            action_factory.helpers.attach_screenshot(name="TC30EditButtonVisibleFailed")
            action_factory.helpers.attach_allure(name="TC_30 Linked Workflow Edit Disabled", text=message)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.edit_button)
        action_factory.ui_utils.smart_wait()
        
        workflow_error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.workflow_edit_error)
        if workflow_error_visible:
            status = "Pass"
            message = f"Error message is displayed for workflow '{workflow_name}' linked to an active project as expected."
            action_factory.helpers.attach_screenshot(name="TC30EditButtonNotVisiblePass")
            action_factory.helpers.attach_allure(name="TC_30 Linked Workflow Edit Disabled", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Error message is not displayed for workflow '{workflow_name}' linked to an active project."
            action_factory.helpers.attach_screenshot(name="TC30EditButtonVisibleFailed")
            action_factory.helpers.attach_allure(name="TC_30 Linked Workflow Edit Disabled", text=message)
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
