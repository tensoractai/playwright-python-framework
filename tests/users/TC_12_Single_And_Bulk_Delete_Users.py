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
@allure.story("Single and Bulk Delete Users Validation")
@allure.title("Verify creating 3 users, single deleting 1 user, and bulk deleting the remaining 2 users")
def test_single_and_bulk_delete_users(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        user1_name = test_data_inputs.single_bulk_delete_user1_name
        user1_email = test_data_inputs.single_bulk_delete_user1_email
        user1_password = test_data_inputs.single_bulk_delete_user1_password
        user1_roles = test_data_inputs.single_bulk_delete_user1_roles

        user2_name = test_data_inputs.single_bulk_delete_user2_name
        user2_email = test_data_inputs.single_bulk_delete_user2_email
        user2_password = test_data_inputs.single_bulk_delete_user2_password
        user2_roles = test_data_inputs.single_bulk_delete_user2_roles

        user3_name = test_data_inputs.single_bulk_delete_user3_name
        user3_email = test_data_inputs.single_bulk_delete_user3_email
        user3_password = test_data_inputs.single_bulk_delete_user3_password
        user3_roles = test_data_inputs.single_bulk_delete_user3_roles

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

        # Create User 2
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

        # Create User 3
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=user3_name,
            email=user3_email,
            password=user3_password,
            confirm_password=user3_password
        )
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.create_roles(user3_roles)
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()

        # Validate that all 3 users are present in Users list
        user_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)
        all_created = user1_email in user_list and user2_email in user_list and user3_email in user_list
        if all_created:
            status = "Pass"
            message = "All 3 users created and verified in users list."
            action_factory.helpers.attach_screenshot(name="ThreeUsersCreatedPresent")
            action_factory.helpers.attach_allure(name="Single and Bulk Delete Users Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User creation validation failed. User 1: {user1_email in user_list}, User 2: {user2_email in user_list}, User 3: {user3_email in user_list}"
            action_factory.helpers.attach_screenshot(name="ThreeUsersCreatedFail")
            action_factory.helpers.attach_allure(name="Single and Bulk Delete Users Validation", text=message)
            assert False, message

        # Single delete first user: select checkbox of User 1 and delete
        action_factory.ui_utils.click_element(action_factory.page_factory.users_page.return_checkbox_click(user1_email))
        action_factory.ui_utils.smart_wait()
        action_factory.users_actions.delete_user()
        action_factory.ui_utils.smart_wait()

        # Validate first user is deleted
        user_list_after_single_delete = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)
        if user1_email not in user_list_after_single_delete:
            status = "Pass"
            message = f"Single user '{user1_email}' deleted successfully."
            action_factory.helpers.attach_screenshot(name="SingleUserDeletedPass")
            action_factory.helpers.attach_allure(name="Single and Bulk Delete Users Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Single user '{user1_email}' was not deleted from users list."
            action_factory.helpers.attach_screenshot(name="SingleUserDeletedFail")
            action_factory.helpers.attach_allure(name="Single and Bulk Delete Users Validation", text=message)
            assert False, message

        # Bulk delete remaining 2 users: select checkboxes of User 2 and User 3 and delete
        action_factory.ui_utils.click_element(action_factory.page_factory.users_page.return_checkbox_click(user2_email))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.users_page.return_checkbox_click(user3_email))
        action_factory.ui_utils.smart_wait()

        action_factory.users_actions.delete_user()
        action_factory.ui_utils.smart_wait()

        # Validate remaining 2 users are deleted
        user_list_after_bulk_delete = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)
        bulk_deleted = user2_email not in user_list_after_bulk_delete and user3_email not in user_list_after_bulk_delete
        if bulk_deleted:
            status = "Pass"
            message = f"Bulk users '{user2_email}' and '{user3_email}' deleted successfully."
            action_factory.helpers.attach_screenshot(name="BulkUsersDeletedPass")
            action_factory.helpers.attach_allure(name="Single and Bulk Delete Users Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Bulk delete validation failed. User 2 deleted: {user2_email not in user_list_after_bulk_delete}, User 3 deleted: {user3_email not in user_list_after_bulk_delete}"
            action_factory.helpers.attach_screenshot(name="BulkUsersDeletedFail")
            action_factory.helpers.attach_allure(name="Single and Bulk Delete Users Validation", text=message)
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
