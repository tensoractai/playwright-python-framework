import allure
import pytest
from actions.action_factory import ActionFactory
from tests.objectwaysSanity.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    password = action_factory.helpers.fetch_dotenv("company_Password")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
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
@allure.title("TC C Validation")
def test_company_admin_C_flow_test(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        
        dataset_name = test_data_inputs.TC_C_dataset_name
        template_name = test_data_inputs.TC_C_template_name
        workflow_name = test_data_inputs.TC_C_workflow_name
        project_name = test_data_inputs.TC_C_project_name
        dataset_type_name = test_data_inputs.TC_A_dataset_type_name
        Dataset_files_upload = test_data_inputs.TC_A_Dataset_files_upload
        Template_files_upload = test_data_inputs.TC_A_Template_files_upload
        nodes_list = test_data_inputs.TC_C_nodes_list
        annotator_1_email = action_factory.helpers.fetch_dotenv("annotator_Username")
        annotator_2_email = action_factory.helpers.fetch_dotenv("annotator_Username_2")
        reviewer_email = action_factory.helpers.fetch_dotenv("reviewer_Username")
        
        # Dataset Creation Functionality
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()

        dataset_names_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        i = action_factory.helpers.resolve_next_index(dataset_names_list, test_data_inputs.TC_C_dataset_name)

        dataset_name = test_data_inputs.TC_C_dataset_name.format(i=i) if "{i}" in test_data_inputs.TC_C_dataset_name else test_data_inputs.TC_C_dataset_name
        template_name = test_data_inputs.TC_C_template_name.format(i=i) if "{i}" in test_data_inputs.TC_C_template_name else test_data_inputs.TC_C_template_name
        workflow_name = test_data_inputs.TC_C_workflow_name.format(i=i) if "{i}" in test_data_inputs.TC_C_workflow_name else test_data_inputs.TC_C_workflow_name
        project_name = test_data_inputs.TC_C_project_name.format(i=i) if "{i}" in test_data_inputs.TC_C_project_name else test_data_inputs.TC_C_project_name

        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name=dataset_type_name)
        action_factory.ui_utils.smart_wait()
        dataset_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        print(f"Dataset names list: {dataset_name_list}")
        if dataset_name in dataset_name_list:
            status = "Pass"
            message = f"Dataset '{dataset_name}' created successfully."
            action_factory.helpers.attach_screenshot(name="DatasetCreated")
            action_factory.helpers.attach_allure(name="Dataset Name", text=dataset_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset '{dataset_name}' creation failed."
            action_factory.helpers.attach_screenshot(name="DatasetCreationFailed")
            action_factory.helpers.attach_allure(name="Dataset Name", text=dataset_name)
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.datasets_actions.upload_files_with_uploadBtn(*Dataset_files_upload)
        action_factory.common_actions.validate_toast_msg("2 files added")
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.files_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files = [file.split("/")[-1] for file in Dataset_files_upload]
        if all(file in files_name_list for file in expected_files):
            status = "Pass"
            message = f"All files uploaded successfully for dataset '{dataset_name}'."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload all files for dataset '{dataset_name}'."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files))
            assert False, message

        # Template Creation Functionality
        action_factory.templates_actions.click_templates_menu()
        action_factory.templates_actions.upload_new_template(template_name=template_name)
        action_factory.templates_actions.upload_template_files(*Template_files_upload)
        action_factory.ui_utils.smart_wait()
        template_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        print(f"Template names list: {template_name_list}")
        if template_name in template_name_list:
            status = "Pass"
            message = f"Template '{template_name}' created successfully."
            action_factory.helpers.attach_screenshot(name="TemplateCreated")
            action_factory.helpers.attach_allure(name="Template Name", text=template_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Template '{template_name}' creation failed."
            action_factory.helpers.attach_screenshot(name="TemplateCreationFailed")
            action_factory.helpers.attach_allure(name="Template Name", text=template_name)
            assert False, message

        # Workflow Creation Functionality
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description="Test workflow for automation")
        action_factory.ui_utils.smart_wait()
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name)
        action_factory.ui_utils.smart_wait()
        template_applied = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.template_applied_name)
        if template_name in template_applied:
            status = "Pass"
            message = f"Workflow '{workflow_name}' created successfully with template '{template_name}' applied."
            action_factory.helpers.attach_screenshot(name="WorkflowCreated")
            action_factory.helpers.attach_allure(name="Workflow Name", text=workflow_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_name}' creation failed or template '{template_name}' not applied."
            action_factory.helpers.attach_screenshot(name="WorkflowCreationFailed")
            action_factory.helpers.attach_allure(name="Workflow Name", text=workflow_name)
            assert False, message
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.nodes_connection_flow(node_Name1="review", node_index1=1, position1="right", index1=2,
                                                             node_Name2="annotate", node_index2=1, position2="left", index2=1)
        action_factory.workflows_actions.required_annotator("2")
        action_factory.ui_utils.smart_wait()
        save_enabled = action_factory.ui_utils.is_element_enabled(action_factory.page_factory.workflows_page.save_btn)
        if save_enabled :
            status = "Pass"
            message = f"Save Button Enabled So node gets connected"
            action_factory.helpers.attach_screenshot(name="Nodes Connected")
            action_factory.helpers.attach_allure(name="Nodes Connected", text=workflow_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Save button Disabled Nodes not yet connected"
            action_factory.helpers.attach_screenshot(name="Nodes Disconnection")
            action_factory.helpers.attach_allure(name="Nodes Disconnection", text=workflow_name)
            assert False, message
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()
        workflow_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        print(f"WorkFlow names list: {workflow_name_list}")
        if workflow_name in workflow_name_list:
            status = "Pass"
            message = f"WorkFlow '{template_name}' created successfully."
            action_factory.helpers.attach_screenshot(name="WorkFlowCreated")
            action_factory.helpers.attach_allure(name="WorkFlow Name", text=template_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{template_name}' creation failed."
            action_factory.helpers.attach_screenshot(name="WorkflowCreationFailed")
            action_factory.helpers.attach_allure(name="Workflow Name", text=template_name)
            assert False, message

        # Projects Functionality
        action_factory.projects_actions.click_project_menu()
        action_factory.projects_actions.create_project(project_name, dataset_name, workflow_name)
        action_factory.ui_utils.smart_wait()
        workflow_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        print(f"Project names list: {workflow_name_list}")
        if project_name in workflow_name_list:
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
        taskPanel = action_factory.ui_utils.is_element_visible(action_factory.page_factory.projects_page.task_panel)
        if taskPanel:
            status = "Pass"
            message = f"Project '{project_name}' task panel is visible."
            action_factory.helpers.attach_screenshot(name="Project Task Panel Visible")
            action_factory.helpers.attach_allure(name="Project Task Panel", text=project_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' task panel is not visible."
            action_factory.helpers.attach_screenshot(name="Project Task Panel Not Visible")
            action_factory.helpers.attach_allure(name="Project Task Panel", text=project_name)
            assert False, message
        action_factory.projects_actions.click_teams_tab()
        action_factory.projects_actions.add_users(role="Annotator", email_address=annotator_1_email)
        action_factory.projects_actions.add_users(role="Annotator", email_address=annotator_2_email)
        action_factory.projects_actions.add_users(role="Reviewer", email_address=reviewer_email)
        action_factory.ui_utils.smart_wait()
        assigners_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.assigners_list)
        print(f"Assigners list: {assigners_list}")
        if annotator_1_email in assigners_list and reviewer_email in assigners_list and annotator_2_email in assigners_list:
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
