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
@allure.story("Cancel Dataset Addition funnctionality")
@allure.title("Cancel Dataset Addition Functionality")
def test_Cancel_Dataset_Functionality(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        Cancel_Dataset_Files = test_data_inputs.Cancel_Dataset_Files
        Cancel_Dataset_Type = test_data_inputs.Cancel_Dataset_Type
        Cancel_Dataset_Name = test_data_inputs.Cancel_Dataset_Name

        # Create dataset
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.datasets_actions.create_dataset(dataset_name=Cancel_Dataset_Name, dataset_type_name=Cancel_Dataset_Type)
        action_factory.ui_utils.smart_wait()

        # From Files Tab Upload Files and add in Dataset ::
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.datasets_actions.upload_files_with_uploadBtn(*Cancel_Dataset_Files)
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files_single = [file.split("/")[-1] for file in Cancel_Dataset_Files]        
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
        
        action_factory.files_actions.click_file_name_checkbox(expected_files_single[0])
        action_factory.files_actions.add_to_dataset(Cancel_Dataset_Name)
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_button)
        action_factory.ui_utils.smart_wait()

        dataset_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_file_name_list)
        if Cancel_Dataset_Name not in dataset_name_list:
            status = "Pass"
            message = f"Dataset '{Cancel_Dataset_Name}' is not associated with the file after cancelling addition."
            action_factory.helpers.attach_screenshot(name="DatasetNotAssociatedAfterCancel")
            action_factory.helpers.attach_allure(name="Cancel Dataset Addition", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset '{Cancel_Dataset_Name}' was incorrectly associated with the file after cancelling addition."
            action_factory.helpers.attach_screenshot(name="DatasetAssociatedAfterCancelFailed")
            action_factory.helpers.attach_allure(name="Cancel Dataset Addition", text=message)
            assert False, message

        add_dataset_panel = action_factory.ui_utils.is_element_visible(action_factory.page_factory.files_page.add_dataset_Panel)
        print(f"Add to Dataset panel visible: {add_dataset_panel}")
        if not add_dataset_panel:
            status = "Pass"
            message = f"Add to Dataset panel closed successfully."
            action_factory.helpers.attach_screenshot(name="AddToDatasetPanelClosed")
            action_factory.helpers.attach_allure(name="Panel Closed", text="Add to Dataset panel closed successfully.")
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to close Add to Dataset panel."
            action_factory.helpers.attach_screenshot(name="AddToDatasetPanelNotClosed")
            action_factory.helpers.attach_allure(name="Panel Not Closed", text="Add to Dataset panel not closed.")
            assert False, message
        
        add_to_dataset_enabled = action_factory.ui_utils.is_element_enabled(action_factory.page_factory.files_page.add_to_dataset)
        print(f"Add to Dataset button enabled: {add_to_dataset_enabled}")
        if add_to_dataset_enabled:
            status = "Pass"
            message = f"Add to Dataset button enabled successfully."
            action_factory.helpers.attach_screenshot(name="AddToDatasetButtonEnabled")
            action_factory.helpers.attach_allure(name="Button Enabled", text="Add to Dataset button enabled successfully.")
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to enable Add to Dataset button."
            action_factory.helpers.attach_screenshot(name="AddToDatasetButtonNotEnabled")
            action_factory.helpers.attach_allure(name="Button Not Enabled", text="Add to Dataset button not enabled.")
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