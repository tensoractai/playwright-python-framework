from utils.ui_utils import UIUtils

class AnnotatorPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.frame = page.frame_locator("iframe")
        self.home_menu = page.get_by_role('link', name="Home")
        self.tasks_menu = page.get_by_role("link", name="Task")
        self.project_name_list = page.locator("span[class*='truncate']")
        self.files_name_list = page.locator("td[class*='truncate']")
        self.email_list = page.locator("div[class*='truncate']")
        self.claim_button = page.get_by_role("button", name="Claim Task")
        self.ok_button = page.get_by_role("button", name="Ok")
        self.set_text_button = self.frame.get_by_role("button", name="Set Text")
        self.submit_annotation = self.frame.get_by_role("button", name="Submit Annotation")
        self.save_and_exit_button = page.get_by_role("button", name="Save and exit")
        self.begin_recording = self.frame.locator("div[class*='trackaddrecording']")
        self.stop_recording = self.frame.locator("div[class*='trackaddrecording trackrecording']")
        self.input_text_field = self.frame.get_by_role("textbox", name="Enter transcription text")
        self.current_task_heading = page.get_by_role("heading", name="Current Tasks")
        self.back_button = page.locator("button[class*='cursor-pointer']")
        self.search_input = page.get_by_placeholder("search")
        self.transcription = self.frame.locator("tr[class*='reporttr'] td")
        self.step_forward = self.frame.locator("i[class*='step-forward']")
        self.step_backward = self.frame.locator("i[class*='step-backward']")
        self.auto_save_toast = self.page.get_by_text('Auto-saved successfully')



    def click_project_name(self, project_name):
        return self.page.get_by_text(project_name, exact=True)
    
    def click_transcription(self, transcription):
        return self.frame.get_by_role('cell', name= transcription)