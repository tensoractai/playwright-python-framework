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
@allure.story("Create Workflow with Annotation & Review Radio Option")
@allure.title("Verify creating a workflow using Annotation & Review radio selection, applying template and saving")
def test_create_workflow_annotation_and_review_radio(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        template_name = test_data_inputs.common_template_name_A
        workflow_name = "AUT_WF_Ann_Rev_Radio"
        description = test_data_inputs.description

        # Open Workflows Menu and click Create Workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.create_workflow_btn)
        action_factory.ui_utils.smart_wait()

        # Fill workflow details and select Annotation & Review radio button
        action_factory.ui_utils.fill_input(action_factory.page_factory.workflows_page.enter_workflow_name_input, workflow_name)
        action_factory.ui_utils.fill_input(action_factory.page_factory.workflows_page.description_input, description)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.annotators_review)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.next_button)
        action_factory.ui_utils.smart_wait()

        # Adjust view and apply template
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name, position=0)
        action_factory.ui_utils.smart_wait()

        # Save Workflow
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

        # Validate Workflow Presence
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        workflow_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)
        if workflow_name in workflow_list:
            status = "Pass"
            message = f"Workflow '{workflow_name}' created with Annotation & Review radio button applied successfully."
            action_factory.helpers.attach_screenshot(name="WorkflowAnnRevRadioPass")
            action_factory.helpers.attach_allure(name="Annotation & Review Workflow Creation", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_name}' not found after creation."
            action_factory.helpers.attach_screenshot(name="WorkflowAnnRevRadioFailed")
            action_factory.helpers.attach_allure(name="Annotation & Review Workflow Creation", text=message)
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
