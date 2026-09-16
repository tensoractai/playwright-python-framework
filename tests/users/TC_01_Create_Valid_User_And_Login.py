import allure
import pytest
from actions.action_factory import ActionFactory
from tests.users.test_data_inputs import test_data_inputs

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

@allure.feature("Users")
@allure.story("Create Valid User & Verify Login as Company Admin")
@allure.title("Verify creating a valid user with multiple roles and logging in with newly created credentials")
def test_create_valid_user_and_login(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        url = action_factory.helpers.fetch_dotenv("Execution_url")
        company_Name = action_factory.helpers.fetch_dotenv("company_Name")
        diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
        diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")
        
        user_name = test_data_inputs.valid_user_name
        user_email = test_data_inputs.valid_user_email
        user_password = test_data_inputs.valid_user_password
        user_roles = test_data_inputs.valid_user_roles
        updated_new_password = test_data_inputs.updated_new_password

        # Open Users Menu and Click Create User and create one Valid User 
        action_factory.users_actions.click_users_menu()
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(full_name=user_name, email=user_email, password=user_password, confirm_password=user_password)
        action_factory.users_actions.create_roles(user_roles)
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()
        user_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)
        if user_email in user_list:
            status = "Pass"
            message = f"Valid user '{user_email}' created successfully."
            action_factory.helpers.attach_screenshot(name="User Created Successfully")
            action_factory.helpers.attach_allure(name="User Created Successfully", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Valid user '{user_email}' not created successfully."
            action_factory.helpers.attach_screenshot(name="User Created Failed")
            action_factory.helpers.attach_allure(name="User Created Failed", text=message)
            assert False, message

        # Open new Chromium browser instance/context without logging out current session
        new_context = action_factory.page.context.browser.new_context()
        new_page = new_context.new_page()
        new_action_factory = ActionFactory(new_page)

        try:
            new_action_factory.login_actions.perform_login_new_user(url=url, email=user_email, password=user_password)
            new_action_factory.users_actions.user_settings_changePassword(updated_new_password)
            new_action_factory.login_actions.perform_login(url=url, email=user_email, password=updated_new_password)
            new_action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
            new_action_factory.login_actions.select_organization(company_Name, "Company Admin")
            new_action_factory.ui_utils.smart_wait()
            welcome_visible = new_action_factory.ui_utils.is_element_visible(new_action_factory.page_factory.login_page.home_page_welcome)
            if welcome_visible:
                status = "pass"
                message = f"Valid user '{user_email}' created successfully and verified login as Company Admin in new browser instance."
                new_action_factory.helpers.attach_screenshot(name="User Logged In successfully")
                new_action_factory.helpers.attach_allure(name="User Logged In successfully", text=message)
                assert True, message
            else:
                status = "fail"
                message = f"Valid user '{user_email}' failed login verification in new browser instance."
                new_action_factory.helpers.attach_screenshot(name="User Failed To Login")
                new_action_factory.helpers.attach_allure(name="User Failed To Login", text=message)
                assert False, message
        finally:
            new_context.close()
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
