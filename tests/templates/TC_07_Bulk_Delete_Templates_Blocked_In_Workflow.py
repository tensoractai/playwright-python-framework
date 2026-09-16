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
@allure.story("Bulk Delete Templates Blocked When Used in Workflow")
@allure.title("Verify bulk deletion prevention when templates are configured in workflow annotate nodes")
def test_bulk_delete_templates_blocked_in_workflow(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each

        template1 = test_data_inputs.bulk_prevent_template_1
        template2 = test_data_inputs.bulk_prevent_template_2
        workflow_name = test_data_inputs.bulk_prevent_workflow_name
        nodes_list = test_data_inputs.bulk_prevent_node_list
        description = test_data_inputs.valid_template_description
        template_files = test_data_inputs.text_template_file

        # Click Template menu and create 2 templates
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.upload_new_template(template_name=template1, description=description)
        action_factory.templates_actions.upload_template_files(template_files)
        action_factory.ui_utils.smart_wait()

        action_factory.templates_actions.upload_new_template(template_name=template2, description=description)
        action_factory.templates_actions.upload_template_files(template_files)
        action_factory.ui_utils.smart_wait()
        template_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        if template1 in template_list and template2 in template_list:
            status = "Pass"
            message = f"Templates '{template1}' and '{template2}' were uploaded successfully."
            action_factory.helpers.attach_screenshot(name="TemplatesUploadedSuccessfully")
            action_factory.helpers.attach_allure(name="Bulk Delete Templates Blocked", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Templates '{template1}' and '{template2}' were not found in the template list."
            action_factory.helpers.attach_screenshot(name="TemplatesNotFoundInList")
            action_factory.helpers.attach_allure(name="Bulk Delete Templates Blocked", text=message)
            assert False, message

        # Navigate to Workflows and create workflow with nodes [Start, Annotate, Review, Annotate, Review, Complete]
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description="Workflow for testing bulk template deletion prevention")
        action_factory.ui_utils.smart_wait()
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        # Configure Template 1 on Annotate Node 1 and Template 2 on Annotate Node 2
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template1, position=0)
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template2, position=0)
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.nodes_connection_flow(node_Name1="review", node_index1=1, position1="right", index1=2,
                                                             node_Name2="annotate", node_index2=1, position2="left", index2=1)
        action_factory.workflows_actions.nodes_connection_flow(node_Name1="review", node_index1=2, position1="right", index1=2,
                                                             node_Name2="annotate", node_index2=2, position2="left", index2=1)
        # Save the workflow
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

        # Navigate back to Templates menu and attempt to bulk delete both templates
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.delete_template([template1, template2])
        action_factory.ui_utils.smart_wait()

        # Validate error message indicating templates cannot be deleted
        delete_failed_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.templates_page.template_delete_failed_msg)
        if delete_failed_visible:
            status = "Pass"
            message = "Bulk template deletion correctly failed with 'Failed Deleted Template' message as expected."
            action_factory.helpers.attach_screenshot(name="BulkTemplateDeletionBlockedMsgVisible")
            action_factory.helpers.attach_allure(name="Bulk Delete Templates Blocked", text=message)
            assert True, message
        else:
            status = "Fail"
            message = "Error message was not displayed when attempting bulk deletion of templates configured in workflow."
            action_factory.helpers.attach_screenshot(name="BulkTemplateDeletionBlockedMsgNotVisible")
            action_factory.helpers.attach_allure(name="Bulk Delete Templates Blocked", text=message)
            assert False, message

        # Cancel the popup and validate both templates are still present in the template list
        action_factory.ui_utils.click_element(action_factory.page_factory.files_page.cancel_popup)
        action_factory.ui_utils.smart_wait()

        template_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        if template1 in template_list and template2 in template_list:
            status = "Pass"
            message = f"Both templates '{template1}' and '{template2}' were retained in the template list as expected."
            action_factory.helpers.attach_screenshot(name="BothTemplatesRetainedInList")
            action_factory.helpers.attach_allure(name="Bulk Delete Templates Blocked", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"One or both templates ('{template1}', '{template2}') were unexpectedly removed from the template list."
            action_factory.helpers.attach_screenshot(name="TemplatesNotRetainedInList")
            action_factory.helpers.attach_allure(name="Bulk Delete Templates Blocked", text=message)
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
