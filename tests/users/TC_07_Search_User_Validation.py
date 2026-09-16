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
@allure.story("Search User Validation")
@allure.title("Verify user creation, searching valid user, and searching non-existing user displays No users found message")
def test_search_user_validation(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        user_name = test_data_inputs.search_user_name
        user_email = test_data_inputs.search_user_email
        user_password = test_data_inputs.search_user_password
        user_roles = test_data_inputs.search_user_roles
        invalid_search_text = test_data_inputs.non_existing_search_user
        
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
        action_factory.users_actions.create_roles(user_roles)
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()
        
        # Search created user and validate presence
        action_factory.users_actions.search_user(user_email)
        user_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)
        if user_email in user_list:
            status = "Pass"
            message = f"User is created successfully"
            action_factory.helpers.attach_screenshot(name="ValidUserSearchResult")
            action_factory.helpers.attach_allure(name="User Created", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User is not created"
            action_factory.helpers.attach_screenshot(name="UserCreatedFail")
            action_factory.helpers.attach_allure(name="User Created", text=message)
            assert False, message

        # Search invalid non-existing user name
        action_factory.users_actions.search_user(invalid_search_text)
        no_users_found_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.users_page.no_user_found)
        if no_users_found_visible:
            status = "Pass"
            message = f"No users found message is displayed for invalid search"
            action_factory.helpers.attach_screenshot(name="InvalidUserSearchNoUsersFound")
            action_factory.helpers.attach_allure(name="User Created", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"No users found message is not displayed for invalid search"
            action_factory.helpers.attach_screenshot(name="InvalidUserSearchNoUsersFoundFail")
            action_factory.helpers.attach_allure(name="User Created", text=message)
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
