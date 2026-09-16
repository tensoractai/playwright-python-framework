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
@allure.story("Workflow with 50 Characters Template Name")
@allure.title("Verify creating a template with 50 characters name, configuring it in a workflow, connecting nodes, and saving workflow")
def test_workflow_with_50_chars_template_name(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        template_name = test_data_inputs.template_50_chars_temp_name
        workflow_name = test_data_inputs.workflow_50_chars_temp_name
        description = test_data_inputs.valid_template_description
        template_file = test_data_inputs.valid_template_file
        nodes_list = ["Start", "Annotate", "Review", "Complete"]

        # Create Template with 50 Characters Name
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        template_names = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        if template_name in template_names:
            status = "Pass"
            message = f"Template '{template_name}' created successfully."
            action_factory.helpers.attach_screenshot(name="TemplateCreatedSuccessfully")
            action_factory.helpers.attach_allure(name="Create Valid Template", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Template '{template_name}' was not found in the templates list."
            action_factory.helpers.attach_screenshot(name="TemplateCreationFailed")
            action_factory.helpers.attach_allure(name="Create Valid Template", text=message)
            assert False, message

        # Create Workflow and configure 50 Characters Template Name
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description=description)
        action_factory.ui_utils.smart_wait()
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        # Apply 50 characters template name to Annotate node
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name)
        action_factory.ui_utils.smart_wait()
        # Connect Nodes
        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="review", node_index1=1, position1="right", index1=2,
            node_Name2="annotate", node_index2=1, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()
        # Save Workflow
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()
        # Validate Workflow is created and saved
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        workflow_names = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        if workflow_name in workflow_names:
            status = "Pass"
            message = f"Workflow '{workflow_name}' using 50-character template '{template_name}' was created, saved, and validated successfully."
            action_factory.helpers.attach_screenshot(name="WorkflowWith50CharsTemplateCreated")
            action_factory.helpers.attach_allure(name="Workflow with 50 Chars Template Name", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_name}' was not found in the workflows list."
            action_factory.helpers.attach_screenshot(name="WorkflowCreationFailed")
            action_factory.helpers.attach_allure(name="Workflow with 50 Chars Template Name", text=message)
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
