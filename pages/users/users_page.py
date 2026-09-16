from utils.ui_utils import UIUtils

class Userspage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)
        
        self.user_menu = page.get_by_role('link', name='Users')
        self.create_user = page.get_by_role('button', name='Create User')
        self.enter_name = page.get_by_role('textbox', name='Enter Full Name')
        self.enter_email = page.get_by_role('textbox', name='Enter Email')
        self.enter_password = page.get_by_role('textbox', name='Enter Password')
        self.confirm_password = page.get_by_role('textbox', name='Confirm Password')
        self.allow_MFA_btn = page.get_by_role('checkbox', name='Allow alternate MFA email(')
        self.cancel_btn = page.get_by_role('button', name='Cancel')
        self.change_status = page.get_by_role('button', name='Change Status')
        self.deactivate_btn = page.get_by_role('button', name='Deactivate')
        self.search_filed = page.get_by_role('textbox', name='Search')
        self.search_results = page.get_by_role('row', name='Email')
        self.no_user_found = page.get_by_role('cell', name='No users found')
        self.select_roles = page.get_by_role('button', name='Select roles')
        self.create_user_heading = page.get_by_role('heading', name='Create User')
        self.email_address_list = page.locator("div[class*='truncate']")
        self.invalid_email_error = page.get_by_text('Invalid email address')
        self.min_password_error = page.get_by_text('Password must be at least 8')
        self.passwords_must_match_error = page.get_by_text('Passwords must match')
        self.user_already_exists_error = page.get_by_text('User already exists in this')
        self.close_modal_btn = page.locator('div').filter(has_text='Create User').get_by_role('button').first
        self.all_roles_list_options = page.locator("div[class*='hover:bg-gray-50'] span")
        self.pagination_dropdown = page.locator("#itemsPerPage")
        self.save_roles_btn = page.get_by_role('button', name='Save Roles')
        self.enable_roles_arrow = page.locator("svg[class*='flex-shrink']")
        self.delete_btn = page.get_by_role('button', name='Delete')
        self.delete_confirm_input = page.get_by_role('textbox')
        self.new_password = page.get_by_role('textbox', name= 'New Password' )
        self.save_changes = page.get_by_role('button', name= 'Save Changes' )
        self.sign_in_btn = page.get_by_role('button', name= 'Sign in' )


    def return_checkbox_click(self, email_address):
        return self.page.locator("td").filter(has_text=email_address).locator("xpath=preceding-sibling::td//input[@type='checkbox']")

    def return_user_role(self, email_address):
        return self.page.locator(f"td:has(div:has-text('{email_address}')) ~ td span[class*='user-role']")

    def return_status(self, email_address):
        return self.page.locator(f"td:has(div:has-text('{email_address}')) ~ td span[data-testid*='flowbite-badge'] span")

    def return_roles(self, roles):
        return self.page.locator("div[class*='hover:bg-gray-50']").filter(has_text=roles).first

    def return_edit_roles(self, roles):
        return self.page.locator("label[class*='hover:bg-gray-50']").filter(has_text=roles).first

    def return_row_edit_button(self, user_name):
        return self.page.get_by_role('row', name=user_name).get_by_role('button')