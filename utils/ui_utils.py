import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UIUtils:
    def __init__(self, page):
        self.page = page
        self.logger = logger

    def goto(self, url):
        """
        Navigates to the specified URL.
        """
        self.page.goto(url)
        
    def click_element(self, locator, timeout=3000, force=False):
        """
        Click the given locator.
        """
        try:
            locator.click(timeout=timeout, force=force)
            self.logger.info("Element clicked successfully.")
        except Exception as e:
            self.logger.error(f"Failed to click element: {e}")
            raise

    def double_click_element(self, locator, timeout=3000):
        """
        Double-clicks an element specified by the locator.
        """
        try:
            locator.dblclick(timeout=timeout)
            self.logger.info("Element double clicked successfully.")
        except Exception as e:
            self.logger.error(f"Failed to double click element: {e}")
            raise

    def hover_element(self, locator, timeout=3000):
        """
        Hovers over an element specified by the locator.
        """
        self.page.hover(locator, timeout=timeout)

    def fill_input(self, locator, value, timeout=3000):
        """
        Fills an input element specified by the locator with the given value.
        """
        try:
            locator.fill(value, timeout=timeout)
            self.logger.info(f"Input filled with value: {value}")
        except Exception as e:
            self.logger.error(f"Failed to fill input: {e}")
            raise

    def type_text(self, locator, value, timeout=3000):
        """
        Types text into an element specified by the locator.
        """
        self.page.type(locator, value, timeout=timeout)

    def press_key(self, locator, key, timeout=3000):
        """
        Presses a key on an element specified by the locator.
        """
        self.page.press(locator, key, timeout=timeout)

    def select_option(self, locator, value, timeout=3000):
        locator.select_option(value, timeout=timeout)

    def check_checkbox(self, locator, timeout=3000):
        """
        Checks a checkbox element specified by the locator.
        """
        self.page.check(locator, timeout=timeout)

    def uncheck_checkbox(self, locator, timeout=3000):
        """
        Unchecks a checkbox element specified by the locator.
        """
        self.page.uncheck(locator, timeout=timeout)

    def get_text(self, locator, timeout=3000):
        """
        Gets the text of an element specified by the locator.
        """
        return self.page.text_content(locator, timeout=timeout)

    def get_attribute(self, locator, attribute_name, timeout=3000):
        """
        Gets the value of an attribute of an element specified by the locator.
        """
        return self.page.get_attribute(locator, attribute_name, timeout=timeout)

    def is_element_visible(self, locator, timeout=5000):
        """
        Checks if an element specified by the locator is visible.
        """
        try:
            return locator.is_visible(timeout=timeout)
        except Exception as e:
            self.logger.error(f"Error checking visibility of element: {e}")
            return False

    def is_element_enabled(self, locator):
        """
        Checks if an element specified by the locator is enabled.
        """
        try:
            return locator.is_enabled()
        except Exception as e:
            self.logger.error(f"Error checking enabled status of element: {e}")
            return False

    def is_element_disabled(self, locator):  
        """
        Checks if an element specified by the locator is disabled.
        """
        try:
            return locator.is_disabled()
        except Exception as e:
            self.logger.error(f"Error checking disabled status of element: {e}")
            return True

    def grab_text_from_all(self, locator):
        """
        Returns the text of all matching elements as a list.
        """
        return [element.text_content().strip() for element in locator.all()]

    def element_wait_for(self, locator, state="visible", timeout = 5000):
        try:
            locator.wait_for(state=state, timeout=timeout)
        except Exception as e:
            self.logger.error(f"Element did not reach state '{state}' after {timeout}ms → {locator}. Error: {e}")
            raise

    def drag_and_drop(self, source, target):
        source.wait_for(state="visible")
        target.wait_for(state="visible")
        source_box = source.bounding_box()
        target_box = target.bounding_box()
        if not source_box or not target_box:
            raise Exception("Unable to locate source or target connector.")
        self.page.mouse.move(
            source_box["x"] + source_box["width"] / 2,
            source_box["y"] + source_box["height"] / 2,
        )
        self.page.wait_for_timeout(100)
        self.page.mouse.down()
        self.page.wait_for_timeout(100)
        self.page.mouse.move(
            target_box["x"] + target_box["width"] / 2,
            target_box["y"] + target_box["height"] / 2,
            steps=50,
        )
        self.page.wait_for_timeout(100)
        self.page.mouse.up()

    def wait_for_visible_if_exists(self, locator, timeout=5000):
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def smart_wait(self, timeout = 20000):
        """
        Wait until the page is fully loaded.
        """
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            self.page.wait_for_timeout(2000)
            self.logger.info("Smart wait completed successfully.")
        except Exception as e:
            self.logger.error(f"Smart wait failed: {e}")
            raise

    def scroll_into_view_if_needed(self, locator):
        """
        Scrolls the element into the visible area if it is not already visible.
        """
        try:
            locator.scroll_into_view_if_needed()
            self.logger.info("Element scrolled into view successfully.")
        except Exception as e:
            self.logger.error(
                f"Failed to scroll element into view. Error: {e}"
            )
            raise

    def wait_for_element_with_retry(self, locator, attempts=3, timeout=2000):
        """
        Waits for an element to become visible with multiple retry attempts.
        """
        for attempt in range(1, attempts + 1):
            try:
                self.logger.info(f"Waiting for element - Attempt {attempt}/{attempts}")
                self.element_wait_for(locator, timeout=timeout)
                if self.is_element_visible(locator):
                    self.logger.info(f"Element became visible on attempt {attempt}.")
                    return True
            except Exception as e:
                self.logger.warning(f"Element not visible on attempt {attempt}: {e}")
        self.logger.error(f"Element was not visible after {attempts} attempts.")
        return False

    def keyboard_press(self, key):
        """
        Presses a key on the keyboard.
        """
        try:
            self.page.keyboard.press(key)
            self.logger.info(f"Key '{key}' pressed successfully.")
        except Exception as e:
            self.logger.error(f"Failed to press key: {e}")
            raise