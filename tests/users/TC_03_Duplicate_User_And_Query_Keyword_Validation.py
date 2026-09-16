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
@allure.story("Duplicate User Creation & Query Keyword Input Validation")
@allure.title("Verify error when creating duplicate user and validate query keyword 'DROP' user creation restriction")
def test_duplicate_user_and_query_keyword_validation(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        existing_name = test_data_inputs.valid_user_name
        existing_email = test_data_inputs.valid_user_email
        existing_password = test_data_inputs.valid_user_password
        existing_roles = test_data_inputs.valid_user_roles

        drop_name = test_data_inputs.sql_drop_name
        drop_email = test_data_inputs.sql_drop_email
        drop_password = test_data_inputs.sql_drop_password

        # Navigate to Users Menu and click Create User
        action_factory.users_actions.click_users_menu()
        action_factory.users_actions.click_create_user()

        # Attempt to create duplicate user using TC_01 user details
        action_factory.users_actions.fill_user_form(
            full_name=existing_name.upper(),
            email=existing_email,
            password=existing_password,
            confirm_password=existing_password
        )
        action_factory.users_actions.create_roles(existing_roles)
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()

        # Validate duplicate user error 'User already exists in this'
        duplicate_error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.users_page.user_already_exists_error)
        if duplicate_error_visible:
            status="Pass"
            message="User already exists in this error is visible"
            action_factory.helpers.attach_screenshot(name="DuplicateUserErrorVisible")
            action_factory.helpers.attach_allure(name="Duplicate User Error", text=message)
        else:
            status="Fail"
            message="User already exists in this error is not visible"
            action_factory.helpers.attach_screenshot(name="DuplicateUserErrorNotVisible")
            action_factory.helpers.attach_allure(name="Duplicate User Error", text=message)
            assert False, message

        # Close Create User Window
        action_factory.ui_utils.click_element(action_factory.page_factory.users_page.close_modal_btn)
        action_factory.ui_utils.smart_wait()

        # Click Create User again for Query keyword validation
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=drop_name,
            email=drop_email,
            password=drop_password,
            confirm_password=drop_password
        )
        action_factory.users_actions.create_roles("Company Admin")
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()

        # Validate user list: user with query keyword 'DROP' should not be created
        action_factory.users_actions.search_user(drop_email)
        action_factory.ui_utils.smart_wait()
        user_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)

        if drop_email not in user_list:
            status = "Pass"
            message = "Duplicate user error verified and query keyword 'DROP' user was correctly restricted from creation."
            action_factory.helpers.attach_screenshot(name="QueryKeywordUserNotCreatedPass")
            action_factory.helpers.attach_allure(name="Duplicate & Query Keyword Validation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Query keyword user '{drop_email}' was unexpectedly created in users list."
            action_factory.helpers.attach_screenshot(name="QueryKeywordUserCreatedFail")
            action_factory.helpers.attach_allure(name="Duplicate & Query Keyword Validation", text=message)
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
