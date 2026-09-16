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
@allure.story("Workflows Pagination Check")
@allure.title("Verify workflows pagination control for limits 5, 10, 20, and 50 with creation and tab switching persistence")
def test_workflows_pagination(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        template_name = "AUT_WF_Template_17"
        workflow_name = test_data_inputs.pagination_workflow_name
        description = test_data_inputs.description
        template_file = test_data_inputs.valid_template_file
        nodes_list = ["Start", "Annotate", "Review", "Complete"]

        # Click Workflows menu
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()

        # Check pagination for 5
        action_factory.workflows_actions.set_workflows_pagination("5")
        workflow_count = action_factory.page_factory.workflows_page.workflow_names_list.count()
        if workflow_count <= 5:
            status = "Pass"
            message = f"Workflow count ({workflow_count}) is within limit for pagination 5."
            action_factory.helpers.attach_screenshot(name="WorkflowsPagination5Pass")
            action_factory.helpers.attach_allure(name="Workflows Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow count ({workflow_count}) exceeds limit of 5."
            action_factory.helpers.attach_screenshot(name="WorkflowsPagination5Failed")
            action_factory.helpers.attach_allure(name="Workflows Pagination Check", text=message)
            assert False, message

        # Create Template
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Create Workflow after setting pagination 5
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

        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        workflow_count_after_create = action_factory.page_factory.workflows_page.workflow_names_list.count()
        if workflow_count_after_create <= 5:
            status = "Pass"
            message = f"Workflow count ({workflow_count_after_create}) remains <= 5 after creating a new workflow."
            action_factory.helpers.attach_screenshot(name="PaginationPreservedAfterWorkflowCreation")
            action_factory.helpers.attach_allure(name="Workflows Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow count ({workflow_count_after_create}) exceeded limit of 5 after workflow creation."
            action_factory.helpers.attach_screenshot(name="PaginationNotPreservedAfterCreation")
            action_factory.helpers.attach_allure(name="Workflows Pagination Check", text=message)
            assert False, message

        # Switch to Datasets menu and come back to Workflows page
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()

        workflow_count_after_switch = action_factory.page_factory.workflows_page.workflow_names_list.count()
        if workflow_count_after_switch <= 5:
            status = "Pass"
            message = f"Workflow count ({workflow_count_after_switch}) remains <= 5 after switching menu and returning."
            action_factory.helpers.attach_screenshot(name="PaginationPreservedAfterMenuSwitch")
            action_factory.helpers.attach_allure(name="Workflows Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow count ({workflow_count_after_switch}) exceeded limit of 5 after menu switch."
            action_factory.helpers.attach_screenshot(name="PaginationNotPreservedAfterSwitch")
            action_factory.helpers.attach_allure(name="Workflows Pagination Check", text=message)
            assert False, message

        # Check pagination for 10
        action_factory.workflows_actions.set_workflows_pagination("10")
        workflow_count = action_factory.page_factory.workflows_page.workflow_names_list.count()
        if workflow_count <= 10:
            status = "Pass"
            message = f"Workflow count ({workflow_count}) is within limit for pagination 10."
            action_factory.helpers.attach_screenshot(name="WorkflowsPagination10Pass")
            action_factory.helpers.attach_allure(name="Workflows Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow count ({workflow_count}) exceeds limit of 10."
            action_factory.helpers.attach_screenshot(name="WorkflowsPagination10Failed")
            action_factory.helpers.attach_allure(name="Workflows Pagination Check", text=message)
            assert False, message

        # Check pagination for 20
        action_factory.workflows_actions.set_workflows_pagination("20")
        workflow_count = action_factory.page_factory.workflows_page.workflow_names_list.count()
        if workflow_count <= 20:
            status = "Pass"
            message = f"Workflow count ({workflow_count}) is within limit for pagination 20."
            action_factory.helpers.attach_screenshot(name="WorkflowsPagination20Pass")
            action_factory.helpers.attach_allure(name="Workflows Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow count ({workflow_count}) exceeds limit of 20."
            action_factory.helpers.attach_screenshot(name="WorkflowsPagination20Failed")
            action_factory.helpers.attach_allure(name="Workflows Pagination Check", text=message)
            assert False, message

        # Check pagination for 50
        action_factory.workflows_actions.set_workflows_pagination("50")
        workflow_count = action_factory.page_factory.workflows_page.workflow_names_list.count()
        if workflow_count <= 50:
            status = "Pass"
            message = f"Workflow count ({workflow_count}) is within limit for pagination 50."
            action_factory.helpers.attach_screenshot(name="WorkflowsPagination50Pass")
            action_factory.helpers.attach_allure(name="Workflows Pagination Check", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow count ({workflow_count}) exceeds limit of 50."
            action_factory.helpers.attach_screenshot(name="WorkflowsPagination50Failed")
            action_factory.helpers.attach_allure(name="Workflows Pagination Check", text=message)
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
