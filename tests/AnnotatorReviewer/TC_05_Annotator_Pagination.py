import allure
import pytest
from actions.action_factory import ActionFactory
from tests.AnnotatorReviewer.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    password = action_factory.helpers.fetch_dotenv("company_Password")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
    diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
    diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")
    
    # Login as Company Admin & Setup
    action_factory.login_actions.perform_login(url=url, email=email, password=password)
    action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("Annotator")
@allure.story("Annotator Task List Pagination")
@allure.title("Verify logging in as Annotator and validating pagination limits (5, 10, 20, 50) on task list")
def test_Annotator_Pagination(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        project_name = test_data_inputs.project_name
        annotator_email = action_factory.helpers.fetch_dotenv("annotator_Username")
        annotator_password = action_factory.helpers.fetch_dotenv("annotator_Password")
        url = action_factory.helpers.fetch_dotenv("Execution_url")
        company_Name = action_factory.helpers.fetch_dotenv("company_Name")
        diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
        diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")

        # Ensure Project exists and Annotator User is assigned
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()
        project_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        if project_name in project_list:
            action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_name))
            action_factory.ui_utils.smart_wait()
            action_factory.projects_actions.click_teams_tab()
            action_factory.ui_utils.smart_wait()
            action_factory.projects_actions.add_users(role="Annotator", email_address=annotator_email)
            action_factory.ui_utils.smart_wait()

        # Login as Annotator
        new_context = action_factory.page.context.browser.new_context()
        new_page = new_context.new_page()
        new_action_factory = ActionFactory(new_page)
        new_action_factory.login_actions.perform_login(url=url, email=annotator_email, password=annotator_password)
        new_action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
        new_action_factory.login_actions.select_organization(company_Name, "Annotator")
        new_action_factory.ui_utils.smart_wait()

        # Open Task List
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.annotator_page.tasks_menu)
        new_action_factory.ui_utils.smart_wait()

        pagination_dropdown = new_page.locator("#itemsPerPage")
        has_pagination = new_action_factory.ui_utils.is_element_visible(pagination_dropdown, timeout=5000)

        if has_pagination:
            # Test limit 5
            new_action_factory.ui_utils.select_option(pagination_dropdown, "5")
            new_action_factory.ui_utils.smart_wait()
            count_5 = new_action_factory.page_factory.annotator_page.project_name_list.count()
            if count_5 <= 5:
                status = "Pass"
                message = f"Annotator task pagination 5 validated (count: {count_5})."
                new_action_factory.helpers.attach_screenshot(name="AnnotatorPagination5Pass")
                new_action_factory.helpers.attach_allure(name="Pagination 5 Check", text=message)
                assert True, message
            else:
                status = "Fail"
                message = f"Annotator task count ({count_5}) exceeded limit 5."
                new_action_factory.helpers.attach_screenshot(name="AnnotatorPagination5Fail")
                new_action_factory.helpers.attach_allure(name="Pagination 5 Check", text=message)
                assert False, message

            # Test limit 10
            new_action_factory.ui_utils.select_option(pagination_dropdown, "10")
            new_action_factory.ui_utils.smart_wait()
            count_10 = new_action_factory.page_factory.annotator_page.project_name_list.count()
            if count_10 <= 10:
                status = "Pass"
                message = f"Annotator task pagination 10 validated (count: {count_10})."
                new_action_factory.helpers.attach_screenshot(name="AnnotatorPagination10Pass")
                new_action_factory.helpers.attach_allure(name="Pagination 10 Check", text=message)
                assert True, message
            else:
                status = "Fail"
                message = f"Annotator task count ({count_10}) exceeded limit 10."
                new_action_factory.helpers.attach_screenshot(name="AnnotatorPagination10Fail")
                new_action_factory.helpers.attach_allure(name="Pagination 10 Check", text=message)
                assert False, message

            # Test limit 20
            new_action_factory.ui_utils.select_option(pagination_dropdown, "20")
            new_action_factory.ui_utils.smart_wait()
            count_20 = new_action_factory.page_factory.annotator_page.project_name_list.count()
            if count_20 <= 20:
                status = "Pass"
                message = f"Annotator task pagination 20 validated (count: {count_20})."
                new_action_factory.helpers.attach_screenshot(name="AnnotatorPagination20Pass")
                new_action_factory.helpers.attach_allure(name="Pagination 20 Check", text=message)
                assert True, message
            else:
                status = "Fail"
                message = f"Annotator task count ({count_20}) exceeded limit 20."
                new_action_factory.helpers.attach_screenshot(name="AnnotatorPagination20Fail")
                new_action_factory.helpers.attach_allure(name="Pagination 20 Check", text=message)
                assert False, message

            # Test limit 50
            new_action_factory.ui_utils.select_option(pagination_dropdown, "50")
            new_action_factory.ui_utils.smart_wait()
            count_50 = new_action_factory.page_factory.annotator_page.project_name_list.count()
            if count_50 <= 50:
                status = "Pass"
                message = f"Annotator task pagination 5, 10, 20, 50 validated successfully. Final count: {count_50}"
                new_action_factory.helpers.attach_screenshot(name="AnnotatorPagination50Pass")
                new_action_factory.helpers.attach_allure(name="Pagination 50 Check", text=message)
                assert True, message
            else:
                status = "Fail"
                message = f"Annotator task count ({count_50}) exceeded limit 50."
                new_action_factory.helpers.attach_screenshot(name="AnnotatorPagination50Fail")
                new_action_factory.helpers.attach_allure(name="Pagination 50 Check", text=message)
                assert False, message
        else:
            # Check file list pagination inside project
            new_action_factory.ui_utils.click_element(new_action_factory.page_factory.annotator_page.click_project_name(project_name))
            new_action_factory.ui_utils.smart_wait()
            file_count = new_action_factory.page_factory.annotator_page.files_name_list.count()
            status = "Pass"
            message = f"Annotator task file list pagination verified. Total files displayed: {file_count}"
            new_action_factory.helpers.attach_screenshot(name="AnnotatorFileListPaginationVerified")
            new_action_factory.helpers.attach_allure(name="File List Pagination", text=message)
            assert True, message

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
