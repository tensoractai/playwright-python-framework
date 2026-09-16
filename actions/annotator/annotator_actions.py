from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils
from utils.helpers import Helpers

class AnnotatorActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)
        self.helpers = Helpers(page)

    def annontate_files(self, input_text, fast_forward = 0):
        self.ui_utils.element_wait_for(self.page_factory.annotator_page.begin_recording, timeout = 10000)
        for index in range(int(fast_forward)):
            self.ui_utils.click_element(self.page_factory.annotator_page.step_forward)
        self.ui_utils.click_element(self.page_factory.annotator_page.begin_recording)
        self.ui_utils.smart_wait()
        self.ui_utils.element_wait_for(self.page_factory.annotator_page.stop_recording, timeout = 10000)
        self.ui_utils.click_element(self.page_factory.annotator_page.stop_recording)
        self.ui_utils.click_element(self.page_factory.annotator_page.input_text_field)
        self.ui_utils.fill_input(self.page_factory.annotator_page.input_text_field, input_text)
        self.ui_utils.click_element(self.page_factory.annotator_page.set_text_button)
        self.ui_utils.smart_wait()

    def perform_save_exit(self):
        def handle_dialog(dialog):
            print(f"Dialog message: {dialog.message}")
            dialog.accept()

        self.page_factory.annotator_page.page.once("dialog", handle_dialog)
        self.ui_utils.click_element(self.page_factory.annotator_page.save_and_exit_button)
        # If custom HTML confirmation popup overlay is visible, click OK
        ok_btn = self.page_factory.files_page.page.get_by_role('button', name='OK', exact=True)
        if self.ui_utils.is_element_visible(ok_btn, timeout=3000):
            self.ui_utils.click_element(ok_btn)
            self.ui_utils.smart_wait()

    def perform_edit_transcription(self, old_transcription, new_transcription):
        self.ui_utils.double_click_element(self.page_factory.annotator_page.click_transcription(old_transcription))
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.annotator_page.input_text_field)
        self.ui_utils.fill_input(self.page_factory.annotator_page.input_text_field, new_transcription)
        self.ui_utils.click_element(self.page_factory.annotator_page.set_text_button)
        self.ui_utils.smart_wait()

    def perform_delete_transcription(self, transcription):
        self.ui_utils.click_element(self.page_factory.annotator_page.click_transcription(transcription))
        self.ui_utils.smart_wait()
        self.ui_utils.keyboard_press('Delete')
        self.ui_utils.smart_wait()

    def perform_auto_save_functionality(self):
        self.ui_utils.element_wait_for(self.page_factory.annotator_page.auto_save_toast, timeout = 35000)
        toast_visible = self.ui_utils.is_element_visible(self.page_factory.annotator_page.auto_save_toast)
        if toast_visible:
            return True
        else:
            return False