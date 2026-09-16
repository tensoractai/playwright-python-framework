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
@allure.story("Create User Form Input Field Validation Errors")
@allure.title("Verify inline validation errors for invalid email, short password, mismatched confirm password, and disabled submit state")
def test_create_user_validation_errors(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        invalid_name = test_data_inputs.invalid_user_name
        invalid_email = test_data_inputs.invalid_email
        short_pwd = test_data_inputs.invalid_short_password
        confirm_pwd = test_data_inputs.invalid_confirm_password

        # Open Users Menu and click Create User
        action_factory.users_actions.click_users_menu()
        action_factory.users_actions.click_create_user()

        # Fill Invalid Name and Invalid Email
        action_factory.ui_utils.fill_input(action_factory.page_factory.users_page.enter_name, invalid_name)
        action_factory.ui_utils.fill_input(action_factory.page_factory.users_page.enter_email, invalid_email)

        # Click Password Field and Validate Invalid email address error is visible
        action_factory.ui_utils.click_element(action_factory.page_factory.users_page.enter_password)
        action_factory.ui_utils.smart_wait()
        invalid_email_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.users_page.invalid_email_error)
        if invalid_email_visible:
            status="Pass"
            message="Validation error 'Invalid email address' is visible"
            action_factory.helpers.attach_screenshot(name="CreateUserInvalidEmailErrorVisible")
            action_factory.helpers.attach_allure(name="CreateUserInvalidEmailErrorVisible", text=message)
        else:
            status = "Fail"
            message = "Validation error 'Invalid email address' is not visible."
            action_factory.helpers.attach_screenshot(name="CreateUserInvalidEmailErrorNotVisible")
            action_factory.helpers.attach_allure(name="CreateUserInvalidEmailErrorNotVisible", text=message)
            assert False, message

        # Enter short password
        action_factory.ui_utils.fill_input(action_factory.page_factory.users_page.enter_password, short_pwd)

        # Click Confirm Password field and Validate error 'Password must be at least 8'
        action_factory.ui_utils.click_element(action_factory.page_factory.users_page.confirm_password)
        action_factory.ui_utils.smart_wait()
        min_password_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.users_page.min_password_error)
        if min_password_visible:
            status="Pass"
            message="Validation error 'Password must be at least 8' is visible"
            action_factory.helpers.attach_screenshot(name="CreateUserMinPasswordErrorVisible")
            action_factory.helpers.attach_allure(name="CreateUserMinPasswordErrorVisible", text=message)
        else:
            status = "Fail"
            message = "Validation error 'Password must be at least 8' is not visible."
            action_factory.helpers.attach_screenshot(name="CreateUserMinPasswordErrorNotVisible")
            action_factory.helpers.attach_allure(name="CreateUserMinPasswordErrorNotVisible", text=message)
            assert False, message

        # Enter confirm password
        action_factory.ui_utils.fill_input(action_factory.page_factory.users_page.confirm_password, confirm_pwd)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.users_page.create_user_heading)
        mismatch_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.users_page.passwords_must_match_error)
        if mismatch_visible:
            status="Pass"
            message="Validation error 'Passwords must match' is visible"
            action_factory.helpers.attach_screenshot(name="CreateUserPasswordsMustMatchErrorVisible")
            action_factory.helpers.attach_allure(name="CreateUserPasswordsMustMatchErrorVisible", text=message)
        else:
            status = "Fail"
            message = "Validation error 'Passwords must match' is not visible."
            action_factory.helpers.attach_screenshot(name="CreateUserPasswordsMustMatchErrorNotVisible")
            action_factory.helpers.attach_allure(name="CreateUserPasswordsMustMatchErrorNotVisible", text=message)
            assert False, message

        # Select Roles and click Company Admin
        action_factory.users_actions.create_roles("Company Admin")

        # Enable Allow MFA
        action_factory.users_actions.enable_allow_mfa_email()

        # Validate Create User button is in disabled mode
        create_user_disabled = not action_factory.ui_utils.is_element_enabled(action_factory.page_factory.users_page.create_user)
        if create_user_disabled:
            status = "Pass"
            message = "Inline field validation errors verified successfully and Create User button is disabled for invalid form input."
            action_factory.helpers.attach_screenshot(name="CreateUserDisabledAfterInvalidInputs")
            action_factory.helpers.attach_allure(name="CreateUserDisabledAfterInvalidInputs", text=message)
            assert True, message
        else:
            status = "Fail"
            message = "Create User button was unexpectedly enabled for invalid form input."
            action_factory.helpers.attach_screenshot(name="CreateUserEnabledAfterInvalidInputs")
            action_factory.helpers.attach_allure(name="CreateUserEnabledAfterInvalidInputs", text=message)
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
