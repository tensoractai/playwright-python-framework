from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils
from pathlib import Path

class FilesActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)

    def upload_files_without_uploadbtn(self, *file_paths):
        self.ui_utils.click_element(self.page_factory.datasets_page.upload_files_button)
        self.ui_utils.smart_wait()
        files = []
        for file_path in file_paths:
            full_path = Path("test_data") / "files" / file_path
            # Folder
            if full_path.is_dir():
                files.extend(
                    str(file)
                    for file in full_path.iterdir()
                    if file.is_file()
                )
            # Individual file
            elif full_path.is_file():
                files.append(str(full_path))
            else:
                raise FileNotFoundError(f"File or folder not found: {full_path}")
        self.page_factory.datasets_page.upload_files.set_input_files(files)
        self.ui_utils.smart_wait()

    def set_files_pagination(self, num_of_files):
        self.ui_utils.select_option(self.page_factory.files_page.pagination_dropdown, num_of_files)
        self.ui_utils.smart_wait()

    def search_files_name(self, file_name):
        self.ui_utils.click_element(self.page_factory.files_page.search_btn)
        self.ui_utils.fill_input(self.page_factory.files_page.search_btn, file_name)
        self.ui_utils.smart_wait()

    def delete_multiple_files(self, count):
        for index in range(count):
            self.ui_utils.click_element(self.page_factory.files_page.files_checkbox.nth(index+1))
        self.ui_utils.click_element(self.page_factory.files_page.delete_btn)
        delete_popup = self.ui_utils.wait_for_visible_if_exists(self.page_factory.files_page.delete_confirmation)
        if delete_popup:
            self.ui_utils.fill_input(self.page_factory.files_page.delete_text, "DELETE")
            self.ui_utils.click_element(self.page_factory.files_page.delete_btn)
        else:
            raise Exception("Delete popup not found")

    def delete_single_files(self, file_Name):
        if isinstance(file_Name, str):
            file_Name = [file_Name]
        for file in file_Name:
            self.ui_utils.click_element(self.page_factory.files_page.return_file_checkbox(file).first)
            self.ui_utils.click_element(self.page_factory.files_page.delete_btn)
            delete_popup = self.ui_utils.wait_for_visible_if_exists(self.page_factory.files_page.delete_confirmation)
            if delete_popup:
                self.ui_utils.fill_input(self.page_factory.files_page.delete_text, "DELETE")
                self.ui_utils.click_element(self.page_factory.files_page.delete_btn)
            else:
                raise Exception("Delete popup not found")
        print("Deleted All Files")


    def click_file_name_checkbox(self, file_name):
        self.ui_utils.click_element(self.page_factory.files_page.return_file_checkbox(file_name).first)
        add_dataset_enabled = self.ui_utils.is_element_enabled(self.page_factory.files_page.add_to_dataset)
        if not add_dataset_enabled:
            raise Exception("Add to dataset button is disabled")
    
    def add_to_dataset(self, dataset_name):
        self.ui_utils.click_element(self.page_factory.files_page.add_to_dataset)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.files_page.return_file_checkbox(dataset_name))
        print("Dataset Check Box Clicked successfully")

    def validate_add_items_datatype(self, dataType):
        data_type = self.ui_utils.grab_text_from_all(self.page_factory.files_page.add_items_datatype)
        text_values = [value for value in data_type if not value.strip().isdigit()]
        result = all(value == dataType for value in text_values if not value.isdigit())
        print(result, "Add Items Data Type Assertion")
        assert  result, (f"Expected datatype '{dataType}', "f"but found {text_values}")

    def create_new_dataset(self, dataset_name):
        self.ui_utils.click_element(self.page_factory.files_page.create_new_dataset)
        self.ui_utils.click_element(self.page_factory.files_page.dataset_name_enter)
        self.ui_utils.fill_input(self.page_factory.files_page.dataset_name_enter, dataset_name)
        self.ui_utils.click_element(self.page_factory.files_page.create_button)
        self.ui_utils.smart_wait()

    def cancel_file_upload(self):
        def handle_dialog(dialog):
            print(f"Dialog message: {dialog.message}")
            dialog.accept()

        self.page_factory.files_page.page.once("dialog", handle_dialog)
        self.ui_utils.element_wait_for(self.page_factory.files_page.cancel_button, state="visible", timeout=10000)
        self.ui_utils.click_element(self.page_factory.files_page.cancel_button)
        self.ui_utils.smart_wait()

        # If custom HTML confirmation popup overlay is visible, click OK
        ok_btn = self.page_factory.files_page.page.get_by_role('button', name='OK', exact=True)
        if self.ui_utils.is_element_visible(ok_btn, timeout=3000):
            self.ui_utils.click_element(ok_btn)
            self.ui_utils.smart_wait()
