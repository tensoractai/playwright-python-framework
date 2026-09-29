import allure
import pytest
from actions.action_factory import ActionFactory
from tests.changeState.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    password = action_factory.helpers.fetch_dotenv("company_Password")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
    diff_email = action_factory.helpers.fetch_dotenv("MICROSOFT_OTP_EMAIL")
    # Login
    action_factory.login_actions.perform_login(
        url=url,
        email=email,
        password=password
    )
    action_factory.login_actions.use_different_email_OTP(diff_email)
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("Change State")
@allure.story("Check Change State Flow")
@allure.title("Check Change State Flow")
def test_change_state_flow(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        Dataset_Name = test_data_inputs.Dataset_changeState
        Dataset_Type = test_data_inputs.Dataset_changeState_Type        
        Dataset_Files = test_data_inputs.Dataset_Files
        Template_Name = test_data_inputs.Template_changeState
        Template_Image = test_data_inputs.Template_Image
        workflow_Name = test_data_inputs.workflow_Name
        workflow_Nodes = test_data_inputs.workflow_Nodes
        project_Name = test_data_inputs.project_Name
        annotator_email = action_factory.helpers.fetch_dotenv("annotator_Username")
        reviewer_email = action_factory.helpers.fetch_dotenv("reviewer_Username")

         # Dataset Creation Functionality
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.create_dataset(dataset_name=Dataset_Name, dataset_type_name=Dataset_Type)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(Dataset_Name))
        action_factory.datasets_actions.upload_files_with_uploadBtn(*Dataset_Files)
        action_factory.common_actions.validate_toast_msg("1 file added")
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_inside_file_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files = [file.split("/")[-1] for file in Dataset_Files]
        if all(file in files_name_list for file in expected_files):
            status = "Pass"
            message = f"All files uploaded successfully for dataset '{Dataset_Name}'."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload all files for dataset '{Dataset_Name}'."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files))
            assert False, message

        # Template Creation Functionality
        action_factory.templates_actions.click_templates_menu()
        action_factory.templates_actions.upload_new_template(template_name=Template_Name)
        action_factory.templates_actions.upload_template_files(*Template_Image)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.templates_page.template_names_list.nth(0))
        template_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        print(f"Template names list: {template_name_list}")
        if Template_Name in template_name_list:
            status = "Pass"
            message = f"Template '{Template_Name}' created successfully."
            action_factory.helpers.attach_screenshot(name="TemplateCreated")
            action_factory.helpers.attach_allure(name="Template Name", text=Template_Name)
            assert True, message
        else:
            status = "Fail"
            message = f"Template '{Template_Name}' creation failed."
            action_factory.helpers.attach_screenshot(name="TemplateCreationFailed")
            action_factory.helpers.attach_allure(name="Template Name", text=Template_Name)
            assert False, message

        # Workflow Creation Functionality
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_Name, description="Test workflow for automation")
        action_factory.ui_utils.smart_wait()
        for node in workflow_Nodes:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=Template_Name, position=0)
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.apply_template_to_annotate(template_name=Template_Name, position=0)
        action_factory.ui_utils.smart_wait()
        template_applied = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.template_applied_name)
        if Template_Name in template_applied and Template_Name in template_applied:
            status = "Pass"
            message = f"Workflow '{workflow_Name}' created successfully with template '{Template_Name}' and '{Template_Name}' applied."
            action_factory.helpers.attach_screenshot(name="WorkflowCreated")
            action_factory.helpers.attach_allure(name="Workflow Name", text=workflow_Name)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_Name}' creation failed or template '{Template_Name}' and '{Template_Name}' not applied."
            action_factory.helpers.attach_screenshot(name="WorkflowCreationFailed")
            action_factory.helpers.attach_allure(name="Workflow Name", text=workflow_Name)
            assert False, message
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.nodes_connection_flow(node_Name1="review", node_index1=1, position1="right", index1=2,
                                                             node_Name2="annotate", node_index2=1, position2="left", index2=1)
        action_factory.workflows_actions.nodes_connection_flow(node_Name1="review", node_index1=2, position1="right", index1=2,
                                                             node_Name2="annotate", node_index2=2, position2="left", index2=1)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()
        workflow_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        print(f"WorkFlow names list: {workflow_name_list}")
        if workflow_Name in workflow_name_list:
            status = "Pass"
            message = f"WorkFlow '{workflow_Name}' created successfully."
            action_factory.helpers.attach_screenshot(name="WorkFlowCreated")
            action_factory.helpers.attach_allure(name="WorkFlow Name", text=workflow_Name)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_Name}' creation failed."
            action_factory.helpers.attach_screenshot(name="WorkflowCreationFailed")
            action_factory.helpers.attach_allure(name="Workflow Name", text=workflow_Name)
            assert False, message

        # Projects Functionality
        action_factory.projects_actions.click_project_menu()
        action_factory.projects_actions.create_project(project_Name, Dataset_Type, Dataset_Name, workflow_Name)
        action_factory.ui_utils.smart_wait()
        workflow_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        print(f"Project names list: {workflow_name_list}")
        if project_Name in workflow_name_list:
            status = "Pass"
            message = f"Project '{project_Name}' created successfully."
            action_factory.helpers.attach_screenshot(name="Project Created")
            action_factory.helpers.attach_allure(name="Project Name", text=project_Name)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_Name}' creation failed."
            action_factory.helpers.attach_screenshot(name="Project Creation Failed")
            action_factory.helpers.attach_allure(name="Project Name", text=project_Name)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_Name))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.projects_page.task_panel, timeout = 10000)
        action_factory.projects_actions.click_teams_tab()
        action_factory.projects_actions.add_users(role="Annotator", email_address=annotator_email)
        action_factory.projects_actions.add_users(role="Reviewer", email_address=reviewer_email)
        action_factory.ui_utils.smart_wait()
        assigners_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.assigners_list)
        print(f"Assigners list: {assigners_list}")
        if annotator_email in assigners_list and reviewer_email in assigners_list:
            status = "Pass"
            message = f"Annotator and Reviewer added successfully."
            action_factory.helpers.attach_screenshot(name="Annotator and Reviewer Added")
            action_factory.helpers.attach_allure(name="Assigner List", text="Passed")
            assert True, message
        else:
            status = "Fail"
            message = f"Annotator and Reviewer not added."
            action_factory.helpers.attach_screenshot(name="Annotator and Reviewer Not Added")
            action_factory.helpers.attach_allure(name="Assigner List", text="Failed")
            assert False, message

        # Check the Change Status : 
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.task_panel)
        for file_name in expected_files:
            target_fname = file_name if isinstance(file_name, str) else file_name[0]
            action_factory.projects_actions.changeStatus_ofProject(target_fname, "Review 1")
            action_factory.ui_utils.smart_wait()
            status_after = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.get_file_status(target_fname))
            if "Review 1" in status_after:
                status = "Pass"
                message = f"File '{target_fname}' status changed successfully to Review 1."
                action_factory.helpers.attach_screenshot(name="File Status Changed to Review 1")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert True, message
            else:
                status = "Fail"
                message = f"File '{target_fname}' status not changed to Review 1."
                action_factory.helpers.attach_screenshot(name="File Status Not Changed to Review 1")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert False, message

        for file_name in expected_files:
            target_fname = file_name if isinstance(file_name, str) else file_name[0]
            action_factory.projects_actions.changeStatus_ofProject(target_fname, "Complete")
            action_factory.ui_utils.smart_wait()
            status_after = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.get_file_status(target_fname))
            if "Complete" in status_after:
                status = "Pass"
                message = f"File '{target_fname}' status changed successfully to Complete."
                action_factory.helpers.attach_screenshot(name="File Status Changed to Complete")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert True, message
            else:
                status = "Fail"
                message = f"File '{target_fname}' status not changed to Complete."
                action_factory.helpers.attach_screenshot(name="File Status Not Changed to Complete")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert False, message

        # Export Project JSON and Validate that there are no annotation values (empty {})
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.task_panel)
        action_factory.ui_utils.smart_wait()

        file_transcriptions = action_factory.projects_actions.export_and_validate_transcription_json(
            expected_files=expected_files,
            allow_empty=True
        )
        print(f"Exported JSON Transcriptions: {file_transcriptions}")

        transcriptions_dict = file_transcriptions.get("transcriptions", {})
        all_empty = True
        for file_name in expected_files:
            target_fname = file_name if isinstance(file_name, str) else file_name[0]
            texts = transcriptions_dict.get(target_fname, [])
            if len(texts) > 0:
                all_empty = False
                break

        if all_empty:
            status = "Pass"
            message = f"Project '{project_Name}' exported successfully and validated to have no annotation values (empty {{}})."
            action_factory.helpers.attach_screenshot(name="ExportJSONEmptyPass")
            action_factory.helpers.attach_allure(name="Export JSON Validation", text=str(file_transcriptions))
            assert True, message
        else:
            status = "Fail"
            message = f"Exported JSON for project '{project_Name}' contained unexpected annotation values: {file_transcriptions}"
            action_factory.helpers.attach_screenshot(name="ExportJSONEmptyFail")
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


