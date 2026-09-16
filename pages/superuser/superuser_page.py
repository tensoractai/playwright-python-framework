from utils.ui_utils import UIUtils

class SuperUserPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.companies_menu = page.get_by_role('link', name='Companies')
        self.add_company_btn = page.get_by_role('button', name='Add Company')
        self.company_name_input = page.get_by_role('textbox', name='Company Name *')
        self.legal_name_input = page.get_by_role('textbox', name='Legal Name')
        self.email_domain_input = page.get_by_role('textbox', name='Email Domain *')
        self.select_roles_btn = page.get_by_role('button', name='Select roles')
        self.add_new_company_heading = page.get_by_role('heading', name='Add New Company')
        self.add_company_submit_btn = page.get_by_role('button', name='Add company')
        self.save_btn = page.get_by_role('button', name='Save')
        self.select_company_btn = page.get_by_role('button', name='Select Company')
        self.modal_text_click = page.get_by_text('Full Name*:Email*:Password*:').first
        self.company_name_list = page.locator("td[class*='medium truncate']")
        self.acknowledge_delete_checkbox = page.get_by_role('checkbox', name='Acknowledge to delete company')
        self.delete_company_btn = page.get_by_role('button', name='Delete Company')
        self.type_delete_input = page.get_by_role('textbox', name="type 'delete a company'")
        self.confirm_delete_btn = page.get_by_role('button', name='Delete')

    def return_company_cell(self, company_name):
        return self.page.locator(f"td[data-testid='companies-col-name']:has-text('{company_name}')")

    def return_role_checkbox(self, role_name):
        return self.page.get_by_role('checkbox', name=role_name)

    def return_role_div(self, role_name):
        return self.page.locator("div[class*='hover:bg-gray-50']").filter(has_text=role_name).first

    def return_company_div(self, company_name):
        return self.page.locator("div[class*='hover:bg-gray-50']").filter(has_text=company_name).first
