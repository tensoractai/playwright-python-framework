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
@allure.story("Edit Workflow Functionality")
@allure.title("Verify opening a workflow, validating Edit button visibility, editing template, annotators, deleting node, adding reviewer/complete nodes, and saving updated workflow")
def test_edit_workflow_functionality(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        template_name_A = "AUT_WF_Temp_14A"
        template_name_B = "AUT_WF_Temp_14B"
        workflow_name = test_data_inputs.edit_workflow_name
        description = test_data_inputs.description
        template_file = test_data_inputs.valid_template_file
        nodes_list = ["Start", "Annotate", "Review", "Complete"]

        # Create Template A
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.upload_new_template(template_name=template_name_A, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Create Template B (for edit update)
        action_factory.templates_actions.upload_new_template(template_name=template_name_B, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Create valid workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description=description)
        action_factory.ui_utils.smart_wait()

        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)

        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name_A, position=0)
        action_factory.ui_utils.smart_wait()

        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="review", node_index1=1, position1="right", index1=2,
            node_Name2="annotate", node_index2=1, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

        workflow_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        if workflow_name in workflow_name_list:
            status = "Pass"
            message = f"Workflow name '{workflow_name}' was successfully created."
            action_factory.helpers.attach_screenshot(name="WorkflowCreatedPass")
            action_factory.helpers.attach_allure(name="Workflow Created", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow name '{workflow_name}' was not created."
            action_factory.helpers.attach_screenshot(name="WorkflowCreatedFailed")
            action_factory.helpers.attach_allure(name="Workflow Created", text=message)
            assert False, message

        # Click the created workflow and validate Edit button visibility
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.click_workflow_name(workflow_name))
        action_factory.ui_utils.smart_wait()

        edit_btn_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.edit_button)
        print(f"Edit button visibility: {edit_btn_visible}")

        if edit_btn_visible:
            status = "Pass"
            message = "Edit button is visible on workflow details page."
            action_factory.helpers.attach_screenshot(name="EditButtonVisiblePass")
            action_factory.helpers.attach_allure(name="Edit Workflow Functionality", text=message)
            assert True, message
        else:
            status = "Fail"
            message = "Edit button is not visible on workflow details page."
            action_factory.helpers.attach_screenshot(name="EditButtonVisibleFailed")
            action_factory.helpers.attach_allure(name="Edit Workflow Functionality", text=message)
            assert False, message

        # Click Edit button and perform edits:
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
            message = f"Workflow '{workflow_name}' created successfully with template '{template_name_B}' applied."
            action_factory.helpers.attach_screenshot(name="WorkflowCreated")
            action_factory.helpers.attach_allure(name="Workflow Name", text=workflow_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_name}' creation failed or template '{template_name_B}' not applied."
            action_factory.helpers.attach_screenshot(name="WorkflowCreationFailed")
            action_factory.helpers.attach_allure(name="Workflow Name", text=workflow_name)
            assert False, message
        # Delete Complete node
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.delete_node_btn("complete"))
        action_factory.ui_utils.smart_wait()
        # Add second Reviewer node and Complete node
        action_factory.workflows_actions.click_nodes("Review")
        action_factory.workflows_actions.click_nodes("Complete")
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.ui_utils.smart_wait()
        # Connect new nodes
        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="review", node_index1=2, position1="right", index1=2,
            node_Name2="review", node_index2=1, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()
        save_enabled = action_factory.ui_utils.is_element_enabled(action_factory.page_factory.workflows_page.save_btn)
        if save_enabled :
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
        action_factory.workflows_actions.edit_node_pencil(edit_node="annotate",index=1,new_Name="New_Ann")
        action_factory.workflows_actions.edit_node_pencil(edit_node="review",index=1,new_Name="New_Rev")
        # Save Updated Workflow
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

        # Validate workflow updated
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()

        workflow_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        print(f"Workflows list after edit: {workflow_list}")

        if workflow_name in workflow_list:
            status = "Pass"
            message = f"Workflow '{workflow_name}' was edited and updated successfully."
            action_factory.helpers.attach_screenshot(name="WorkflowUpdatedSuccessfully")
            action_factory.helpers.attach_allure(name="Edit Workflow Functionality", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_name}' was not found in the workflow list after update."
            action_factory.helpers.attach_screenshot(name="WorkflowUpdateFailed")
            action_factory.helpers.attach_allure(name="Edit Workflow Functionality", text=message)
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
