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
        self.ui_utils.click_element(self.page_factory.annotator_page.input_text_field)
        self.ui_utils.fill_input(self.page_factory.annotator_page.input_text_field, new_transcription)
        self.ui_utils.click_element(self.page_factory.annotator_page.set_text_button)

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

    def draw_bounding_box(self, from_coords, to_coords):
        """
        Draws a bounding box on the image inside the Annotator iframe.

        :param from_coords: Tuple/list (x1, y1) or dict {"x": x1, "y": y1} for start position.
        :param to_coords: Tuple/list (x2, y2) or dict {"x": x2, "y": y2} for end position.
        """
        if isinstance(from_coords, (list, tuple)):
            start_x, start_y = from_coords[0], from_coords[1]
        elif isinstance(from_coords, dict):
            start_x, start_y = from_coords.get("x", 0), from_coords.get("y", 0)
        else:
            raise ValueError("from_coords must be a tuple/list (x, y) or dict {'x': x, 'y': y}")

        if isinstance(to_coords, (list, tuple)):
            end_x, end_y = to_coords[0], to_coords[1]
        elif isinstance(to_coords, dict):
            end_x, end_y = to_coords.get("x", 0), to_coords.get("y", 0)
        else:
            raise ValueError("to_coords must be a tuple/list (x, y) or dict {'x': x, 'y': y}")

        img_element = self.page_factory.annotator_page.main_video_image
        img_element.wait_for(state="visible", timeout=10000)

        # Move to start position, press mouse down, drag to end position, and release
        img_element.hover(position={"x": start_x, "y": start_y})
        self.ui_utils.page.mouse.down()
        img_element.hover(position={"x": end_x, "y": end_y})
        self.ui_utils.page.mouse.up()
        self.ui_utils.smart_wait()

    def perform_annotation_for_image_files(self, objects, from_coords, to_coords):
        self.ui_utils.click_element(self.page_factory.annotator_page.return_objects_click(objects))
        self.ui_utils.smart_wait()
        self.draw_bounding_box(from_coords, to_coords)
        
