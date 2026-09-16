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
@allure.story("Prevent Delete Workflow Linked To Project")
@allure.title("Verify that deleting a workflow linked to an active project is prevented while unlinked workflow is deleted")
def test_prevent_delete_workflow_linked_to_project(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        dataset_name = test_data_inputs.linked_delete_dataset_name
        template_name = test_data_inputs.linked_delete_template_name
        linked_workflow_name = test_data_inputs.linked_delete_workflow_name
        unlinked_workflow_name = test_data_inputs.unlinked_delete_workflow_name
        project_name = test_data_inputs.linked_delete_project_name
        description = test_data_inputs.description
        template_file = test_data_inputs.valid_template_file
        dataset_files = test_data_inputs.dataset_files
        nodes_list = ["Start", "Annotate", "Review", "Complete"]

        # Create Dataset
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name="Audio", description=description)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*dataset_files)
        action_factory.common_actions.validate_toast_msg("1 file added")
        action_factory.ui_utils.smart_wait()

        # Create Template
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Create Linked Workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=linked_workflow_name, description=description)
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

        # Create Unlinked Workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=unlinked_workflow_name, description=description)
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
        if linked_workflow_name in workflow_list and unlinked_workflow_name in workflow_list:
            status = "Pass"
            message = f"Workflows '{linked_workflow_name}' and '{unlinked_workflow_name}' were created successfully."
            action_factory.helpers.attach_screenshot(name="WorkflowsCreatedSuccess")
            action_factory.helpers.attach_allure(name="Create Workflows", text=message)
            assert True, message
        else:
            status = "Fail"
            message = "Workflows were not found in the workflow list after creation."
            action_factory.helpers.attach_screenshot(name="WorkflowsNotFound")
            action_factory.helpers.attach_allure(name="Create Workflows", text=message)
            assert False, message

        # Create Project linking dataset and linked_workflow_name
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.projects_actions.create_project(
            project_name=project_name,
            dataset_name=dataset_name,
            workflow_name=linked_workflow_name,
            description=description
        )
        action_factory.ui_utils.smart_wait()
        project_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        if project_name in project_list:
            status = "Pass"
            message = f"Project '{project_name}' was created successfully."
            action_factory.helpers.attach_screenshot(name="ProjectCreatedSuccess")
            action_factory.helpers.attach_allure(name="Create Project", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' was not found in the project list."
            action_factory.helpers.attach_screenshot(name="ProjectNotFound")
            action_factory.helpers.attach_allure(name="Create Project", text=message)
            assert False, message

        # Attempt to delete linked workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.delete_workflow(linked_workflow_name)
        action_factory.ui_utils.smart_wait()
        error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.workflow_delete_failed_popup)
        print(f"Delete linked workflow error visibility: {error_visible}")
        if error_visible:
            status = "Pass"
            message = f"Deletion of linked workflow '{linked_workflow_name}' was blocked as expected."
            action_factory.helpers.attach_screenshot(name="PreventDeleteLinkedWorkflowPass")
            action_factory.helpers.attach_allure(name="Prevent Delete Workflow Linked To Project", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{linked_workflow_name}' linked to project '{project_name}' was unexpectedly deleted."
            action_factory.helpers.attach_screenshot(name="PreventDeleteLinkedWorkflowFailed")
            action_factory.helpers.attach_allure(name="Prevent Delete Workflow Linked To Project", text=message)
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        # Attempt to delete both linked and unlinked workflows
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        combined_workflow = [linked_workflow_name, unlinked_workflow_name]
        action_factory.workflows_actions.delete_workflow(combined_workflow)
        action_factory.ui_utils.smart_wait()

        success_popup_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.workflow_delete_success_popup)
        failed_popup_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.workflow_delete_failed_popup)
        print(f"Success popup visible: {success_popup_visible}, Failed popup visible: {failed_popup_visible}")

        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        remaining_workflows = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        print(f"Workflows list after delete attempt: {remaining_workflows}")

        if linked_workflow_name in remaining_workflows and unlinked_workflow_name not in remaining_workflows:
            status = "Pass"
            message = f"Deletion of linked workflow '{linked_workflow_name}' was blocked while unlinked workflow '{unlinked_workflow_name}' was successfully deleted."
            action_factory.helpers.attach_screenshot(name="PreventDeleteLinkedWorkflowPass")
            action_factory.helpers.attach_allure(name="Prevent Delete Workflow Linked To Project", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow deletion validation failed. Remaining workflows: {remaining_workflows}"
            action_factory.helpers.attach_screenshot(name="PreventDeleteLinkedWorkflowFailed")
            action_factory.helpers.attach_allure(name="Prevent Delete Workflow Linked To Project", text=message)
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
