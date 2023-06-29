import allure
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.webdriver.support.select import Select

class PageBase:

    def __init__(self, driver):
        self.driver = driver
    def find_element(self, locator, clickable = False):

        logging.info(f'Find element {locator}')
        if clickable:
            web_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator))
        else:
            web_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(locator))
        return web_element

    def send_key(self, locator, key_value, select_all = False):

        logging.info(f'Send key {key_value} for element {locator}')
        web_element = self.find_element(locator, clickable=True)
        if select_all == True:
            web_element.clear()
        web_element.send_keys(key_value)

    def find_elements(self, locator):

        logging.info(f'Find elements {locator}')
        try:
            web_element = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(locator))
            return web_element
        except TimeoutException:
            logging.warning(f'Elements not found: {locator}')
            return []

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def confirm_popup(self):
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        title = alert.text
        alert.accept()
        logging.info(f'return message: {title}')
        return title

    def save_snapshot(self):
        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot',attachment_type=allure.attachment_type.PNG)

    @allure.step('Switch to iFrame')
    def switch_to_iframe(self, iframe):
        logging.info(f'Switch to iFrame, iframe name is {iframe}')
        self.driver.switch_to.frame(self.find_element(self.select_iframe(iframe)))
        logging.info(f'enter iframe successful')

    @allure.step('Switch to main page')
    def switch_to_default(self):
        self.driver.switch_to.default_content()
        logging.info(f'back to default successful')

    @allure.step("Send value to iframe's field")
    def send_key_in_iframe(self, iframe, locator, key_value, select_all=False):

        logging.info(f'Send key {key_value} for element {locator} in iframe={iframe}')
        self.switch_to_iframe(iframe)
        web_element = self.find_element(locator, clickable=True)
        if select_all == True:
            web_element.clear()
        web_element.send_keys(key_value)
        self.switch_to_default()

    def select_dropdown(self, locator, text):
        logging.info(f'Select text is {text} in element {locator}')
        select = Select(self.find_element(locator))
        select.select_by_visible_text(text)

    def switch_page(self):
        current_window = self.driver.current_window_handle
        logging.info(f'current window is {current_window}')
        all_windows = self.driver.window_handles
        for window in all_windows:
            if window != current_window:
                self.driver.switch_to.window(window)
                logging.info('switch successful')
                break

        return current_window

    def refresh_page(self):
        logging.info('refresh page.....')
        self.driver.refresh()

