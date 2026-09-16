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
@allure.story("Search Workflow Names")
@allure.title("Verify searching existing workflow returns correct results and non-existing search shows no workflows message")
def test_search_workflow_names(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        template_name = "AUT_WF_Template_13"
        workflow_name = test_data_inputs.search_workflow_name
        non_existing_name = test_data_inputs.non_existing_workflow_name
        description = test_data_inputs.description
        template_file = test_data_inputs.valid_template_file
        nodes_list = ["Start", "Annotate", "Review", "Complete"]

        # Create Template
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Create Workflow to search
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description=description)
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
        workflow_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        if workflow_name in workflow_name_list:
            status = "Pass"
            message = f"Workflow name '{workflow_name}' was successfully created."
            action_factory.helpers.attach_screenshot(name="WorkflowCreatedPass")
            action_factory.helpers.attach_allure(name="Workflow Created", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow name '{workflow_name}' was not created."
            action_factory.helpers.attach_screenshot(name="WorkflowCreatedFailed")
            action_factory.helpers.attach_allure(name="Workflow Created", text=message)
            assert False, message

        # Search existing workflow name
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.search_workflow_name(workflow_name)
        action_factory.ui_utils.smart_wait()

        search_results = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        print(f"Search results for '{workflow_name}': {search_results}")

        if workflow_name in search_results:
            status = "Pass"
            message = f"Search returned expected workflow '{workflow_name}'."
            action_factory.helpers.attach_screenshot(name="SearchWorkflowPass")
            action_factory.helpers.attach_allure(name="Search Workflow Names", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Search failed to return expected workflow '{workflow_name}'."
            action_factory.helpers.attach_screenshot(name="SearchWorkflowFailed")
            action_factory.helpers.attach_allure(name="Search Workflow Names", text=message)
            assert False, message

        # Search non-existing workflow name
        action_factory.workflows_actions.search_workflow_name(non_existing_name)
        action_factory.ui_utils.smart_wait()

        no_workflows_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.no_workflows_found)
        non_existing_results = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        print(f"Search results for non-existing workflow '{non_existing_name}': {non_existing_results}")

        if no_workflows_visible and non_existing_name not in non_existing_results:
            status = "Pass"
            message = f"Non-existing workflow search for '{non_existing_name}' correctly returned no results."
            action_factory.helpers.attach_screenshot(name="NonExistingWorkflowSearchPass")
            action_factory.helpers.attach_allure(name="Search Workflow Names", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Non-existing workflow search for '{non_existing_name}' returned unexpected results."
            action_factory.helpers.attach_screenshot(name="NonExistingWorkflowSearchFailed")
            action_factory.helpers.attach_allure(name="Search Workflow Names", text=message)
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
