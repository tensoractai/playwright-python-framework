import allure
import pytest
from actions.action_factory import ActionFactory
from tests.changeState.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    action_factory.helpers._screenshot_failures.clear()
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
@allure.story("Check Change State Flow - 1 Annotator, 2 Reviewers with Save & Exit and Rejections")
@allure.title("Complete multi-stage save & exit, state transition, edit, delete, and validation flow")
def test_change_state_oneAnn_TwoRev_OnlySave(before_each):
    status = "Fail"
    message = ""
    action_factory = before_each
    active_action_factory = action_factory
    try: 
        # Project Creation Step :
        # 1. Dataset Creation Functionality
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()

        dataset_names_list = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.datasets_page.dataset_names_list)
        i = action_factory.helpers.resolve_next_index(dataset_names_list, test_data_inputs.Dataset_changeState_03)

        Dataset_Name = test_data_inputs.Dataset_changeState_03.format(i=i) if "{i}" in test_data_inputs.Dataset_changeState_03 else test_data_inputs.Dataset_changeState_03
        Dataset_Type = test_data_inputs.Dataset_changeState_Type_03        
        Dataset_Files = test_data_inputs.Dataset_Files_03
        Template_Name = test_data_inputs.Template_changeState_03.format(i=i) if "{i}" in test_data_inputs.Template_changeState_03 else test_data_inputs.Template_changeState_03
        Template_Image = test_data_inputs.Template_Image_03
        workflow_Name = test_data_inputs.workflow_Name_03.format(i=i) if "{i}" in test_data_inputs.workflow_Name_03 else test_data_inputs.workflow_Name_03
        workflow_Nodes = test_data_inputs.workflow_Nodes_03
        project_Name = test_data_inputs.project_Name_03.format(i=i) if "{i}" in test_data_inputs.project_Name_03 else test_data_inputs.project_Name_03
        
        url = action_factory.helpers.fetch_dotenv("Execution_url")
        company_Name = action_factory.helpers.fetch_dotenv("company_Name")
        diff_email = action_factory.helpers.fetch_dotenv("MICROSOFT_OTP_EMAIL")
        annotator_email = action_factory.helpers.fetch_dotenv("annotator_Username")
        annotator_password = action_factory.helpers.fetch_dotenv("annotator_Password")
        reviewer_email = action_factory.helpers.fetch_dotenv("reviewer_Username")
        reviewer_password = action_factory.helpers.fetch_dotenv("reviewer_Password")

        action_factory.datasets_actions.create_dataset(dataset_name=Dataset_Name, dataset_type_name=Dataset_Type)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(Dataset_Name))
        action_factory.datasets_actions.upload_files_with_uploadBtn(*Dataset_Files)
        action_factory.common_actions.validate_toast_msg("1 file added")
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
        action_factory.ui_utils.element_wait_for(action_factory.page_factory.templates_page.template_names_list.nth(0), timeout=3000)
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
        for node in workflow_Nodes:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
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
        action_factory.workflows_actions.nodes_connection_flow(node_Name1="review", node_index1=1, position1="right", index1=2,
                                                             node_Name2="annotate", node_index2=1, position2="left", index2=1)
        action_factory.workflows_actions.nodes_connection_flow(node_Name1="review", node_index1=2, position1="right", index1=2,
                                                             node_Name2="annotate", node_index2=1, position2="left", index2=1)
        save_btn = action_factory.page_factory.workflows_page.save_btn
        action_factory.ui_utils.click_element(save_btn)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.element_wait_for(save_btn, state="hidden", timeout=20000)

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
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_Name))
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
        
        #......................................................................................................................
        # Step 1: Annotator Claim Task, Drop 1 Segment (Person), and Save and Exit :
        annotator_context = action_factory.page.context.browser.new_context()
        annotator_page = annotator_context.new_page()
        annotator_action_factory = ActionFactory(annotator_page)
        active_action_factory = annotator_action_factory
        annotator_action_factory.login_actions.perform_login(url=url, email=annotator_email, password=annotator_password)
        annotator_action_factory.login_actions.use_different_email_OTP(diff_email)
        annotator_action_factory.login_actions.select_organization(company_Name, "Annotator")
        annotator_action_factory.ui_utils.smart_wait()

        # Open Tasks menu and click project
        annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.tasks_menu)
        annotator_action_factory.ui_utils.smart_wait()
        annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.click_project_name(project_Name))
        annotator_action_factory.ui_utils.smart_wait()

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
            annotator_action_factory.annotator_actions.perform_annotation_for_image_files("Person", (180, 230), (180, 470))
            annotator_action_factory.ui_utils.smart_wait()
            annotator_action_factory.helpers.compare_screenshot(name=f"01_Annotator_{target_file}_SaveAndExit_Annotate1", locator=annotator_action_factory.page_factory.annotator_page.main_video_image)

            # Save and Exit
            annotator_action_factory.annotator_actions.perform_save_exit()
            annotator_action_factory.ui_utils.smart_wait()
            claim_after = annotator_action_factory.ui_utils.wait_for_visible_if_exists(
                annotator_action_factory.page_factory.annotator_page.claim_button, timeout=5000
            )
            if claim_after:
                annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.back_button)
                annotator_action_factory.ui_utils.smart_wait()

        #......................................................................................................................
        # Step 2: Company Admin Changes State to Review 1 :
        action_factory.page.bring_to_front()
        active_action_factory = action_factory
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.task_panel)
        action_factory.ui_utils.smart_wait()

        for file_name in expected_files:
            target_fname = file_name if isinstance(file_name, str) else file_name[0]
            action_factory.projects_actions.changeStatus_ofProject(target_fname, "Review 1")
            action_factory.ui_utils.smart_wait()
            status_after = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.get_file_status(target_fname))
            if "Review 1" in status_after:
                status = "Pass"
                message = f"File '{target_fname}' status changed successfully to Review 1."
                action_factory.helpers.attach_screenshot(name="File Status Changed to Review 1")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert True, message
            else:
                status = "Fail"
                message = f"File '{target_fname}' status not changed to Review 1."
                action_factory.helpers.attach_screenshot(name="File Status Not Changed to Review 1")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert False, message

        #......................................................................................................................
        # Step 3: Login as Reviewer 1, Drop 1 Segment (Bicycle), and Reject the Task :
        reviewer_context = action_factory.page.context.browser.new_context()
        reviewer_page = reviewer_context.new_page()
        reviewer_action_factory = ActionFactory(reviewer_page)
        active_action_factory = reviewer_action_factory

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
            reviewer_action_factory.annotator_actions.perform_annotation_for_image_files("Bicycle", (260, 230), (260, 470))
            reviewer_action_factory.ui_utils.smart_wait()
            reviewer_action_factory.helpers.compare_screenshot(name=f"02_Reviewer1_{target_file}_Drop1_Segment_Reject", locator=reviewer_action_factory.page_factory.annotator_page.main_video_image)

            # Reject task with feedback comments
            reviewer_action_factory.reviewer_actions.reject_task("Need Correction")
            claim_after = reviewer_action_factory.ui_utils.wait_for_visible_if_exists(
                reviewer_action_factory.page_factory.reviewer_page.claim_button, timeout=5000
            )
            if claim_after:
                reviewer_action_factory.ui_utils.click_element(reviewer_action_factory.page_factory.reviewer_page.back_button)
                reviewer_action_factory.ui_utils.smart_wait()

        #......................................................................................................................
        # Step 4: Login as Annotator, Drop 1 More Segment (Motorcycle), and Save and Exit :
        annotator_page.bring_to_front()
        active_action_factory = annotator_action_factory
        annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.home_menu)
        annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.tasks_menu)
        annotator_action_factory.ui_utils.smart_wait()
        annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.click_project_name(project_Name))
        annotator_action_factory.ui_utils.smart_wait()

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

            # Check feedback comments if visible
            feedback_comment = annotator_action_factory.page_factory.annotator_page.get_feedback_comment("Need Correction")
            is_feedback_visible = annotator_action_factory.ui_utils.wait_for_visible_if_exists(feedback_comment, timeout=3000)
            if is_feedback_visible:
                annotator_action_factory.ui_utils.click_element(feedback_comment)
                close_btn = annotator_action_factory.page_factory.annotator_page.close_button
                if annotator_action_factory.ui_utils.is_element_visible(close_btn, timeout=3000):
                    annotator_action_factory.ui_utils.click_element(close_btn)
                annotator_action_factory.ui_utils.smart_wait()

            # Drop 1 more segment (Motorcycle)
            annotator_action_factory.annotator_actions.perform_annotation_for_image_files("Motorcycle", (340, 230), (340, 470))
            annotator_action_factory.ui_utils.smart_wait()
            annotator_action_factory.helpers.compare_screenshot(name=f"03_Annotator_{target_file}_SaveAndExit_Annotate2", locator=annotator_action_factory.page_factory.annotator_page.main_video_image)

            # Save and Exit
            annotator_action_factory.annotator_actions.perform_save_exit()
            annotator_action_factory.ui_utils.smart_wait()
            claim_after = annotator_action_factory.ui_utils.wait_for_visible_if_exists(
                annotator_action_factory.page_factory.annotator_page.claim_button, timeout=5000
            )
            if claim_after:
                annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.back_button)
                annotator_action_factory.ui_utils.smart_wait()

        #......................................................................................................................
        # Step 5: Company Admin Changes State to Review 1 :
        action_factory.page.bring_to_front()
        active_action_factory = action_factory
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.task_panel)
        action_factory.ui_utils.smart_wait()

        for file_name in expected_files:
            target_fname = file_name if isinstance(file_name, str) else file_name[0]
            action_factory.projects_actions.changeStatus_ofProject(target_fname, "Review 1")
            action_factory.ui_utils.smart_wait()
            status_after = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.get_file_status(target_fname))
            if "Review 1" in status_after:
                status = "Pass"
                message = f"File '{target_fname}' status changed successfully to Review 1."
                action_factory.helpers.attach_screenshot(name="File Status Changed to Review 1 Second Time")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert True, message
            else:
                status = "Fail"
                message = f"File '{target_fname}' status not changed to Review 1."
                action_factory.helpers.attach_screenshot(name="File Status Not Changed to Review 1 Second Time")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert False, message

        #......................................................................................................................
        # Step 6: Reviewer 1 Drops 1 Segment (Truck), Edits Annotator Segment (Person), and Save and Exit :
        reviewer_page.bring_to_front()
        active_action_factory = reviewer_action_factory
        reviewer_action_factory.ui_utils.click_element(reviewer_action_factory.page_factory.reviewer_page.home_menu)
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

            # Drop 1 Segment (Truck)
            reviewer_action_factory.annotator_actions.perform_annotation_for_image_files("Truck", (580, 80), (790, 80))
            reviewer_action_factory.ui_utils.smart_wait()

            # Edit Annotator segment (Person)
            reviewer_action_factory.annotator_actions.edit_old_annotation("Person", from_coords=(180, 470), to_coords=(20, 470))
            reviewer_action_factory.ui_utils.smart_wait()
            reviewer_action_factory.helpers.compare_screenshot(name=f"04_Reviewer1_{target_file}_Edited_Segment_Reject", locator=reviewer_action_factory.page_factory.annotator_page.main_video_image)

            # Save and Exit
            reviewer_action_factory.annotator_actions.perform_save_exit()
            reviewer_action_factory.ui_utils.smart_wait()
            claim_after = reviewer_action_factory.ui_utils.wait_for_visible_if_exists(
                reviewer_action_factory.page_factory.reviewer_page.claim_button, timeout=5000
            )
            if claim_after:
                reviewer_action_factory.ui_utils.click_element(reviewer_action_factory.page_factory.reviewer_page.back_button)
                reviewer_action_factory.ui_utils.smart_wait()

        #......................................................................................................................
        # Step 7: Company Admin Changes State to Review 2 :
        action_factory.page.bring_to_front()
        active_action_factory = action_factory
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.task_panel)
        action_factory.ui_utils.smart_wait()

        for file_name in expected_files:
            target_fname = file_name if isinstance(file_name, str) else file_name[0]
            action_factory.projects_actions.changeStatus_ofProject(target_fname, "Review 2")
            action_factory.ui_utils.smart_wait()
            status_after = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.get_file_status(target_fname))
            if "Review 2" in status_after:
                status = "Pass"
                message = f"File '{target_fname}' status changed successfully to Review 2."
                action_factory.helpers.attach_screenshot(name="File Status Changed to Review 2")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert True, message
            else:
                status = "Fail"
                message = f"File '{target_fname}' status not changed to Review 2."
                action_factory.helpers.attach_screenshot(name="File Status Not Changed to Review 2")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert False, message

        #......................................................................................................................
        # Step 8: Login as Reviewer 2, Drop New Segment (Bus), Delete Annotator Segment (Bicycle), and Reject Task :
        reviewer2_context = action_factory.page.context.browser.new_context()
        reviewer2_page = reviewer2_context.new_page()
        reviewer2_action_factory = ActionFactory(reviewer2_page)
        active_action_factory = reviewer2_action_factory

        reviewer2_action_factory.login_actions.perform_login(url=url, email=reviewer_email, password=reviewer_password)
        reviewer2_action_factory.login_actions.use_different_email_OTP(diff_email)
        reviewer2_action_factory.login_actions.select_organization(company_Name, "Reviewer")
        reviewer2_action_factory.ui_utils.smart_wait()

        reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.tasks_menu)
        reviewer2_action_factory.ui_utils.smart_wait()
        reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.click_project_name(project_Name))
        reviewer2_action_factory.ui_utils.smart_wait()

        for target_file in expected_files:
            reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.click_project_name(target_file))
            reviewer2_action_factory.ui_utils.smart_wait()
            claim_visible = reviewer2_action_factory.ui_utils.wait_for_visible_if_exists(
                reviewer2_action_factory.page_factory.reviewer_page.claim_button, timeout=5000
            )
            if claim_visible:
                reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.claim_button)
                reviewer2_action_factory.ui_utils.smart_wait()

            reviewer2_action_factory.reviewer_actions.wait_for_iframe_ready()

            # Drop New Segment (Bus)
            reviewer2_action_factory.annotator_actions.perform_annotation_for_image_files("Bus", (570, 165), (790, 165))
            reviewer2_action_factory.ui_utils.smart_wait()

            # Delete Annotator Segment (Bicycle)
            reviewer2_action_factory.annotator_actions.delete_annotation("Bicycle")
            reviewer2_action_factory.ui_utils.smart_wait()
            reviewer2_action_factory.helpers.compare_screenshot(name=f"05_Reviewer2_{target_file}_Delete_Segment", locator=reviewer2_action_factory.page_factory.annotator_page.main_video_image)

            # Reject task with feedback comments
            reviewer2_action_factory.reviewer_actions.reject_task("Need Correction")
            claim_after = reviewer2_action_factory.ui_utils.wait_for_visible_if_exists(
                reviewer2_action_factory.page_factory.reviewer_page.claim_button, timeout=5000
            )
            if claim_after:
                reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.back_button)
                reviewer2_action_factory.ui_utils.smart_wait()

        #......................................................................................................................
        # Step 9: Login as Annotator, Edit Reviewer 2 Segment (Bus), and Save and Exit :
        annotator_page.bring_to_front()
        active_action_factory = annotator_action_factory
        annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.home_menu)
        annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.tasks_menu)
        annotator_action_factory.ui_utils.smart_wait()
        annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.click_project_name(project_Name))
        annotator_action_factory.ui_utils.smart_wait()

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

            # Check feedback comments if visible
            feedback_comment = annotator_action_factory.page_factory.annotator_page.get_feedback_comment("Need Correction")
            is_feedback_visible = annotator_action_factory.ui_utils.wait_for_visible_if_exists(feedback_comment, timeout=3000)
            if is_feedback_visible:
                annotator_action_factory.ui_utils.click_element(feedback_comment)
                close_btn = annotator_action_factory.page_factory.annotator_page.close_button
                if annotator_action_factory.ui_utils.is_element_visible(close_btn, timeout=3000):
                    annotator_action_factory.ui_utils.click_element(close_btn)
                annotator_action_factory.ui_utils.smart_wait()

            # Edit Reviewer 2 segment (Bus: draw 1 vertical center line)
            annotator_action_factory.annotator_actions.edit_old_annotation("Bus", from_coords=(680, 165), to_coords=(680, 470))
            annotator_action_factory.ui_utils.smart_wait()
            annotator_action_factory.helpers.compare_screenshot(name=f"06_Annotator_{target_file}_Edit_Segment", locator=annotator_action_factory.page_factory.annotator_page.main_video_image)

            # Save and Exit
            annotator_action_factory.annotator_actions.perform_save_exit()
            annotator_action_factory.ui_utils.smart_wait()
            claim_after = annotator_action_factory.ui_utils.wait_for_visible_if_exists(
                annotator_action_factory.page_factory.annotator_page.claim_button, timeout=5000
            )
            if claim_after:
                annotator_action_factory.ui_utils.click_element(annotator_action_factory.page_factory.annotator_page.back_button)
                annotator_action_factory.ui_utils.smart_wait()

        #......................................................................................................................
        # Step 10: Company Admin Changes State to Review 1 :
        action_factory.page.bring_to_front()
        active_action_factory = action_factory
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.task_panel)
        action_factory.ui_utils.smart_wait()

        for file_name in expected_files:
            target_fname = file_name if isinstance(file_name, str) else file_name[0]
            action_factory.projects_actions.changeStatus_ofProject(target_fname, "Review 1")
            action_factory.ui_utils.smart_wait()
            status_after = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.get_file_status(target_fname))
            if "Review 1" in status_after:
                status = "Pass"
                message = f"File '{target_fname}' status changed successfully to Review 1."
                action_factory.helpers.attach_screenshot(name="File Status Changed to Review 1 Third Time")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert True, message
            else:
                status = "Fail"
                message = f"File '{target_fname}' status not changed to Review 1."
                action_factory.helpers.attach_screenshot(name="File Status Not Changed to Review 1 Third Time")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert False, message

        #......................................................................................................................
        # Step 11: Reviewer 1 Drops 1 Segment (Traffic Light) and Save and Exit :
        reviewer_page.bring_to_front()
        active_action_factory = reviewer_action_factory
        reviewer_action_factory.ui_utils.click_element(reviewer_action_factory.page_factory.reviewer_page.home_menu)
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

            # Drop 1 Segment (Traffic Light)
            reviewer_action_factory.annotator_actions.perform_annotation_for_image_files("Traffic Light", (420, 230), (420, 470))
            reviewer_action_factory.ui_utils.smart_wait()
            reviewer_action_factory.helpers.compare_screenshot(name=f"07_Reviewer1_{target_file}_Drop1_Segment", locator=reviewer_action_factory.page_factory.annotator_page.main_video_image)

            # Save and Exit
            reviewer_action_factory.annotator_actions.perform_save_exit()
            reviewer_action_factory.ui_utils.smart_wait()
            claim_after = reviewer_action_factory.ui_utils.wait_for_visible_if_exists(
                reviewer_action_factory.page_factory.reviewer_page.claim_button, timeout=5000
            )
            if claim_after:
                reviewer_action_factory.ui_utils.click_element(reviewer_action_factory.page_factory.reviewer_page.back_button)
                reviewer_action_factory.ui_utils.smart_wait()

        #......................................................................................................................
        # Step 12: Company Admin Changes State to Review 2 :
        action_factory.page.bring_to_front()
        active_action_factory = action_factory
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.task_panel)
        action_factory.ui_utils.smart_wait()

        for file_name in expected_files:
            target_fname = file_name if isinstance(file_name, str) else file_name[0]
            action_factory.projects_actions.changeStatus_ofProject(target_fname, "Review 2")
            action_factory.ui_utils.smart_wait()
            status_after = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.get_file_status(target_fname))
            if "Review 2" in status_after:
                status = "Pass"
                message = f"File '{target_fname}' status changed successfully to Review 2."
                action_factory.helpers.attach_screenshot(name="File Status Changed to Review 2 Second Time")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert True, message
            else:
                status = "Fail"
                message = f"File '{target_fname}' status not changed to Review 2."
                action_factory.helpers.attach_screenshot(name="File Status Not Changed to Review 2 Second Time")
                action_factory.helpers.attach_allure(name="File Name", text=target_fname)
                assert False, message

        #......................................................................................................................
        # Step 13: Reviewer 2 Edits Segment, Drops New Segment (Car), and Submits / Approves :
        reviewer2_page.bring_to_front()
        active_action_factory = reviewer2_action_factory
        reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.home_menu)
        reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.tasks_menu)
        reviewer2_action_factory.ui_utils.smart_wait()
        reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.click_project_name(project_Name))
        reviewer2_action_factory.ui_utils.smart_wait()

        for target_file in expected_files:
            reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.click_project_name(target_file))
            reviewer2_action_factory.ui_utils.smart_wait()
            claim_visible = reviewer2_action_factory.ui_utils.wait_for_visible_if_exists(
                reviewer2_action_factory.page_factory.reviewer_page.claim_button, timeout=5000
            )
            if claim_visible:
                reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.claim_button)
                reviewer2_action_factory.ui_utils.smart_wait()

            reviewer2_action_factory.reviewer_actions.wait_for_iframe_ready()

            # Edit Segment (Bus)
            bus_reapply_coords = [(710, 165), (840, 165), (870, 195), (800, 195)]
            reviewer2_action_factory.annotator_actions.edit_old_annotation("Bus", edit_coords=bus_reapply_coords)
            reviewer2_action_factory.ui_utils.smart_wait()

            # Drop New Segment (Car)
            reviewer2_action_factory.annotator_actions.perform_annotation_for_image_files("Car", (500, 230), (500, 470))
            reviewer2_action_factory.ui_utils.smart_wait()
            reviewer2_action_factory.helpers.compare_screenshot(name=f"08_Reviewer2_{target_file}_Add_Segment", locator=reviewer2_action_factory.page_factory.annotator_page.main_video_image)

            # Approve Task
            reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.approve_button)
            reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.approve_button)
            reviewer2_action_factory.ui_utils.smart_wait()
            claim_after = reviewer2_action_factory.ui_utils.wait_for_visible_if_exists(
                reviewer2_action_factory.page_factory.reviewer_page.claim_button, timeout=5000
            )
            if claim_after:
                reviewer2_action_factory.ui_utils.click_element(reviewer2_action_factory.page_factory.reviewer_page.back_button)
                reviewer2_action_factory.ui_utils.smart_wait()

        #......................................................................................................................
        # Step 14: Comeback to Company Admin, Validate Complete Status, Click File, and Compare Screenshot :
        action_factory.page.bring_to_front()
        active_action_factory = action_factory
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.project_menu)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_projects_name(project_Name))
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.task_panel)
        action_factory.ui_utils.smart_wait()

        for file_name in expected_files:
            target_fname = file_name if isinstance(file_name, str) else file_name[0]
            status_after = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.projects_page.get_file_status(target_fname))
            if "Complete" in status_after:
                status = "Pass"
                message = f"File '{target_fname}' status changed successfully to Complete"
                action_factory.helpers.attach_screenshot(name="File Status Changed to Complete")
                action_factory.helpers.attach_allure(name="File complete Status", text=target_fname)
                assert True, message
            else:
                status = "Fail"
                message = f"File '{target_fname}' status not changed to Complete"
                action_factory.helpers.attach_screenshot(name="File Status Not Changed to Complete")
                action_factory.helpers.attach_allure(name="File not complete Status", text=target_fname)
                assert False, message

            # Click the file name and wait for Iframe load and use compare screenshot
            action_factory.ui_utils.click_element(action_factory.page_factory.projects_page.click_task_file_name(target_fname))
            action_factory.ui_utils.smart_wait()
            claim_visible = action_factory.ui_utils.wait_for_visible_if_exists(
                action_factory.page_factory.annotator_page.claim_button, timeout=5000
            )
            if claim_visible:
                action_factory.ui_utils.click_element(action_factory.page_factory.annotator_page.claim_button)
                action_factory.ui_utils.smart_wait()

            action_factory.reviewer_actions.wait_for_iframe_ready()
            action_factory.helpers.compare_screenshot(name=f"01_Admin_{target_fname}_TC03_Completed_Segment", locator=action_factory.page_factory.annotator_page.main_video_image)
            back_btn = action_factory.page_factory.annotator_page.back_button
            if action_factory.ui_utils.is_element_visible(back_btn, timeout=3000):
                action_factory.ui_utils.click_element(back_btn)
                action_factory.ui_utils.smart_wait()

        # Validate deferred screenshot comparison failures after executing the full flow
        action_factory.helpers.assert_screenshot_comparisons()
       
    except Exception as e:
        status = "Fail"
        message = str(e)
        active_action_factory.helpers.handle_failure(message=message)
        raise

    finally:
        active_action_factory.helpers.write_test_results(
            status=status,
            message=message
        )

