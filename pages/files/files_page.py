from utils.ui_utils import UIUtils
import re

class FilesPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.files_menu = page.get_by_role("link", name="Files")
        self.invalid_file_error = page.get_by_text('files skipped (incompatible', exact= False)
        self.pagination_dropdown = page.locator("#itemsPerPage")
        self.search_btn = page.get_by_role('textbox', name= 'search' )
        self.files_checkbox = page.locator("*[type='checkbox']")
        self.delete_btn = page.get_by_role('button', name= 'Delete', exact=True)
        self.delete_confirmation = page.get_by_role('heading', name= 'Deletion Confirmation' )
        self.delete_text = page.get_by_role('textbox')
        self.cancel_popup = page.locator("button[data-testid*='modal-close-btn']")
        self.add_to_dataset = page.locator("button[data-testid*='add-to-dataset-btn']")
        self.add_button = page.locator("button[data-testid*='add-to-dataset-modal-submit-btn']")
        self.cancel_button = page.locator("button[data-testid*='add-to-dataset-modal-cancel-btn']")
        self.failure_file_popup = page.get_by_text('Failed DeletionFile')
        self.add_dataset_Panel = page.get_by_role('heading', name= 'Add Items to Dataset' )
        self.create_new_dataset = page.get_by_role('tab', name= 'Create New Dataset' )
        self.dataset_name_enter = page.get_by_role('textbox', name= 'Dataset Name*' )
        self.create_button = page.get_by_role('button', name= 'Create' )
        self.add_items_datatype = page.locator("td[class*='center whitespace']")
        self.files_delete_success_popup = page.get_by_text('Successfully Detached File')
        self.upload_files_tabs = page.locator("button[class*='pb-2 text']")
        self.search_datasets_input = page.get_by_role('textbox', name='Search datasets...')
        self.uploading_btn = page.get_by_role('button', name= '% Uploading' )
        self.failed_detached_file = page.get_by_text('Failed Detached File', exact=False)

    def return_toast_msg_locator(self, toast_msg):
        return self.page.locator("div[class*='center gap-2 text']").filter(has_text=toast_msg)

    def return_delete_message(self, delete_msg):
        return self.page.get_by_text(delete_msg)

    def return_file_checkbox(self, file_name):
        return self.page.get_by_role("row").filter(has_text=file_name).get_by_role("checkbox")
