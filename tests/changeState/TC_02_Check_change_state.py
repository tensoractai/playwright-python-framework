import allure
import pytest
from actions.action_factory import ActionFactory
from tests.changeState.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    password = action_factory.helpers.fetch_dotenv("company_Password")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
    diff_email = action_factory.helpers.fetch_dotenv("MICROSOFT_OTP_EMAIL")
    # Login as Admin
    action_factory.login_actions.perform_login(
        url=url,
        email=email,
        password=password
    )
    action_factory.login_actions.use_different_email_OTP(diff_email)
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("Change State")
@allure.story("Check Change State Flow - Annotator Bounding Box and Reviewer Reject")
@allure.title("Create project with 2 image files, annotate using bounding box, move to Review 2, and reject as Reviewer")
def test_change_state_flow_02(before_each):
    status = "Fail"
    message = ""
    try: 
        action_factory = before_each
        Dataset_Name = test_data_inputs.Dataset_changeState_02
        Dataset_Type = test_data_inputs.Dataset_changeState_Type_02        
        Dataset_Files = test_data_inputs.Dataset_Files_02
        Template_Name = test_data_inputs.Template_changeState_02
        Template_Image = test_data_inputs.Template_Image_02
        workflow_Name = test_data_inputs.workflow_Name_02
        workflow_Nodes = test_data_inputs.workflow_Nodes_02
        project_Name = test_data_inputs.project_Name_02
        
        url = action_factory.helpers.fetch_dotenv("Execution_url")
        company_Name = action_factory.helpers.fetch_dotenv("company_Name")
        diff_email = action_factory.helpers.fetch_dotenv("MICROSOFT_OTP_EMAIL")
        annotator_email = action_factory.helpers.fetch_dotenv("annotator_Username")
        annotator_password = action_factory.helpers.fetch_dotenv("annotator_Password")
        reviewer_email = action_factory.helpers.fetch_dotenv("reviewer_Username")
        reviewer_password = action_factory.helpers.fetch_dotenv("reviewer_Password")

        # 1. Dataset Creation Functionality
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.create_dataset(dataset_name=Dataset_Name, dataset_type_name=Dataset_Type)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(Dataset_Name))
        action_factory.datasets_actions.upload_files_with_uploadBtn(*Dataset_Files)
        action_factory.common_actions.validate_toast_msg("2 files added")
        action_factory.ui_utils.smart_wait()
        files_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_inside_file_name_list)
        print(f"Files names list: {files_name_list}")

        expected_files = [file.split("/")[-1] for file in Dataset_Files]
        if all(file in files_name_list for file in expected_files):
            status = "Pass"
            message = f"All files uploaded successfully for dataset '{Dataset_Name}'."
            action_factory.helpers.attach_screenshot(name="FilesUploaded")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files))
            assert True, message
        else:
            status = "Fail"
            message = f"Failed to upload all files for dataset '{Dataset_Name}'."
            action_factory.helpers.attach_screenshot(name="FilesUploadFailed")
            action_factory.helpers.attach_allure(name="Uploaded Files", text=", ".join(expected_files))
            assert False, message

        # 2. Template Creation Functionality
        action_factory.templates_actions.click_templates_menu()
        action_factory.templates_actions.upload_new_template(template_name=Template_Name)
        action_factory.templates_actions.upload_template_files(*Template_Image)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.templates_page.template_names_list.nth(0))
        template_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.templates_page.template_names_list)
        print(f"Template names list: {template_name_list}")
        if Template_Name in template_name_list:
            status = "Pass"
            message = f"Template '{Template_Name}' created successfully."
            action_factory.helpers.attach_screenshot(name="TemplateCreated")
            action_factory.helpers.attach_allure(name="Template Name", text=Template_Name)
            assert True, message
        else:
            status = "Fail"
            message = f"Template '{Template_Name}' creation failed."
            action_factory.helpers.attach_screenshot(name="TemplateCreationFailed")
            action_factory.helpers.attach_allure(name="Template Name", text=Template_Name)
            assert False, message

        # 3. Workflow Creation Functionality
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_Name, description="Test workflow for automation")
        action_factory.ui_utils.smart_wait()
        for node in workflow_Nodes:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=Template_Name, position=0)
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.apply_template_to_annotate(template_name=Template_Name, position=0)
        action_factory.ui_utils.smart_wait()
        template_applied = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.template_applied_name)
        if Template_Name in template_applied:
            status = "Pass"
            message = f"Workflow '{workflow_Name}' created successfully with template applied."
            action_factory.helpers.attach_screenshot(name="WorkflowCreated")
            action_factory.helpers.attach_allure(name="Workflow Name", text=workflow_Name)
            assert True, message
        else:
            status = "Fail"
            message = f"Workflow '{workflow_Name}' creation failed."
            action_factory.helpers.attach_screenshot(name="WorkflowCreationFailed")
            action_factory.helpers.attach_allure(name="Workflow Name", text=workflow_Name)
            assert False, message
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.nodes_connection_flow(node_Name1="review", node_index1=1, position1="right", index1=2,
                                                             node_Name2="annotate", node_index2=1, position2="left", index2=1)
        action_factory.workflows_actions.nodes_connection_flow(node_Name1="review", node_index1=2, position1="right", index1=2,
                                                             node_Name2="annotate", node_index2=2, position2="left", index2=1)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

        # 4. Projects Creation & User Addition Functionality
        action_factory.projects_actions.click_project_menu()
        action_factory.projects_actions.create_project(project_Name, Dataset_Type, Dataset_Name, workflow_Name)
        action_factory.ui_utils.smart_wait()
        project_name_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.project_names_list)
        if project_Name in project_name_list:
            status = "Pass"
            message = f"Project '{project_Name}' created successfully."
            action_factory.helpers.attach_screenshot(name="Project Created")
            action_factory.helpers.attach_allure(name="Project Name", text=project_Name)
            assert True, message
        else:
            status = "Fail"
            message = f"Project '{project_Name}' creation failed."
            action_factory.helpers.attach_screenshot(name="Project Creation Failed")
            action_factory.helpers.attach_allure(name="Project Name", text=project_Name)
            assert False, message

        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_Name))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.projects_page.task_panel, timeout=10000)
        action_factory.projects_actions.click_teams_tab()
        action_factory.projects_actions.add_users(role="Annotator", email_address=annotator_email)
        action_factory.projects_actions.add_users(role="Reviewer", email_address=reviewer_email)
        action_factory.ui_utils.smart_wait()
        assigners_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.assigners_list)
        if annotator_email in assigners_list and reviewer_email in assigners_list:
            status = "Pass"
            message = "Annotator and Reviewer added successfully."
            action_factory.helpers.attach_screenshot(name="Annotator and Reviewer Added")
            action_factory.helpers.attach_allure(name="Assigner List", text="Passed")
            assert True, message
        else:
            status = "Fail"
            message = "Annotator and Reviewer not added."
            action_factory.helpers.attach_screenshot(name="Annotator and Reviewer Not Added")
            action_factory.helpers.attach_allure(name="Assigner List", text="Failed")
            assert False, message

        # 5. Open new browser context for Annotator (Keep existing Admin browser open)
        annotator_context = action_factory.page.context.browser.new_context()
        annotator_page = annotator_context.new_page()
        annotator_action_factory = ActionFactory(annotator_page)

        # Login as Annotator
        annotator_action_factory.login_actions.perform_login(url=url, email=annotator_email, password=annotator_password)
        annotator_action_factory.login_actions.use_different_email_OTP(diff_email)
        annotator_action_factory.login_actions.select_organization(company_Name, "Annotator")
        annotator_action_factory.ui_utils.smart_wait()

        # Open Tasks menu and click project
        annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.tasks_menu)
        annotator_action_factory.ui_utils.smart_wait()
        annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.click_project_name(project_Name))
        annotator_action_factory.ui_utils.smart_wait()

        # Annotate image files using bounding box function and submit
        for target_file in expected_files:
            annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.click_project_name(target_file))
            annotator_action_factory.ui_utils.smart_wait()
            claim_visible = annotator_action_factory.ui_utils.wait_for_visible_if_exists(
                annotator_action_factory.page_factory.annotator_page.claim_button, timeout=5000
            )
            if claim_visible:
                annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.claim_button)
                annotator_action_factory.ui_utils.smart_wait()

            annotator_action_factory.reviewer_actions.wait_for_iframe_ready()
            # Draw bounding box annotation
            annotator_action_factory.annotator_actions.draw_bounding_box((50, 50), (200, 200))
            annotator_action_factory.ui_utils.smart_wait()

            # Submit Annotation Task
            annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.submit_annotation)
            annotator_action_factory.ui_utils.smart_wait()
            claim_after = annotator_action_factory.ui_utils.wait_for_visible_if_exists(
                annotator_action_factory.page_factory.annotator_page.claim_button, timeout=5000
            )
            if claim_after:
                annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.back_button)
                annotator_action_factory.ui_utils.smart_wait()

        # 6. Bring Admin screen front and move tasks to Review 2
        action_factory.page.bring_to_front()
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.task_panel)
        action_factory.ui_utils.smart_wait()

        for file_name in expected_files:
            target_fname = file_name if isinstance(file_name, str) else file_name[0]
            action_factory.projects_actions.changeStatus_ofProject(target_fname, "Review 2")
            action_factory.ui_utils.smart_wait()

        # 7. Open new browser context for Reviewer, login, and reject the file
        reviewer_context = action_factory.page.context.browser.new_context()
        reviewer_page = reviewer_context.new_page()
        reviewer_action_factory = ActionFactory(reviewer_page)

        reviewer_action_factory.login_actions.perform_login(url=url, email=reviewer_email, password=reviewer_password)
        reviewer_action_factory.login_actions.use_different_email_OTP(diff_email)
        reviewer_action_factory.login_actions.select_organization(company_Name, "Reviewer")
        reviewer_action_factory.ui_utils.smart_wait()

        reviewer_action_factory.ui_utils.click_element(reviewer_action_factory.page_factory.reviewer_page.tasks_menu)
        reviewer_action_factory.ui_utils.smart_wait()
        reviewer_action_factory.ui_utils.click_element(reviewer_action_factory.page_factory.reviewer_page.click_project_name(project_Name))
        reviewer_action_factory.ui_utils.smart_wait()

        for target_file in expected_files:
            reviewer_action_factory.ui_utils.click_element(reviewer_action_factory.page_factory.reviewer_page.click_project_name(target_file))
            reviewer_action_factory.ui_utils.smart_wait()
            claim_visible = reviewer_action_factory.ui_utils.wait_for_visible_if_exists(
                reviewer_action_factory.page_factory.reviewer_page.claim_button, timeout=5000
            )
            if claim_visible:
                reviewer_action_factory.ui_utils.click_element(reviewer_action_factory.page_factory.reviewer_page.claim_button)
                reviewer_action_factory.ui_utils.smart_wait()

            reviewer_action_factory.reviewer_actions.wait_for_iframe_ready()
            reviewer_action_factory.ui_utils.click_element(reviewer_action_factory.page_factory.reviewer_page.reject_button)
            reviewer_action_factory.ui_utils.click_element(reviewer_action_factory.page_factory.reviewer_page.submit_button)
            reviewer_action_factory.ui_utils.smart_wait()
            claim_after = reviewer_action_factory.ui_utils.wait_for_visible_if_exists(
                reviewer_action_factory.page_factory.reviewer_page.claim_button, timeout=5000
            )
            if claim_after:
                reviewer_action_factory.ui_utils.click_element(reviewer_action_factory.page_factory.reviewer_page.back_button)
                reviewer_action_factory.ui_utils.smart_wait()

        status = "Pass"
        message = "Annotations completed, stage moved to Review 2, and file rejected successfully by Reviewer."
        action_factory.helpers.attach_screenshot(name="TC02_Success")
        action_factory.helpers.attach_allure(name="Test Summary", text=message)
        assert True, message

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
