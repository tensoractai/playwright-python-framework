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
    action_factory.login_actions.perform_login(url=url, email=email, password=password)
    action_factory.login_actions.use_different_email_OTP(diff_email,diff_email_password)
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("Dataset")
@allure.story("Invalid Dataset Creation")
@allure.title("Invalid Dataset Creation")
def test_create_dataset_Invalid(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        Invalid_Dataset_Name = test_data_inputs.Invalid_Dataset_Name
        Dataset_Type_PDF = test_data_inputs.Dataset_Type_PDF
        TC_02_Dataset_Name = test_data_inputs.Dataset_Name_Invalid

        # Invalid File Name Validation and Already Present Dataset Name error Validation :
        # Enter Invalid File Name :
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.datasets_actions.create_dataset(dataset_name=Invalid_Dataset_Name, dataset_type_name=Dataset_Type_PDF)
        action_factory.ui_utils.smart_wait()
        error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.datasets_page.dataset_name_error_msg)
        if error_visible:
            status = "Pass"
            message = f"Error message for invalid dataset name is visible."
            action_factory.helpers.attach_screenshot(name="DatasetNameError")
            action_factory.helpers.attach_allure(name="Error Message", text="Error message for invalid dataset name is visible")
            assert True, message
        else:
            status = "Fail"
            message = f"Error message is not visible."
            action_factory.helpers.attach_screenshot(name="ErrorMessageFailed")
            action_factory.helpers.attach_allure(name="Error Message", text="Error message is not visible")
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)   
        
        #  Validate Already present error is accepted or not      
        action_factory.datasets_actions.create_dataset(dataset_name=TC_02_Dataset_Name, dataset_type_name=Dataset_Type_PDF)
        action_factory.ui_utils.smart_wait()
        error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.datasets_page.dataset_exists_error)
        if error_visible:
            status = "Pass"
            message = f"Error message for already present dataset name is visible."
            action_factory.helpers.attach_screenshot(name="DatasetNameError")
            action_factory.helpers.attach_allure(name="Error Message", text="Error message for already present dataset name is visible")
            assert True, message
        else:
            status = "Fail"
            message = f"Error message is not visible."
            action_factory.helpers.attach_screenshot(name="ErrorMessageFailed")
            action_factory.helpers.attach_allure(name="Error Message", text="Error message is not visible")
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

