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
@allure.story("Fies Pagination Check")
@allure.title("Files Pagination Check")
def test_Files_Pagination(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        multiple_file = test_data_inputs.multiple_file
        # Check files Pagination Functionality 
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.files_actions.set_files_pagination("5")
        files_name_count = action_factory.page_factory.datasets_page.files_name_list.count()
        if files_name_count > 5:
            status = "Fail"
            message = "Files name count is greater than 5"
            action_factory.helpers.attach_screenshot(name="FilesNameCountGreaterThan5")
            action_factory.helpers.attach_allure(name="Files Name Count", text="Files name count is greater than 5")
            assert False, message
        else:
            status = "Pass"
            message = "Files name count is not greater than 5"
            action_factory.helpers.attach_screenshot(name="FilesNameCountNotGreaterThan10")
            action_factory.helpers.attach_allure(name="Files Name Count", text="Files name count is not greater than 5")
            assert True, message
        # Upload Files with Pagination 5
        action_factory.datasets_actions.upload_files_with_uploadBtn(*multiple_file)
        action_factory.common_actions.validate_toast_msg("Files uploaded successfully")
        action_factory.ui_utils.smart_wait()
        files_name_count = action_factory.page_factory.datasets_page.files_name_list.count()
        if files_name_count > 5:
            status = "Fail"
            message = "Files name count is greater than 5"
            action_factory.helpers.attach_screenshot(name="FilesNameCountGreaterThan5")
            action_factory.helpers.attach_allure(name="Files Name Count", text="Files name count is greater than 5")
            assert False, message
        else:
            status = "Pass"
            message = "Files name count is not greater than 5"
            action_factory.helpers.attach_screenshot(name="FilesNameCountNotGreaterThan5")
            action_factory.helpers.attach_allure(name="Files Name Count", text="Files name count is not greater than 5")
            assert True, message
        # Next Tab Swich and Check the files Count Pagination : 
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.ui_utils.smart_wait()
        files_name_count = action_factory.page_factory.datasets_page.files_name_list.count()
        if files_name_count > 5:
            status = "Fail"
            message = "Files name count is greater than 5"
            action_factory.helpers.attach_screenshot(name="FilesNameCountGreaterThan5")
            action_factory.helpers.attach_allure(name="Files Name Count", text="Files name count is greater than 5")
            assert False, message
        else:
            status = "Pass"
            message = "Files name count is not greater than 5"
            action_factory.helpers.attach_screenshot(name="FilesNameCountNotGreaterThan10")
            action_factory.helpers.attach_allure(name="Files Name Count", text="Files name count is not greater than 5")
            assert True, message
        # Pagination for 10
        action_factory.files_actions.set_files_pagination("10")
        files_name_count = action_factory.page_factory.datasets_page.files_name_list.count()
        if files_name_count > 10:
            status = "Fail"
            message = "Files name count is greater than 10"
            action_factory.helpers.attach_screenshot(name="FilesNameCountGreaterThan10")
            action_factory.helpers.attach_allure(name="Files Name Count", text="Files name count is greater than 10")
            assert False, message
        else:
            status = "Pass"
            message = "Files name count is not greater than 10"
            action_factory.helpers.attach_screenshot(name="FilesNameCountNotGreaterThan10")
            action_factory.helpers.attach_allure(name="Files Name Count", text="Files name count is not greater than 10")
            assert True, message
        # Pagination for 20
        action_factory.files_actions.set_files_pagination("20")
        files_name_count = action_factory.page_factory.datasets_page.files_name_list.count()
        if files_name_count > 20:
            status = "Fail"
            message = "Files name count is greater than 20"
            action_factory.helpers.attach_screenshot(name="FilesNameCountGreaterThan20")
            action_factory.helpers.attach_allure(name="Files Name Count", text="Files name count is greater than 20")
            assert False, message
        else:
            status = "Pass"
            message = "Files name count is not greater than 20"
            action_factory.helpers.attach_screenshot(name="FilesNameCountNotGreaterThan20")
            action_factory.helpers.attach_allure(name="Files Name Count", text="Files name count is not greater than 20")
            assert True, message
        # Pagination for 50
        action_factory.files_actions.set_files_pagination("50")
        files_name_count = action_factory.page_factory.datasets_page.files_name_list.count()
        if files_name_count > 50:
            status = "Fail"
            message = "Files name count is greater than 50"
            action_factory.helpers.attach_screenshot(name="FilesNameCountGreaterThan50")
            action_factory.helpers.attach_allure(name="Files Name Count", text="Files name count is greater than 50")
            assert False, message
        else:
            status = "Pass"
            message = "Files name count is not greater than 50"
            action_factory.helpers.attach_screenshot(name="FilesNameCountNotGreaterThan50")
            action_factory.helpers.attach_allure(name="Files Name Count", text="Files name count is not greater than 50")
            assert True, message

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