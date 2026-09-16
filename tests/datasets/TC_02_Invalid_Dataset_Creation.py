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
@allure.story("Invalid Dataset Creation")
@allure.title("Invalid Dataset Creation")
def test_create_dataset_Invalid(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        Dataset_Name_Invalid = test_data_inputs.Dataset_Name_Invalid
        Dataset_Type_PDF = test_data_inputs.Dataset_Type_PDF
        Dataset_File_Invalid = test_data_inputs.Dataset_File_Invalid
        description = test_data_inputs.description

        # Create Valid Dataset and Upload File and Validate in Files Page as well 
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.datasets_actions.create_dataset(dataset_name=Dataset_Name_Invalid, dataset_type_name=Dataset_Type_PDF, description = description)
        action_factory.ui_utils.smart_wait()
        dataset_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        print(f"Dataset names list: {dataset_name_list}")
        if Dataset_Name_Invalid in dataset_name_list:
            status = "Pass"
            message = f"Dataset '{Dataset_Name_Invalid}' created successfully."
            action_factory.helpers.attach_screenshot(name="DatasetCreated")
            action_factory.helpers.attach_allure(name="Dataset Name", text=Dataset_Name_Invalid)
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset '{Dataset_Name_Invalid}' creation failed."
            action_factory.helpers.attach_screenshot(name="DatasetCreationFailed")
            action_factory.helpers.attach_allure(name="Dataset Name", text=Dataset_Name_Invalid)
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(Dataset_Name_Invalid))
        action_factory.files_actions.upload_files_without_uploadbtn(*Dataset_File_Invalid)
        action_factory.ui_utils.smart_wait()
        invalid_error = action_factory.ui_utils.is_element_visible(action_factory.page_factory.files_page.invalid_file_error)
        if invalid_error:
            status = "Pass"
            message = f"Invalid file error is visible."
            action_factory.helpers.attach_screenshot(name="InvalidFileError")
            action_factory.helpers.attach_allure(name="Invalid File Error", text="Invalid file error is visible")
            assert True, message
        else:
            status = "Fail"
            message = f"Invalid file error is not visible."
            action_factory.helpers.attach_screenshot(name="InvalidFileErrorFailed")
            action_factory.helpers.attach_allure(name="Invalid File Error", text="Invalid file error is not visible")
            assert False, message

        upload_btn_disabled = action_factory.ui_utils.is_element_disabled(action_factory.page_factory.datasets_page.upload_button.nth(1))
        if upload_btn_disabled:
            status = "Pass"
            message = f"Upload button is not enabled."
            action_factory.helpers.attach_screenshot(name="UploadButtonNotEnabled")
            action_factory.helpers.attach_allure(name="Upload Button", text="Upload button is not enabled")
            assert True, message
        else:
            status = "Fail"
            message = f"Upload button is enabled."
            action_factory.helpers.attach_screenshot(name="UploadButtonEnabled")
            action_factory.helpers.attach_allure(name="Upload Button", text="Upload button is enabled")
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


