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
@allure.story("Bulk Deactivate Users Validation")
@allure.title("Verify creating two users with different roles, selecting their checkboxes, performing bulk deactivation, and validating Inactive status")
def test_bulk_deactivate_users(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        user1_name = test_data_inputs.bulk_deactivate_user1_name
        user1_email = test_data_inputs.bulk_deactivate_user1_email
        user1_password = test_data_inputs.bulk_deactivate_user1_password
        user1_roles = test_data_inputs.bulk_deactivate_user1_roles

        user2_name = test_data_inputs.bulk_deactivate_user2_name
        user2_email = test_data_inputs.bulk_deactivate_user2_email
        user2_password = test_data_inputs.bulk_deactivate_user2_password
        user2_roles = test_data_inputs.bulk_deactivate_user2_roles

        # Navigate to Users menu and create User 1
        action_factory.users_actions.click_users_menu()
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=user1_name,
            email=user1_email,
            password=user1_password,
            confirm_password=user1_password
        )
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.create_roles(user1_roles)
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()

        # Create User 2 with a different role
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=user2_name,
            email=user2_email,
            password=user2_password,
            confirm_password=user2_password
        )
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.create_roles(user2_roles)
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()

        # Validate both users are present in Users list
        user_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)
        if user1_email in user_list and user2_email in user_list:
            status = "Pass"
            message = f"Both users '{user1_email}' and '{user2_email}' are present in users list."
            action_factory.helpers.attach_screenshot(name="BulkUsersCreatedAndPresent")
            action_factory.helpers.attach_allure(name="Bulk Deactivate Users Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User creation validation failed. User 1 present: {user1_email in user_list}, User 2 present: {user2_email in user_list}"
            action_factory.helpers.attach_screenshot(name="BulkUsersCreatedFail")
            action_factory.helpers.attach_allure(name="Bulk Deactivate Users Validation", text=message)
            assert False, message

        # Select checkboxes of both users and perform bulk deactivation
        action_factory.ui_utils.click_element(action_factory.page_factory.users_page.return_checkbox_click(user1_email))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.users_page.return_checkbox_click(user2_email))
        action_factory.ui_utils.smart_wait()

        action_factory.users_actions.deactivate_user()
        action_factory.ui_utils.smart_wait()

        # Validate status of both users is Deactivated / Inactive
        statuses1 = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.return_status(user1_email))
        statuses2 = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.return_status(user2_email))

        status1_text = " ".join(statuses1).lower()
        status2_text = " ".join(statuses2).lower()

        is_user1_deactivated = status1_text == "inactive" 
        is_user2_deactivated = status2_text == "inactive"

        if is_user1_deactivated and is_user2_deactivated:
            status = "Pass"
            message = f"Both users '{user1_email}' and '{user2_email}' were successfully deactivated."
            action_factory.helpers.attach_screenshot(name="BulkUsersDeactivatedPass")
            action_factory.helpers.attach_allure(name="Bulk Deactivate Users Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Bulk deactivation status validation failed. User 1 status: '{statuses1}', User 2 status: '{statuses2}'."
            action_factory.helpers.attach_screenshot(name="BulkUsersDeactivatedFail")
            action_factory.helpers.attach_allure(name="Bulk Deactivate Users Validation", text=message)
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
