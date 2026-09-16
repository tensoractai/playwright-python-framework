from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils
from utils.helpers import Helpers

class CommonActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)
        self.helpers = Helpers(page)

    def validate_toast_msg(self, expected_msg):
        toast_locator = self.page_factory.files_page.return_toast_msg_locator(expected_msg)
        self.ui_utils.element_wait_for(toast_locator,timeout=10000)
        toast_visible = self.ui_utils.is_element_visible(toast_locator,timeout=10000)
        assert toast_visible is True, f"Toast message '{expected_msg}' is not visible"
