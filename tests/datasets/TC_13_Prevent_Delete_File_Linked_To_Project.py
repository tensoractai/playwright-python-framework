import allure
import pytest
from actions.action_factory import ActionFactory
from tests.datasets.test_data_inputs import test_data_inputs

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

@allure.feature("Datasets")
@allure.story("Prevent Deleting File in Dataset Linked to Project")
@allure.title("Verify file deletion is blocked while dataset is linked to project and succeeds after unlinking")
def test_prevent_delete_file_linked_to_project(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        dataset_name = test_data_inputs.TC_13_Dataset_name
        dataset_type = test_data_inputs.Dataset_Type_Audio
        audio_files = test_data_inputs.Audio_Files
        audio_file_name = [f.split("/")[-1] for f in audio_files][0]
        template_name = test_data_inputs.TC_13_Template_name
        template_files = test_data_inputs.Template_files_upload
        workflow_name = test_data_inputs.TC_13_WorkFlow_name
        nodes_list = test_data_inputs.Prevent_node_list
        project_name = test_data_inputs.TC_13_Project_name
        description = test_data_inputs.description

        # Create dataset and upload audio file
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name=dataset_type, description=description)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*audio_files)
        action_factory.ui_utils.smart_wait()

        # Validate file uploaded
        files_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        if audio_file_name in files_list:
            status = "Pass"
            message = f"File '{audio_file_name}' was not uploaded to dataset."
            action_factory.helpers.attach_screenshot(name="FileUploadedSuccessfully")
            action_factory.helpers.attach_allure(name="Prevent Delete File Linked To Project", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"File '{audio_file_name}' was not uploaded to dataset."
            action_factory.helpers.attach_screenshot(name="FileUploadedFailed")
            action_factory.helpers.attach_allure(name="Prevent Delete File Linked To Project", text=message)
            assert False, message

        # Create Template
        action_factory.templates_actions.click_templates_menu()
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(*template_files)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Create Workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description=description)
        action_factory.ui_utils.smart_wait()
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name)
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
        action_factory.projects_actions.create_project(
            project_name=project_name, dataset_name=dataset_name, workflow_name=workflow_name, description=description
        )
        action_factory.ui_utils.smart_wait()

        # Go to Datasets, open dataset, try to delete file -> Validate File Should NOT get deleted
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.return_file_checkbox(audio_file_name).first)
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.delete_btn)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.fill_input(action_factory.page_factory.files_page.delete_text, "DELETE")
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.delete_btn)
        action_factory.ui_utils.smart_wait()
        # Validate this error is visible or not : Failed Detached File
        failed_detached_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.files_page.failed_detached_file)
        print(f"Failed Detached File error visibility: {failed_detached_visible}")
        if failed_detached_visible:
            status = "Pass"
            message = "File 'audio_file_name' deletion was correctly blocked with 'Failed Detached File' error because dataset is linked to project."
            action_factory.helpers.attach_screenshot(name="FileDeletionBlockedWhenLinkedToProject")
            action_factory.helpers.attach_allure(name="Prevent Delete File Linked To Project", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"File '{audio_file_name}' was deleted or 'Failed Detached File' error was not visible."
            action_factory.helpers.attach_screenshot(name="FileDeletionNotBlockedFailed")
            action_factory.helpers.attach_allure(name="Prevent Delete File Linked To Project", text=message)
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()
        files_after_delete_attempt = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files after initial delete attempt: {files_after_delete_attempt}")

        if audio_file_name in files_after_delete_attempt:
            status = "Pass"
            message = f"File '{audio_file_name}' deletion was correctly blocked with 'Failed Detached File' error because dataset is linked to project."
            action_factory.helpers.attach_screenshot(name="FileDeletionBlockedWhenLinkedToProject")
            action_factory.helpers.attach_allure(name="Prevent Delete File Linked To Project", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"File '{audio_file_name}' was deleted or 'Failed Detached File' error was not visible."
            action_factory.helpers.attach_screenshot(name="FileDeletionNotBlockedFailed")
            action_factory.helpers.attach_allure(name="Prevent Delete File Linked To Project", text=message)
            assert False, message

        # Navigate to Projects, open project, Datasets tab, and delete/remove dataset from project
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_name))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.project_datasets_tab)
        action_factory.ui_utils.smart_wait()

        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.return_file_checkbox(dataset_name).first)
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.delete_toolbar_btn)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.delete_toolbar_btn)
        action_factory.common_actions.validate_toast_msg("Datasets deleted successfully")

        # Go back to Datasets, open dataset, select file and delete again -> Validate File GETS deleted
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.return_file_checkbox(audio_file_name).first)
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.delete_btn)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.fill_input(action_factory.page_factory.files_page.delete_text, "DELETE")
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.delete_btn)
        action_factory.ui_utils.smart_wait()
        success_popup = action_factory.ui_utils.is_element_visible(action_factory.page_factory.files_page.files_delete_success_popup)
        if success_popup:
            status = "Pass"
            message = f"File '{audio_file_name}' deleted successfully after dataset was removed from project."
            action_factory.helpers.attach_screenshot(name="FileDeletedSuccessfullyAfterUnlinking")
            action_factory.helpers.attach_allure(name="Prevent Delete File Linked To Project", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"File '{audio_file_name}' was not deleted after dataset was removed from project."
            action_factory.helpers.attach_screenshot(name="FileDeletionAfterUnlinkingFailed")
            action_factory.helpers.attach_allure(name="Prevent Delete File Linked To Project", text=message)
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()
        files_after_unlinking = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files after unlinking and deleting: {files_after_unlinking}")

        if audio_file_name not in files_after_unlinking:
            status = "Pass"
            message = f"File '{audio_file_name}' deleted successfully after dataset was removed from project."
            action_factory.helpers.attach_screenshot(name="FileDeletedSuccessfullyAfterUnlinking")
            action_factory.helpers.attach_allure(name="Prevent Delete File Linked To Project", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"File '{audio_file_name}' was not deleted after dataset was removed from project."
            action_factory.helpers.attach_screenshot(name="FileDeletionAfterUnlinkingFailed")
            action_factory.helpers.attach_allure(name="Prevent Delete File Linked To Project", text=message)
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
