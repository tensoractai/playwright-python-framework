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
@allure.story("Super User Company & Admin User Provisioning and Workflow")
@allure.title("Verify Super User creating company, configuring roles, creating Company Admin, and Company Admin creating Annotator & Reviewer users")
def test_superuser_company_creation_and_admin_user_flow(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        url = action_factory.helpers.fetch_dotenv("Execution_url")
        diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
        diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")

        company_name = test_data_inputs.superuser_company_name
        legal_name = test_data_inputs.superuser_legal_name
        email_domain = test_data_inputs.superuser_email_domain
        admin_name = test_data_inputs.new_company_admin_name
        admin_email = test_data_inputs.new_company_admin_email
        admin_password = test_data_inputs.new_company_admin_password
        annotator_name = test_data_inputs.annotator_name
        annotator_email = test_data_inputs.annotator_email
        reviewer_name = test_data_inputs.reviewer_name
        reviewer_email = test_data_inputs.reviewer_email
        updated_new_password = test_data_inputs.updated_new_password

        # Super User creates new Company
        action_factory.superuser_actions.click_companies_menu()
        action_factory.superuser_actions.click_add_company()
        action_factory.superuser_actions.create_company(
            company_name=company_name,
            legal_name=legal_name,
            email_domain=email_domain,
            initial_role="Project Supervisor"
        )
        action_factory.ui_utils.smart_wait()

        # Configure company roles
        action_factory.superuser_actions.select_company_cell(company_name)
        action_factory.ui_utils.smart_wait()
        company_roles = ["Company Admin", "Project Viewer", "Annotator", "Reviewer", "Dataset Supervisor", "Dataset Viewer", "API User"]
        action_factory.superuser_actions.check_company_roles(company_roles)
        action_factory.ui_utils.smart_wait()
        company_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.superuser_page.company_name_list)
        if company_name in company_name_list:
            status = "Pass"
            message = f"Super User company flow and Company Admin creation of Annotator ('{annotator_email}') and Reviewer ('{reviewer_email}') verified successfully."
            action_factory.helpers.attach_screenshot(name="Company Name Created")
            action_factory.helpers.attach_allure(name="Company Name Created", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Company '{company_name}' not found in user list."
            action_factory.helpers.attach_screenshot(name="Company Name Not Created")
            action_factory.helpers.attach_allure(name="Company Name Not Created", text=message)
            assert False, message

        # Super User creates Company Admin user
        action_factory.users_actions.click_users_menu()
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=admin_name,
            email=admin_email,
            password=admin_password,
            confirm_password=admin_password
        )
        action_factory.superuser_actions.select_company_for_user(company_name)
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.create_roles(["Company Admin", "Project Supervisor"])
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()
        user_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)
        if admin_email in user_name_list:
            status = "Pass"
            message = f"Super User company flow and Company Admin creation of Annotator ('{annotator_email}') and Reviewer ('{reviewer_email}') verified successfully."
            action_factory.helpers.attach_screenshot(name="User Name Created")
            action_factory.helpers.attach_allure(name="User Name Created", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"User '{admin_name}' not found in user list."
            action_factory.helpers.attach_screenshot(name="User Name Not Created")
            action_factory.helpers.attach_allure(name="User Name Not Created", text=message)
            assert False, message

        # Login as new Company Admin in new browser instance
        new_context = action_factory.page.context.browser.new_context()
        new_page = new_context.new_page()
        admin_action_factory = ActionFactory(new_page)

        try:
            admin_action_factory.login_actions.perform_login_new_user(url=url, email=admin_email, password=admin_password)
            admin_action_factory.users_actions.user_settings_changePassword(updated_new_password)
            admin_action_factory.login_actions.perform_login(url=url, email=admin_email, password=updated_new_password)
            admin_action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
            admin_action_factory.login_actions.select_organization(company_name, "Company Admin")
            admin_action_factory.ui_utils.smart_wait()
            home_visible = admin_action_factory.ui_utils.is_element_visible(admin_action_factory.page_factory.login_page.home_page_welcome)
            if home_visible:
                status = "Pass"
                message = f"Super User company flow and Company Admin creation of Annotator ('{annotator_email}') and Reviewer ('{reviewer_email}') verified successfully."
                admin_action_factory.helpers.attach_screenshot(name="Home Page Visible")
                admin_action_factory.helpers.attach_allure(name="Home Page Visible", text=message)
                assert True, message
            else:
                status = "Fail"
                message = f"Home page not visible after login as Company Admin."
                admin_action_factory.helpers.attach_screenshot(name="Home Page Not Visible")
                admin_action_factory.helpers.attach_allure(name="Home Page Not Visible", text=message)
                assert False, message

            # Company Admin creates Annotator user
            admin_action_factory.users_actions.click_users_menu()
            admin_action_factory.users_actions.click_create_user()
            admin_action_factory.users_actions.fill_user_form(
                full_name=annotator_name,
                email=annotator_email,
                password=admin_password,
                confirm_password=admin_password
            )
            admin_action_factory.users_actions.enable_allow_mfa_email()
            admin_action_factory.users_actions.create_roles(["Annotator"])
            admin_action_factory.users_actions.submit_create_user()
            admin_action_factory.ui_utils.smart_wait()

            # Company Admin creates Reviewer user
            admin_action_factory.users_actions.click_create_user()
            admin_action_factory.users_actions.fill_user_form(
                full_name=reviewer_name,
                email=reviewer_email,
                password=admin_password,
                confirm_password=admin_password
            )
            admin_action_factory.users_actions.enable_allow_mfa_email()
            admin_action_factory.users_actions.create_roles(["Reviewer"])
            admin_action_factory.users_actions.submit_create_user()
            admin_action_factory.ui_utils.smart_wait()

            # Validate Annotator and Reviewer in user list
            user_list = admin_action_factory.ui_utils.grab_text_from_all(admin_action_factory.page_factory.users_page.email_address_list)

            if annotator_email in user_list and reviewer_email in user_list:
                status = "Pass"
                message = f"Super User company flow and Company Admin creation of Annotator ('{annotator_email}') and Reviewer ('{reviewer_email}') verified successfully."
                admin_action_factory.helpers.attach_screenshot(name="SuperUserCompanyAndAdminFlowPass")
                admin_action_factory.helpers.attach_allure(name="Super User Company & Admin Flow", text=message)
                assert True, message
            else:
                status = "Fail"
                message = f"Annotator user '{annotator_email}' was not found in users list."
                admin_action_factory.helpers.attach_screenshot(name="SuperUserCompanyAndAdminFlowFail")
                admin_action_factory.helpers.attach_allure(name="Super User Company & Admin Flow", text=message)
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
