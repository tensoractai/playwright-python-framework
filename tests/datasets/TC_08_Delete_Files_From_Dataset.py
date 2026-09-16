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
@allure.story("Delete File From Dataset")
@allure.title("Verify creation of dataset, uploading a file, and deleting the file")
def test_Delete_File_From_Dataset(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        dataset_name =  test_data_inputs.Dataset_Delete_Files
        dataset_type = test_data_inputs.Dataset_Type_CSV
        file_relative_path = test_data_inputs.Dataset_File_Valid[0]  # "csv/CSV Test data.csv"
        file_name = file_relative_path.split("/")[-1]                # "CSV Test data.csv"

        # Click on Datasets menu
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name=dataset_type)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(file_relative_path)
        action_factory.ui_utils.smart_wait()

        # Go to Files Tab and Verify Dataset is added to that File 
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.ui_utils.smart_wait()
        dataset_names_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_file_name_list)
        print(f"Dataset names list: {dataset_names_list}")
        if dataset_name in dataset_names_list:
            status = "Pass"
            message = f"Dataset {dataset_name} is visible in the files tab."
            action_factory.helpers.attach_screenshot(name="Dataset_is_visible_in_the_files_tab")
            action_factory.helpers.attach_allure(name="Dataset Name", text=dataset_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset {dataset_name} is not visible in the files tab."
            action_factory.helpers.attach_screenshot(name="Dataset_is_not_visible_in_the_files_tab")
            action_factory.helpers.attach_allure(name="Delete File From Dataset", text=message)
            assert False, message
        # Now Delete the File
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.files_actions.delete_single_files(file_name)
        action_factory.ui_utils.smart_wait()
        delete_success = action_factory.ui_utils.is_element_visible(action_factory.page_factory.files_page.files_delete_success_popup)
        if delete_success:
            status = "Pass"
            message = f"File '{file_name}' deleted successfully from dataset '{dataset_name}'."
            action_factory.helpers.attach_screenshot(name="FileDeletedFromDatasetSuccessfully")
            action_factory.helpers.attach_allure(name="Delete File From Dataset", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to delete file '{file_name}' from dataset '{dataset_name}'."
            action_factory.helpers.attach_screenshot(name="FileDeletionFromDatasetFailed")
            action_factory.helpers.attach_allure(name="Delete File From Dataset", text=message)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files in dataset after deletion: {files_name_list}")

        if file_name not in files_name_list:
            status = "Pass"
            message = f"File '{file_name}' deleted successfully from dataset '{dataset_name}'."
            action_factory.helpers.attach_screenshot(name="FileDeletedFromDatasetSuccessfully")
            action_factory.helpers.attach_allure(name="Delete File From Dataset", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to delete file '{file_name}' from dataset '{dataset_name}'."
            action_factory.helpers.attach_screenshot(name="FileDeletionFromDatasetFailed")
            action_factory.helpers.attach_allure(name="Delete File From Dataset", text=message)
            assert False, message

        # Now Check Dataset Name is not present in  Files Tab 
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.ui_utils.smart_wait()
        dataset_names_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_file_name_list)
        print(f"Dataset names list: {dataset_names_list}")
        if dataset_name not in dataset_names_list:
            status = "Pass"
            message = f"Dataset {dataset_name} is not visible in the files tab."
            action_factory.helpers.attach_screenshot(name="Dataset_is_not_visible_in_the_files_tab")
            action_factory.helpers.attach_allure(name="Delete File From Dataset", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset {dataset_name} is visible in the files tab."
            action_factory.helpers.attach_screenshot(name="Dataset_is_visible_in_the_files_tab")
            action_factory.helpers.attach_allure(name="Delete File From Dataset", text=message)
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
