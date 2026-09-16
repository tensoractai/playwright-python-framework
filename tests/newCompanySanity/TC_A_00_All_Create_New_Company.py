import allure
import pytest
from actions.action_factory import ActionFactory
from tests.newCompanySanity.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    password = action_factory.helpers.fetch_dotenv("company_Password")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
    diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
    diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")
    
    # Login & Setup as Super User
    action_factory.login_actions.perform_login(url=url, email=email, password=password)
    action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
    action_factory.login_actions.select_organization(company_Name, "Super User")
    return action_factory

@allure.feature("Super User Company & User Provisioning")
@allure.story("Create New Company & Provision Users")
@allure.title("Super User Create Company and Provision 2 Annotators and 1 Reviewer")
def test_create_new_company_and_users(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        url = action_factory.helpers.fetch_dotenv("Execution_url")
        default_password =test_data_inputs.default_password
        updated_new_password = test_data_inputs.updated_new_password
        diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
        diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")
        
        # Navigate to Companies menu and resolve next available index
        action_factory.superuser_actions.click_companies_menu()
        action_factory.ui_utils.smart_wait()
        
        company_names_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.superuser_page.company_name_list)
        i = action_factory.helpers.resolve_next_index(company_names_list, test_data_inputs.company_name)
        
        company_name = test_data_inputs.company_name.format(i=i) if "{i}" in test_data_inputs.company_name else test_data_inputs.company_name
        company_admin_email = test_data_inputs.company_admin_email.format(i=i) if "{i}" in test_data_inputs.company_admin_email else test_data_inputs.company_admin_email
        annotator_1_email = test_data_inputs.annotator_1_email.format(i=i) if "{i}" in test_data_inputs.annotator_1_email else test_data_inputs.annotator_1_email
        annotator_2_email = test_data_inputs.annotator_2_email.format(i=i) if "{i}" in test_data_inputs.annotator_2_email else test_data_inputs.annotator_2_email
        reviewer_1_email = test_data_inputs.reviewer_1_email.format(i=i) if "{i}" in test_data_inputs.reviewer_1_email else test_data_inputs.reviewer_1_email
        reviewer_2_email = test_data_inputs.reviewer_2_email.format(i=i) if "{i}" in test_data_inputs.reviewer_2_email else test_data_inputs.reviewer_2_email
        
        # Create New Company
        action_factory.superuser_actions.click_add_company()
        action_factory.superuser_actions.create_company(
            company_name=company_name,
            legal_name=test_data_inputs.legal_name,
            email_domain=test_data_inputs.email_domain,
            initial_role="Project Supervisor"
        )
        action_factory.ui_utils.smart_wait()
        
        # Configure Company Roles
        action_factory.superuser_actions.select_company_cell(company_name)
        action_factory.ui_utils.smart_wait()
        company_roles = ["Company Admin", "Project Supervisor", "Annotator", "Reviewer"]
        action_factory.superuser_actions.check_company_roles(company_roles)
        action_factory.ui_utils.smart_wait()
        
        company_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.superuser_page.company_name_list)
        if company_name in company_list:
            status = "Pass"
            message = f"Company '{company_name}' was created successfully."
            action_factory.helpers.attach_screenshot(name="Company_Created")
            action_factory.helpers.attach_allure(name="Create New Company", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Company '{company_name}' was not found in company list."
            action_factory.helpers.attach_screenshot(name="Company_Creation_Failed")
            action_factory.helpers.attach_allure(name="Create New Company", text=message)
            assert False, message

        # Create Company Admin 
        action_factory.users_actions.click_users_menu()
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=test_data_inputs.company_admin_name,
            email=company_admin_email,
            password=test_data_inputs.default_password,
            confirm_password=test_data_inputs.default_password
        )
        action_factory.superuser_actions.select_company_for_user(company_name)
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.create_roles(["Company Admin"])
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()

        # Create Annotator 1
        action_factory.users_actions.click_users_menu()
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=test_data_inputs.annotator_1_name,
            email=annotator_1_email,
            password=test_data_inputs.default_password,
            confirm_password=test_data_inputs.default_password
        )
        action_factory.superuser_actions.select_company_for_user(company_name)
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.create_roles(["Annotator"])
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()
        
        # Create Annotator 2
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=test_data_inputs.annotator_2_name,
            email=annotator_2_email,
            password=test_data_inputs.default_password,
            confirm_password=test_data_inputs.default_password
        )
        action_factory.superuser_actions.select_company_for_user(company_name)
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.create_roles(["Annotator"])
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()
        
        # Create Reviewer 1
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=test_data_inputs.reviewer_1_name,
            email=reviewer_1_email,
            password=test_data_inputs.default_password,
            confirm_password=test_data_inputs.default_password
        )
        action_factory.superuser_actions.select_company_for_user(company_name)
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.create_roles(["Reviewer"])
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()

        # Create Reviewer 2
        action_factory.users_actions.click_create_user()
        action_factory.users_actions.fill_user_form(
            full_name=test_data_inputs.reviewer_2_name,
            email=reviewer_2_email,
            password=test_data_inputs.default_password,
            confirm_password=test_data_inputs.default_password
        )
        action_factory.superuser_actions.select_company_for_user(company_name)
        action_factory.users_actions.enable_allow_mfa_email()
        action_factory.users_actions.create_roles(["Reviewer"])
        action_factory.users_actions.submit_create_user()
        action_factory.ui_utils.smart_wait()
        
        # Validate Created Users in User List
        user_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.users_page.email_address_list)
        if annotator_1_email in user_list and annotator_2_email in user_list and reviewer_1_email in user_list:
            # Save created data to test_data_inputs and runtime state
            test_data_inputs.created_company_name = company_name
            test_data_inputs.created_annotator_1_email = annotator_1_email
            test_data_inputs.created_annotator_2_email = annotator_2_email
            test_data_inputs.created_reviewer_1_email = reviewer_1_email
            
            action_factory.helpers.save_runtime_data("created_company_name", company_name)
            action_factory.helpers.save_runtime_data("created_annotator_1_email", annotator_1_email)
            action_factory.helpers.save_runtime_data("created_annotator_2_email", annotator_2_email)
            action_factory.helpers.save_runtime_data("created_reviewer_1_email", reviewer_1_email)
            
            status = "Pass"
            message = f"Company '{company_name}', Annotator 1 ('{annotator_1_email}'), Annotator 2 ('{annotator_2_email}'), and Reviewer 1 ('{reviewer_1_email}') created and saved successfully."
            action_factory.helpers.attach_screenshot(name="Company_And_Users_Created_Pass")
            action_factory.helpers.attach_allure(name="Company and Users Provisioning", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to verify creation of Annotators ({annotator_1_email}, {annotator_2_email}) and Reviewer ({reviewer_1_email}) in user list."
            action_factory.helpers.attach_screenshot(name="Company_And_Users_Created_Fail")
            action_factory.helpers.attach_allure(name="Company and Users Provisioning", text=message)
            assert False, message

        # Open New Browser and Login Company Admin User Settings 
        new_context = action_factory.page.context.browser.new_context()
        new_page = new_context.new_page()
        new_action_factory = ActionFactory(new_page)
        new_action_factory.login_actions.perform_login_new_user(url=url, email=company_admin_email, password=default_password)
        new_action_factory.users_actions.user_settings_changePassword(updated_new_password)
        new_action_factory.login_actions.perform_login(url=url, email=company_admin_email, password=updated_new_password)
        new_action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
        new_action_factory.login_actions.select_organization(company_name, "Company Admin")
        new_action_factory.ui_utils.smart_wait()
        welcome_visible = new_action_factory.ui_utils.is_element_visible(new_action_factory.page_factory.login_page.home_page_welcome)
        if welcome_visible:
            status = "pass"
            message = f"Valid user '{company_admin_email}' created successfully and verified login as Company Admin in new browser instance."
            new_action_factory.helpers.attach_screenshot(name="User Logged In successfully")
            new_action_factory.helpers.attach_allure(name="User Logged In successfully", text=message)
            assert True, message
        else:
            status = "fail"
            message = f"Valid user '{company_admin_email}' failed login verification in new browser instance."
            new_action_factory.helpers.attach_screenshot(name="User Failed To Login")
            new_action_factory.helpers.attach_allure(name="User Failed To Login", text=message)
            assert False, message
            
        # Open New browser and Login Annotator 1
        new_context = action_factory.page.context.browser.new_context()
        new_page = new_context.new_page()
        new_action_factory = ActionFactory(new_page)
        new_action_factory.login_actions.perform_login_new_user(url=url, email=annotator_1_email, password=default_password)
        new_action_factory.users_actions.user_settings_changePassword(updated_new_password)
        new_action_factory.login_actions.perform_login(url=url, email=annotator_1_email, password=updated_new_password)
        new_action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
        new_action_factory.login_actions.select_organization(company_name, "Annotator")
        new_action_factory.ui_utils.smart_wait()
        welcome_visible = new_action_factory.ui_utils.is_element_visible(new_action_factory.page_factory.login_page.home_page_welcome)
        if welcome_visible:
            status = "pass"
            message = f"Valid user '{annotator_1_email}' created successfully and verified login as Annotator in new browser instance."
            new_action_factory.helpers.attach_screenshot(name="User Logged In successfully")
            new_action_factory.helpers.attach_allure(name="User Logged In successfully", text=message)
            assert True, message
        else:
            status = "fail"
            message = f"Valid user '{annotator_1_email}' failed login verification in new browser instance."
            new_action_factory.helpers.attach_screenshot(name="User Failed To Login")
            new_action_factory.helpers.attach_allure(name="User Failed To Login", text=message)
            assert False, message

        # Open New browser and Login Annotator 2
        new_context = action_factory.page.context.browser.new_context()
        new_page = new_context.new_page()
        new_action_factory = ActionFactory(new_page)
        new_action_factory.login_actions.perform_login_new_user(url=url, email=annotator_2_email, password=default_password)
        new_action_factory.users_actions.user_settings_changePassword(updated_new_password)
        new_action_factory.login_actions.perform_login(url=url, email=annotator_2_email, password=updated_new_password)
        new_action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
        new_action_factory.login_actions.select_organization(company_name, "Annotator")
        new_action_factory.ui_utils.smart_wait()
        welcome_visible = new_action_factory.ui_utils.is_element_visible(new_action_factory.page_factory.login_page.home_page_welcome)
        if welcome_visible:
            status = "pass"
            message = f"Valid user '{annotator_2_email}' created successfully and verified login as Annotator in new browser instance."
            new_action_factory.helpers.attach_screenshot(name="User Logged In successfully")
            new_action_factory.helpers.attach_allure(name="User Logged In successfully", text=message)
            assert True, message
        else:
            status = "fail"
            message = f"Valid user '{annotator_2_email}' failed login verification in new browser instance."
            new_action_factory.helpers.attach_screenshot(name="User Failed To Login")
            new_action_factory.helpers.attach_allure(name="User Failed To Login", text=message)
            assert False, message
        
        # Open New Browser and Login reviewer 1 
        new_context = action_factory.page.context.browser.new_context()
        new_page = new_context.new_page()
        new_action_factory = ActionFactory(new_page)
        new_action_factory.login_actions.perform_login_new_user(url=url, email=reviewer_1_email, password=default_password)
        new_action_factory.users_actions.user_settings_changePassword(updated_new_password)
        new_action_factory.login_actions.perform_login(url=url, email=reviewer_1_email, password=updated_new_password)
        new_action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
        new_action_factory.login_actions.select_organization(company_name, "Reviewer")
        new_action_factory.ui_utils.smart_wait()
        welcome_visible = new_action_factory.ui_utils.is_element_visible(new_action_factory.page_factory.login_page.home_page_welcome)
        if welcome_visible:
            status = "pass"
            message = f"Valid user '{reviewer_1_email}' created successfully and verified login as Reviewer in new browser instance."
            new_action_factory.helpers.attach_screenshot(name="User Logged In successfully")
            new_action_factory.helpers.attach_allure(name="User Logged In successfully", text=message)
            assert True, message
        else:
            status = "fail"
            message = f"Valid user '{reviewer_1_email}' failed login verification in new browser instance."
            new_action_factory.helpers.attach_screenshot(name="User Failed To Login")
            new_action_factory.helpers.attach_allure(name="User Failed To Login", text=message)
            assert False, message

        # Open New Browser and Login reviewer 2 
        new_context = action_factory.page.context.browser.new_context()
        new_page = new_context.new_page()
        new_action_factory = ActionFactory(new_page)
        new_action_factory.login_actions.perform_login_new_user(url=url, email=reviewer_2_email, password=default_password)
        new_action_factory.users_actions.user_settings_changePassword(updated_new_password)
        new_action_factory.login_actions.perform_login(url=url, email=reviewer_2_email, password=updated_new_password)
        new_action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
        new_action_factory.login_actions.select_organization(company_name, "Reviewer")
        new_action_factory.ui_utils.smart_wait()
        welcome_visible = new_action_factory.ui_utils.is_element_visible(new_action_factory.page_factory.login_page.home_page_welcome)
        if welcome_visible:
            status = "pass"
            message = f"Valid user '{reviewer_2_email}' created successfully and verified login as Reviewer in new browser instance."
            new_action_factory.helpers.attach_screenshot(name="User Logged In successfully")
            new_action_factory.helpers.attach_allure(name="User Logged In successfully", text=message)
            assert True, message
        else:
            status = "fail"
            message = f"Valid user '{reviewer_2_email}' failed login verification in new browser instance."
            new_action_factory.helpers.attach_screenshot(name="User Failed To Login")
            new_action_factory.helpers.attach_allure(name="User Failed To Login", text=message)
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
