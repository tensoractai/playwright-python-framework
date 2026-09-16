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
@allure.story("Reviewer Task Claim, Annotate, Validate, and Approve")
@allure.title("Verify logging in as Reviewer to claim annotator submitted task, annotate, validate transcription, and submit task")
def test_Reviewer_Flow(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        project_name = test_data_inputs.project_name
        dataset_files_upload = test_data_inputs.dataset_files_upload
        annotation_text = test_data_inputs.annotation_text
        reviewer_annotation_text = test_data_inputs.reviewer_annotation_text

        reviewer_email = action_factory.helpers.fetch_dotenv("reviewer_Username")
        reviewer_password = action_factory.helpers.fetch_dotenv("reviewer_Password")
        url = action_factory.helpers.fetch_dotenv("Execution_url")
        company_Name = action_factory.helpers.fetch_dotenv("company_Name")
        diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
        diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")
        target_file_name = dataset_files_upload[0].split("/")[-1]

        # Ensure Project exists and add Reviewer User to Project Team
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()
        project_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        if project_name in project_list:
            status = "Pass"
            message = f"Project '{project_name}' found."
            action_factory.helpers.attach_screenshot(name="ProjectFound")
            action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' not found."
            action_factory.helpers.attach_screenshot(name="ProjectNotFound")
            action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_name))
        action_factory.ui_utils.smart_wait()
        action_factory.projects_actions.click_teams_tab()
        action_factory.ui_utils.smart_wait()
        action_factory.projects_actions.add_users(role="Reviewer", email_address=reviewer_email)
        action_factory.ui_utils.smart_wait()
        assigners = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.assigners_list)
        if reviewer_email in assigners:
            status = "Pass"
            message = "Reviewer user added successfully to the project."
            action_factory.helpers.attach_screenshot(name="ReviewerAdded")
            action_factory.helpers.attach_allure(name="Reviewer Name", text=reviewer_email)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to add reviewer user '{reviewer_email}' to the project."
            action_factory.helpers.attach_screenshot(name="ReviewerNotAdded")
            action_factory.helpers.attach_allure(name="Reviewer Name", text=reviewer_email)
            assert False, message

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

        # Validate Annotator Transcription & Perform Reviewer Annotation
        new_action_factory.ui_utils.element_wait_for(new_action_factory.page_factory.annotator_page.transcription.nth(0), timeout=50000)
        annotator_transcription = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.annotator_page.transcription)
        if annotation_text in annotator_transcription:
            status = "Pass"
            message = "Annotator transcription matched successfully."
            new_action_factory.helpers.attach_screenshot(name="AnnotatorTranscriptionMatched")
            new_action_factory.helpers.attach_allure(name="Annotator Transcription", text="\n".join(annotator_transcription))
            assert True, message
        else:
            status = "Fail"
            message = "Annotator transcription text did not match."
            new_action_factory.helpers.attach_screenshot(name="AnnotatorTranscriptionNotMatched")
            new_action_factory.helpers.attach_allure(name="Annotator Transcription", text="\n".join(annotator_transcription))
            assert False, message

        new_action_factory.annotator_actions.annontate_files(reviewer_annotation_text, fast_forward="15")
        new_action_factory.ui_utils.smart_wait()
        reviewer_transcription = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.annotator_page.transcription)
        if reviewer_annotation_text in reviewer_transcription:
            status = "Pass"
            message = "Reviewer annotation added successfully."
            new_action_factory.helpers.attach_screenshot(name="ReviewerAnnotationAdded")
            new_action_factory.helpers.attach_allure(name="Reviewer Transcription", text="\n".join(reviewer_transcription))
            assert True, message
        else:
            status = "Fail"
            message = "Failed to add reviewer annotation."
            new_action_factory.helpers.attach_screenshot(name="ReviewerAnnotationFailed")
            new_action_factory.helpers.attach_allure(name="Reviewer Transcription", text="\n".join(reviewer_transcription))
            assert False, message

        # Submit / Approve from Reviewer End
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.reviewer_page.approve_button)
        new_action_factory.ui_utils.smart_wait()
        claim_visible = new_action_factory.ui_utils.is_element_visible(new_action_factory.page_factory.reviewer_page.claim_button, timeout=5000)
        if claim_visible:
            new_action_factory.ui_utils.click_element(new_action_factory.page_factory.annotator_page.back_button)
            new_action_factory.ui_utils.smart_wait()

        # Validate File is No Longer in Task List
        new_action_factory.ui_utils.element_wait_for(new_action_factory.page_factory.annotator_page.search_input, timeout=10000)
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.reviewer_page.click_project_name(project_name))
        new_action_factory.ui_utils.smart_wait()
        files_list = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.reviewer_page.files_name_list)
        if target_file_name not in files_list:
            status = "Pass"
            message = f"Reviewer completed and file '{target_file_name}' is no longer in the task list."
            new_action_factory.helpers.attach_screenshot(name="ReviewerCompletedFileRemoved")
            new_action_factory.helpers.attach_allure(name="Reviewer Email", text=reviewer_email)
            assert True, message
        else:
            status = "Fail"
            message = f"File '{target_file_name}' is still in reviewer task list."
            new_action_factory.helpers.attach_screenshot(name="ReviewerFileNotRemoved")
            new_action_factory.helpers.attach_allure(name="Reviewer Email", text=reviewer_email)
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
