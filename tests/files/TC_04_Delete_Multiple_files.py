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
@allure.story("Delete Multiple Files")
@allure.title("Delete Multiple Files")
def test_Delete_Multiple_Files(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        multiple_file = test_data_inputs.multiple_file

        # Delete Multiple Files and Validate the Popups
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.datasets_actions.upload_files_with_uploadBtn(*multiple_file)
        action_factory.ui_utils.smart_wait()
        action_factory.files_actions.delete_multiple_files(5)
        action_factory.ui_utils.smart_wait()
        delete_success = action_factory.ui_utils.wait_for_visible_if_exists(action_factory.page_factory.files_page.return_delete_message("Successfully Deleted Files"))
        if delete_success:
            status = "Pass"
            message = f"Delete success message found"
            action_factory.helpers.attach_screenshot(name="DeleteSuccessMessageFound")
            action_factory.helpers.attach_allure(name="Delete Success Message", text="Delete success message found")
            assert True, message
        else:
            status = "Fail"
            message = f"Delete success message not found"
            action_factory.helpers.attach_screenshot(name="DeleteSuccessMessageNotFound")
            action_factory.helpers.attach_allure(name="Delete Success Message", text="Delete success message not found")
            assert False, message 
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()
        delete_confirmation = action_factory.ui_utils.wait_for_visible_if_exists(action_factory.page_factory.files_page.delete_confirmation)
        if not delete_confirmation:
            status = "Pass"
            message = f"Delete confirmation not found"
            action_factory.helpers.attach_screenshot(name="DeleteConfirmationNotFoun")
            action_factory.helpers.attach_allure(name="Delete Confirmation", text="Delete confirmation not found")
            assert True, message
        else:
            status = "Fail"
            message = f"Delete confirmation found"
            action_factory.helpers.attach_screenshot(name="DeleteConfirmationFound")
            action_factory.helpers.attach_allure(name="Delete Confirmation", text="Delete confirmation found")
            assert False, message 

        # Delete Single Files and Validate the Popups
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.files_actions.delete_multiple_files(1)
        action_factory.ui_utils.smart_wait()
        delete_success = action_factory.ui_utils.wait_for_visible_if_exists(action_factory.page_factory.files_page.return_delete_message("Successfully Deleted File"))
        if delete_success:
            status = "Pass"
            message = f"Delete success message found"
            action_factory.helpers.attach_screenshot(name="DeleteSuccessMessageFound")
            action_factory.helpers.attach_allure(name="Delete Success Message", text="Delete success message found")
            assert True, message
        else:
            status = "Fail"
            message = f"Delete success message not found"
            action_factory.helpers.attach_screenshot(name="DeleteSuccessMessageNotFound")
            action_factory.helpers.attach_allure(name="Delete Success Message", text="Delete success message not found")
            assert False, message 
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()
        delete_confirmation = action_factory.ui_utils.wait_for_visible_if_exists(action_factory.page_factory.files_page.delete_confirmation)
        if not delete_confirmation:
            status = "Pass"
            message = f"Delete confirmation not found"
            action_factory.helpers.attach_screenshot(name="DeleteConfirmationNotFoun")
            action_factory.helpers.attach_allure(name="Delete Confirmation", text="Delete confirmation not found")
            assert True, message
        else:
            status = "Fail"
            message = f"Delete confirmation found"
            action_factory.helpers.attach_screenshot(name="DeleteConfirmationFound")
            action_factory.helpers.attach_allure(name="Delete Confirmation", text="Delete confirmation found")
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