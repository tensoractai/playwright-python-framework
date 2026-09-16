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
@allure.story("Search Files Name")
@allure.title("Search Files Name")
def test_Search_Files_Name(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        search_file = test_data_inputs.search_file
        search_dataset_name = test_data_inputs.search_dataset_name
        search_dataset_type = test_data_inputs.search_dataset_type
        search_dataset_file = test_data_inputs.search_dataset_file

        # Upload one file 
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.datasets_actions.upload_files_with_uploadBtn(*search_file)
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")
        action_factory.ui_utils.smart_wait()

        # Search the file Name and Validate
        search_file_name = search_file[0].split("/")[-1]
        action_factory.files_actions.search_files_name(search_file_name)
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        if search_file_name in files_name_list:
            status = "Pass"
            message = f"Seached file displayed properly"
            action_factory.helpers.attach_screenshot(name="SearchedFileDisplayedProperly")
            action_factory.helpers.attach_allure(name="Searched File", text="Searched file displayed properly")
            assert True, message
        else:
            status = "Fail"
            message = f"Searched file not displayed properly"
            action_factory.helpers.attach_screenshot(name="SearchedFileNotDisplayedProperly")
            action_factory.helpers.attach_allure(name="Searched File", text="Searched file not displayed properly")
            assert False, message    

        # Create One Dataset and Upload and Search that File :
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.datasets_actions.create_dataset(dataset_name=search_dataset_name, dataset_type_name=search_dataset_type)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(search_dataset_name))
        action_factory.datasets_actions.upload_files_with_uploadBtn(*search_dataset_file)
        action_factory.common_actions.validate_toast_msg("1 file added")
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files_single = [file.split("/")[-1] for file in search_dataset_file]        
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
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.ui_utils.smart_wait()
        expected_files_search = expected_files_single[0].split("/")[-1]
        action_factory.files_actions.search_files_name(expected_files_search)
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        if expected_files_search in files_name_list:
            status = "Pass"
            message = f"Seached file displayed properly"
            action_factory.helpers.attach_screenshot(name="SearchedFileDisplayedProperly")
            action_factory.helpers.attach_allure(name="Searched File", text="Searched file displayed properly")
            assert True, message
        else:
            status = "Fail"
            message = f"Searched file not displayed properly"
            action_factory.helpers.attach_screenshot(name="SearchedFileNotDisplayedProperly")
            action_factory.helpers.attach_allure(name="Searched File", text="Searched file not displayed properly")
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