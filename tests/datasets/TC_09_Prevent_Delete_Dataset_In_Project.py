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
@allure.story("Prevent deleting a dataset that is used in a project")
@allure.title("Verify prevention of deleting a dataset linked to an active project")
def test_Prevent_Delete_Dataset_Used_In_Project(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        dataset_name = test_data_inputs.Prevent_dataset_name
        template_name = test_data_inputs.Prevent_template_name
        workflow_name = test_data_inputs.Prevent_workflow_name
        project_name = test_data_inputs.Prevent_project_name
        dataset_type_name = test_data_inputs.Dataset_Type_Audio
        Dataset_files_upload = test_data_inputs.Audio_Files
        Template_files_upload = test_data_inputs.Template_files_upload
        nodes_list = test_data_inputs.Prevent_node_list

        # Navigate to Datasets menu and create dataset "AUT_Prevent_Dataset"
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name=dataset_type_name)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*Dataset_files_upload)
        action_factory.ui_utils.smart_wait()

        # Create Template "AUT_Prevent_Template"
        action_factory.templates_actions.click_templates_menu()
        action_factory.templates_actions.upload_new_template(template_name=template_name)
        action_factory.templates_actions.upload_template_files(*Template_files_upload)
        action_factory.ui_utils.smart_wait()

        # Create Workflow "AUT_Prevent_WorkFlow"
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description="Workflow for testing dataset deletion prevention")
        action_factory.ui_utils.smart_wait()
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name)
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.nodes_connection_flow(node_Name1="review", node_index1=1, position1="right", index1=2, node_Name2="annotate", node_index2=1, position2="left", index2=1)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

        # Create Project "AUT_Prevent_Project" linking dataset and workflow
        action_factory.projects_actions.click_project_menu()
        action_factory.projects_actions.create_project(project_name=project_name,dataset_name=dataset_name,workflow_name=workflow_name)
        action_factory.ui_utils.smart_wait()

        # Go to Datasets and attempt to delete "AUT_Prevent_Dataset" (Should be prevented / retained)
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.delete_dataset(dataset_name)
        action_factory.ui_utils.smart_wait()
        delete_error_popup = action_factory.ui_utils.is_element_visible(action_factory.page_factory.datasets_page.dataset_delete_failed_popup)
        if delete_error_popup :
            status = "Pass"
            message = f"Dataset '{dataset_name}' was correctly prevented from deletion while linked to a project."
            action_factory.helpers.attach_screenshot(name="DatasetDeletionPreventedSuccessfully")
            action_factory.helpers.attach_allure(name="Prevent Delete Dataset", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset '{dataset_name}' was not prevented from deletion while linked to a project."
            action_factory.helpers.attach_screenshot(name="DatasetDeletionPreventionFailed")
            action_factory.helpers.attach_allure(name="Prevent Delete Dataset", text=message)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()
        existing_datasets_step6 = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)

        if dataset_name in existing_datasets_step6:
            status = "Pass"
            message = f"Dataset '{dataset_name}' was correctly prevented from deletion while linked to a project."
            action_factory.helpers.attach_screenshot(name="DatasetDeletionPreventedSuccessfully")
            action_factory.helpers.attach_allure(name="Prevent Delete Dataset", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset '{dataset_name}' was deleted despite being attached to project '{project_name}'."
            action_factory.helpers.attach_screenshot(name="DatasetDeletionPreventionFailed")
            action_factory.helpers.attach_allure(name="Prevent Delete Dataset", text=message)
            assert False, message

        # Go to Projects and delete project "AUT_Prevent_Project" to remove association
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.projects_actions.delete_project(project_name)
        action_factory.ui_utils.smart_wait()
        success_popup = action_factory.ui_utils.is_element_visible(action_factory.page_factory.projects_page.project_delete_success)
        if success_popup :
            status = "Pass"
            message = f"Project '{project_name}' was deleted successfully after removing dataset association."
            action_factory.helpers.attach_screenshot(name="ProjectDeletionSuccessAfterDatasetRemoval")
            action_factory.helpers.attach_allure(name="Prevent Delete Dataset", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' was not deleted after removing dataset association."
            action_factory.helpers.attach_screenshot(name="ProjectDeletionFailedAfterDatasetRemoval")
            action_factory.helpers.attach_allure(name="Prevent Delete Dataset", text=message)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        # Go back to Datasets and delete "AUT_Prevent_Dataset" (Should now be deleted)
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.delete_dataset(dataset_name)
        action_factory.ui_utils.smart_wait()
        success_popup  = action_factory.ui_utils.is_element_visible(action_factory.page_factory.datasets_page.dataset_delete_success_popup)
        if success_popup :
            status = "Pass"
            message = f"Dataset '{dataset_name}' was deleted successfully after removing project association."
            action_factory.helpers.attach_screenshot(name="DatasetDeletedSuccessfullyAfterProjectRemoval")
            action_factory.helpers.attach_allure(name="Prevent Delete Dataset", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset '{dataset_name}' was not deleted after removing project association."
            action_factory.helpers.attach_screenshot(name="DatasetDeletionFailedAfterProjectRemoval")
            action_factory.helpers.attach_allure(name="Prevent Delete Dataset", text=message)
            assert False, message

        existing_datasets_step = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        if dataset_name not in existing_datasets_step:
            status = "Pass"
            message = f"Dataset '{dataset_name}' was deleted successfully after removing project association."
            action_factory.helpers.attach_screenshot(name="DatasetDeletedSuccessfullyAfterProjectRemoval")
            action_factory.helpers.attach_allure(name="Prevent Delete Dataset", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to delete dataset '{dataset_name}' even after removing project association."
            action_factory.helpers.attach_screenshot(name="DatasetDeletionFailedAfterProjectRemoval")
            action_factory.helpers.attach_allure(name="Prevent Delete Dataset", text=message)
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
