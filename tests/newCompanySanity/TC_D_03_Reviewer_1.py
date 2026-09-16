import allure
import pytest
from actions.action_factory import ActionFactory
from tests.newCompanySanity.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = test_data_inputs.get_reviewer_1_email(action_factory.helpers)
    password = test_data_inputs.updated_new_password
    company_Name = test_data_inputs.get_company_name(action_factory.helpers)
    diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
    diff_email_password = action_factory.helpers.fetch_dotenv(
        "different_email_for_otp_password"
    )
    # Login
    action_factory.login_actions.perform_login(
        url=url,
        email=email,
        password=password
    )
    action_factory.login_actions.use_different_email_OTP(
        diff_email,
        diff_email_password
    )
    action_factory.login_actions.select_organization(company_Name, "Reviewer")
    return action_factory

@allure.feature("Reviewer 1")
@allure.story("Reviewer 1 Flow")
@allure.title("Reviewer 1 Flow Validation")
def test_Reviewer_Flow_1_test(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each

        Dataset_files_path = test_data_inputs.TC_A_Dataset_files_upload
        Dataset_files_upload = [file.split("/")[-1] for file in Dataset_files_path]
        TC_D_annotation_1_1 = test_data_inputs.TC_D_annotation_1_1
        TC_D_annotation_1_2 = test_data_inputs.TC_D_annotation_1_2
        TC_D_annotation_1_3 = test_data_inputs.TC_D_annotation_1_3
        TC_D_annotation_1_4 = test_data_inputs.TC_D_annotation_1_4
        TC_D_annotation_1_Edit = test_data_inputs.TC_D_annotation_1_Edit    
        TC_D_reviewer_1_text_Edit = test_data_inputs.TC_D_reviewer_1_text_Edit
        TC_D_reviewer_1_text_Approve = test_data_inputs.TC_D_reviewer_1_text_Approve
        TC_D_reviewer_2_text_Edit = test_data_inputs.TC_D_reviewer_2_text_Edit
        TC_D_reviewer_2_text_Approve = test_data_inputs.TC_D_reviewer_2_text_Approve
        
        # Reviewer Functionality 
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.tasks_menu)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.reviewer_page.current_task_heading)
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.project_name_list.nth(0))
        project_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.reviewer_page.project_name_list)
        i = action_factory.helpers.resolve_latest_index(project_list, test_data_inputs.TC_D_project_name)
        project_name = test_data_inputs.TC_D_project_name.format(i=i) if "{i}" in test_data_inputs.TC_D_project_name else test_data_inputs.TC_D_project_name
        if project_name in project_list:
            status = "Pass"
            message = f"Project '{project_name}' found in the list."
            action_factory.helpers.attach_screenshot(name="ProjectFound")
            action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' not found in the list."
            action_factory.helpers.attach_screenshot(name="ProjectNotFound")
            action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert False, message
        
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.click_project_name(project_name))
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.reviewer_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        if all(file in files_name_list for file in Dataset_files_upload):
            status = "Pass"
            message = f"All files uploaded successfully for dataset '{Dataset_files_upload}'."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(Dataset_files_upload))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload all files for dataset '{Dataset_files_upload}'."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(Dataset_files_upload))
            assert False, message

        # Review 1 st file Claim , Review and Annotate
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.click_project_name(Dataset_files_upload[0]))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.reviewer_page.claim_button, timeout = 10000)
        action_factory.reviewer_actions.wait_for_iframe_ready()
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.claim_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.reviewer_page.begin_recording, timeout = 30000)
        is_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.reviewer_page.begin_recording)
        if is_visible:
            status = "Pass"
            message = f"Begin Recording button is visible."
            action_factory.helpers.attach_screenshot(name="Begin Recording button")
            action_factory.helpers.attach_allure(name="Begin Recording button", text="egin Recording button is visible")
            assert True, message
        else:
            status = "Fail"
            message = f"Begin Recording button is not visible."
            action_factory.helpers.attach_screenshot(name="Begin RecordingButtonNotVisible")
            action_factory.helpers.attach_allure(name="Begin Recording button", text="Begin Recording button is not visible")
            assert False, message
        # Validate 1st Annotator Annotations 
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        Transcription_to_have = TC_D_annotation_1_1 in transcription and TC_D_annotation_1_2 in transcription and TC_D_annotation_1_Edit in transcription
        Transcription_do_not_have = TC_D_annotation_1_3 not in transcription and TC_D_annotation_1_4 not in transcription
        if Transcription_to_have and Transcription_do_not_have:
            status = "Pass"
            message = f"Transcription text matches the input text."
            action_factory.helpers.attach_screenshot(name="TranscriptionMatches")
            action_factory.helpers.attach_allure(name="Transcription", text="\n".join(transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Transcription text does not match the input text."
            action_factory.helpers.attach_screenshot(name="TranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Transcription", text="\n".join(transcription))
            assert False, message
        
        action_factory.annotator_actions.annontate_files(TC_D_reviewer_1_text_Approve, fast_forward = "15")
        # Validate Reviewer Annotation
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        if TC_D_reviewer_1_text_Approve in transcription:
            status = "Pass"
            message = f"Transcription text matches the input text."
            action_factory.helpers.attach_screenshot(name="TranscriptionMatches")
            action_factory.helpers.attach_allure(name="Transcription", text="\n".join(transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Transcription text does not match the input text."
            action_factory.helpers.attach_screenshot(name="TranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Transcription", text="\n".join(transcription))
            assert False, message

        # perform Save and Exit Functionality
        action_factory.annotator_actions.perform_save_exit()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.search_input,timeout=20000)
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.files_name_list)
        print(f"Files names list: {files_name_list}")
        if Dataset_files_upload[0] in files_name_list:
            status = "Pass"
            message = f"Reviewer completed and file is back to the list."
            action_factory.helpers.attach_screenshot(name="ReviewerCompleted")
            action_factory.helpers.attach_allure(name="Reviewer", text="Reviewer completed and file is back to the list.")
            assert True, message
        else:
            status = "Fail"
            message = f"Reviewer is not completed and file is not back to the list."
            action_factory.helpers.attach_screenshot(name="ReviewerNotCompleted")
            action_factory.helpers.attach_allure(name="Reviewer", text="Reviewer is not completed and file is not back to the list.")
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.click_project_name(Dataset_files_upload[0]))
        action_factory.ui_utils.smart_wait()
        action_factory.reviewer_actions.wait_for_iframe_ready()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.begin_recording,timeout=30000)
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.transcription.nth(0),timeout=50000)
        # Validate Reviewer Transcription after save and exit
        reviewer_transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        if TC_D_reviewer_1_text_Approve in reviewer_transcription:
            status = "Pass"
            message = f"Save and Exit - reviewer transcription saved successfully."
            action_factory.helpers.attach_screenshot(name="SaveAndExit_ReviewerTranscriptionSaved")
            action_factory.helpers.attach_allure(name="Save and Exit - reviewer transcription", text="\n".join(reviewer_transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Save and Exit - reviewer transcription text does not match the reviewer text."
            action_factory.helpers.attach_screenshot(name="SaveAndExit_ReviewerTranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Save and Exit - reviewer transcription", text="\n".join(reviewer_transcription))
            assert False, message

        # perform edit transcription 
        action_factory.annotator_actions.perform_edit_transcription(TC_D_annotation_1_2, TC_D_reviewer_1_text_Edit)
        # Validate Reviewer Transcription after edit
        reviewer_transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        Transcription_to_have = TC_D_reviewer_1_text_Approve in reviewer_transcription and TC_D_reviewer_1_text_Edit in reviewer_transcription and TC_D_annotation_1_1 in reviewer_transcription and TC_D_annotation_1_Edit in reviewer_transcription
        Transcription_do_not_have = TC_D_annotation_1_2 not in reviewer_transcription and TC_D_annotation_1_3 not in reviewer_transcription and TC_D_annotation_1_4 not in reviewer_transcription
        if Transcription_to_have and Transcription_do_not_have:
            status = "Pass"
            message = f"Reviewer Transcription matches the reviewer text."
            action_factory.helpers.attach_screenshot(name="ReviewerTranscriptionMatches")
            action_factory.helpers.attach_allure(name="Reviewer Transcription", text="\n".join(reviewer_transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Reviewer transcription text does not match the reviewer text."
            action_factory.helpers.attach_screenshot(name="ReviewerTranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Reviewer Transcription", text="\n".join(reviewer_transcription))
            assert False, message
        
         # Check Auto save Functionality 
        auto_save = action_factory.annotator_actions.perform_auto_save_functionality()
        if auto_save:
            status = "Pass"
            message = f"Auto-save functionality works successfully."
            action_factory.helpers.attach_screenshot(name="AutoSave")
            action_factory.helpers.attach_allure(name="Auto save", text="Auto-save functionality works successfully.")
            assert True, message
        else:
            status = "Fail"
            message = f"Auto-save functionality does not work."
            action_factory.helpers.attach_screenshot(name="AutoSaveFailed")
            action_factory.helpers.attach_allure(name="Auto save", text="Auto-save functionality does not work.")
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.back_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.search_input,timeout=10000)
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.click_project_name(Dataset_files_upload[0]))
        action_factory.ui_utils.smart_wait()
        action_factory.reviewer_actions.wait_for_iframe_ready()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.transcription.nth(0),timeout=30000)
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        Transcription_to_have = TC_D_reviewer_1_text_Approve in reviewer_transcription and TC_D_reviewer_1_text_Edit in reviewer_transcription and TC_D_annotation_1_1 in reviewer_transcription and TC_D_annotation_1_Edit in reviewer_transcription
        Transcription_do_not_have = TC_D_annotation_1_2 not in reviewer_transcription and TC_D_annotation_1_3 not in reviewer_transcription and TC_D_annotation_1_4 not in reviewer_transcription
        if Transcription_to_have and Transcription_do_not_have:
            status = "Pass"
            message = f"Auto-save - transcription saved successfully."
            action_factory.helpers.attach_screenshot(name="AutoSave_TranscriptionSaved")
            action_factory.helpers.attach_allure(name="Auto save - transcription", text="\n".join(transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Auto-save - Transcription text does not match the input text."
            action_factory.helpers.attach_screenshot(name="AutoSave_TranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Auto save - transcription", text="\n".join(transcription))
            assert False, message


        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.approve_button)
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.approve_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.smart_wait()
        claim_visible = action_factory.ui_utils.wait_for_visible_if_exists(action_factory.page_factory.annotator_page.claim_button, timeout=10000)
        if claim_visible:
            action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.back_button)
            action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.search_input,timeout=10000)
        count = action_factory.page_factory.annotator_page.files_name_list.count()
        if count > 0:
            files_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.files_name_list)
            if Dataset_files_upload[0] not in files_list:
                status = "Pass"
                message = f"Reviewer completed the file"
                action_factory.helpers.attach_screenshot(name="ReviewerCompleted")
                action_factory.helpers.attach_allure(name="Reviewer Completed", text="Reviewer")
                assert True, message
            else:
                status = "Fail"
                message = f"Annotator does not completed the file"
                action_factory.helpers.attach_screenshot(name="AnnotatorNotCompleted")
                action_factory.helpers.attach_allure(name="Reviewer Email", text="Reviewer")
                assert False, message
        else:
            status = "Pass"
            message = f"Reviewer completed all the files"
            action_factory.helpers.attach_screenshot(name="Reviewer Completed")
            action_factory.helpers.attach_allure(name="Reviewer Completed All Files", text="Reviewer")
            assert True, message

        # Review 2 st file Claim , Review and Annotate
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.click_project_name(Dataset_files_upload[1]))
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.reviewer_page.claim_button, timeout = 10000)
        action_factory.reviewer_actions.wait_for_iframe_ready()
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.claim_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.reviewer_page.begin_recording, timeout = 30000)
        is_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.reviewer_page.begin_recording)
        if is_visible:
            status = "Pass"
            message = f"Begin Recording button is visible."
            action_factory.helpers.attach_screenshot(name="Begin Recording button")
            action_factory.helpers.attach_allure(name="Begin Recording button", text="egin Recording button is visible")
            assert True, message
        else:
            status = "Fail"
            message = f"Begin Recording button is not visible."
            action_factory.helpers.attach_screenshot(name="Begin RecordingButtonNotVisible")
            action_factory.helpers.attach_allure(name="Begin Recording button", text="Begin Recording button is not visible")
            assert False, message
        action_factory.ui_utils.smart_wait()
        # Validate 1st Annotator Annotations 
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        Transcription_to_have = TC_D_annotation_1_1 in transcription and TC_D_annotation_1_2 in transcription and TC_D_annotation_1_Edit in transcription
        Transcription_do_not_have = TC_D_annotation_1_3 not in transcription and TC_D_annotation_1_4 not in transcription
        if Transcription_to_have and Transcription_do_not_have:
            status = "Pass"
            message = f"Transcription text matches the input text."
            action_factory.helpers.attach_screenshot(name="TranscriptionMatches")
            action_factory.helpers.attach_allure(name="Transcription", text="\n".join(transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Transcription text does not match the input text."
            action_factory.helpers.attach_screenshot(name="TranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Transcription", text="\n".join(transcription))
            assert False, message
        
        action_factory.annotator_actions.annontate_files(TC_D_reviewer_1_text_Approve, fast_forward = "15")
        # Validate Reviewer Annotation
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        if TC_D_reviewer_1_text_Approve in transcription:
            status = "Pass"
            message = f"Transcription text matches the input text."
            action_factory.helpers.attach_screenshot(name="TranscriptionMatches")
            action_factory.helpers.attach_allure(name="Transcription", text="\n".join(transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Transcription text does not match the input text."
            action_factory.helpers.attach_screenshot(name="TranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Transcription", text="\n".join(transcription))
            assert False, message

        # perform Save and Exit Functionality
        action_factory.annotator_actions.perform_save_exit()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.search_input,timeout=20000)
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.files_name_list)
        print(f"Files names list: {files_name_list}")
        if Dataset_files_upload[1] in files_name_list:
            status = "Pass"
            message = f"Reviewer completed and file is back to the list."
            action_factory.helpers.attach_screenshot(name="ReviewerCompleted")
            action_factory.helpers.attach_allure(name="Reviewer", text="Reviewer completed and file is back to the list.")
            assert True, message
        else:
            status = "Fail"
            message = f"Reviewer is not completed and file is not back to the list."
            action_factory.helpers.attach_screenshot(name="ReviewerNotCompleted")
            action_factory.helpers.attach_allure(name="Reviewer", text="Reviewer is not completed and file is not back to the list.")
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.click_project_name(Dataset_files_upload[1]))
        action_factory.ui_utils.smart_wait()
        action_factory.reviewer_actions.wait_for_iframe_ready()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.begin_recording,timeout=30000)
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.transcription.nth(0),timeout=50000)
        # Validate Reviewer Transcription after save and exit
        reviewer_transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        if TC_D_reviewer_1_text_Approve in reviewer_transcription:
            status = "Pass"
            message = f"Save and Exit - reviewer transcription saved successfully."
            action_factory.helpers.attach_screenshot(name="SaveAndExit_ReviewerTranscriptionSaved")
            action_factory.helpers.attach_allure(name="Save and Exit - reviewer transcription", text="\n".join(reviewer_transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Save and Exit - reviewer transcription text does not match the reviewer text."
            action_factory.helpers.attach_screenshot(name="SaveAndExit_ReviewerTranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Save and Exit - reviewer transcription", text="\n".join(reviewer_transcription))
            assert False, message

        # perform edit transcription 
        action_factory.annotator_actions.perform_edit_transcription(TC_D_annotation_1_2, TC_D_reviewer_1_text_Edit)
        # Validate Reviewer Transcription after edit
        reviewer_transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        reviewer_transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        Transcription_to_have = TC_D_reviewer_1_text_Approve in reviewer_transcription and TC_D_reviewer_1_text_Edit in reviewer_transcription and TC_D_annotation_1_1 in reviewer_transcription and TC_D_annotation_1_Edit in reviewer_transcription
        Transcription_do_not_have = TC_D_annotation_1_2 not in reviewer_transcription and TC_D_annotation_1_3 not in reviewer_transcription and TC_D_annotation_1_4 not in reviewer_transcription
        if Transcription_to_have and Transcription_do_not_have:
            status = "Pass"
            message = f"Reviewer Transcription matches the reviewer text."
            action_factory.helpers.attach_screenshot(name="ReviewerTranscriptionMatches")
            action_factory.helpers.attach_allure(name="Reviewer Transcription", text="\n".join(reviewer_transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Reviewer transcription text does not match the reviewer text."
            action_factory.helpers.attach_screenshot(name="ReviewerTranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Reviewer Transcription", text="\n".join(reviewer_transcription))
            assert False, message
        
         # Check Auto save Functionality 
        auto_save = action_factory.annotator_actions.perform_auto_save_functionality()
        if auto_save:
            status = "Pass"
            message = f"Auto-save functionality works successfully."
            action_factory.helpers.attach_screenshot(name="AutoSave")
            action_factory.helpers.attach_allure(name="Auto save", text="Auto-save functionality works successfully.")
            assert True, message
        else:
            status = "Fail"
            message = f"Auto-save functionality does not work."
            action_factory.helpers.attach_screenshot(name="AutoSaveFailed")
            action_factory.helpers.attach_allure(name="Auto save", text="Auto-save functionality does not work.")
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.back_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.search_input,timeout=10000)
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.click_project_name(Dataset_files_upload[1]))
        action_factory.ui_utils.smart_wait()
        action_factory.reviewer_actions.wait_for_iframe_ready()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.transcription.nth(0),timeout=30000)
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        reviewer_transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        Transcription_to_have = TC_D_reviewer_1_text_Approve in reviewer_transcription and TC_D_reviewer_1_text_Edit in reviewer_transcription and TC_D_annotation_1_1 in reviewer_transcription and TC_D_annotation_1_Edit in reviewer_transcription
        Transcription_do_not_have = TC_D_annotation_1_2 not in reviewer_transcription and TC_D_annotation_1_3 not in reviewer_transcription and TC_D_annotation_1_4 not in reviewer_transcription
        if Transcription_to_have and Transcription_do_not_have:
            status = "Pass"
            message = f"Auto-save - transcription saved successfully."
            action_factory.helpers.attach_screenshot(name="AutoSave_TranscriptionSaved")
            action_factory.helpers.attach_allure(name="Auto save - transcription", text="\n".join(transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Auto-save - Transcription text does not match the input text."
            action_factory.helpers.attach_screenshot(name="AutoSave_TranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Auto save - transcription", text="\n".join(transcription))
            assert False, message


        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.approve_button)
        action_factory.ui_utils.click_element(action_factory.page_factory.reviewer_page.approve_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.smart_wait()
        claim_visible = action_factory.ui_utils.wait_for_visible_if_exists(action_factory.page_factory.annotator_page.claim_button, timeout=10000)
        if claim_visible:
            action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.back_button)
            action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.search_input,timeout=10000)
        count = action_factory.page_factory.annotator_page.files_name_list.count()
        if count > 0:
            files_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.files_name_list)
            if Dataset_files_upload[1] not in files_list:
                status = "Pass"
                message = f"Reviewer completed the file"
                action_factory.helpers.attach_screenshot(name="ReviewerCompleted")
                action_factory.helpers.attach_allure(name="Reviewer Completed", text="Reviewer")
                assert True, message
            else:
                status = "Fail"
                message = f"Annotator does not completed the file"
                action_factory.helpers.attach_screenshot(name="AnnotatorNotCompleted")
                action_factory.helpers.attach_allure(name="Reviewer Email", text="Reviewer")
                assert False, message
        else:
            status = "Pass"
            message = f"Reviewer completed all the files"
            action_factory.helpers.attach_screenshot(name="Reviewer Completed")
            action_factory.helpers.attach_allure(name="Reviewer Completed All Files", text="Reviewer")
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