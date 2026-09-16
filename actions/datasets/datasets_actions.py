from pathlib import Path
from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils

class DatasetsActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)

    def click_datasets_menu(self):
        self.ui_utils.click_element(self.page_factory.datasets_page.datasets_menu)
        self.ui_utils.element_wait_for(self.page_factory.datasets_page.create_dataset_button, state="visible", timeout=10000)
        create_dataset_button_visible = self.ui_utils.is_element_visible(self.page_factory.datasets_page.create_dataset_button, timeout=10000)
        print(f"Create Dataset button visibility: {create_dataset_button_visible}")
        if create_dataset_button_visible:
            print("Create Dataset button is visible")
        else:
            raise Exception("Create Dataset button is not visible after clicking the Datasets menu.")

    def dataset_type(self, dataset_type_name):
        self.ui_utils.click_element(self.page_factory.datasets_page.select_dataset_type)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.datasets_page.get_dataset_type_option(dataset_type_name))
        print(f"Selected dataset type: {dataset_type_name}")
        
    def create_dataset(self, dataset_name, dataset_type_name, description = None):
        self.ui_utils.click_element(self.page_factory.datasets_page.create_dataset_button)
        self.ui_utils.smart_wait()
        self.ui_utils.fill_input(self.page_factory.datasets_page.enter_dataset_name, dataset_name)
        self.dataset_type(dataset_type_name)
        if description:
            self.ui_utils.fill_input(self.page_factory.datasets_page.dataset_description, description)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.datasets_page.create_button)
        self.ui_utils.element_wait_for(self.page_factory.datasets_page.dataset_cell, state="visible", timeout=10000)
        dataset_cell_visible = self.ui_utils.is_element_visible(self.page_factory.datasets_page.dataset_cell, timeout=10000)
        print(f"Dataset cell visibility: {dataset_cell_visible}")
        if dataset_cell_visible:
            print("Dataset cell is visible")
        else:
            raise Exception("Dataset cell is not visible after creating the dataset.")

    def upload_files_with_uploadBtn(self, *file_paths):
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
        self.ui_utils.click_element(self.page_factory.datasets_page.upload_button.nth(1))
        self.ui_utils.smart_wait()
        loading = self.page_factory.datasets_page.upload_loading
        self.ui_utils.element_wait_for(loading, state="hidden", timeout=200000)
        self.ui_utils.smart_wait()
        

    def add_files_dataset(self, *files):
        file_list = []
        for item in files:
            if isinstance(item, (list, tuple)):
                file_list.extend(item)
            else:
                file_list.append(item)
        self.ui_utils.click_element(self.page_factory.datasets_page.add_files)
        self.ui_utils.smart_wait()
        for file in file_list:
            self.ui_utils.click_element(self.page_factory.files_page.return_file_checkbox(file))
        self.ui_utils.click_element(self.page_factory.datasets_page.add_files)
        self.ui_utils.smart_wait()

    def delete_dataset(self, dataset_names):
        if isinstance(dataset_names, str):
            dataset_names = [dataset_names]
        for name in dataset_names:
            self.ui_utils.click_element(self.page_factory.files_page.return_file_checkbox(name).first)
        self.ui_utils.click_element(self.page_factory.files_page.delete_btn)
        self.ui_utils.smart_wait()
        delete_popup = self.ui_utils.wait_for_visible_if_exists(self.page_factory.files_page.delete_confirmation)
        if delete_popup:
            self.ui_utils.fill_input(self.page_factory.files_page.delete_text, "DELETE")
            self.ui_utils.click_element(self.page_factory.files_page.delete_btn)
            self.ui_utils.smart_wait()
        else:
            raise Exception(f"Delete popup not found when attempting to delete dataset: {dataset_names}")


        