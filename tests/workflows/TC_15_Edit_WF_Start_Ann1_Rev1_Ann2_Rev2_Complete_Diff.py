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
@allure.story("TC_15: Start -> Annotate 1 -> Review 1 -> Annotate 2 -> Review 2 -> Complete Diff Templates (Edit)")
@allure.title("Verify creating, editing, and saving a TC_15 workflow with different templates on alternating Annotate/Review nodes")
def test_tc15_edit_wf_start_ann1_rev1_ann2_rev2_complete_diff(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        template_name_A = test_data_inputs.common_template_name_A
        template_name_B = test_data_inputs.common_template_name_B
        workflow_name = test_data_inputs.tc15_edit_workflow_name
        description = test_data_inputs.description
        template_file = test_data_inputs.valid_template_file
        nodes_list = ["Start", "Annotate", "Review", "Annotate", "Review", "Complete"]

        # Create Workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description=description)
        action_factory.ui_utils.smart_wait()
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name_A, position=0)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name_B, position=1)
        action_factory.ui_utils.smart_wait()

        # Connect Nodes
        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="review", node_index1=1, position1="right", index1=2,
            node_Name2="annotate", node_index2=1, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="review", node_index1=2, position1="right", index1=2,
            node_Name2="annotate", node_index2=2, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()

        # Save Workflow
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()
        workflow_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        print("Workflow List: ", workflow_list)
        if workflow_name in workflow_list:
            status = "Pass"
            message = f"Workflow '{workflow_name}' created and saved successfully."
            action_factory.helpers.attach_screenshot(name="TC15WorkflowCreationPass")
            action_factory.helpers.attach_allure(name="TC_15 Create Workflow", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_name}' not found after creation."
            action_factory.helpers.attach_screenshot(name="TC15WorkflowCreationFailed")
            action_factory.helpers.attach_allure(name="TC_15 Create Workflow", text=message)
            assert False, message

        # Perform Edit Operations
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.click_workflow_name(workflow_name))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.edit_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)

        # Change Template to Template B
        action_factory.workflows_actions.apply_existing_template_new(old_template_name=template_name_A, new_template_name=template_name_B, index=1)
        action_factory.ui_utils.smart_wait()

        # Change Required Annotators to 3
        action_factory.workflows_actions.required_annotator("3")
        action_factory.ui_utils.smart_wait()

        # Validate that template name is changed or not 
        template_applied = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.template_applied_name)
        if template_name_B in template_applied:
            status = "Pass"
            message = f"Workflow '{workflow_name}' template updated to '{template_name_B}' successfully."
            action_factory.helpers.attach_screenshot(name="TemplateUpdated")
            action_factory.helpers.attach_allure(name="Template Updated", text=workflow_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Template '{template_name_B}' not applied to workflow '{workflow_name}'."
            action_factory.helpers.attach_screenshot(name="TemplateUpdateFailed")
            action_factory.helpers.attach_allure(name="Template Update Failed", text=workflow_name)
            assert False, message
        action_factory.ui_utils.smart_wait()
        save_enabled = action_factory.ui_utils.is_element_enabled(action_factory.page_factory.workflows_page.save_btn)
        if save_enabled:
            status = "Pass"
            message = f"Save Button Enabled So node gets connected"
            action_factory.helpers.attach_screenshot(name="Nodes Connected")
            action_factory.helpers.attach_allure(name="Nodes Connected", text=workflow_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Save button Disabled Nodes not yet connected"
            action_factory.helpers.attach_screenshot(name="Nodes Disconnection")
            action_factory.helpers.attach_allure(name="Nodes Disconnection", text=workflow_name)
            assert False, message

        # Edit Annotation | Reviewer Names 
        action_factory.workflows_actions.edit_node_pencil(edit_node="annotate", index=1, new_Name="New_Ann")
        action_factory.workflows_actions.edit_node_pencil(edit_node="review", index=1, new_Name="New_Rev")

        # Save Updated Workflow
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

        # Validate Workflow Updated
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        workflow_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        if workflow_name in workflow_list:
            status = "Pass"
            message = f"Workflow '{workflow_name}' edited and updated successfully."
            action_factory.helpers.attach_screenshot(name="TC15WorkflowEditPass")
            action_factory.helpers.attach_allure(name="TC_15 Edit Workflow", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_name}' not found after edit."
            action_factory.helpers.attach_screenshot(name="TC15WorkflowEditFailed")
            action_factory.helpers.attach_allure(name="TC_15 Edit Workflow", text=message)
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
