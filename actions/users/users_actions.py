from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils

class UsersActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)

    def click_users_menu(self):
        self.ui_utils.click_element(self.page_factory.users_page.user_menu)
        self.ui_utils.smart_wait()

    def click_create_user(self):
        self.ui_utils.click_element(self.page_factory.users_page.create_user)
        self.ui_utils.smart_wait()

    def fill_user_form(self, full_name, email, password, confirm_password):
        self.ui_utils.fill_input(self.page_factory.users_page.enter_name, full_name)
        self.ui_utils.fill_input(self.page_factory.users_page.enter_email, email)
        self.ui_utils.fill_input(self.page_factory.users_page.enter_password, password)
        self.ui_utils.fill_input(self.page_factory.users_page.confirm_password, confirm_password)

    def enable_allow_mfa_email(self):
        self.ui_utils.click_element(self.page_factory.users_page.allow_MFA_btn)
        self.ui_utils.smart_wait()

    def create_roles(self, roles):
        if isinstance(roles, str):
            roles = [roles]
        self.ui_utils.click_element(self.page_factory.users_page.select_roles)
        for role in roles:
            self.ui_utils.click_element(self.page_factory.users_page.return_roles(role), force=True)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.users_page.create_user_heading)

    def submit_create_user(self):
        self.ui_utils.click_element(self.page_factory.users_page.create_user)
        self.ui_utils.smart_wait()

    def search_user(self, search_text):
        self.ui_utils.click_element(self.page_factory.users_page.search_filed)
        self.ui_utils.fill_input(self.page_factory.users_page.search_filed, search_text)
        self.ui_utils.smart_wait()

    def set_users_pagination(self, num_of_items):
        self.ui_utils.select_option(self.page_factory.users_page.pagination_dropdown, str(num_of_items))
        self.ui_utils.smart_wait()

    def deactivate_user(self):
        self.ui_utils.click_element(self.page_factory.users_page.change_status)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.users_page.deactivate_btn)
        self.ui_utils.smart_wait()

    def edit_user_roles(self, user_name, roles_to_toggle):
        if isinstance(roles_to_toggle, str):
            roles_to_toggle = [roles_to_toggle]
        self.ui_utils.click_element(self.page_factory.users_page.return_row_edit_button(user_name))
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.users_page.enable_roles_arrow)
        for role in roles_to_toggle:
            self.ui_utils.click_element(self.page_factory.users_page.return_edit_roles(role), force=True)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.users_page.save_roles_btn)
        self.ui_utils.smart_wait()

    def delete_user(self):
        self.ui_utils.click_element(self.page_factory.users_page.delete_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.users_page.delete_confirm_input)
        self.ui_utils.fill_input(self.page_factory.users_page.delete_confirm_input, "DELETE")
        self.ui_utils.click_element(self.page_factory.users_page.delete_btn)
        self.ui_utils.smart_wait()

    def user_settings_changePassword(self, password):
        self.ui_utils.click_element(self.page_factory.users_page.new_password)
        self.ui_utils.fill_input(self.page_factory.users_page.new_password, password)
        self.ui_utils.click_element(self.page_factory.users_page.confirm_password)
        self.ui_utils.fill_input(self.page_factory.users_page.confirm_password, password)
        self.ui_utils.click_element(self.page_factory.users_page.save_changes)
        self.ui_utils.smart_wait()
        
       
