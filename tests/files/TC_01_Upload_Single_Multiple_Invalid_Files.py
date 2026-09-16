import allure
import pytest
from actions.action_factory import ActionFactory
from tests.files.test_data_inputs import test_data_inputs

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
@allure.story("Upload Single Multiple and Invalid files")
@allure.title("Upload Single Multiple and Invalid files")
def test_Upload_Single_Multiple_Invalid_Files(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        single_file = test_data_inputs.single_file
        multiple_file = test_data_inputs.multiple_file
        invalid_file = test_data_inputs.invalid_file

        # Upload Single File
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.datasets_actions.upload_files_with_uploadBtn(*single_file)
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_single_file = [file.split("/")[-1] for file in single_file]        
        if all(file in files_name_list for file in expected_single_file):
            status = "Pass"
            message = f"Single file uploaded successfully."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_single_file))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload Single files."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_single_file))
            assert False, message

        # Upload Multiple Files 
        action_factory.datasets_actions.upload_files_with_uploadBtn(*multiple_file)
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_multiple_files = [file.split("/")[-1] for file in multiple_file]
        if all(file in files_name_list for file in expected_multiple_files):
            status = "Pass"
            message = f"All files uploaded successfully."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_multiple_files))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload all files."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_multiple_files))
            assert False, message

        # Upload Invalid Files 
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.files_actions.upload_files_without_uploadbtn(*invalid_file)
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
        upload_btn_disabled = action_factory.ui_utils.is_element_disabled(action_factory.page_factory.datasets_page.upload_button)
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
