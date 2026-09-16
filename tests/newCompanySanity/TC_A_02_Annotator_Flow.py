import allure
import pytest
from actions.action_factory import ActionFactory
from tests.newCompanySanity.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = test_data_inputs.get_annotator_1_email(action_factory.helpers)
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
    action_factory.login_actions.select_organization(company_Name, "Annotator")
    return action_factory

@allure.feature("DataSet")
@allure.story("Data Set Flow")
@allure.title("Data Set Flow Validation")
def test_Annotator_Flow_test(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        annotator_email = test_data_inputs.get_annotator_1_email(action_factory.helpers)
        Dataset_files_path = test_data_inputs.TC_A_Dataset_files_upload
        Dataset_files_upload = [file.split("/")[-1] for file in Dataset_files_path]
        Annotation_1 = test_data_inputs.TC_A_annotation_text_1
        Annotation_2 = test_data_inputs.TC_A_annotation_text_2
        Annotation_3 = test_data_inputs.TC_A_annotation_text_3
        Annotation_4 = test_data_inputs.TC_A_annotation_text_4
        TC_A_annotation_text_Edit = test_data_inputs.TC_A_annotation_text_Edit

        # Annotator Functionality Check files is replicating in annotators page
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.tasks_menu)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.current_task_heading)
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.project_name_list.nth(0))
        project_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.project_name_list)
        i = action_factory.helpers.resolve_latest_index(project_list, test_data_inputs.TC_A_project_name)
        project_name = test_data_inputs.TC_A_project_name.format(i=i) if "{i}" in test_data_inputs.TC_A_project_name else test_data_inputs.TC_A_project_name
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
        # Check files is replicating in annotators page
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.click_project_name(project_name))
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.files_name_list)
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
        # Click first file and claim and perform annotation
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.click_project_name(Dataset_files_upload[0]))
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.claim_button, timeout = 10000)
        action_factory.reviewer_actions.wait_for_iframe_ready()
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.claim_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.save_and_exit_button, timeout = 10000)
        is_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.annotator_page.save_and_exit_button)
        if is_visible:
            status = "Pass"
            message = f"Save and exit button is visible."
            action_factory.helpers.attach_screenshot(name="SaveAndExitButtonVisible")
            action_factory.helpers.attach_allure(name="Save and exit button", text="Save and exit button is visible")
            assert True, message
        else:
            status = "Fail"
            message = f"Save and exit button is not visible."
            action_factory.helpers.attach_screenshot(name="SaveAndExitButtonNotVisible")
            action_factory.helpers.attach_allure(name="Save and exit button", text="Save and exit button is not visible")
            assert False, message
        action_factory.ui_utils.smart_wait()
        action_factory.annotator_actions.annontate_files(Annotation_1)
        action_factory.annotator_actions.annontate_files(Annotation_2)
        action_factory.annotator_actions.annontate_files(Annotation_3)
        action_factory.annotator_actions.annontate_files(Annotation_4)
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        found_annotations = [ann for ann in [Annotation_1, Annotation_2, Annotation_3, Annotation_4] if ann in transcription]
        
        if len(found_annotations) == 4:
            status = "Pass"
            message = f"All four annotation texts found in the transcription."
            action_factory.helpers.attach_screenshot(name="AllAnnotationsFound")
            action_factory.helpers.attach_allure(name="All Annotations Found", text=f"Found: {len(found_annotations)}/4 annotations")
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to find all four annotation texts in the transcription. Found: {len(found_annotations)}/4"
            action_factory.helpers.attach_screenshot(name="AllAnnotationsNotFound")
            action_factory.helpers.attach_allure(name="All Annotations Not Found", text=f"Found: {len(found_annotations)}/4 annotations")
            assert False, message

        # perform Edit Annotation :
        action_factory.annotator_actions.perform_edit_transcription(old_transcription = Annotation_2, new_transcription=TC_A_annotation_text_Edit)
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        if TC_A_annotation_text_Edit in transcription and Annotation_2 not in transcription:
            status = "Pass"
            message = f"Annotation text edited successfully."
            action_factory.helpers.attach_screenshot(name="AnnotationEdited")
            action_factory.helpers.attach_allure(name="Annotation Edit", text="Annotation text edited successfully.")
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to edit annotation text."
            action_factory.helpers.attach_screenshot(name="AnnotationEditFailed")
            action_factory.helpers.attach_allure(name="Annotation Edit", text="Failed to edit annotation text.")
            assert False, message
        # Save and Exit Check : 
        action_factory.annotator_actions.perform_save_exit()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.search_input,timeout=20000)
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.files_name_list)
        print(f"Files names list: {files_name_list}")
        if Dataset_files_upload[0] in files_name_list:
            status = "Pass"
            message = f"Annotation completed and file is back to the list."
            action_factory.helpers.attach_screenshot(name="AnnotationCompleted")
            action_factory.helpers.attach_allure(name="Annotation", text="Annotation completed and file is back to the list.")
            assert True, message
        else:
            status = "Fail"
            message = f"Annotation is not completed and file is not back to the list."
            action_factory.helpers.attach_screenshot(name="AnnotationNotCompleted")
            action_factory.helpers.attach_allure(name="Annotation", text="Annotation is not completed and file is not back to the list.")
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.click_project_name(Dataset_files_upload[0]))
        action_factory.ui_utils.smart_wait()
        action_factory.reviewer_actions.wait_for_iframe_ready()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.transcription.nth(0),timeout=30000)
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        if Annotation_1 in transcription and TC_A_annotation_text_Edit in transcription and Annotation_3 in transcription and Annotation_4 in transcription:
            status = "Pass"
            message = f"Save and Exit - transcription saved successfully."
            action_factory.helpers.attach_screenshot(name="SaveAndExit_TranscriptionSaved")
            action_factory.helpers.attach_allure(name="Save and Exit - transcription", text="\n".join(transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Transcription text does not match the input text."
            action_factory.helpers.attach_screenshot(name="TranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Transcription", text="\n".join(transcription))
            assert False, message
        # Perform Delete Annotation :
        action_factory.annotator_actions.perform_delete_transcription(Annotation_3)
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        if Annotation_3 not in transcription:
            status = "Pass"
            message = f"Annotation text deleted successfully."
            action_factory.helpers.attach_screenshot(name="AnnotationDeleted")
            action_factory.helpers.attach_allure(name="Annotation Delete", text="Annotation text deleted successfully.")
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to delete annotation text."
            action_factory.helpers.attach_screenshot(name="AnnotationDeleteFailed")
            action_factory.helpers.attach_allure(name="Annotation Delete", text="Failed to delete annotation text.")
            assert False, message
        action_factory.ui_utils.smart_wait()
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
        if Annotation_1 in transcription and TC_A_annotation_text_Edit in transcription and  Annotation_3 not in transcription and Annotation_4 in transcription:
            status = "Pass"
            message = f"Auto-save - transcription saved successfully."
            action_factory.helpers.attach_screenshot(name="AutoSave_TranscriptionSaved")
            action_factory.helpers.attach_allure(name="Auto save - transcription", text="\n".join(transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Transcription text does not match the input text."
            action_factory.helpers.attach_screenshot(name="TranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Transcription", text="\n".join(transcription))
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.submit_annotation)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.claim_button, timeout=10000)
        claim_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.annotator_page.claim_button)
        if claim_visible:
            action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.back_button)
            action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.search_input,timeout=10000)
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.click_project_name(project_name))
        action_factory.ui_utils.smart_wait()
        files_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.files_name_list)
        if Dataset_files_upload[0] not in files_list:
            status = "Pass"
            message = f"Annotator completed the file"
            action_factory.helpers.attach_screenshot(name="AnnotatorCompleted")
            action_factory.helpers.attach_allure(name="Annotator Email", text=annotator_email)
            assert True, message
        else:
            status = "Fail"
            message = f"Annotator does not completed the file"
            action_factory.helpers.attach_screenshot(name="AnnotatorNotCompleted")
            action_factory.helpers.attach_allure(name="Annotator Email", text=annotator_email)
            assert False, message

        # Click the Second File and Perform Annotation : 
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.click_project_name(Dataset_files_upload[1]))
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.claim_button, timeout = 10000)
        action_factory.reviewer_actions.wait_for_iframe_ready()
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.claim_button)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.save_and_exit_button, timeout = 10000)
        is_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.annotator_page.save_and_exit_button)
        if is_visible:
            status = "Pass"
            message = f"Save and exit button is visible for 1st file"
            action_factory.helpers.attach_screenshot(name="SaveAndExitButtonVisible_1stFile")
            action_factory.helpers.attach_allure(name="Save and exit button", text="Save and exit button is visible for 1st file")
            assert True, message
        else:
            status = "Fail"
            message = f"Save and exit button is not visible for 1st file"
            action_factory.helpers.attach_screenshot(name="SaveAndExitButtonNotVisible_1stFile")
            action_factory.helpers.attach_allure(name="Save and exit button", text="Save and exit button is not visible for 1st file")
            assert False, message
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.smart_wait()
        action_factory.annotator_actions.annontate_files(Annotation_1)
        action_factory.annotator_actions.annontate_files(Annotation_2)
        action_factory.annotator_actions.annontate_files(Annotation_3)
        action_factory.annotator_actions.annontate_files(Annotation_4)
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        found_annotations = [ann for ann in [Annotation_1, Annotation_2, Annotation_3, Annotation_4] if ann in transcription]
        
        if len(found_annotations) == 4:
            status = "Pass"
            message = f"All four annotation texts found in the transcription."
            action_factory.helpers.attach_screenshot(name="AllAnnotationsFound")
            action_factory.helpers.attach_allure(name="All Annotations Found", text=f"Found: {len(found_annotations)}/3 annotations")
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to find all four annotation texts in the transcription. Found: {len(found_annotations)}/3"
            action_factory.helpers.attach_screenshot(name="AllAnnotationsNotFound")
            action_factory.helpers.attach_allure(name="All Annotations Not Found", text=f"Found: {len(found_annotations)}/3 annotations")
            assert False, message

        # perform Edit Annotation :
        action_factory.annotator_actions.perform_edit_transcription(Annotation_2, TC_A_annotation_text_Edit)
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        if TC_A_annotation_text_Edit in transcription and Annotation_2 not in transcription:
            status = "Pass"
            message = f"Annotation text edited successfully."
            action_factory.helpers.attach_screenshot(name="AnnotationEdited")
            action_factory.helpers.attach_allure(name="Annotation Edit", text="Annotation text edited successfully.")
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to edit annotation text."
            action_factory.helpers.attach_screenshot(name="AnnotationEditFailed")
            action_factory.helpers.attach_allure(name="Annotation Edit", text="Failed to edit annotation text.")
            assert False, message
        # Save and Exit Check : 
        action_factory.annotator_actions.perform_save_exit()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.search_input,timeout=20000)
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.files_name_list)
        print(f"Files names list: {files_name_list}")
        if Dataset_files_upload[1] in files_name_list:
            status = "Pass"
            message = f"Annotation completed and file is back to the list."
            action_factory.helpers.attach_screenshot(name="AnnotationCompleted")
            action_factory.helpers.attach_allure(name="Annotation", text="Annotation completed and file is back to the list.")
            assert True, message
        else:
            status = "Fail"
            message = f"Annotation is not completed and file is not back to the list."
            action_factory.helpers.attach_screenshot(name="AnnotationNotCompleted")
            action_factory.helpers.attach_allure(name="Annotation", text="Annotation is not completed and file is not back to the list.")
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.click_project_name(Dataset_files_upload[1]))
        action_factory.ui_utils.smart_wait()
        action_factory.reviewer_actions.wait_for_iframe_ready()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.transcription.nth(0),timeout=30000)
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        if Annotation_1 in transcription and TC_A_annotation_text_Edit in transcription and Annotation_3 in transcription and Annotation_4 in transcription:
            status = "Pass"
            message = f"Save and Exit - transcription saved successfully."
            action_factory.helpers.attach_screenshot(name="SaveAndExit_TranscriptionSaved")
            action_factory.helpers.attach_allure(name="Save and Exit - transcription", text="\n".join(transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Transcription text does not match the input text."
            action_factory.helpers.attach_screenshot(name="TranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Transcription", text="\n".join(transcription))
            assert False, message
        # Perform Delete Annotation :
        action_factory.annotator_actions.perform_delete_transcription(Annotation_3)
        transcription = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.transcription)
        if Annotation_3 not in transcription:
            status = "Pass"
            message = f"Annotation text deleted successfully."
            action_factory.helpers.attach_screenshot(name="AnnotationDeleted")
            action_factory.helpers.attach_allure(name="Annotation Delete", text="Annotation text deleted successfully.")
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to delete annotation text."
            action_factory.helpers.attach_screenshot(name="AnnotationDeleteFailed")
            action_factory.helpers.attach_allure(name="Annotation Delete", text="Failed to delete annotation text.")
            assert False, message
        action_factory.ui_utils.smart_wait()
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
        if Annotation_1 in transcription and TC_A_annotation_text_Edit in transcription and  Annotation_3 not in transcription and Annotation_4 in transcription:
            status = "Pass"
            message = f"Auto-save - transcription saved successfully."
            action_factory.helpers.attach_screenshot(name="AutoSave_TranscriptionSaved")
            action_factory.helpers.attach_allure(name="Auto save - transcription", text="\n".join(transcription))
            assert True, message
        else:
            status = "Fail"
            message = f"Transcription text does not match the input text."
            action_factory.helpers.attach_screenshot(name="TranscriptionNotMatches")
            action_factory.helpers.attach_allure(name="Transcription", text="\n".join(transcription))
            assert False, message
            
        action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.submit_annotation)
        action_factory.ui_utils.smart_wait()
        claim_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.annotator_page.claim_button)
        if claim_visible:
            action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.back_button)
            action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.annotator_page.search_input,timeout=10000)
        files_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.annotator_page.files_name_list)
        if Dataset_files_upload[1] not in files_list:
            status = "Pass"
            message = f"Annotator completed the file"
            action_factory.helpers.attach_screenshot(name="AnnotatorCompleted")
            action_factory.helpers.attach_allure(name="Annotator Email", text=annotator_email)
            assert True, message
        else:
            status = "Fail"
            message = f"Annotator does not completed the file"
            action_factory.helpers.attach_screenshot(name="AnnotatorNotCompleted")
            action_factory.helpers.attach_allure(name="Annotator Email", text=annotator_email)
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