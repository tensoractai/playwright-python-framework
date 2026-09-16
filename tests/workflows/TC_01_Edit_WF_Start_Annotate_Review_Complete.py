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
@allure.story("TC_01: Start -> Annotate -> Review -> Complete (Edit)")
@allure.title("Verify creating, editing, and saving a TC_01 workflow (Start -> Annotate -> Review -> Complete)")
def test_tc01_edit_wf_start_annotate_review_complete(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        template_name = test_data_inputs.common_template_name_A
        template_name_B = test_data_inputs.common_template_name_B
        workflow_name = test_data_inputs.tc01_edit_workflow_name
        description = test_data_inputs.description
        template_file = test_data_inputs.valid_template_file
        dataset_name  = test_data_inputs.common_dataset_name
        dataset_type  = test_data_inputs.common_dataset_Type
        dataset_files  = test_data_inputs.Audio_Files
        nodes_list = ["Start", "Annotate", "Review", "Complete"]

        # Create Dataset 
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name=dataset_type)
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.datasets_actions.upload_files_with_uploadBtn(*dataset_files)
        action_factory.ui_utils.smart_wait()
        action_factory.common_actions.validate_toast_msg("1 file added")
        action_factory.ui_utils.smart_wait()

        # Create Template
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Create Template B
        action_factory.templates_actions.upload_new_template(template_name=template_name_B, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        template_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        if template_name_B in template_name_list and template_name in template_name_list:
            status = "Pass"
            message = f"Template '{template_name_B}' and '{template_name}' created successfully."
            action_factory.helpers.attach_screenshot(name="TemplateCreated")
            action_factory.helpers.attach_allure(name="Template Created", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template '{template_name_B}' and '{template_name}' not created."
            action_factory.helpers.attach_screenshot(name="TemplateCreationFailed")
            action_factory.helpers.attach_allure(name="Template Creation Failed", text=message)
            assert False, message

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
        workflow_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        print("Workflow List: ", workflow_list)
        if workflow_name in workflow_list:
            status = "Pass"
            message = f"Workflow '{workflow_name}' created and saved successfully."
            action_factory.helpers.attach_screenshot(name="TC01WorkflowCreationPass")
            action_factory.helpers.attach_allure(name="TC_01 Create Workflow", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_name}' not found after creation."
            action_factory.helpers.attach_screenshot(name="TC01WorkflowCreationFailed")
            action_factory.helpers.attach_allure(name="TC_01 Create Workflow", text=message)
            assert False, message
        action_factory.ui_utils.smart_wait()
        # Perform Edit Operations
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.click_workflow_name(workflow_name))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.edit_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_existing_template_new(old_template_name=template_name, new_template_name=template_name_B, index=1)
        action_factory.ui_utils.smart_wait()
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
            action_factory.helpers.attach_screenshot(name="TC01WorkflowEditPass")
            action_factory.helpers.attach_allure(name="TC_01 Edit Workflow", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_name}' not found after edit."
            action_factory.helpers.attach_screenshot(name="TC01WorkflowEditFailed")
            action_factory.helpers.attach_allure(name="TC_01 Edit Workflow", text=message)
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
