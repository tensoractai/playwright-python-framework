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
@allure.story("Dataset Files Add Delete Functionality")
@allure.title("Dataset Files Add Delete Functionality")
def test_Dataset_Files_Add_Functionality(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        dataset_name_1 = test_data_inputs.Dataset_Name_1
        dataset_name_2 = test_data_inputs.Dataset_Name_2
        dataset_type_name = test_data_inputs.dataset_type_name
        Image_Single_Files = test_data_inputs.Image_Single_Files
        Image_Multiple_Files =  test_data_inputs.Image_Multiple_Files
        Image_Extra_Files = test_data_inputs.Image_Extra_Files
        
        # Add Single File to Dataset :
        # Create 2 Dataset :: 
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name_1, dataset_type_name=dataset_type_name)
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name_2, dataset_type_name=dataset_type_name)
        action_factory.ui_utils.smart_wait()
        dataset_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        print(f"Dataset names list: {dataset_name_list}")
        if dataset_name_1 in dataset_name_list and dataset_name_2 in dataset_name_list:
            status = "Pass"
            message = f"Dataset '{dataset_name_1}' and '{dataset_name_2}' created successfully."
            action_factory.helpers.attach_screenshot(name="DatasetCreated")
            action_factory.helpers.attach_allure(name="Dataset Name", text=f"{dataset_name_1}, {dataset_name_2}")
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset '{dataset_name_1}' and '{dataset_name_2}' creation failed."
            action_factory.helpers.attach_screenshot(name="DatasetCreationFailed")
            action_factory.helpers.attach_allure(name="Dataset Name", text=f"{dataset_name_1}, {dataset_name_2}")
            assert False, message

        # From Files Tab Upload Files and add in Dataset ::
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.datasets_actions.upload_files_with_uploadBtn(*Image_Single_Files)
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files_single = [file.split("/")[-1] for file in Image_Single_Files]        
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

        # Validate File is added to dataset ::
        action_factory.files_actions.click_file_name_checkbox(expected_files_single[0])
        action_factory.files_actions.add_to_dataset(dataset_name_1)
        action_factory.files_actions.validate_add_items_datatype("IMAGE")
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.add_button)
        action_factory.ui_utils.smart_wait()
        action_factory.common_actions.validate_toast_msg("Files added successfully")
        dataset_names_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_file_name_list)
        print(f"Dataset names list: {dataset_names_list}")
        if dataset_name_1 in dataset_names_list:
            status = "Pass"
            message = f"Files added successfully."
            action_factory.helpers.attach_screenshot(name="FilesAddedToDataset")
            action_factory.helpers.attach_allure(name="Dataset Name", text=dataset_name_1)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to add files to dataset."
            action_factory.helpers.attach_screenshot(name="FilesAddedToDatasetFailed")
            action_factory.helpers.attach_allure(name="Dataset Name", text=dataset_name_1)
            assert False, message

        #........................................................................................................................................
        # Add Multiple File to Single DataSet :: 
        # From Files Tab Upload Files and add in Dataset ::
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.datasets_actions.upload_files_with_uploadBtn(*Image_Multiple_Files)
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files_multiple = [file.split("/")[-1] for file in Image_Multiple_Files]        
        if all(file in files_name_list for file in expected_files_multiple):
            status = "Pass"
            message = f"Files uploaded successfully."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files_multiple))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload files."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files_multiple))
            assert False, message

        # Validate File is added to dataset ::
        action_factory.files_actions.click_file_name_checkbox(expected_files_multiple[0])
        action_factory.files_actions.click_file_name_checkbox(expected_files_multiple[1])
        action_factory.files_actions.click_file_name_checkbox(expected_files_multiple[2])
        action_factory.files_actions.add_to_dataset(dataset_name_2)
        action_factory.files_actions.validate_add_items_datatype("IMAGE")
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.add_button)
        action_factory.ui_utils.smart_wait()
        action_factory.common_actions.validate_toast_msg("Files added successfully")
        dataset_names_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_file_name_list)
        print(f"Dataset names list: {dataset_names_list}")
        if dataset_name_2 in dataset_names_list:
            status = "Pass"
            message = f"Files added successfully."
            action_factory.helpers.attach_screenshot(name="FilesAddedToDataset")
            action_factory.helpers.attach_allure(name="Dataset Name", text=dataset_name_1)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to add files to dataset."
            action_factory.helpers.attach_screenshot(name="FilesAddedToDatasetFailed")
            action_factory.helpers.attach_allure(name="Dataset Name", text=dataset_name_1)
            assert False, message

        #..............................................................................................................
        # Add files to dataset with some already existing
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.datasets_actions.upload_files_with_uploadBtn(*Image_Extra_Files)
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files_extra = [file.split("/")[-1] for file in Image_Extra_Files]        
        if all(file in files_name_list for file in expected_files_extra):
            status = "Pass"
            message = f"Files uploaded successfully."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files_extra))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload files."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files_extra))
            assert False, message

        # Validate File is added to dataset ::
        action_factory.files_actions.click_file_name_checkbox(expected_files_extra[0])
        action_factory.files_actions.click_file_name_checkbox(expected_files_multiple[0])
        action_factory.files_actions.click_file_name_checkbox(expected_files_single[0])
        action_factory.files_actions.add_to_dataset(dataset_name_1)
        action_factory.files_actions.validate_add_items_datatype("IMAGE")
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.add_button)
        action_factory.ui_utils.smart_wait()
        action_factory.common_actions.validate_toast_msg("Files added successfully")
        dataset_names_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_file_name_list)
        print(f"Dataset names list: {dataset_names_list}")
        if dataset_name_2 in dataset_names_list:
            status = "Pass"
            message = f"Files added successfully."
            action_factory.helpers.attach_screenshot(name="FilesAddedToDataset")
            action_factory.helpers.attach_allure(name="Dataset Name", text=dataset_name_1)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to add files to dataset."
            action_factory.helpers.attach_screenshot(name="FilesAddedToDatasetFailed")
            action_factory.helpers.attach_allure(name="Dataset Name", text=dataset_name_1)
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