import allure
import pytest
from actions.action_factory import ActionFactory
from tests.projects.test_data_inputs import test_data_inputs

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
@allure.story("Create Valid Project")
@allure.title("Verify creating a valid project with dataset, template, and workflow")
def test_Create_Valid_Project(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        dataset_name = test_data_inputs.valid_dataset_Name
        template_name = test_data_inputs.valid_template_Name
        workflow_name = test_data_inputs.valid_workflow_Name
        project_name = test_data_inputs.valid_project_Name
        dataset_type_name = test_data_inputs.dataset_type_name
        dataset_files_upload = test_data_inputs.dataset_files_upload
        template_files_upload = test_data_inputs.template_files_upload
        nodes_list = test_data_inputs.nodes_list

        # Dataset Creation
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name=dataset_type_name)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.datasets_actions.upload_files_with_uploadBtn(*dataset_files_upload)
        action_factory.common_actions.validate_toast_msg("2 files added")
        action_factory.ui_utils.smart_wait()

        # Template Creation
        action_factory.templates_actions.click_templates_menu()
        action_factory.templates_actions.upload_new_template(template_name=template_name)
        action_factory.templates_actions.upload_template_files(*template_files_upload)
        action_factory.ui_utils.smart_wait()

        # Workflow Creation
        action_factory.workflows_actions.click_workflows_menu()
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
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

        # Project Creation
        action_factory.projects_actions.click_project_menu()
        action_factory.projects_actions.create_project(project_name=project_name, dataset_name=dataset_name, workflow_name=workflow_name)
        action_factory.ui_utils.smart_wait()

        # Validate project presence
        projects_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        if project_name in projects_list:
            status = "Pass"
            message = f"Project '{project_name}' created successfully."
            action_factory.helpers.attach_screenshot(name="ProjectCreatedSuccess")
            action_factory.helpers.attach_allure(name="Project Name", text=project_name)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_name}' not found in projects list."
            action_factory.helpers.attach_screenshot(name="ProjectCreatedFailed")
            action_factory.helpers.attach_allure(name="Project Name", text=project_name)
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
