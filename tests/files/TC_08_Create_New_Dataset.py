import allure
import pytest
from actions.action_factory import ActionFactory
from test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    password = action_factory.helpers.fetch_dotenv("company_Password")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
    diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
    diff_email_password = action_factory.helpers.fetch_dotenv(
        "different_email_for_otp_password"
    )
    # Login
    action_factory.login_actions.perform_login(
        url=url,
        email=email,
        password=password
    )
    action_factory.login_actions.use_different_email_OTP(
        diff_email,
        diff_email_password
    )
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("Files")
@allure.story("Create New Dataset Functionality")
@allure.title("Create New Dataset Functionality")
def test_Create_New_Dataset_Functionality(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        Cancel_Dataset_Files = test_data_inputs.Cancel_Dataset_Files
        Create_New_Dataset = test_data_inputs.Create_New_Dataset

        # From Files Tab Upload Files and create new Dataset ::
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.datasets_actions.upload_files_with_uploadBtn(*Cancel_Dataset_Files)
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")
        action_factory.ui_utils.smart_wait()
        expected_files_single = [file.split("/")[-1] for file in Cancel_Dataset_Files] 
        action_factory.files_actions.click_file_name_checkbox(expected_files_single[0])
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.add_to_dataset)
        action_factory.files_actions.create_new_dataset(Create_New_Dataset)
        dataset_names_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_file_name_list)
        print(f"Dataset names list: {dataset_names_list}")
        if Create_New_Dataset in dataset_names_list:
            status = "Pass"
            message = f"Files added successfully."
            action_factory.helpers.attach_screenshot(name="FilesAddedToDataset")
            action_factory.helpers.attach_allure(name="Dataset Name", text=Create_New_Dataset)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to add files to dataset."
            action_factory.helpers.attach_screenshot(name="FilesAddedToDatasetFailed")
            action_factory.helpers.attach_allure(name="Dataset Name", text=Create_New_Dataset)
            assert False, message
        # Check Back to Dataset Tab 
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.ui_utils.smart_wait()
        dataset_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        print(f"Dataset names list: {dataset_name_list}")
        if Create_New_Dataset in dataset_name_list :
            status = "Pass"
            message = f"Dataset '{Create_New_Dataset}' created successfully."
            action_factory.helpers.attach_screenshot(name="DatasetCreated")
            action_factory.helpers.attach_allure(name="Dataset Name", text=f"{Create_New_Dataset}")
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset '{Create_New_Dataset}' creation failed."
            action_factory.helpers.attach_screenshot(name="DatasetCreationFailed")
            action_factory.helpers.attach_allure(name="Dataset Name", text=f"{Create_New_Dataset}")
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(Create_New_Dataset))
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files = [file.split("/")[-1] for file in expected_files_single]
        if all(file in files_name_list for file in expected_files_single):
            status = "Pass"
            message = f"All files uploaded successfully for dataset '{expected_files_single}'."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload all files for dataset '{expected_files_single}'."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files))
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
    