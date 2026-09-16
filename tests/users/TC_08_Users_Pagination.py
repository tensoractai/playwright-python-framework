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
@allure.story("Users Pagination Check")
@allure.title("Verify users pagination control for limits 5, 10, 20, and 50 with user creation and tab switching persistence")
def test_users_pagination(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        user_name = test_data_inputs.pagination_user_name
        user_email = test_data_inputs.pagination_user_email
        user_password = test_data_inputs.pagination_user_password
        user_roles = test_data_inputs.pagination_user_roles

        # Navigate to Users menu
        action_factory.users_actions.click_users_menu()
        action_factory.ui_utils.smart_wait()

        # Set pagination to 5 and validate 5 or less shown
        action_factory.users_actions.set_users_pagination("5")
        user_count = action_factory.page_factory.users_page.email_address_list.count()
        if user_count <= 5:
            status = "Pass"
            message = f"User count ({user_count}) is within limit for pagination 5."
            action_factory.helpers.attach_screenshot(name="UsersPagination5Pass")
            action_factory.helpers.attach_allure(name="Users Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User count ({user_count}) exceeds limit of 5."
            action_factory.helpers.attach_screenshot(name="UsersPagination5Failed")
            action_factory.helpers.attach_allure(name="Users Pagination Check", text=message)
            assert False, message

        # Create new user after setting pagination to 5 and check pagination 5 persists
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

        user_count_after_create = action_factory.page_factory.users_page.email_address_list.count()
        if user_count_after_create <= 5:
            status = "Pass"
            message = f"User count ({user_count_after_create}) remains <= 5 after creating a new user."
            action_factory.helpers.attach_screenshot(name="PaginationPreservedAfterUserCreation")
            action_factory.helpers.attach_allure(name="Users Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User count ({user_count_after_create}) exceeded limit of 5 after user creation."
            action_factory.helpers.attach_screenshot(name="PaginationNotPreservedAfterCreation")
            action_factory.helpers.attach_allure(name="Users Pagination Check", text=message)
            assert False, message

        # Switch tabs/menu to Datasets and return to Users menu, then verify pagination 5 persists
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.users_actions.click_users_menu()
        action_factory.ui_utils.smart_wait()

        user_count_after_switch = action_factory.page_factory.users_page.email_address_list.count()
        if user_count_after_switch <= 5:
            status = "Pass"
            message = f"User count ({user_count_after_switch}) remains <= 5 after switching menu and returning."
            action_factory.helpers.attach_screenshot(name="PaginationPreservedAfterMenuSwitch")
            action_factory.helpers.attach_allure(name="Users Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User count ({user_count_after_switch}) exceeded limit of 5 after menu switch."
            action_factory.helpers.attach_screenshot(name="PaginationNotPreservedAfterSwitch")
            action_factory.helpers.attach_allure(name="Users Pagination Check", text=message)
            assert False, message

        # Set pagination to 10 and check
        action_factory.users_actions.set_users_pagination("10")
        user_count_10 = action_factory.page_factory.users_page.email_address_list.count()
        if user_count_10 <= 10:
            status = "Pass"
            message = f"User count ({user_count_10}) is within limit for pagination 10."
            action_factory.helpers.attach_screenshot(name="UsersPagination10Pass")
            action_factory.helpers.attach_allure(name="Users Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User count ({user_count_10}) exceeds limit of 10."
            action_factory.helpers.attach_screenshot(name="UsersPagination10Failed")
            action_factory.helpers.attach_allure(name="Users Pagination Check", text=message)
            assert False, message

        # Set pagination to 20 and check
        action_factory.users_actions.set_users_pagination("20")
        user_count_20 = action_factory.page_factory.users_page.email_address_list.count()
        if user_count_20 <= 20:
            status = "Pass"
            message = f"User count ({user_count_20}) is within limit for pagination 20."
            action_factory.helpers.attach_screenshot(name="UsersPagination20Pass")
            action_factory.helpers.attach_allure(name="Users Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User count ({user_count_20}) exceeds limit of 20."
            action_factory.helpers.attach_screenshot(name="UsersPagination20Failed")
            action_factory.helpers.attach_allure(name="Users Pagination Check", text=message)
            assert False, message

        # Set pagination to 50 and check
        action_factory.users_actions.set_users_pagination("50")
        user_count_50 = action_factory.page_factory.users_page.email_address_list.count()
        if user_count_50 <= 50:
            status = "Pass"
            message = f"User count ({user_count_50}) is within limit for pagination 50."
            action_factory.helpers.attach_screenshot(name="UsersPagination50Pass")
            action_factory.helpers.attach_allure(name="Users Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User count ({user_count_50}) exceeds limit of 50."
            action_factory.helpers.attach_screenshot(name="UsersPagination50Failed")
            action_factory.helpers.attach_allure(name="Users Pagination Check", text=message)
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
