import allure
import pytest
from actions.action_factory import ActionFactory
from tests.templates.test_data_inputs import test_data_inputs

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

@allure.feature("Templates")
@allure.story("Bulk Delete Templates with Linked and Unlinked Templates")
@allure.title("Verify deleting unlinked template succeeds while deleting template linked to workflow/project is blocked")
def test_bulk_delete_linked_unlinked_templates(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        dataset_name = test_data_inputs.bulk_linked_dataset_name
        linked_template = test_data_inputs.bulk_linked_template_name
        unlinked_template = test_data_inputs.bulk_unlinked_template_name
        workflow_name = test_data_inputs.bulk_linked_workflow_name
        project_name = test_data_inputs.bulk_linked_project_name
        nodes_list = test_data_inputs.prevent_template_node_list
        description = test_data_inputs.valid_template_description
        template_file = test_data_inputs.valid_template_file
        audio_files = test_data_inputs.Audio_Files

        # Create Dataset
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name="Audio", description=description)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*audio_files)
        action_factory.ui_utils.smart_wait()

        # Create First Template (linked template)
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.upload_new_template(template_name=linked_template, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Create Workflow with First Template
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description=description)
        action_factory.ui_utils.smart_wait()
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=linked_template)
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="review", node_index1=1, position1="right", index1=2,
            node_Name2="annotate", node_index2=1, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

        # Create Project
        action_factory.projects_actions.click_project_menu()
        action_factory.projects_actions.create_project(
            project_name=project_name, dataset_name=dataset_name, workflow_name=workflow_name, description=description
        )
        action_factory.ui_utils.smart_wait()

        # Create Second Template (unlinked template)
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.upload_new_template(template_name=unlinked_template, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Select both First Template (linked) and Second Template (unlinked) and perform Delete
        action_factory.templates_actions.delete_template([linked_template, unlinked_template])
        action_factory.ui_utils.smart_wait()

        # Validate error message "Failed Deleted Template" is visible
        error_msg_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.templates_page.template_delete_failed_msg)
        print(f"Failed Deleted Template error message visibility: {error_msg_visible}")

        if error_msg_visible:
            status = "Pass"
            message = "Error message 'Failed Deleted Template' displayed as expected for linked template."
            action_factory.helpers.attach_screenshot(name="FailedDeletedTemplateMsgVisible")
            action_factory.helpers.attach_allure(name="Bulk Delete Linked Unlinked Templates", text=message)
            assert True, message
        else:
            status = "Fail"
            message = "Error message 'Failed Deleted Template' was not displayed."
            action_factory.helpers.attach_screenshot(name="FailedDeletedTemplateMsgNotVisible")
            action_factory.helpers.attach_allure(name="Bulk Delete Linked Unlinked Templates", text=message)
            assert False, message

        # Cancel the popup
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        # Validate Second Created Template is DELETED and First Created Template (linked) is NOT DELETED
        template_list = action_factory.ui_utils.grab_text_from_all(
            action_factory.page_factory.templates_page.template_names_list
        )
        print(f"Templates list after popup cancel: {template_list}")

        if linked_template in template_list and unlinked_template not in template_list:
            status = "Pass"
            message = f"Unlinked template '{unlinked_template}' was deleted and linked template '{linked_template}' was retained as expected."
            action_factory.helpers.attach_screenshot(name="BulkDeleteResultVerified")
            action_factory.helpers.attach_allure(name="Bulk Delete Linked Unlinked Templates", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Bulk delete result check failed. Template list: {template_list}"
            action_factory.helpers.attach_screenshot(name="BulkDeleteResultFailed")
            action_factory.helpers.attach_allure(name="Bulk Delete Linked Unlinked Templates", text=message)
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
