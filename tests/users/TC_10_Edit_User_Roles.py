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
@allure.story("Edit User Roles Validation")
@allure.title("Verify user creation, editing user roles, and validating user presence after role update")
def test_edit_user_roles(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        user_name = test_data_inputs.edit_roles_user_name
        user_email = test_data_inputs.edit_roles_user_email
        user_password = test_data_inputs.edit_roles_user_password
        initial_roles = test_data_inputs.edit_roles_initial_roles
        new_role = test_data_inputs.edit_roles_new_role

        # Navigate to Users menu and create new user
        action_factory.users_actions.click_users_menu()
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=user_name,
            email=user_email,
            password=user_password,
            confirm_password=user_password
        )
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.create_roles(initial_roles)
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()

        # Validate created user is present
        user_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)
        if user_email in user_list:
            status = "Pass"
            message = f"User '{user_email}' created successfully and present in users list."
            action_factory.helpers.attach_screenshot(name="UserCreatedPresent")
            action_factory.helpers.attach_allure(name="Edit User Roles Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User '{user_email}' was not found in users list after creation."
            action_factory.helpers.attach_screenshot(name="UserNotPresentFail")
            action_factory.helpers.attach_allure(name="Edit User Roles Validation", text=message)
            assert False, message

        # Select edit button for user and change roles
        action_factory.users_actions.edit_user_roles(
            user_name=user_name,
            roles_to_toggle=[new_role, "Company Admin"]
        )

        # Validate user is still present after role update
        action_factory.ui_utils.smart_wait()
        users_after_edit = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)
        if user_email in users_after_edit:
            status = "Pass"
            message = f"User '{user_email}' roles edited successfully and user is present in users list."
            action_factory.helpers.attach_screenshot(name="UserPresentAfterRoleEditPass")
            action_factory.helpers.attach_allure(name="Edit User Roles Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User '{user_email}' was not found in users list after editing roles."
            action_factory.helpers.attach_screenshot(name="UserNotPresentAfterRoleEditFail")
            action_factory.helpers.attach_allure(name="Edit User Roles Validation", text=message)
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
