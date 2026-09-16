import re
from utils.ui_utils import UIUtils

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.email_input       = page.get_by_role("textbox", name="Email")
        self.password_input    = page.get_by_role("textbox", name="Password")
        self.sign_in_button    = page.get_by_role("button",  name="Sign in", exact=True)
        self.sign_In_button    = page.get_by_role("button",  name="Sign In", exact=True)
        self.organization_card = page.get_by_role("heading", name="Select Your Organization")
        self.company_admin_role = page.get_by_role("paragraph").filter(has_text=re.compile(r"^Company Admin$"))
        self.continue_button   = page.get_by_role("button", name="Continue")
        self.home_sidebar_link = page.get_by_role("link", name="Home")
        self.back_to_login = page.locator("button:has-text('Back to Login')")
        self.home_icon = page.get_by_text("Home")
        self.home_page_welcome = page.get_by_role('heading', name = 'Welcome to' ) ###Checkkk TensorAct is converted to Image 
        self.different_email_for_otp_link = page.get_by_role('button', name = 'Send code to a different email' )
        self.email_address_input = page.get_by_role('textbox', name = 'Email Address' )
        self.send_code_button = page.get_by_role('button', name = 'Send Code' )
        self.enter_otp_input = page.get_by_text("Enter OTP", exact=True)
        self.admin_profile_btn = page.locator("div[class*='full shadow-sm']")
        self.switch_role_btn = page.locator("svg[class*='lucide-user']")
        self.logout_icon = page.locator('div:nth-child(6) > .relative > .p-2')
        self.logout_btn =  page.get_by_role("button", name="Logout")
        self.account_not_active_error = page.get_by_text('Your account is not active.')

    def get_organization_card(self, company_name):
        return self.page.get_by_role("heading", name=company_name)
    
    def get_organization_option(self, organization_name):
        return self.page.get_by_text(organization_name, exact=True)

    def enter_otp(self, index):
        return self.page.locator(f'#otp-digit-{index}')

    def return_user_role(self, role):
        return  self.page.get_by_role('button', name= role )