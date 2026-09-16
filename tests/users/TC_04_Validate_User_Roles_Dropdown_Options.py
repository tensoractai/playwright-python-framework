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
@allure.story("Validate Roles Dropdown Options List")
@allure.title("Verify opening Roles dropdown in Create User form and validating that only expected valid user roles are present")
def test_validate_user_roles_dropdown_options(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        expected_roles = test_data_inputs.valid_user_roles

        # Open Users Menu and click Create User
        action_factory.users_actions.click_users_menu()
        action_factory.users_actions.click_create_user()
        action_factory.ui_utils.click_element(action_factory.page_factory.users_page.select_roles)
        action_factory.ui_utils.smart_wait()
        actual_roles = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.all_roles_list_options)
        actual_roles_lower = [role.strip().lower() for role in actual_roles if role.strip()]
        missing_roles = [role for role in expected_roles if role.lower() not in actual_roles_lower]

        if len(missing_roles) == 0:
            status = "Pass"
            message = f"Roles dropdown options validated successfully. Found roles: {actual_roles}."
            action_factory.helpers.attach_screenshot(name="RolesDropdownOptionsValidationPass")
            action_factory.helpers.attach_allure(name="Validate Roles Options", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Missing expected roles in dropdown: {missing_roles}. Found roles: {actual_roles}"
            action_factory.helpers.attach_screenshot(name="RolesDropdownOptionsValidationFail")
            action_factory.helpers.attach_allure(name="Validate Roles Options", text=message)
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
