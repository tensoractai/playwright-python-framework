import allure
import pytest
from actions.action_factory import ActionFactory
from tests.projects.test_data_inputs import test_data_inputs

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

@allure.feature("Projects")
@allure.story("Add/Sync Additional Dataset")
@allure.title("Verify creating Image and Video datasets, creating project, and adding Video dataset via Add/Sync")
def test_Add_Sync_Additional_Dataset_To_Project(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        image_dataset_name = test_data_inputs.image_dataset_name
        video_dataset_name = test_data_inputs.video_dataset_name
        image_files = test_data_inputs.image_files_upload
        video_files = test_data_inputs.video_files_upload
        template_name = test_data_inputs.valid_template_Name
        template_files = test_data_inputs.template_files_upload
        workflow_name = test_data_inputs.valid_workflow_Name
        nodes_list = test_data_inputs.nodes_list
        project_name = test_data_inputs.add_sync_project_name

        # Create Image Dataset
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.create_dataset(dataset_name=image_dataset_name, dataset_type_name="Image")
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(image_dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*image_files)
        action_factory.ui_utils.smart_wait()

        # Create Video Dataset
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.create_dataset(dataset_name=video_dataset_name, dataset_type_name="Video")
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(video_dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*video_files)
        action_factory.ui_utils.smart_wait()

        # Create Project with Image Dataset
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.projects_actions.create_project(project_name=project_name, dataset_name=image_dataset_name, workflow_name=workflow_name)
        action_factory.ui_utils.smart_wait()

        # Open Project and Navigate to Datasets Tab
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_name))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.project_datasets_tab)
        action_factory.ui_utils.smart_wait()

        # Perform Add/Sync for Video Dataset
        action_factory.projects_actions.add_dataset_to_project(video_dataset_name)
        # Validate that both Image and Video datasets are present in project
        project_datasets = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.dataset_name_list)
        print(f"Project datasets after Add/Sync: {project_datasets}")

        if image_dataset_name in project_datasets and video_dataset_name in project_datasets:
            status = "Pass"
            message = f"Both datasets '{image_dataset_name}' and '{video_dataset_name}' are present in project '{project_name}'."
            action_factory.helpers.attach_screenshot(name="AddSyncDatasetsSuccess")
            action_factory.helpers.attach_allure(name="Add Sync Datasets", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Datasets validation failed. Found: {project_datasets}. Expected both '{image_dataset_name}' and '{video_dataset_name}'."
            action_factory.helpers.attach_screenshot(name="AddSyncDatasetsFailed")
            action_factory.helpers.attach_allure(name="Add Sync Datasets", text=message)
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
