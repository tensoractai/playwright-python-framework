import allure
import pytest
from actions.action_factory import ActionFactory
from tests.users.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
    password = action_factory.helpers.fetch_dotenv("company_Password")
    diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
    diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")
    
    # Login & Setup as Super User
    action_factory.login_actions.perform_login(url=url, email=email, password=password)
    action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
    action_factory.login_actions.select_organization(company_Name, "Super User")
    return action_factory

@allure.feature("Users")
@allure.story("Delete Company and Validate Cascade Removal of Users")
@allure.title("Verify creating company and user as Super User, deleting company, and validating removal from Companies and Users lists")
def test_delete_company_and_validate_user_removal(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        company_name = test_data_inputs.delete_company_name
        company_domain = test_data_inputs.delete_company_domain
        user_name = test_data_inputs.delete_user_name
        user_email = test_data_inputs.delete_user_email
        user_password = test_data_inputs.new_company_admin_password

        # Super User creates new Company
        action_factory.superuser_actions.click_companies_menu()
        action_factory.superuser_actions.click_add_company()
        action_factory.superuser_actions.create_company(
            company_name=company_name,
            legal_name=company_name,
            email_domain=company_domain,
            initial_role="Company Admin"
        )
        action_factory.ui_utils.smart_wait()

        # Validate Company is created
        action_factory.superuser_actions.select_company_cell(company_name)
        action_factory.ui_utils.smart_wait()
        company_roles = ["Project Viewer", "Annotator", "Reviewer", "Dataset Supervisor", "Dataset Viewer", "API User"]
        action_factory.superuser_actions.check_company_roles(company_roles)
        action_factory.ui_utils.smart_wait()
        company_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.superuser_page.company_name_list)
        if company_name in company_list:
            status = "Pass"
            message = f"Company is created successfully"
            action_factory.helpers.attach_screenshot(name="CompanyCreatedSuccess")
            action_factory.helpers.attach_allure(name="Company Created", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Company is not created."
            action_factory.helpers.attach_screenshot(name="CompanyCreatedFail")
            action_factory.helpers.attach_allure(name="Company Created", text=message)
            assert False, message

        # Create User associated with new Company
        action_factory.users_actions.click_users_menu()
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=user_name,
            email=user_email,
            password=user_password,
            confirm_password=user_password
        )
        action_factory.superuser_actions.select_company_for_user(company_name)
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.create_roles(["Company Admin", "Project Viewer"])
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()

        # Validate User is created
        user_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)
        if user_email in user_list:
            status = "Pass"
            message = f"User is created successfully"
            action_factory.helpers.attach_screenshot(name="UserCreatedSuccess")
            action_factory.helpers.attach_allure(name="User Created", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User is not created."
            action_factory.helpers.attach_screenshot(name="UserCreatedFail")
            action_factory.helpers.attach_allure(name="User Created", text=message)
            assert False, message

        # Navigate back to Companies, select company and delete it
        action_factory.superuser_actions.click_companies_menu()
        action_factory.superuser_actions.select_company_cell(company_name)
        action_factory.superuser_actions.delete_company()
        action_factory.ui_utils.smart_wait()

        # Validate Company is no longer in Companies list
        companies_after_delete = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.superuser_page.company_name_list)
        if company_name not in companies_after_delete:
            status = "Pass"
            message = f"Company name got deleted"
            action_factory.helpers.attach_screenshot(name="Comapany Name Deleted")
            action_factory.helpers.attach_allure(name="Company Deletion", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Company name is not deleted"
            action_factory.helpers.attach_screenshot(name="Company Not Deleted")
            action_factory.helpers.attach_allure(name="Company Deletion", text=message)
            assert False, message

        # Validate User is no longer in Users list
        action_factory.users_actions.click_users_menu()
        action_factory.ui_utils.smart_wait()
        users_after_delete = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)

        if user_email not in users_after_delete:
            status = "Pass"
            message = f"User email is deleted"
            action_factory.helpers.attach_screenshot(name="User got deleted")
            action_factory.helpers.attach_allure(name="User Deletion", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"user email id is not deleted"
            action_factory.helpers.attach_screenshot(name="User Not Deleted")
            action_factory.helpers.attach_allure(name="User Deletion", text=message)
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
