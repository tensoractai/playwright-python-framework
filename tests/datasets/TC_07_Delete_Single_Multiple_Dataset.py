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
    action_factory.login_actions.use_different_email_OTP(diff_email,
        diff_email_password
    )
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("Datasets")
@allure.story("Delete Dataset Functionality")
@allure.title("Verify Creation and Deletion of Single and Multiple Datasets")
def test_Delete_Dataset_Functionality(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        # Define dataset names for testing
        dataset_names = [f"AUT_Delete_Dataset_{i}" for i in range(1, 5)]
        dataset_type = test_data_inputs.Dataset_Type_CSV

        # Navigate to Datasets menu
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.ui_utils.smart_wait()
        # Create 4 Datasets
        for dataset_name in dataset_names:
            action_factory.datasets_actions.create_dataset(dataset_name=dataset_name,dataset_type_name=dataset_type)
            action_factory.ui_utils.smart_wait()

        # Click one dataset and Delete
        first_dataset = dataset_names[0]
        action_factory.datasets_actions.delete_dataset(first_dataset)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()
        existing_datasets = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        if first_dataset not in existing_datasets:
            status = "Pass"
            message = "One dataset deleted successfully and verified."
            action_factory.helpers.attach_screenshot(name="OneDatasetDeletedSuccessfully")
            action_factory.helpers.attach_allure(name="Delete Dataset Functionality", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to delete datasets: {first_dataset}"
            action_factory.helpers.attach_screenshot(name="DatasetDeletionFailed")
            action_factory.helpers.attach_allure(name="Delete Dataset Functionality", text=message)
            assert False, message

        # Click all other 3 datasets and Delete
        remaining_datasets = dataset_names[1:]
        action_factory.datasets_actions.delete_dataset(remaining_datasets)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        # Validate that all deleted datasets are no longer displayed in list
        existing_datasets = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        deleted_datasets_present = [name for name in dataset_names if name in existing_datasets]

        if not deleted_datasets_present:
            status = "Pass"
            message = "All 4 datasets deleted successfully and verified."
            action_factory.helpers.attach_screenshot(name="AllDatasetsDeletedSuccessfully")
            action_factory.helpers.attach_allure(name="Delete Dataset Functionality", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to delete datasets: {deleted_datasets_present}"
            action_factory.helpers.attach_screenshot(name="DatasetDeletionFailed")
            action_factory.helpers.attach_allure(name="Delete Dataset Functionality", text=message)
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
