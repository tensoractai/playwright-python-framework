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
@allure.story("Switch Role and Validate Company Name")
@allure.title("Verify dataset company name matches environment company_Name after switching role to Super User")
def test_switch_role_validate_company_name(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        dataset_name = test_data_inputs.switch_role_dataset_name
        dataset_type = test_data_inputs.Dataset_Type_Text
        text_files = test_data_inputs.popup_text_file
        expected_company_name = action_factory.helpers.fetch_dotenv("company_Name")

        # Create dataset and upload file
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name=dataset_type)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*text_files)
        action_factory.ui_utils.smart_wait()

        # Switch Role to Super User
        action_factory.login_actions.switch_role("Super User")
        action_factory.ui_utils.smart_wait()

        # Navigate to Datasets menu
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()

        # Grab company name associated with dataset
        company_name_locator = action_factory.page_factory.datasets_page.get_company_name_by_dataset(dataset_name)
        actual_company_name = action_factory.ui_utils.grab_text_from_all(company_name_locator)
        print(f"Actual Company Name: '{actual_company_name}', Expected Company Name: '{expected_company_name}'")

        if expected_company_name in actual_company_name:
            status = "Pass"
            message = f"Company name '{actual_company_name}' matches expected company name '{expected_company_name}'."
            action_factory.helpers.attach_screenshot(name="CompanyNameValidationPass")
            action_factory.helpers.attach_allure(name="Switch Role Company Name Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Company name '{actual_company_name}' does not match expected company name '{expected_company_name}'."
            action_factory.helpers.attach_screenshot(name="CompanyNameValidationFailed")
            action_factory.helpers.attach_allure(name="Switch Role Company Name Validation", text=message)
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
