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
@allure.story("All Dataset Types Lifecycle & Files Validation")
@allure.title("Verify creation, file upload, files tab validation, and deletion of all dataset types")
def test_all_dataset_types_lifecycle(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        datasets_to_test = test_data_inputs.datasets_to_test
        expected_dataset_types = test_data_inputs.expected_dataset_types

        # Click on Datasets menu
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.ui_utils.smart_wait()

        # Click Create Dataset, open Dataset Type dropdown and validate types
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.create_dataset_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.select_dataset_type)
        action_factory.ui_utils.smart_wait()
        dataset_type = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_type_list)
        if dataset_type == expected_dataset_types:
            status = "Pass"
            message = "All dataset types are present"
            action_factory.helpers.attach_screenshot(name="AllDatasetTypesPresent")
            action_factory.helpers.attach_allure(name="Dataset Type Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Missing dataset types. Expected: {expected_dataset_types}, Found: {dataset_type}"
            action_factory.helpers.attach_screenshot(name="DatasetTypeValidationFailed")
            action_factory.helpers.attach_allure(name="Dataset Type Validation", text=message)
            assert False, message
        # Cancel the create dataset popup
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        # Create Datasets for each type, upload file, and validate
        created_dataset_names = []
        uploaded_file_names = []

        for item in datasets_to_test:
            ds_name = item["name"]
            ds_type = item["type"]
            ds_file = item["file"]
            file_name = ds_file.split("/")[-1]

            # Navigate to Datasets menu and create dataset
            action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
            action_factory.ui_utils.smart_wait()
            action_factory.datasets_actions.create_dataset(dataset_name=ds_name, dataset_type_name=ds_type)
            action_factory.ui_utils.smart_wait()

            # Open created dataset and upload file
            action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(ds_name))
            action_factory.ui_utils.smart_wait()
            action_factory.datasets_actions.upload_files_with_uploadBtn(ds_file)
            action_factory.ui_utils.smart_wait()

            created_dataset_names.append(ds_name)
            uploaded_file_names.append(file_name)

        # Validate from Files Menu all Datasets and files are present
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.ui_utils.smart_wait()

        files_in_files_tab = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        datasets_in_files_tab = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_file_name_list)

        all_datasets_present = all(ds in datasets_in_files_tab for ds in created_dataset_names)
        all_files_present = all(f in files_in_files_tab for f in uploaded_file_names)

        if all_datasets_present and all_files_present:
            status = "Pass"
            message = "All created datasets and uploaded files are present in Files Menu."
            action_factory.helpers.attach_screenshot(name="AllDatasetsAndFilesPresentInFilesMenu")
            action_factory.helpers.attach_allure(name="Files Menu Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Missing datasets or files in Files Menu. Datasets: {created_dataset_names}, Files: {uploaded_file_names}"
            action_factory.helpers.attach_screenshot(name="FilesMenuValidationFailed")
            action_factory.helpers.attach_allure(name="Files Menu Validation", text=message)
            assert False, message

        # Delete all datasets one by one and validate
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.ui_utils.smart_wait()

        for ds_name in created_dataset_names:
            action_factory.datasets_actions.delete_dataset(ds_name)
            action_factory.ui_utils.smart_wait()
            action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
            action_factory.ui_utils.smart_wait()

        existing_datasets = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        deleted_datasets_present = [ds for ds in created_dataset_names if ds in existing_datasets]

        if not deleted_datasets_present:
            status = "Pass"
            message = "All datasets deleted successfully from Datasets page."
            action_factory.helpers.attach_screenshot(name="AllDatasetsDeletedFromDatasetsPage")
            action_factory.helpers.attach_allure(name="Dataset Deletion Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Datasets not deleted from Datasets page: {deleted_datasets_present}"
            action_factory.helpers.attach_screenshot(name="DatasetDeletionFailed")
            action_factory.helpers.attach_allure(name="Dataset Deletion Validation", text=message)
            assert False, message

        # Validate from Files Menu all Datasets and files are no longer present
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.ui_utils.smart_wait()

        final_datasets_in_files_tab = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_file_name_list)
        remaining_datasets = [ds for ds in created_dataset_names if ds in final_datasets_in_files_tab]

        if not remaining_datasets:
            status = "Pass"
            message = "All datasets and files successfully removed from Files Menu."
            action_factory.helpers.attach_screenshot(name="FilesMenuCleanedAfterDatasetDeletion")
            action_factory.helpers.attach_allure(name="Final Files Menu Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Datasets still present in Files Menu after deletion: {remaining_datasets}"
            action_factory.helpers.attach_screenshot(name="FilesMenuCleanFailed")
            action_factory.helpers.attach_allure(name="Final Files Menu Validation", text=message)
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
