from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils
from utils.helpers import Helpers

class ReviewerActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)
        self.helpers = Helpers(page)

    def is_annotation_present(self, annotator):
        self.ui_utils.click_element(self.page_factory.reviewer_page.annotation_dropdown)
        self.ui_utils.click_element(self.page_factory.reviewer_page.click_annotator_dropdown(annotator))
        self.ui_utils.smart_wait()
        self.wait_for_iframe_ready()

    def wait_for_iframe_ready(self, timeout=180000):
        iframe = self.page_factory.reviewer_page.iframe
        loading = self.page_factory.reviewer_page.loading_spinner
        visible = self.ui_utils.wait_for_visible_if_exists(loading, timeout=10000)
        if visible:
            self.ui_utils.element_wait_for(loading, state="hidden", timeout=timeout)
            message = "Iframe loaded successfully."
        self.ui_utils.smart_wait()
