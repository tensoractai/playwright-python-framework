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

@allure.feature("Datset")
@allure.story("Dataset Files Add Delete Functionality")
@allure.title("Dataset Files Add Delete Functionality")
def test_Dataset_Files_Add_Functionality(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        Text_Files = test_data_inputs.Text_Files
        dataset_name_text = test_data_inputs.Dataset_Name_Text
        dataset_type_text = test_data_inputs.Dataset_Type_Text
        Extra_Text_Files = test_data_inputs.Extra_Text_Files
        
        # Upload One File in Files Tab 
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.datasets_actions.upload_files_with_uploadBtn(*Text_Files)
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*Extra_Text_Files)
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files_single = [file.split("/")[-1] for file in Text_Files]        
        if all(file in files_name_list for file in expected_files_single):
            status = "Pass"
            message = f"Files uploaded successfully."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files_single))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload files."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files_single))
            assert False, message

        # Create Dataset 
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name_text, dataset_type_name=dataset_type_text)
        action_factory.ui_utils.smart_wait()
        dataset_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        print(f"Dataset names list: {dataset_name_list}")
        if dataset_name_text in dataset_name_list :
            status = "Pass"
            message = f"Dataset '{dataset_name_text}' created successfully."
            action_factory.helpers.attach_screenshot(name="DatasetCreated")
            action_factory.helpers.attach_allure(name="Dataset Name", text=dataset_name_text)
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset '{dataset_name_text}' creation failed."
            action_factory.helpers.attach_screenshot(name="DatasetCreationFailed")
            action_factory.helpers.attach_allure(name="Dataset Name", text=f"{dataset_name_text}")
            assert False, message

        # Add File to that Dataset 
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name_text))
        action_factory.ui_utils.smart_wait()
        file_names = [file.split("/")[-1] for file in Text_Files]
        for file in file_names:
            action_factory.datasets_actions.add_files_dataset(file)
            action_factory.common_actions.validate_toast_msg("1 file added")
            action_factory.ui_utils.smart_wait()

        # Validate File is added
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")
        if all(file in files_name_list for file in file_names):
            status = "Pass"
            message = f"Files uploaded successfully."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(file_names))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload files."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(file_names))
            assert False, message

        # Add Files that are already in dataset 
        Extra_Files = [file.split("/")[-1] for file in Extra_Text_Files]
        print(f"Files names list: {Extra_Files}")
        combined_files = Extra_Files + file_names
        print(f"Combined files list: {combined_files}")
        action_factory.datasets_actions.add_files_dataset(*combined_files)
        action_factory.common_actions.validate_toast_msg("1 file added, 4 files skipped")
        action_factory.ui_utils.smart_wait()

        # Validate File is added
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")
        if all(file in files_name_list for file in file_names):
            status = "Pass"
            message = f"Files uploaded successfully."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(file_names))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload files."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(file_names))
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