import allure
import pytest
from actions.action_factory import ActionFactory
from tests.datasets.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    password = action_factory.helpers.fetch_dotenv("company_Password")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
    diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
    diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")
    
    # Login & Setup
    action_factory.login_actions.perform_login(url=url, email=email, password=password)
    action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("Projects")
@allure.story("Prevent Adding Incompatible Dataset Type to Project")
@allure.title("Verify creating datasets, template, workflow, project, and preventing incompatible dataset addition in project session")
def test_prevent_add_incompatible_dataset_to_project(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        dataset_text_name = test_data_inputs.TC_12_Dataset_name
        dataset_image_name = test_data_inputs.TC_12_Dataset_name
        description = test_data_inputs.description
        text_files = test_data_inputs.Text_Files[:1]
        image_files = test_data_inputs.Image_Single_File
        template_name = test_data_inputs.TC_12_Template_name
        template_files = test_data_inputs.Template_files_upload
        workflow_name = test_data_inputs.TC_12_WorkFlow_name
        nodes_list = test_data_inputs.Prevent_node_list
        project_name = test_data_inputs.TC_12_Project_name

        text_file_name = [f.split("/")[-1] for f in text_files][0]
        image_file_name = [f.split("/")[-1] for f in image_files][0]

        # Create Text Dataset "AUT_Dataset_Text"
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_text_name, dataset_type_name="TEXT", description=description)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_text_name))
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*text_files)
        action_factory.ui_utils.smart_wait()

        # Create Image Dataset "AUT_Dataset_Image"
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_image_name, dataset_type_name="Image", description=description)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_image_name))
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*image_files)
        action_factory.ui_utils.smart_wait()
        # Validate Dataset Names is present or not 
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.datasets_menu)
        action_factory.ui_utils.smart_wait()
        dataset_names = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        if dataset_text_name and dataset_image_name in dataset_names:
            status = "Pass"
            message = f"Incompatible dataset '{dataset_text_name}' was correctly prevented from being added to project."
            action_factory.helpers.attach_screenshot(name="IncompatibleDatasetAdditionPrevented")
            action_factory.helpers.attach_allure(name="Prevent Add Incompatible Dataset", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Incompatible dataset '{dataset_text_name}' was incorrectly added to the project."
            action_factory.helpers.attach_screenshot(name="IncompatibleDatasetAdditionFailed")
            action_factory.helpers.attach_allure(name="Prevent Add Incompatible Dataset", text=message)
            assert False, message

        # Navigate to Files Tab and validate dataset names are shown
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.files_menu)
        action_factory.ui_utils.smart_wait()
        dataset_names_in_files = action_factory.ui_utils.grab_text_from_all(
            action_factory.page_factory.datasets_page.dataset_file_name_list
        )
        print(f"Dataset names in files tab: {dataset_names_in_files}")
        if dataset_text_name in dataset_names_in_files and dataset_image_name in dataset_names_in_files:
            status = "Pass"
            message = f"Dataset '{dataset_text_name}' and '{dataset_image_name}' was correctly prevented from being added to project."
            action_factory.helpers.attach_screenshot(name="DatasetNamesFoundInFilesTab")
            action_factory.helpers.attach_allure(name="Dataset Names Found In Files Tab", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Dataset '{dataset_text_name}' and '{dataset_image_name}' was not found in files tab."
            action_factory.helpers.attach_screenshot(name="DatasetNamesNotFoundInFilesTab")
            action_factory.helpers.attach_allure(name="Dataset Names Found In Files Tab", text=message)
            assert False, message
            
        # Create Template
        action_factory.templates_actions.click_templates_menu()
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(*template_files)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Validate Template Name is present or not 
        template_names = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        if template_name in template_names:
            status = "Pass"
            message = f"Template '{template_name}' was correctly prevented from being added to project."
            action_factory.helpers.attach_screenshot(name="TemplateNamesFoundInTemplatesTab")
            action_factory.helpers.attach_allure(name="Template Names Found In Templates Tab", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template '{template_name}' was not found in templates tab."
            action_factory.helpers.attach_screenshot(name="TemplateNamesNotFoundInTemplatesTab")
            action_factory.helpers.attach_allure(name="Template Names Found In Templates Tab", text=message)
            assert False, message

        # Create Workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description=description)
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
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

        # Validate workflow is created
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

        # Create Project linking Image dataset and workflow
        action_factory.projects_actions.click_project_menu()
        action_factory.projects_actions.create_project(
            project_name=project_name, dataset_name=dataset_image_name, workflow_name=workflow_name, description=description
        )
        action_factory.ui_utils.smart_wait()

        # Validate project is created
        project_names = action_factory.ui_utils.grab_text_from_all(
            action_factory.page_factory.projects_page.project_names_list
        )
        print(f"Project names list: {project_names}")
        if project_name in project_names:
            status = "Pass"
            message = f"Project '{project_name}' was created successfully."
            action_factory.helpers.attach_screenshot(name="ProjectNamesFoundInProjectsTab")
            action_factory.helpers.attach_allure(name="Project Names Found In Projects Tab", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' was not found in projects tab."
            action_factory.helpers.attach_screenshot(name="ProjectNamesNotFoundInProjectsTab")
            action_factory.helpers.attach_allure(name="Project Names Found In Projects Tab", text=message)
            assert False, message

        # Open Project and verify Tasks tab has only Image uploaded file
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_name))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.tasks_tab)
        action_factory.ui_utils.smart_wait()

        tasks_files = action_factory.ui_utils.grab_text_from_all(
            action_factory.page_factory.projects_page.file_name_list_Task_tab
        )
        print(f"Files in tasks tab: {tasks_files}")
        if image_file_name in tasks_files and text_file_name not in tasks_files:
            status = "Pass"
            message = f"Only Image file '{image_file_name}' was found in tasks tab."
            action_factory.helpers.attach_screenshot(name="ProjectNamesFoundInProjectsTab")
            action_factory.helpers.attach_allure(name="Project Names Found In Projects Tab", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Only Image file '{image_file_name}' was not found in tasks tab."
            action_factory.helpers.attach_screenshot(name="ProjectNamesNotFoundInProjectsTab")
            action_factory.helpers.attach_allure(name="Project Names Found In Projects Tab", text=message)
            assert False, message

        # Click Datasets tab in project session and click Add button
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.project_datasets_tab)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.add_datasets_btn)
        action_factory.ui_utils.smart_wait()

        # Select Text dataset and click Add/Sync button
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.dataset_name_search)
        action_factory.ui_utils.type_text(action_factory.page_factory.projects_page.dataset_name_search, dataset_text_name)
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.return_file_checkbox(dataset_text_name).first)
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.add_sync_btn)
        action_factory.ui_utils.smart_wait()

        # Validate Text dataset should NOT get added to the project
        project_datasets = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.dataset_name_list)   
        print(f"Project datasets after add/sync attempt: {project_datasets}")

        if dataset_text_name not in project_datasets:
            status = "Pass"
            message = f"Incompatible dataset '{dataset_text_name}' was correctly prevented from being added to project."
            action_factory.helpers.attach_screenshot(name="IncompatibleDatasetAdditionPrevented")
            action_factory.helpers.attach_allure(name="Prevent Add Incompatible Dataset", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Incompatible dataset '{dataset_text_name}' was incorrectly added to the project."
            action_factory.helpers.attach_screenshot(name="IncompatibleDatasetAdditionFailed")
            action_factory.helpers.attach_allure(name="Prevent Add Incompatible Dataset", text=message)
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
