from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils

class SuperUserActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)

    def click_companies_menu(self):
        self.ui_utils.click_element(self.page_factory.superuser_page.companies_menu)
        self.ui_utils.smart_wait()

    def click_add_company(self):
        self.ui_utils.click_element(self.page_factory.superuser_page.add_company_btn)
        self.ui_utils.smart_wait()

    def create_company(self, company_name, legal_name, email_domain, initial_role=None):
        self.ui_utils.fill_input(self.page_factory.superuser_page.company_name_input, company_name)
        self.ui_utils.fill_input(self.page_factory.superuser_page.legal_name_input, legal_name)
        self.ui_utils.fill_input(self.page_factory.superuser_page.email_domain_input, email_domain)
        if initial_role:
            self.ui_utils.click_element(self.page_factory.superuser_page.select_roles_btn)
            self.ui_utils.click_element(self.page_factory.superuser_page.return_role_div(initial_role))
            self.ui_utils.click_element(self.page_factory.superuser_page.add_new_company_heading)
        self.ui_utils.click_element(self.page_factory.superuser_page.add_company_submit_btn)
        self.ui_utils.smart_wait()

    def select_company_cell(self, company_name):
        self.ui_utils.click_element(self.page_factory.superuser_page.return_company_cell(company_name).first)
        self.ui_utils.smart_wait()

    def check_company_roles(self, roles_list):
        for role in roles_list:
            checkbox = self.page_factory.superuser_page.return_role_checkbox(role)
            if self.ui_utils.is_element_visible(checkbox):
                checkbox.check()
            else:
                role_div = self.page_factory.superuser_page.return_role_div(role)
                self.ui_utils.click_element(role_div)
                checkbox.check()
        self.ui_utils.click_element(self.page_factory.superuser_page.save_btn)
        self.ui_utils.smart_wait()

    def select_company_for_user(self, company_name):
        self.ui_utils.click_element(self.page_factory.superuser_page.select_company_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.superuser_page.return_company_div(company_name))
        self.ui_utils.smart_wait()

    def delete_company(self):
        self.page_factory.superuser_page.acknowledge_delete_checkbox.check()
        self.ui_utils.click_element(self.page_factory.superuser_page.delete_company_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.fill_input(self.page_factory.superuser_page.type_delete_input, "delete a company")
        self.ui_utils.click_element(self.page_factory.superuser_page.confirm_delete_btn)
        self.ui_utils.smart_wait()
