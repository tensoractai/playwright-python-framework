from utils.ui_utils import UIUtils

class datasetsPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.datasets_menu          = page.get_by_role("link", name="Datasets")
        self.create_dataset_button  = page.get_by_role("button", name="Create Dataset")
        self.enter_dataset_name = page.get_by_role('textbox', name='Enter Dataset Name' )
        self.select_dataset_type = page.get_by_role('button', name='Select Type' )
        self.create_button = page.get_by_role('button', name='Create' )
        self.dataset_names_list = page.locator('span[data-testid*="col-name"]')
        self.dataset_cell = page.locator('th[data-testid*="view-header-name"]')
        self.upload_files_button = page.get_by_role('button',  name='Upload Files')
        self.upload_files = page.locator('label').filter(has_text='Click to upload from this')
        self.upload_button = page.get_by_role('button', name= 'Upload',exact = True)
        self.files_name_list = page.locator("button[data-testid*='dataview-col-name']")
        self.dataset_file_name_list = page.locator("td[data-testid*='files-dataview'] div[class*='dataset-name']")
        self.dataset_name_error_msg = self.page.get_by_text("Only letters, numbers, spaces, _ and - are allowed", exact=True)
        self.dataset_exists_error = page.get_by_text("A Dataset with this name already exists", exact=True)
        self.add_files = page.get_by_role('button', name='Add Files')
        self.dataset_delete_success_popup = self.page.get_by_text('Successfully Deleted Dataset')
        self.dataset_delete_failed_popup = self.page.get_by_text('Failed Deleted Dataset')
        self.dataset_type_list = self.page.locator("div[data-testid*='modal-type-option'] span")
        self.dataset_description = page.get_by_role('textbox', name='Enter Dataset Description' )
        self.upload_loading = page.get_by_text("Uploading")


    def get_dataset_type_option(self, dataset_type_name):
        return self.page.get_by_test_id(f"create-dataset-modal-type-option-{dataset_type_name.upper()}")

    def click_dataset_file_name(self, file_name):
        return self.page.locator("span").filter(has_text=file_name)

    def get_company_name_by_dataset(self, dataset_name):
        return self.page.locator('td:has(span[data-testid*="col-name"]:has-text("AUT"))').locator('xpath=following-sibling::td[contains(@data-testid,"col-company")]//div')