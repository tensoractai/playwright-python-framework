from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils

class ProjectsActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)

    def click_project_menu(self):
        self.ui_utils.click_element(self.page_factory.projects_page.project_menu)
        self.ui_utils.element_wait_for(self.page_factory.projects_page.create_project_btn, state="visible", timeout=10000)
        create_project_btn_visible = self.ui_utils.is_element_visible(self.page_factory.projects_page.create_project_btn, timeout=10000)
        print(f"Create Project button visibility: {create_project_btn_visible}")
        if create_project_btn_visible:
            print("Create Project button is visible")
        else:
            raise Exception("Create Project button is not visible after clicking the Projects menu.")

    def create_project(self, project_name, dataset_name, workflow_name, description=None):
        self.ui_utils.click_element(self.page_factory.projects_page.create_project_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.fill_input(self.page_factory.projects_page.project_name_input, project_name)  
        if description and self.ui_utils.is_element_visible(self.page_factory.projects_page.project_description_input, timeout=2000):
            self.ui_utils.fill_input(self.page_factory.projects_page.project_description_input, description)
        self.ui_utils.element_wait_for(self.page_factory.projects_page.create_project_page, state="visible", timeout=10000)
        create_project_page_visible = self.ui_utils.is_element_visible(self.page_factory.projects_page.create_project_page, timeout=10000)
        print(f"Create Project page visibility: {create_project_page_visible}")
        if create_project_page_visible:
            print("Create Project page is visible")
        else:
            raise Exception("Select Dataset button is not visible after clicking the Create Project button.")
        self.ui_utils.click_element(self.page_factory.projects_page.select_dataset)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.projects_page.select_dropdowns(dataset_name))
        self.ui_utils.click_element(self.page_factory.projects_page.heading_create_project)
        self.ui_utils.click_element(self.page_factory.projects_page.select_workflow)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.projects_page.select_dropdowns(workflow_name))
        self.ui_utils.click_element(self.page_factory.projects_page.heading_create_project)
        create_project_enabled = self.ui_utils.is_element_enabled(self.page_factory.projects_page.create_project_btn)
        print(f"Create Project button enabled: {create_project_enabled}")
        if create_project_enabled:
            print("Create Project button is enabled")
        else:
            raise Exception("Create Project button is not enabled after selecting the dataset and workflow.")
        self.ui_utils.click_element(self.page_factory.projects_page.create_project_btn)

    def click_teams_tab(self):
        self.ui_utils.click_element(self.page_factory.projects_page.teams_tab)
        self.ui_utils.smart_wait()
        teams_panel_visible = self.ui_utils.is_element_visible(self.page_factory.projects_page.teams_panel)
        print(f"Teams panel visibility: {teams_panel_visible}")
        if teams_panel_visible:
            print("Teams panel is visible")
        else:
            raise Exception("Teams panel is not visible after clicking the Teams tab.")

    def add_users(self, role, email_address):
        self.ui_utils.click_element(self.page_factory.projects_page.add_user_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.select_option(self.page_factory.projects_page.assign_user_dropdown, role.upper())
        self.ui_utils.click_element(self.page_factory.projects_page.get_user_checkbox(email_address))
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.projects_page.add_btn)
        self.ui_utils.smart_wait()
        add_user_btn_visible = self.ui_utils.is_element_visible(self.page_factory.projects_page.add_user_btn)
        print(f"Add user button visibility: {add_user_btn_visible}")
        if add_user_btn_visible:
            print("Add user button is visible")
        else:
            raise Exception("Add user button is not visible after adding the user.")

    def remove_user(self, email_address):
        self.ui_utils.click_element(self.page_factory.projects_page.get_email_click_checkbox(email_address))
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.projects_page.remove_selected_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.fill_input(self.page_factory.projects_page.remove_user_confirm, "DELETE")
        self.ui_utils.click_element(self.page_factory.projects_page.remove_btn)
        self.ui_utils.smart_wait()
        removed_user_toast_visible = self.ui_utils.is_element_visible(self.page_factory.projects_page.removed_user_toast)
        print(f"Removed user toast visibility: {removed_user_toast_visible}")
        if removed_user_toast_visible:
            print("Removed user toast is visible")
        else:
            raise Exception("Remove user button is not visible after removing the user.")


    def delete_project(self, project_name):
        self.ui_utils.click_element(self.page_factory.files_page.return_file_checkbox(project_name).first)
        self.ui_utils.click_element(self.page_factory.projects_page.delete_toolbar_btn)
        self.ui_utils.smart_wait()
        delete_popup = self.ui_utils.wait_for_visible_if_exists(self.page_factory.files_page.delete_confirmation)
        if delete_popup:
            self.ui_utils.fill_input(self.page_factory.files_page.delete_text, "DELETE")
            self.ui_utils.click_element(self.page_factory.files_page.delete_btn)
            self.ui_utils.smart_wait()
        else:
            raise Exception(f"Delete popup not found when attempting to delete project: {project_name}")

    def export_and_validate_transcription_json(self, expected_files=None, expected_texts=None, unexpected_texts=None, fields=None):
        import json, zipfile
        self.ui_utils.click_element(self.page_factory.projects_page.tasks_table_master_checkbox)
        self.ui_utils.smart_wait()
        with self.page_factory.projects_page.page.expect_download() as download_info:
            self.ui_utils.click_element(self.page_factory.projects_page.export_json_btn)
        download_path = download_info.value.path()

        raw_items, project_name = [], None
        if zipfile.is_zipfile(download_path):
            with zipfile.ZipFile(download_path, "r") as z:
                raw_items = [json.loads(z.read(f).decode("utf-8")) for f in z.namelist() if f.endswith(".json")]
        else:
            with open(download_path, "r", encoding="utf-8") as f:
                raw_items = [json.load(f)]

        records = []
        for item in raw_items:
            if isinstance(item, dict):
                for k, v in item.items():
                    if isinstance(v, list):
                        project_name = project_name or k
                        records.extend(v)
                    elif k == "taskFileName":
                        records.append(item)
            elif isinstance(item, list):
                records.extend(item)

        transcriptions = {}
        for r in records:
            fname = r.get("taskFileName")
            if fname:
                streams = r.get("data", {}).get("annotations", {}).get("streams", {})
                texts = [t["text"] for t in streams.get("Transcription", []) if isinstance(t, dict) and "text" in t]
                transcriptions.setdefault(fname, []).extend(texts)

        exp_files = [expected_files] if isinstance(expected_files, str) else (expected_files or [])
        exp_texts = [expected_texts] if isinstance(expected_texts, str) else (expected_texts or [])
        unexp_texts = [unexpected_texts] if isinstance(unexpected_texts, str) else (unexpected_texts or [])

        missing = [f for f in exp_files if f not in transcriptions]
        failed_exp = [f"'{f}' missing '{t}'" for f in exp_files if f in transcriptions for t in exp_texts if not any(t in act for act in transcriptions[f])]
        failed_unexp = [f"'{f}' contains unexpected '{t}'" for f in exp_files if f in transcriptions for t in unexp_texts if any(t in act for act in transcriptions[f])]

        if missing or failed_exp or failed_unexp:
            raise Exception(f"Export JSON validation failed. Missing files: {missing}. Missing expected: {failed_exp}. Unexpected present: {failed_unexp}")

        custom_data = {}
        if fields:
            for field in ([fields] if isinstance(fields, str) else fields):
                custom_data[field] = [r.get(field) for r in records if field in r]

        result = dict(transcriptions)
        result["project_name"] = project_name
        result["transcriptions"] = transcriptions
        result["records"] = records
        result["custom_data"] = custom_data
        print(result)
        return result

    def set_projects_pagination(self, num_of_items):
        self.ui_utils.select_option(self.page_factory.projects_page.pagination_dropdown, str(num_of_items))
        self.ui_utils.smart_wait()

    def add_dataset_to_project(self, dataset_name):
        self.ui_utils.click_element(self.page_factory.projects_page.project_datasets_add_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.select_option(self.page_factory.projects_page.modal_pagination_select.last, "50")
        self.ui_utils.click_element(self.page_factory.projects_page.return_Dataset_checkbox_addsync(dataset_name))
        self.ui_utils.click_element(self.page_factory.projects_page.add_sync_btn)
        self.ui_utils.smart_wait()

