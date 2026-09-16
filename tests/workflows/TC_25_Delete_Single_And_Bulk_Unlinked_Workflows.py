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
@allure.story("Delete Unlinked Workflows (Single & Bulk)")
@allure.title("Verify creating and deleting a single workflow as well as bulk deleting multiple unlinked workflows")
def test_delete_single_and_bulk_unlinked_workflows(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        template_name = "AUT_WF_Template_15"
        single_wf = test_data_inputs.single_delete_workflow_name
        bulk_wfs = [
            test_data_inputs.bulk_delete_wf_1,
            test_data_inputs.bulk_delete_wf_2,
            test_data_inputs.bulk_delete_wf_3
        ]
        description = test_data_inputs.description
        template_file = test_data_inputs.valid_template_file
        nodes_list = ["Start", "Annotate", "Review", "Complete"]

        # Create Template
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Part 1: Single Workflow Creation & Deletion
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=single_wf, description=description)
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
        if single_wf in workflow_list:
            status = "Pass"
            message = f"Workflow '{single_wf}' created successfully with template '{template_name}' applied."
            action_factory.helpers.attach_screenshot(name="WorkflowCreatedPass")
            action_factory.helpers.attach_allure(name="Create Workflow", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{single_wf}' was not created successfully."
            action_factory.helpers.attach_screenshot(name="WorkflowCreatedFailed")
            action_factory.helpers.attach_allure(name="Create Workflow", text=message)
            assert False, message

        # Delete single workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.delete_workflow(single_wf)
        action_factory.ui_utils.smart_wait()
        popup_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.workflow_delete_success_popup)
        if popup_visible:
            action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
            status = "Pass"
            message = f"Single workflow '{single_wf}' deleted successfully."
            action_factory.helpers.attach_screenshot(name="SingleWorkflowDeletedPass")
            action_factory.helpers.attach_allure(name="Delete Single Workflow", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Single workflow '{single_wf}' was not deleted successfully."
            action_factory.helpers.attach_screenshot(name="SingleWorkflowDeletedFailed")
            action_factory.helpers.attach_allure(name="Delete Single Workflow", text=message)
            assert False, message
        remaining_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        if single_wf not in remaining_list:
            status = "Pass"
            message = f"Single workflow '{single_wf}' deleted successfully."
            action_factory.helpers.attach_screenshot(name="SingleWorkflowDeletedPass")
            action_factory.helpers.attach_allure(name="Delete Single Workflow", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Single workflow '{single_wf}' was not deleted successfully."
            action_factory.helpers.attach_screenshot(name="SingleWorkflowDeletedFailed")
            action_factory.helpers.attach_allure(name="Delete Single Workflow", text=message)
            assert False, message

        # Part 2: Create 3 Workflows and Bulk Delete
        for wf in bulk_wfs:
            action_factory.workflows_actions.click_workflows_menu()
            action_factory.workflows_actions.create_workflow(workflow_name=wf, description=description)
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
            if wf in workflow_list:
                status = "Pass"
                message = f"Workflow '{wf}' created successfully with template '{template_name}' applied."
                action_factory.helpers.attach_screenshot(name="WorkflowCreatedPass")
                action_factory.helpers.attach_allure(name="Create Workflow", text=message)
                assert True, message
            else:
                status = "Fail"
                message = f"Workflow '{wf}' was not created successfully."
                action_factory.helpers.attach_screenshot(name="WorkflowCreatedFailed")
                action_factory.helpers.attach_allure(name="Create Workflow", text=message)
                assert False, message

        # Bulk Delete 3 Workflows
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.delete_workflow(bulk_wfs)
        action_factory.ui_utils.smart_wait()
        popup_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.workflow_delete_success_popup)
        if popup_visible:
            action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
            status = "Pass"
            message = f"Single workflow '{single_wf}' deleted successfully."
            action_factory.helpers.attach_screenshot(name="SingleWorkflowDeletedPass")
            action_factory.helpers.attach_allure(name="Delete Single Workflow", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Single workflow '{single_wf}' was not deleted successfully."
            action_factory.helpers.attach_screenshot(name="SingleWorkflowDeletedFailed")
            action_factory.helpers.attach_allure(name="Delete Single Workflow", text=message)
            assert False, message

        final_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        if all(wf not in final_list for wf in bulk_wfs):
            status = "Pass"
            message = "Single and bulk workflow deletions executed successfully."
            action_factory.helpers.attach_screenshot(name="WorkflowBulkDeletePass")
            action_factory.helpers.attach_allure(name="Delete Single and Bulk Workflows", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Some bulk workflows were not deleted: {bulk_wfs}"
            action_factory.helpers.attach_screenshot(name="WorkflowBulkDeleteFailed")
            action_factory.helpers.attach_allure(name="Delete Single and Bulk Workflows", text=message)
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
