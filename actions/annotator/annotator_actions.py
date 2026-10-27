from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils
from utils.helpers import Helpers

class AnnotatorActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)
        self.helpers = Helpers(page)
        self.frame = self.page_factory.annotator_page.frame

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
        Draws a bounding box or line on the image inside the Annotator iframe.

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

        box = img_element.bounding_box()
        if box:
            start_page_x = box["x"] + start_x
            start_page_y = box["y"] + start_y
            end_page_x = box["x"] + end_x
            end_page_y = box["y"] + end_y

            # Perform mouse drag with intermediate mousemove steps (draws line once)
            self.ui_utils.page.mouse.move(start_page_x, start_page_y)
            self.ui_utils.page.mouse.down()
            self.ui_utils.page.mouse.move(end_page_x, end_page_y, steps=20)
            self.ui_utils.page.mouse.up()
            self.ui_utils.smart_wait()
        else:
            img_element.click(position={"x": start_x, "y": start_y}, force=True)
            self.ui_utils.smart_wait()
            img_element.click(position={"x": end_x, "y": end_y}, force=True)
            self.ui_utils.smart_wait()

    def perform_annotation_for_image_files(self, objects, from_coords, to_coords):
        target_object = self.page_factory.annotator_page.return_objects_click(objects)
        target_object.wait_for(state="visible", timeout=10000)
        self.ui_utils.click_element(target_object)
        self.ui_utils.smart_wait()
        self.draw_bounding_box(from_coords, to_coords)
        self.ui_utils.keyboard_press('Enter')
        self.ui_utils.smart_wait()

    def edit_old_annotation(self, object_name, from_coords=None, to_coords=None, edit_coords=None):
        labels_section = self.frame.locator("#labelsSection")
        if not self.ui_utils.is_element_visible(labels_section, timeout=2000):
            labels_bar = self.page_factory.annotator_page.labels_header_bar
            if self.ui_utils.is_element_visible(labels_bar, timeout=3000):
                self.ui_utils.click_element(labels_bar)
                self.ui_utils.smart_wait()

        img_element = self.page_factory.annotator_page.main_video_image
        img_element.wait_for(state="visible", timeout=10000)

        # Click label row for object in labelsSection
        label_item = self.page_factory.annotator_page.get_label_item(object_name)
        label_item.wait_for(state="visible", timeout=10000)
        label_item.click(force=True)
        self.ui_utils.smart_wait()

        # Activate Brush tool: click Brush button (or fallback to keyboard shortcut 'f')
        brush_btn = self.page_factory.annotator_page.brush_button
        if self.ui_utils.is_element_visible(brush_btn, timeout=2000):
            self.ui_utils.click_element(brush_btn)
        else:
            self.ui_utils.keyboard_press('f')
        self.ui_utils.smart_wait()

        # Determine start and end coordinates
        if from_coords and to_coords:
            start_x, start_y = from_coords[0], from_coords[1]
            end_x, end_y = to_coords[0], to_coords[1]
        elif edit_coords and len(edit_coords) >= 2:
            start_x, start_y = edit_coords[0][0], edit_coords[0][1]
            end_x, end_y = edit_coords[-1][0], edit_coords[-1][1]
        elif edit_coords and len(edit_coords) == 1:
            start_x, start_y = edit_coords[0][0], edit_coords[0][1]
            end_x, end_y = start_x, start_y
        else:
            start_x, start_y = 680, 165
            end_x, end_y = 680, 470

        # Perform mouse drag from start to end point on Main Image to draw line
        box = img_element.bounding_box()
        if box:
            if edit_coords and isinstance(edit_coords, (list, tuple)) and len(edit_coords) > 1 and isinstance(edit_coords[0], (list, tuple)):
                start_page_x = box["x"] + edit_coords[0][0]
                start_page_y = box["y"] + edit_coords[0][1]
                self.ui_utils.page.mouse.move(start_page_x, start_page_y)
                self.ui_utils.page.mouse.down()
                for coord in edit_coords[1:]:
                    pt_x = box["x"] + coord[0]
                    pt_y = box["y"] + coord[1]
                    self.ui_utils.page.mouse.move(pt_x, pt_y, steps=25)
                self.ui_utils.page.mouse.up()
                self.ui_utils.smart_wait()
            else:
                start_page_x = box["x"] + start_x
                start_page_y = box["y"] + start_y
                end_page_x = box["x"] + end_x
                end_page_y = box["y"] + end_y

                self.ui_utils.page.mouse.move(start_page_x, start_page_y)
                self.ui_utils.page.mouse.down()
                self.ui_utils.page.mouse.move(end_page_x, end_page_y, steps=25)
                self.ui_utils.page.mouse.up()
                self.ui_utils.smart_wait()
        else:
            img_element.click(position={"x": start_x, "y": start_y}, force=True)
            self.ui_utils.smart_wait()
            img_element.click(position={"x": end_x, "y": end_y}, force=True)
            self.ui_utils.smart_wait()

        # Press Enter to finalize annotation line
        self.ui_utils.keyboard_press('Enter')
        self.ui_utils.smart_wait()

    def erase_annotation(self, object_name, erase_coords=None):
        labels_section = self.frame.locator("#labelsSection")
        if not self.ui_utils.is_element_visible(labels_section, timeout=2000):
            labels_bar = self.page_factory.annotator_page.labels_header_bar
            if self.ui_utils.is_element_visible(labels_bar, timeout=3000):
                self.ui_utils.click_element(labels_bar)
                self.ui_utils.smart_wait()

        label_item = self.page_factory.annotator_page.get_label_item(object_name)
        label_item.wait_for(state="visible", timeout=10000)
        label_item.click(force=True)
        self.ui_utils.smart_wait()

        img_element = self.page_factory.annotator_page.main_video_image
        img_element.wait_for(state="visible", timeout=10000)

        # Activate Eraser tool: try eraser button, or keyboard shortcut 'h' (Eraser is 'H', never 'e' which selects Fire Hydrant)
        eraser_btn = self.page_factory.annotator_page.eraser_button
        if self.ui_utils.is_element_visible(eraser_btn, timeout=2000):
            self.ui_utils.click_element(eraser_btn)
        else:
            self.ui_utils.keyboard_press('h')
        self.ui_utils.smart_wait()

        box = img_element.bounding_box()

        if erase_coords:
            if isinstance(erase_coords, (list, tuple)):
                if len(erase_coords) > 0 and isinstance(erase_coords[0], (list, tuple)):
                    if box:
                        start_page_x = box["x"] + erase_coords[0][0]
                        start_page_y = box["y"] + erase_coords[0][1]
                        self.ui_utils.page.mouse.move(start_page_x, start_page_y)
                        self.ui_utils.page.mouse.down()
                        for coord in erase_coords[1:]:
                            pt_x = box["x"] + coord[0]
                            pt_y = box["y"] + coord[1]
                            self.ui_utils.page.mouse.move(pt_x, pt_y, steps=25)
                        self.ui_utils.page.mouse.up()
                        self.ui_utils.smart_wait()
                else:
                    img_element.click(position={"x": erase_coords[0], "y": erase_coords[1]}, force=True)
        else:
            img_element.click(force=True)

        self.ui_utils.keyboard_press('Enter')
        self.ui_utils.smart_wait()

    def delete_annotation(self, object_name):
        labels_section = self.frame.locator("#labelsSection")
        if not self.ui_utils.is_element_visible(labels_section, timeout=2000):
            labels_bar = self.page_factory.annotator_page.labels_header_bar
            if self.ui_utils.is_element_visible(labels_bar, timeout=3000):
                self.ui_utils.click_element(labels_bar)
                self.ui_utils.smart_wait()

        label_item = self.page_factory.annotator_page.get_label_item(object_name)
        label_item.wait_for(state="visible", timeout=10000)
        label_item.click(force=True)
        self.ui_utils.smart_wait()

        # Press Delete to delete selected annotation
        self.ui_utils.keyboard_press('Delete')
        self.ui_utils.smart_wait()

        
