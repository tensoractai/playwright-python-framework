from utils.ui_utils import UIUtils

class TemplatesPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.templates_menu          = page.get_by_role("link", name="Templates")
        self.upload_new_template_btn = page.get_by_role("button", name="Upload New Template")
        self.template_name_input = page.get_by_role('textbox', name= 'Template Name * Upload file *')
        self.description_input = page.get_by_role('textbox', name='Description')
        self.file_upload = page.locator('label').filter(has_text='Click to upload')
        self.upload_button = page.get_by_role('button', name= 'Upload')
        self.template_names_list = page.locator('div[class*="medium text"]')
        self.template_file_upload_error = page.get_by_text('Only ZIP files are allowed')
        self.template_exists_error = page.get_by_text('A template with this name already exists', exact=False)
        self.template_invalid_name_error = page.get_by_text('Only letters, numbers, spaces, _ and - are allowed', exact=False)
        self.search_btn = page.get_by_role('textbox', name='search')
        self.no_templates_found = page.get_by_text('No templates found', exact=False)
        self.template_delete_success_msg = page.get_by_text('Successfully Deleted Template')
        self.delete_confirmation = page.get_by_role('heading', name= 'Delete Confirmation' )
        self.template_delete_failed_msg = page.get_by_text('Failed Deleted Template')
        self.invalid_zip_error = page.get_by_text('invalid Zip File', exact=False)


    def return_template_toast(self, toast):
        return self.page.locator('p[class*="semibold text"]').filter(has_text=toast)

    def return_update_button(self, template_name):
        return self.page.locator("td:has(div.template-name)").filter(has_text=template_name).locator("~ td button")
        