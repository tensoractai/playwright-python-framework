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
@allure.story("Annotation & Review Incomplete Workflow Save Validation")
@allure.title("Verify creating workflow with Annotation & Review radio selection without completing connections prevents workflow creation")
def test_annotation_review_incomplete_save(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        template_name = test_data_inputs.linked_delete_template_name
        workflow_name = test_data_inputs.tc28_workflow_name
        description = test_data_inputs.tc28_description

        # Create Workflow with Annotation & Review selection
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.create_workflow_btn)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.fill_input(action_factory.page_factory.workflows_page.enter_workflow_name_input, workflow_name)
        action_factory.ui_utils.fill_input(action_factory.page_factory.workflows_page.description_input, description)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.annotators_review)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.next_button)
        action_factory.ui_utils.smart_wait()

        # Apply template to Annotate node without connecting nodes
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name, position=0)
        action_factory.ui_utils.smart_wait()

        # Attempt to Save
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

        # Navigate to Workflows list and validate workflow is NOT created
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()

        workflow_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        print(f"Workflows list: {workflow_list}")

        if workflow_name not in workflow_list:
            status = "Pass"
            message = f"DB Query Names created in DB '{workflow_name}' was correctly blocked from being created."
            action_factory.helpers.attach_screenshot(name="DB Query Names not created in DB")
            action_factory.helpers.attach_allure(name="DB Query Names not created in DB", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"DB Query Names not created in DB '{workflow_name}' was not created in the workflows list."
            action_factory.helpers.attach_screenshot(name="DB Query Names not created in DB")
            action_factory.helpers.attach_allure(name="DB Query Names not created in DB", text=message)
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
