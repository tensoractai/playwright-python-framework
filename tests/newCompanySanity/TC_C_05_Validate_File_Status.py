import allure
import pytest
from actions.action_factory import ActionFactory
from tests.newCompanySanity.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = test_data_inputs.get_company_admin_email(action_factory.helpers)
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
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("DataSet")
@allure.story("Data Set Flow")
@allure.title("Data Set Flow Validation")
def test_Validate_File_status_test(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each

        Dataset_files_upload = [("audio 2.flac","Complete"),("audio 3.mp3","Complete")]

        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()
        project_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        print(f"Project names list: {project_name_list}")
        i = action_factory.helpers.resolve_latest_index(project_name_list, test_data_inputs.TC_C_project_name)
        project_name = test_data_inputs.TC_C_project_name.format(i=i) if "{i}" in test_data_inputs.TC_C_project_name else test_data_inputs.TC_C_project_name
        if project_name in project_name_list:
            status = "Pass"
            message = f"Project '{project_name}' created successfully."
            action_factory.helpers.attach_screenshot(name="Project Created")
            action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' creation failed."
            action_factory.helpers.attach_screenshot(name="Project Creation Failed")
            action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_name))
        action_factory.ui_utils.smart_wait()
        for file_Name, expected_status in Dataset_files_upload:
            action_factory.ui_utils.smart_wait()
            actual_status = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.get_file_status(file_Name))
            if expected_status in actual_status:
                status = "Pass"
                message = f"File status '{file_Name}' completed successfully."
                action_factory.helpers.attach_screenshot(name="File Status Completed")
                action_factory.helpers.attach_allure(name="File Status", text=file_Name)
                assert True, message
            else:
                status = "Fail"
                message = f"File status '{file_Name}' completion failed."
                action_factory.helpers.attach_screenshot(name="File Status Completion Failed")
                action_factory.helpers.attach_allure(name="File Status", text=file_Name)
                assert False, message

        
        # Validate Json Files : 
        TC_C_annotation_1_1 = test_data_inputs.TC_C_annotation_1_1
        TC_C_annotation_1_2 = test_data_inputs.TC_C_annotation_1_2
        TC_C_annotation_1_3 = test_data_inputs.TC_C_annotation_1_3
        TC_C_annotation_1_4 = test_data_inputs.TC_C_annotation_1_4
        TC_C_annotation_1_Edit = test_data_inputs.TC_C_annotation_1_Edit
        TC_C_annotation_2_1 = test_data_inputs.TC_C_annotation_2_1
        TC_C_annotation_2_2 = test_data_inputs.TC_C_annotation_2_2
        TC_C_annotation_2_3 = test_data_inputs.TC_C_annotation_2_3
        TC_C_annotation_2_4 = test_data_inputs.TC_C_annotation_2_4
        TC_C_annotation_2_Edit = test_data_inputs.TC_C_annotation_2_Edit
        TC_C_reviewer_1_text_Edit = test_data_inputs.TC_C_reviewer_1_text_Edit
        TC_C_reviewer_1_text_Approve = test_data_inputs.TC_C_reviewer_1_text_Approve
        Dataset_files_path = test_data_inputs.TC_A_Dataset_files_upload
        Dataset_files_upload = [file.split("/")[-1] for file in Dataset_files_path]

        expected_texts = [TC_C_annotation_1_1, TC_C_annotation_1_Edit, TC_C_annotation_2_1, TC_C_annotation_2_Edit,TC_C_reviewer_1_text_Approve,TC_C_reviewer_1_text_Edit, TC_C_annotation_2_2]
        unexpected_texts = [TC_C_annotation_1_2,TC_C_annotation_1_3, TC_C_annotation_1_4, TC_C_annotation_2_3, TC_C_annotation_2_4]
        file_transcriptions = action_factory.projects_actions.export_and_validate_transcription_json(
            expected_files=Dataset_files_upload,
            expected_texts=expected_texts,
            unexpected_texts=unexpected_texts
        )

        if file_transcriptions:
            status = "Pass"
            message = f"Exported JSON file contains Annotator transcription ('{TC_C_annotation_1_1}','{TC_C_annotation_1_Edit}','{TC_C_annotation_2_1}','{TC_C_annotation_2_Edit}') and Reviewer transcription ('{TC_C_reviewer_1_text_Approve}','{TC_C_reviewer_1_text_Edit}','{TC_C_annotation_2_2}') for files {Dataset_files_upload}."
            action_factory.helpers.attach_screenshot(name="ExportJSONValidationPass")
            action_factory.helpers.attach_allure(name="Export JSON Validation", text=str(file_transcriptions))
            assert True, message
        else:
            status = "Fail"
            message = f"Exported JSON file validation failed. Annotator text in JSON: {TC_C_annotation_1_1 in file_transcriptions}, Reviewer text in JSON: {TC_C_reviewer_1_text_Approve in file_transcriptions}."
            action_factory.helpers.attach_screenshot(name="ExportJSONValidationFail")
            action_factory.helpers.attach_allure(name="Export JSON Validation", text=str(file_transcriptions))
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