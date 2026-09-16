from pathlib import Path
from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils

class TemplatesActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)

    def click_templates_menu(self):
        self.ui_utils.click_element(self.page_factory.templates_page.templates_menu)
        self.ui_utils.element_wait_for(self.page_factory.templates_page.upload_new_template_btn, state="visible", timeout=10000)
        upload_new_template_btn_visible = self.ui_utils.is_element_visible(self.page_factory.templates_page.upload_new_template_btn, timeout=10000)
        print(f"Upload New Template button visibility: {upload_new_template_btn_visible}")
        if upload_new_template_btn_visible:
            print("Upload New Template button is visible")
        else:
            raise Exception("Upload New Template button is not visible after clicking the Templates menu.")

    def upload_new_template(self, template_name, description=None):
        self.ui_utils.click_element(self.page_factory.templates_page.upload_new_template_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.fill_input(self.page_factory.templates_page.template_name_input, template_name)
        if description and self.ui_utils.is_element_visible(self.page_factory.templates_page.description_input, timeout=2000):
            self.ui_utils.fill_input(self.page_factory.templates_page.description_input, description)

    def upload_template_files(self, *file_paths):
            files = []
            for file_path in file_paths:
                full_path = Path("test_data") / "files" / file_path
                if not full_path.exists():
                    raise FileNotFoundError(f"File not found: {full_path}")
                files.append(str(full_path))
            self.page_factory.templates_page.file_upload.set_input_files(files)
            self.ui_utils.smart_wait()
            self.ui_utils.click_element(self.page_factory.templates_page.upload_button)
            self.ui_utils.smart_wait()

    def upload_template_files_without_uploadBtn(self, *file_paths):
            files = []
            for file_path in file_paths:
                full_path = Path("test_data") / "files" / file_path
                if not full_path.exists():
                    raise FileNotFoundError(f"File not found: {full_path}")
                files.append(str(full_path))
            self.page_factory.templates_page.file_upload.set_input_files(files)
            self.ui_utils.smart_wait()

    def validate_template_toast_msg(self, expected_msg):
        toast_locator = self.page_factory.templates_page.return_template_toast(expected_msg)
        self.ui_utils.element_wait_for(toast_locator,timeout=10000)
        toast_visible = self.ui_utils.is_element_visible(toast_locator,timeout=10000)
        assert toast_visible is True, f"Toast message '{expected_msg}' is not visible"

    def search_template_name(self, template_name):
        self.ui_utils.click_element(self.page_factory.templates_page.search_btn)
        self.ui_utils.fill_input(self.page_factory.templates_page.search_btn, template_name)
        self.ui_utils.smart_wait()

    def delete_template(self, template_names):
        if isinstance(template_names, str):
            template_names = [template_names]
        for name in template_names:
            self.ui_utils.click_element(self.page_factory.files_page.return_file_checkbox(name).first)
        self.ui_utils.click_element(self.page_factory.files_page.delete_btn)
        self.ui_utils.smart_wait()
        delete_popup = self.ui_utils.wait_for_visible_if_exists(self.page_factory.templates_page.delete_confirmation)
        if delete_popup:
            self.ui_utils.fill_input(self.page_factory.files_page.delete_text, "DELETE")
            self.ui_utils.click_element(self.page_factory.files_page.delete_btn)
            self.ui_utils.smart_wait()
        else:
            raise Exception(f"Delete popup not found when attempting to delete template: {template_names}")

    def update_template(self, template_name, *file_paths):
        update_btn = self.page_factory.templates_page.return_update_button(template_name)
        self.ui_utils.click_element(update_btn)
        self.ui_utils.smart_wait()
        self.upload_template_files(*file_paths)

    def set_templates_pagination(self, num_of_items):
        self.ui_utils.select_option(self.page_factory.files_page.pagination_dropdown, str(num_of_items))
        self.ui_utils.smart_wait()
    