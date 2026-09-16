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
@allure.story("Annotator Task Claim, Save and Exit Validation")
@allure.title("Verify creating project with 4 audio files, claiming first file as Annotator, performing Save & Exit and validating task state")
def test_Save_And_Exit(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        dataset_name = test_data_inputs.dataset_name_4
        template_name = test_data_inputs.template_name_4
        workflow_name = test_data_inputs.workflow_name_4
        project_name = test_data_inputs.project_name_4
        dataset_type_name = test_data_inputs.dataset_type_name
        dataset_files_upload = test_data_inputs.dataset_files_upload_4
        template_files_upload = test_data_inputs.template_files_upload
        nodes_list = test_data_inputs.nodes_list
        annotation_text = test_data_inputs.annotation_text

        annotator_email = action_factory.helpers.fetch_dotenv("annotator_Username")
        annotator_password = action_factory.helpers.fetch_dotenv("annotator_Password")
        url = action_factory.helpers.fetch_dotenv("Execution_url")
        company_Name = action_factory.helpers.fetch_dotenv("company_Name")
        diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
        diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")
        target_files_list = [file.split("/")[-1] for file in dataset_files_upload]
        target_file_name = target_files_list[0]

        # Setup Dataset with 4 Audio Files
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        dataset_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        if dataset_name not in dataset_list:
            action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name=dataset_type_name)
            action_factory.ui_utils.smart_wait()
            action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
            action_factory.ui_utils.smart_wait()
            action_factory.datasets_actions.upload_files_with_uploadBtn(*dataset_files_upload)
            action_factory.ui_utils.smart_wait()

        # Setup Template
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        template_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        if template_name not in template_list:
            action_factory.templates_actions.upload_new_template(template_name=template_name)
            action_factory.templates_actions.upload_template_files(*template_files_upload)
            action_factory.ui_utils.smart_wait()

        # Setup Workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        workflow_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        if workflow_name not in workflow_list:
            action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description="Automation test workflow")
            action_factory.ui_utils.smart_wait()
            for node in nodes_list:
                action_factory.workflows_actions.click_nodes(node_name=node)
            action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
            action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name)
            action_factory.ui_utils.smart_wait()
            action_factory.workflows_actions.nodes_connection_flow(
                node_Name1="review", node_index1=1, position1="right", index1=2,
                node_Name2="annotate", node_index2=1, position2="left", index2=1
            )
            action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
            action_factory.ui_utils.smart_wait()

        # Setup Project
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()
        project_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        if project_name not in project_list:
            action_factory.projects_actions.create_project(project_name=project_name, dataset_name=dataset_name, workflow_name=workflow_name)
            action_factory.ui_utils.smart_wait()
            
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_name))
        action_factory.ui_utils.smart_wait()
        action_factory.projects_actions.click_teams_tab()
        action_factory.ui_utils.smart_wait()
        action_factory.projects_actions.add_users(role="Annotator", email_address=annotator_email)
        action_factory.ui_utils.smart_wait()
        assigners = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.assigners_list)
        if annotator_email in assigners:
            status = "Pass"
            message = "Annotator user added successfully to project team."
            action_factory.helpers.attach_screenshot(name="AnnotatorAdded")
            action_factory.helpers.attach_allure(name="Annotator Name", text=annotator_email)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to add annotator user '{annotator_email}' to project team."
            action_factory.helpers.attach_screenshot(name="AnnotatorNotAdded")
            action_factory.helpers.attach_allure(name="Annotator Name", text=annotator_email)
            assert False, message

        # Login as Annotator
        new_context = action_factory.page.context.browser.new_context()
        new_page = new_context.new_page()
        new_action_factory = ActionFactory(new_page)
        new_action_factory.login_actions.perform_login(url=url, email=annotator_email, password=annotator_password)
        new_action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
        new_action_factory.login_actions.select_organization(company_Name, "Annotator")
        new_action_factory.ui_utils.smart_wait()

        # Open Task and Select Project
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.annotator_page.tasks_menu)
        new_action_factory.ui_utils.smart_wait()
        project_list = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.annotator_page.project_name_list)
        if project_name in project_list:
            status = "Pass"
            message = "Project found in annotator task list."
            new_action_factory.helpers.attach_screenshot(name="ProjectFoundInTask")
            new_action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' not found in annotator task list."
            new_action_factory.helpers.attach_screenshot(name="ProjectNotFoundInTask")
            new_action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert False, message

        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.annotator_page.click_project_name(project_name))
        new_action_factory.ui_utils.smart_wait()
        files_list = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.annotator_page.files_name_list)
        
        # Verify 4 files are present
        if all(file in files_list for file in target_files_list):
            status = "Pass"
            message = "All 4 audio files present in annotator task list."
            new_action_factory.helpers.attach_screenshot(name="FourAudioFilesPresent")
            new_action_factory.helpers.attach_allure(name="Task Files", text=", ".join(files_list))
            assert True, message
        else:
            status = "Fail"
            message = f"Not all 4 audio files present in task list. Found: {files_list}"
            new_action_factory.helpers.attach_screenshot(name="FourAudioFilesNotPresent")
            new_action_factory.helpers.attach_allure(name="Task Files", text=", ".join(files_list))
            assert False, message

        # Click First File & Claim Task
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.annotator_page.click_project_name(target_file_name))
        new_action_factory.reviewer_actions.wait_for_iframe_ready()
        new_action_factory.ui_utils.element_wait_for(new_action_factory.page_factory.annotator_page.claim_button, timeout=10000)
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.annotator_page.claim_button)
        new_action_factory.ui_utils.smart_wait()

        # Perform Annotation
        new_action_factory.annotator_actions.annontate_files(annotation_text)
        new_action_factory.ui_utils.smart_wait()
        transcription = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.annotator_page.transcription)
        if annotation_text in transcription:
            status = "Pass"
            message = "Annotation text added successfully."
            new_action_factory.helpers.attach_screenshot(name="AnnotationAdded")
            new_action_factory.helpers.attach_allure(name="Annotation Text", text=annotation_text)
            assert True, message
        else:
            status = "Fail"
            message = "Failed to add annotation text."
            new_action_factory.helpers.attach_screenshot(name="AnnotationFailed")
            new_action_factory.helpers.attach_allure(name="Annotation Text", text=annotation_text)
            assert False, message

        # Perform Save and Exit
        new_action_factory.annotator_actions.perform_save_exit()
        new_action_factory.ui_utils.smart_wait()
        new_action_factory.ui_utils.element_wait_for(new_action_factory.page_factory.annotator_page.search_input, timeout=20000)
        files_name_list = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.annotator_page.files_name_list)
        
        # Validate File is Back in Task List
        if target_file_name in files_name_list:
            status = "Pass"
            message = f"Save & Exit successful: file '{target_file_name}' is back in the task list."
            new_action_factory.helpers.attach_screenshot(name="FileBackInTaskList")
            new_action_factory.helpers.attach_allure(name="Task List Files", text=", ".join(files_name_list))
            assert True, message
        else:
            status = "Fail"
            message = f"File '{target_file_name}' not found in task list after Save & Exit."
            new_action_factory.helpers.attach_screenshot(name="FileNotBackInTaskList")
            new_action_factory.helpers.attach_allure(name="Task List Files", text=", ".join(files_name_list))
            assert False, message

        # Re-open File and Validate Saved Transcription
        new_action_factory.ui_utils.click_element(new_action_factory.page_factory.annotator_page.click_project_name(target_file_name))
        new_action_factory.ui_utils.smart_wait()
        new_action_factory.reviewer_actions.wait_for_iframe_ready()
        new_action_factory.ui_utils.element_wait_for(new_action_factory.page_factory.annotator_page.transcription.nth(0), timeout=30000)
        saved_transcription = new_action_factory.ui_utils.grab_text_from_all(new_action_factory.page_factory.annotator_page.transcription)
        if annotation_text in saved_transcription:
            status = "Pass"
            message = "Save & Exit validated: saved transcription matched after re-opening."
            new_action_factory.helpers.attach_screenshot(name="SaveAndExitTranscriptionValidated")
            new_action_factory.helpers.attach_allure(name="Saved Transcription", text="\n".join(saved_transcription))
            assert True, message
        else:
            status = "Fail"
            message = "Saved transcription did not match after re-opening."
            new_action_factory.helpers.attach_screenshot(name="SaveAndExitTranscriptionMismatch")
            new_action_factory.helpers.attach_allure(name="Saved Transcription", text="\n".join(saved_transcription))
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
