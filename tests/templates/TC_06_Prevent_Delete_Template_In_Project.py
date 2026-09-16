import allure
import pytest
from actions.action_factory import ActionFactory
from tests.templates.test_data_inputs import test_data_inputs

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

@allure.feature("Templates")
@allure.story("Prevent Deleting Template Used in Project")
@allure.title("Verify prevention of deleting a template associated with an active project")
def test_prevent_delete_template_in_project(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        dataset_name = test_data_inputs.prevent_template_dataset_name
        template_name = test_data_inputs.prevent_template_name
        workflow_name = test_data_inputs.prevent_template_workflow_name
        project_name = test_data_inputs.prevent_template_project_name
        nodes_list = test_data_inputs.prevent_template_node_list
        audio_files = test_data_inputs.Audio_Files
        template_files = test_data_inputs.Template_files_upload

        # Click Dataset menu and create dataset
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name="Audio")
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*audio_files)
        action_factory.ui_utils.smart_wait()

        # Click Template menu and create template "AUT_Delete_Template"
        action_factory.templates_actions.click_templates_menu()
        action_factory.templates_actions.upload_new_template(template_name=template_name)
        action_factory.templates_actions.upload_template_files(*template_files)
        action_factory.ui_utils.smart_wait()

        # Click Workflow menu and create workflow applying the template
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description="Workflow for testing template deletion prevention")
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

        # Click Project menu and create project linking dataset and workflow
        action_factory.projects_actions.click_project_menu()
        action_factory.projects_actions.create_project(project_name=project_name, dataset_name=dataset_name, workflow_name=workflow_name)
        action_factory.ui_utils.smart_wait()

        # Navigate to Template Menu and attempt to delete template "AUT_Delete_Template"
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.delete_template(template_name)
        action_factory.ui_utils.smart_wait()

        # Validate template_delete_failed_msg is visible
        delete_failed_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.templates_page.template_delete_failed_msg)
        if delete_failed_visible:
            status = "Pass"
            message = f"Template '{template_name}' deletion was correctly prevented and 'Failed Deleted Template' message displayed."
            action_factory.helpers.attach_screenshot(name="TemplateDeletionFailedMsgVisible")
            action_factory.helpers.attach_allure(name="Prevent Delete Template in Project", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Failed error message was not displayed when attempting to delete template '{template_name}'."
            action_factory.helpers.attach_screenshot(name="TemplateDeletionFailedMsgNotVisible")
            action_factory.helpers.attach_allure(name="Prevent Delete Template in Project", text=message)
            assert False, message

        # Cancel popup and validate template name is still present in template list
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        template_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        if template_name in template_list:
            status = "Pass"
            message = f"Template '{template_name}' is still present in template list as expected."
            action_factory.helpers.attach_screenshot(name="TemplateRetainedInList")
            action_factory.helpers.attach_allure(name="Prevent Delete Template in Project", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template '{template_name}' was deleted or removed from template list."
            action_factory.helpers.attach_screenshot(name="TemplateNotRetainedInList")
            action_factory.helpers.attach_allure(name="Prevent Delete Template in Project", text=message)
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
