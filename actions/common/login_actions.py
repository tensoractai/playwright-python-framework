from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils
from utils.helpers import Helpers

class LoginActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)
        self.helpers = Helpers(page)

    def perform_login(self, url=None, email=None, password=None):
        self.ui_utils.goto(url)
        self.ui_utils.smart_wait()
        self.ui_utils.fill_input(self.page_factory.login_page.email_input, email)
        self.ui_utils.fill_input(self.page_factory.login_page.password_input, password)
        self.ui_utils.click_element(self.page_factory.login_page.sign_in_button)
        self.ui_utils.element_wait_for(self.page_factory.login_page.back_to_login, state="visible", timeout=10000)
        back_to_login_visible = self.ui_utils.is_element_visible(self.page_factory.login_page.back_to_login, timeout=10000)
        print(f"Back to Login button visibility: {back_to_login_visible}")
        if back_to_login_visible:
            print("Back to Login button is visible")
        else:
            raise Exception("Back to Login button is not visible after login attempt.")

    def perform_login_new_user(self, url=None, email=None, password=None):
        self.ui_utils.goto(url)
        self.ui_utils.smart_wait()
        self.ui_utils.fill_input(self.page_factory.login_page.email_input, email)
        self.ui_utils.fill_input(self.page_factory.login_page.password_input, password)
        self.ui_utils.click_element(self.page_factory.login_page.sign_in_button)
        self.ui_utils.smart_wait()

    def use_different_email_OTP(self, email_address, password):
        self.ui_utils.click_element(self.page_factory.login_page.different_email_for_otp_link)
        self.ui_utils.element_wait_for(self.page_factory.login_page.email_address_input, state="visible", timeout=10000)
        self.ui_utils.fill_input(self.page_factory.login_page.email_address_input, email_address)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.login_page.send_code_button)
        self.ui_utils.element_wait_for(self.page_factory.login_page.enter_otp_input, state="visible", timeout=10000)
        enter_otp_visible = self.ui_utils.is_element_visible(self.page_factory.login_page.enter_otp_input, timeout=10000)
        if enter_otp_visible:
            print("Enter OTP input is visible")
        else:
            raise Exception("Enter OTP input is not visible after clicking 'Send code to a different email' link.")
        otp_mail_tm = self.helpers.fetch_otp_from_mail_tm(email_address, password)
        self.ui_utils.smart_wait()
        for i, digit in enumerate(otp_mail_tm):   
            self.ui_utils.fill_input(self.page_factory.login_page.enter_otp(i), digit)
        self.ui_utils.click_element(self.page_factory.login_page.sign_In_button)
        self.ui_utils.element_wait_for(self.page_factory.login_page.organization_card, state="visible", timeout=10000)
        org_card = self.ui_utils.is_element_visible(self.page_factory.login_page.organization_card, timeout=10000)
        if org_card:
            print("Organization card is visible")
        else:
            raise Exception("Organization card is not visible.")

    def select_organization(self, company_name, organization_name):
        self.ui_utils.click_element(self.page_factory.login_page.get_organization_card(company_name))
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.login_page.get_organization_option(organization_name))
        self.ui_utils.click_element(self.page_factory.login_page.continue_button)
        self.ui_utils.element_wait_for(self.page_factory.login_page.home_sidebar_link, state="visible", timeout=10000)
        self.ui_utils.click_element(self.page_factory.login_page.home_sidebar_link)
        self.ui_utils.element_wait_for(self.page_factory.login_page.home_page_welcome, state="visible", timeout=10000)
        home_sidebar_visible = self.ui_utils.is_element_visible(self.page_factory.login_page.home_page_welcome, timeout=10000)
        print(f"Home sidebar link visibility: {home_sidebar_visible}")
        if home_sidebar_visible:
            print("Home sidebar link is visible")
        else:
            raise Exception("Home sidebar link is not visible after login attempt.")

    def switch_role(self, role_name="Super User"):
        self.ui_utils.click_element(self.page_factory.login_page.admin_profile_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.login_page.switch_role_btn)
        self.ui_utils.smart_wait()
        role_locator = self.page_factory.login_page.return_user_role(role_name)
        self.ui_utils.click_element(role_locator)
        self.ui_utils.smart_wait()
        self.ui_utils.element_wait_for(self.page_factory.login_page.home_page_welcome, state="visible", timeout=10000)
        home_sidebar_visible = self.ui_utils.is_element_visible(self.page_factory.login_page.home_page_welcome, timeout=10000)
        print(f"Home sidebar link visibility: {home_sidebar_visible}")
        if home_sidebar_visible:
            print("Home sidebar link is visible")
        else:
            raise Exception("Home sidebar link is not visible after login attempt.")
        self.ui_utils.click_element(self.page_factory.login_page.admin_profile_btn)
        self.ui_utils.smart_wait()

    def perform_logout(self):
        self.ui_utils.click_element(self.page_factory.login_page.admin_profile_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.login_page.logout_icon)
        self.ui_utils.click_element(self.page_factory.login_page.logout_btn)
        self.ui_utils.smart_wait()