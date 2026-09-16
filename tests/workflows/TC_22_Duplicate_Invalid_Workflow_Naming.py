import allure
import pytest
from actions.action_factory import ActionFactory
from tests.workflows.test_data_inputs import test_data_inputs

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

@allure.feature("Workflows")
@allure.story("Duplicate & Special Character Naming Validation")
@allure.title("Verify creating workflow with duplicate name or special characters is prevented with proper error validation")
def test_duplicate_invalid_workflow_naming(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        template_name = "AUT_WF_Template_12"
        duplicate_name = test_data_inputs.duplicate_workflow_name
        special_char_name = test_data_inputs.special_char_workflow_name
        description = test_data_inputs.description
        template_file = test_data_inputs.valid_template_file
        special_char_workflow_description = test_data_inputs.special_char_workflow_description
        nodes_list = ["Start", "Annotate", "Review", "Complete"]

        # Create Template
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Create initial workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=duplicate_name, description=description)
        action_factory.ui_utils.smart_wait()
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name, position=0)
        action_factory.ui_utils.smart_wait()

        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="review", node_index1=1, position1="right", index1=2,
            node_Name2="annotate", node_index2=1, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()
        workflow_name = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        print(f"Workflow name: {workflow_name}")
        if duplicate_name in workflow_name:
            status = "Pass"
            message = f"Duplicate workflow name '{duplicate_name}' was not blocked."
            action_factory.helpers.attach_screenshot(name="DuplicateWorkflowErrorPass")
            action_factory.helpers.attach_allure(name="Duplicate Workflow Naming", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Duplicate workflow name '{duplicate_name}' was not blocked."
            action_factory.helpers.attach_screenshot(name="DuplicateWorkflowErrorFailed")
            action_factory.helpers.attach_allure(name="Duplicate Workflow Naming", text=message)
            assert False, message

        # Attempt to create duplicate workflow name
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=duplicate_name.upper(), description=description)
        action_factory.ui_utils.smart_wait()
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name, position=0)
        action_factory.ui_utils.smart_wait()

        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="review", node_index1=1, position1="right", index1=2,
            node_Name2="annotate", node_index2=1, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()
        duplicate_error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.workflow_exists_error)
        print(f"Duplicate workflow name error visibility: {duplicate_error_visible}")

        if duplicate_error_visible:
            status = "Pass"
            message = f"Duplicate workflow creation for '{duplicate_name}' was blocked as expected."
            action_factory.helpers.attach_screenshot(name="DuplicateWorkflowErrorPass")
            action_factory.helpers.attach_allure(name="Duplicate Workflow Naming", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Duplicate workflow name '{duplicate_name}' was not blocked."
            action_factory.helpers.attach_screenshot(name="DuplicateWorkflowErrorFailed")
            action_factory.helpers.attach_allure(name="Duplicate Workflow Naming", text=message)
            assert False, message

        # Cancel duplicate creation popup
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.close_btn)
        action_factory.ui_utils.smart_wait()

        # Attempt to create workflow with Special Characters
        action_factory.workflows_actions.create_workflow(workflow_name=special_char_name, description=special_char_workflow_description)
        action_factory.ui_utils.smart_wait()
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name, position=0)
        action_factory.ui_utils.smart_wait()

        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="review", node_index1=1, position1="right", index1=2,
            node_Name2="annotate", node_index2=1, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()
        special_error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.workflow_invalid_name_error)
        print(f"Special character workflow name error visibility: {special_error_visible}")

        if special_error_visible:
            status = "Pass"
            message = f"Special character workflow creation for '{special_char_name}' was blocked as expected."
            action_factory.helpers.attach_screenshot(name="SpecialCharWorkflowErrorPass")
            action_factory.helpers.attach_allure(name="Special Character Workflow Naming", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Special character workflow name '{special_char_name}' was not blocked."
            action_factory.helpers.attach_screenshot(name="SpecialCharWorkflowErrorFailed")
            action_factory.helpers.attach_allure(name="Special Character Workflow Naming", text=message)
            assert False, message

        # Cancel special character creation popup
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.close_btn)
        action_factory.ui_utils.smart_wait()

        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        workflow_name = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        print(f"Workflow name: {workflow_name}")
        if special_char_name not in workflow_name:
            status = "Pass"
            message = f"Special character workflow name '{special_char_name}' was successfully deleted."
            action_factory.helpers.attach_screenshot(name="SpecialCharWorkflowErrorPass")
            action_factory.helpers.attach_allure(name="Duplicate Workflow Naming", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Duplicate workflow name '{special_char_name}' was not deleted."
            action_factory.helpers.attach_screenshot(name="DuplicateWorkflowErrorFailed")
            action_factory.helpers.attach_allure(name="Duplicate Workflow Naming", text=message)
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
