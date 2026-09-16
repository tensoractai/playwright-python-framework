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
@allure.story("Search Dataset Name in Add to Dataset Popup and Link File")
@allure.title("Verify searching for dataset in popup, linking file, and verifying association across tabs")
def test_search_dataset_in_add_to_dataset_popup(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        dataset_name = test_data_inputs.search_popup_dataset_name
        text_file = test_data_inputs.popup_text_file
        file_name = [f.split("/")[-1] for f in text_file][0]
        description  = test_data_inputs.description 

        # Navigate to Datasets menu and create dataset with type TEXT
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name="TEXT", description = description)
        action_factory.ui_utils.smart_wait()

        # Navigate to Files Tab and upload text file
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*text_file)
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")
        action_factory.ui_utils.smart_wait()

        # Select uploaded file and click Add to Dataset
        action_factory.files_actions.click_file_name_checkbox(file_name)
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.add_to_dataset)
        action_factory.ui_utils.smart_wait()

        # Search dataset name in Add to Dataset popup
        action_factory.ui_utils.fill_input(action_factory.page_factory.files_page.search_datasets_input, dataset_name)
        action_factory.ui_utils.smart_wait()

        # Select searched dataset, click Add, and validate toast message
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.return_file_checkbox(dataset_name).first)
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.add_button)
        action_factory.common_actions.validate_toast_msg("Files added successfully")
        action_factory.ui_utils.smart_wait()

        # Validate dataset name is displayed towards the file in Files tab
        dataset_names_in_files = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_file_name_list)
        print(f"Dataset names in files table: {dataset_names_in_files}")

        if dataset_name in dataset_names_in_files:
            status = "Pass"
            message = f"Dataset '{dataset_name}' successfully associated with file '{file_name}' in Files tab."
            action_factory.helpers.attach_screenshot(name="DatasetAssociatedInFilesTab")
            action_factory.helpers.attach_allure(name="Search Dataset Popup Link File", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset '{dataset_name}' was not associated with file '{file_name}' in Files tab."
            action_factory.helpers.attach_screenshot(name="DatasetAssociationFailedInFilesTab")
            action_factory.helpers.attach_allure(name="Search Dataset Popup Link File", text=message)
            assert False, message

        # Switch to Datasets tab and validate file is attached to Dataset here as well
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.ui_utils.smart_wait()

        files_in_dataset = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files inside dataset '{dataset_name}': {files_in_dataset}")

        if file_name in files_in_dataset:
            status = "Pass"
            message = f"File '{file_name}' is attached and visible inside dataset '{dataset_name}'."
            action_factory.helpers.attach_screenshot(name="FileVisibleInsideDataset")
            action_factory.helpers.attach_allure(name="Search Dataset Popup Link File", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"File '{file_name}' was not found inside dataset '{dataset_name}'."
            action_factory.helpers.attach_screenshot(name="FileNotVisibleInsideDataset")
            action_factory.helpers.attach_allure(name="Search Dataset Popup Link File", text=message)
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
