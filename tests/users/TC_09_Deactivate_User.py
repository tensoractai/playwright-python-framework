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
    
    # Login & Setup as Company Admin
    action_factory.login_actions.perform_login(url=url, email=email, password=password)
    action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("Users")
@allure.story("Deactivate User Validation")
@allure.title("Verify user creation, user presence validation, deactivating user, and verifying Deactive status")
def test_deactivate_user_and_validate_status(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        user_name = test_data_inputs.deactivate_user_name
        user_email = test_data_inputs.deactivate_user_email
        user_password = test_data_inputs.deactivate_user_password
        user_roles = test_data_inputs.deactivate_user_roles

        # Navigate to Users menu and create user
        action_factory.users_actions.click_users_menu()
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=user_name,
            email=user_email,
            password=user_password,
            confirm_password=user_password
        )
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.create_roles(user_roles)
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()

        # Validate user is present in Users list
        user_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)
        if user_email in user_list:
            status = "Pass"
            message = f"User {user_email} is present"
            action_factory.helpers.attach_screenshot(name="UserPresent")
            action_factory.helpers.attach_allure(name="Deactivate User Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User {user_email} is not present"
            action_factory.helpers.attach_screenshot(name="UserNotPresent")
            action_factory.helpers.attach_allure(name="Deactivate User Validation", text=message)
            assert False, message

        # Select user checkbox and deactivate user
        action_factory.ui_utils.click_element(action_factory.page_factory.users_page.return_checkbox_click(user_email))
        action_factory.ui_utils.smart_wait()
        action_factory.users_actions.deactivate_user()
        action_factory.ui_utils.smart_wait()

        # Validate user status is Deactive/Inactive
        statuses = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.return_status(user_email))
        status_text = " ".join(statuses).lower()
        if status_text == "inactive":
            status = "Pass"
            message = f"User '{user_email}' was successfully deactivated and status is '{statuses}'."
            action_factory.helpers.attach_screenshot(name="UserStatusDeactivatedPass")
            action_factory.helpers.attach_allure(name="Deactivate User Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User '{user_email}' status validation failed. Current status text: '{statuses}'."
            action_factory.helpers.attach_screenshot(name="UserStatusDeactivatedFail")
            action_factory.helpers.attach_allure(name="Deactivate User Validation", text=message)
            assert False, message

        # Try logging in with deactivated user in a new context and verify 'Your account is not active.' error
        url = action_factory.helpers.fetch_dotenv("Execution_url")
        new_context = action_factory.page.context.browser.new_context()
        new_page = new_context.new_page()
        new_action_factory = ActionFactory(new_page)
        try:
            new_action_factory.ui_utils.goto(url)
            new_action_factory.ui_utils.smart_wait()
            new_action_factory.ui_utils.fill_input(new_action_factory.page_factory.login_page.email_input, user_email)
            new_action_factory.ui_utils.fill_input(new_action_factory.page_factory.login_page.password_input, user_password)
            new_action_factory.ui_utils.click_element(new_action_factory.page_factory.login_page.sign_in_button)
            new_action_factory.ui_utils.smart_wait()
            error_visible = new_action_factory.ui_utils.is_element_visible(new_action_factory.page_factory.login_page.account_not_active_error)
            if error_visible:
                status = "Pass"
                message = f"Deactivated user '{user_email}' login attempt correctly displayed 'Your account is not active.' error."
                new_action_factory.helpers.attach_screenshot(name="DeactivatedUserAccountNotActiveErrorPass")
                new_action_factory.helpers.attach_allure(name="Deactivated User Login Validation", text=message)
                assert True, message
            else:
                status = "Fail"
                message = f"Deactivated user '{user_email}' login attempt did not display 'Your account is not active.' error."
                new_action_factory.helpers.attach_screenshot(name="DeactivatedUserAccountNotActiveErrorFail")
                new_action_factory.helpers.attach_allure(name="Deactivated User Login Validation", text=message)
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
