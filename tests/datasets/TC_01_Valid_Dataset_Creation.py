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

@allure.feature("Dataset")
@allure.story("Valid Dataset Creation")
@allure.title("Valid Dataset Creation")
def test_create_dataset_valid(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        dataset_Name_Valid = test_data_inputs.Dataset_Name_Valid
        dataset_Type_CSV = test_data_inputs.Dataset_Type_CSV
        Dataset_CSV_File_Valid = test_data_inputs.Dataset_File_Valid

        # Create Valid Dataset and Upload File and Validate in Files Page as well 
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_Name_Valid, dataset_type_name=dataset_Type_CSV)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.smart_wait()
        dataset_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        print(f"Dataset names list: {dataset_name_list}")
        if dataset_Name_Valid in dataset_name_list:
            status = "Pass"
            message = f"Dataset '{dataset_Name_Valid}' created successfully."
            action_factory.helpers.attach_screenshot(name="DatasetCreated")
            action_factory.helpers.attach_allure(name="Dataset Name", text=dataset_Name_Valid)
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset '{dataset_Name_Valid}' creation failed."
            action_factory.helpers.attach_screenshot(name="DatasetCreationFailed")
            action_factory.helpers.attach_allure(name="Dataset Name", text=dataset_Name_Valid)
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_Name_Valid))

        action_factory.datasets_actions.upload_files_with_uploadBtn(*Dataset_CSV_File_Valid)
        action_factory.ui_utils.smart_wait()
        action_factory.common_actions.validate_toast_msg("2 files added")
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files = [file.split("/")[-1] for file in Dataset_CSV_File_Valid]
        if all(file in files_name_list for file in expected_files):
            status = "Pass"
            message = f"All files uploaded successfully for dataset '{dataset_Name_Valid}'."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload all files for dataset '{dataset_Name_Valid}'."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files))
            assert False, message
        # Validate in Files Tab 
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files = [file.split("/")[-1] for file in Dataset_CSV_File_Valid]        
        if all(file in files_name_list for file in expected_files):
            status = "Pass"
            message = f"Files are visible in files tab."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Files", text=", ".join(expected_files))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to find files in files tab."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Files", text=", ".join(expected_files))
            assert False, message

        dataset_names_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_file_name_list)
        print(f"Dataset names list: {dataset_names_list}")
        if dataset_Name_Valid in dataset_names_list:
            status = "Pass"
            message = f"Files are visible in dataset."
            action_factory.helpers.attach_screenshot(name="FilesAddedToDataset")
            action_factory.helpers.attach_allure(name="Dataset Name", text=", ".join(expected_files))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to find files in dataset."
            action_factory.helpers.attach_screenshot(name="FilesAddedToDatasetFailed")
            action_factory.helpers.attach_allure(name="Dataset Name", text=", ".join(expected_files))
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


