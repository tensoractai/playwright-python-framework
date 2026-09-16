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

@allure.feature("Reviewer")
@allure.story("Reviewer Task Search Functionality")
@allure.title("Verify logging in as Reviewer and searching project name and file name in task list")
def test_Reviewer_Search(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        project_name = test_data_inputs.project_name
        dataset_files_upload = test_data_inputs.dataset_files_upload
        target_file_name = dataset_files_upload[0].split("/")[-1]

        reviewer_email = action_factory.helpers.fetch_dotenv("reviewer_Username")
        reviewer_password = action_factory.helpers.fetch_dotenv("reviewer_Password")
        url = action_factory.helpers.fetch_dotenv("Execution_url")
        company_Name = action_factory.helpers.fetch_dotenv("company_Name")
        diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
        diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")

        # Ensure Project exists and Reviewer User is assigned
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()
        project_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        if project_name in project_list:
            action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_name))
            action_factory.ui_utils.smart_wait()
            action_factory.projects_actions.click_teams_tab()
            action_factory.ui_utils.smart_wait()
            action_factory.projects_actions.add_users(role="Reviewer", email_address=reviewer_email)
            action_factory.ui_utils.smart_wait()

        # Login as Reviewer
        new_context = action_factory.page.context.browser.new_context()
        new_page = new_context.new_page()
        new_action_factory = ActionFactory(new_page)
        new_action_factory.login_actions.perform_login(url=url, email=reviewer_email, password=reviewer_password)
        new_action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
        new_action_factory.login_actions.select_organization(company_Name, "Reviewer")
        new_action_factory.ui_utils.smart_wait()

        # Open Task List
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.reviewer_page.tasks_menu)
        new_action_factory.ui_utils.smart_wait()

        # Search Project Name
        new_action_factory.ui_utils.fill_input(new_action_factory.page_factory.reviewer_page.search_input, project_name)
        new_action_factory.ui_utils.smart_wait()
        searched_projects = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.reviewer_page.project_name_list)

        if project_name in searched_projects:
            status = "Pass"
            message = f"Search returned expected project '{project_name}' successfully."
            new_action_factory.helpers.attach_screenshot(name="ReviewerSearchProjectSuccess")
            new_action_factory.helpers.attach_allure(name="Search Project Result", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Search failed to return project '{project_name}'. Found: {searched_projects}"
            new_action_factory.helpers.attach_screenshot(name="ReviewerSearchProjectFail")
            new_action_factory.helpers.attach_allure(name="Search Project Result", text=message)
            assert False, message

        # Select Project and Search File Name
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.reviewer_page.click_project_name(project_name))
        new_action_factory.ui_utils.smart_wait()
        
        new_action_factory.ui_utils.fill_input(new_action_factory.page_factory.reviewer_page.search_input, target_file_name)
        new_action_factory.ui_utils.smart_wait()
        searched_files = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.reviewer_page.files_name_list)

        if target_file_name in searched_files:
            status = "Pass"
            message = f"Search returned expected file '{target_file_name}' successfully."
            new_action_factory.helpers.attach_screenshot(name="ReviewerSearchFileSuccess")
            new_action_factory.helpers.attach_allure(name="Search File Result", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Search failed to return file '{target_file_name}'. Found: {searched_files}"
            new_action_factory.helpers.attach_screenshot(name="ReviewerSearchFileFail")
            new_action_factory.helpers.attach_allure(name="Search File Result", text=message)
            assert False, message

        # Search Non-existing File Name
        invalid_search = "Invalid_File_9999"
        new_action_factory.ui_utils.fill_input(new_action_factory.page_factory.reviewer_page.search_input, invalid_search)
        new_action_factory.ui_utils.smart_wait()
        searched_invalid_files = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.reviewer_page.files_name_list)

        if target_file_name not in searched_invalid_files:
            status = "Pass"
            message = f"Search with invalid query '{invalid_search}' correctly hid target file."
            new_action_factory.helpers.attach_screenshot(name="ReviewerSearchInvalidSuccess")
            new_action_factory.helpers.attach_allure(name="Invalid Search Result", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Target file '{target_file_name}' still displayed for invalid search query."
            new_action_factory.helpers.attach_screenshot(name="ReviewerSearchInvalidFail")
            new_action_factory.helpers.attach_allure(name="Invalid Search Result", text=message)
            assert False, message

        # Clear Search Input
        new_action_factory.ui_utils.fill_input(new_action_factory.page_factory.reviewer_page.search_input, "")
        new_action_factory.ui_utils.smart_wait()

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
