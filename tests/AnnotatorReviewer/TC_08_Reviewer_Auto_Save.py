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
@allure.story("Reviewer Auto Save Functionality")
@allure.title("Verify logging in as Reviewer, performing annotation, and validating auto-save toast and persisted transcription")
def test_Reviewer_Auto_Save(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        project_name = test_data_inputs.project_name
        dataset_files_upload = test_data_inputs.dataset_files_upload
        reviewer_annotation_text = test_data_inputs.reviewer_annotation_text
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

        # Open Task List and Select Project
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.reviewer_page.tasks_menu)
        new_action_factory.ui_utils.smart_wait()
        project_list = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.reviewer_page.project_name_list)
        if project_name in project_list:
            status = "Pass"
            message = "Project found in reviewer task list."
            new_action_factory.helpers.attach_screenshot(name="ProjectFoundInReviewerTasks")
            new_action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' not found in reviewer task list."
            new_action_factory.helpers.attach_screenshot(name="ProjectNotFoundInReviewerTasks")
            new_action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert False, message

        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.reviewer_page.click_project_name(project_name))
        new_action_factory.ui_utils.smart_wait()
        file_list = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.reviewer_page.files_name_list)

        if target_file_name in file_list:
            status = "Pass"
            message = "File found in reviewer task list."
            new_action_factory.helpers.attach_screenshot(name="FileFoundInReviewerTasks")
            new_action_factory.helpers.attach_allure(name="File Name", text=target_file_name)
            assert True, message
        else:
            status = "Fail"
            message = f"File '{target_file_name}' not found in reviewer task list."
            new_action_factory.helpers.attach_screenshot(name="FileNotFoundInReviewerTasks")
            new_action_factory.helpers.attach_allure(name="File Name", text=target_file_name)
            assert False, message

        # Claim Task
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.reviewer_page.click_project_name(target_file_name))
        new_action_factory.reviewer_actions.wait_for_iframe_ready()
        new_action_factory.ui_utils.element_wait_for(new_action_factory.page_factory.reviewer_page.claim_button, timeout=10000)
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.reviewer_page.claim_button)
        new_action_factory.ui_utils.smart_wait()

        # Add Reviewer Annotation
        new_action_factory.annotator_actions.annontate_files(reviewer_annotation_text, fast_forward="15")
        new_action_factory.ui_utils.smart_wait()

        # Validate Auto-Save Toast
        auto_save = new_action_factory.annotator_actions.perform_auto_save_functionality()
        if auto_save:
            status = "Pass"
            message = "Reviewer auto-save functionality works successfully."
            new_action_factory.helpers.attach_screenshot(name="ReviewerAutoSaveSuccess")
            new_action_factory.helpers.attach_allure(name="Reviewer Auto Save", text="Auto-save toast verified.")
            assert True, message
        else:
            status = "Fail"
            message = "Reviewer auto-save toast did not appear."
            new_action_factory.helpers.attach_screenshot(name="ReviewerAutoSaveFailed")
            new_action_factory.helpers.attach_allure(name="Reviewer Auto Save", text="Auto-save toast not triggered.")
            assert False, message

        # Exit and Re-open Task to Verify Auto-Saved Transcription
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.annotator_page.back_button)
        new_action_factory.ui_utils.smart_wait()
        new_action_factory.ui_utils.element_wait_for(new_action_factory.page_factory.reviewer_page.search_input, timeout=10000)
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.reviewer_page.click_project_name(target_file_name))
        new_action_factory.ui_utils.smart_wait()
        new_action_factory.reviewer_actions.wait_for_iframe_ready()
        new_action_factory.ui_utils.element_wait_for(new_action_factory.page_factory.annotator_page.transcription.nth(0), timeout=30000)

        transcription = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.annotator_page.transcription)
        if reviewer_annotation_text in transcription:
            status = "Pass"
            message = "Reviewer auto-save transcription verified successfully after re-opening."
            new_action_factory.helpers.attach_screenshot(name="ReviewerAutoSaveTranscriptionVerified")
            new_action_factory.helpers.attach_allure(name="Reviewer Transcription", text="\n".join(transcription))
            assert True, message
        else:
            status = "Fail"
            message = "Reviewer auto-save transcription text did not match."
            new_action_factory.helpers.attach_screenshot(name="ReviewerAutoSaveTranscriptionMismatch")
            new_action_factory.helpers.attach_allure(name="Reviewer Transcription", text="\n".join(transcription))
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
