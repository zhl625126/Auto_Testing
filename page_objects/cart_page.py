import logging
import random
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from utils.page_base import PageBase

class CartPage(PageBase):

    product_name = (By.CSS_SELECTOR, '.cart__item-name')
    product_id = (By.CSS_SELECTOR, '.cart__item-id')
    product_color = (By.CSS_SELECTOR, '.cart__item-color')
    product_size = (By.CSS_SELECTOR, '.cart__item-size')
    product_price = (By.CSS_SELECTOR, '.cart__item-price-content')
    delete_icon = (By.CSS_SELECTOR, '.cart__delete-button')
    select_option = (By.CSS_SELECTOR, '.cart__item-quantity-selector')
    sub_total = (By.CSS_SELECTOR, '.cart__item-subtotal-content')
    checkout_btn = (By.CSS_SELECTOR, '.checkout-button')
    car_number = (By.ID, 'cc-number')
    expiration_date = (By.ID, 'cc-exp')
    ccv = (By.ID, 'cc-ccv')
    name_field = (By.XPATH, '//div[text()="收件人姓名"]/following-sibling::input')
    email_field = (By.XPATH, '//div[text()="Email"]/following-sibling::input')
    phone_field = (By.XPATH, '//div[text()="手機"]/following-sibling::input')
    address_field = (By.XPATH, '//div[text()="地址"]/following-sibling::input')


    def deliver_time(self, time):
        return (By.XPATH, f'//*[text()="{time}"]')


    def select_iframe(self, name):
        return (By.XPATH, f'//iframe[contains(@src,"{name}")]')

    def success_name(self, name):
        return (By.XPATH, f'//*[text()="{name}"]')

    def success_email(self, email):
        return (By.XPATH, f'//*[text()="{email}"]')

    def success_mobile(self, mobile):
        return (By.XPATH, f'//*[text()="{mobile}"]')

    def success_address(self, address):
        return (By.XPATH, f'//*[text()="{address}"]')

    def success_delivery(self, delivery):
        return (By.XPATH, f'//*[text()="{delivery}"]')


    @allure.step('Get cart item detail,返回dict[產品名稱, ID, 尺寸]')
    def get_cart_info(self, ):
        logging.info("取得購物車產品資訊")

        keys = ['car product name', 'ID', 'size']
        name_info = self.find_element(self.product_name).text
        id_info = self.find_element(self.product_id).text
        #color_info = self.find_element(self.product_color).text
        size_info = self.find_element(self.product_size).text

        details = {key: value for key, value in zip(keys, [name_info, id_info, size_info])}

        logging.info(f'detail字典為: {details}')
        for key, value in details.items():
            if "｜" in value:
                value = value.split('｜')[-1]
                details[key] = value
                logging.info(f"取得 {key} 的值為: {value}")
        return details

    @allure.step("Get cart product color")
    def get_color(self):
        logging.info("get cart product color")
        color = self.find_element(self.product_color).text
        if "｜" in color:
            color = color.split('｜')[-1]
        logging.info(f"color is: {color}")

        return color

    @allure.step('Get product price')
    def get_product_price(self):
        logging.info('Get cart page product price')
        price_info = self.find_element(self.product_price)
        price = price_info.text
        dot = price.find(".")
        price_num = price[dot+1:]
        logging.info(f'price is: {price_num}')
        return price_num

    @allure.step('隨機刪除一個產品')
    def random_delete_product(self):
        logging.info('隨機刪除一個產品')
        items = self.find_elements(self.delete_icon)
        logging.info(f"delete icon list: {items}")
        self.driver.execute_script("arguments[0].click();", random.choice(items))

    @allure.step('獲取當然購物車內產品數量')
    def get_items(self):
        logging.info('返回產品數量')
        items = self.find_elements(self.delete_icon)
        return len(items)

    @allure.step('修改產品數量')
    def modify_quantity(self, quantity):
        logging.info(f"Modify quantity to {quantity}")
        select = Select(self.find_element(self.select_option))
        select.select_by_visible_text(quantity)

    @allure.step('獲取產品total價錢')
    def get_sub_total_price(self):
        logging.info('Get cart page product subtotal')
        sub_total = self.find_element(self.sub_total)
        price = sub_total.text
        dot = price.find(".")
        total = price[dot+1:]
        logging.info(f'sub total is: {total}')
        return int(total)

    @allure.step('點選 checkout button')
    def click_checkout(self):
        logging.info('Click checkout button')
        self.find_element(self.checkout_btn, clickable=True).click()


    @allure.step('Send checkout information to field')
    def send_checkout_info(self, info):
        logging.info('send check out information...')
        logging.info(f"send info is: {info['Receiver']},{info['Email']},{info['Mobile']},\
                        {info['Address']},{info['Deliver Time']},{info['Credit Card No']},\
                        {info['Expiry Date']},{info['Security Code']}")

        self.send_key(self.name_field, info['Receiver'], select_all=True)
        self.send_key(self.email_field, info['Email'], select_all=True)
        self.send_key(self.phone_field, info['Mobile'], select_all=True)
        self.send_key(self.address_field, info['Address'], select_all=True)
        if info['Deliver Time'] != '':
            self.find_element(self.deliver_time(info['Deliver Time'])).click()
        self.send_key_in_iframe('expiration-date', self.expiration_date, info['Expiry Date'], select_all=True)
        self.send_key_in_iframe('card-number', self.car_number, info['Credit Card No'], select_all=True)

        self.send_key_in_iframe('ccv', self.ccv, info['Security Code'], select_all=True)

        self.click_checkout()

    @allure.step('Check order info on thankyou page')
    def check_success_info(self, info):
        self.find_element(self.success_name(info['Receiver']))
        self.find_element(self.success_email(info['Email']))
        self.find_element(self.success_mobile(info['Mobile']))
        self.find_element(self.success_address(info['Address']))
        self.find_element(self.success_address(info['Deliver Time']))

    @allure.step('Check order info on thankyou page')
    def modify_success_time(self, info):
        if info['Deliver Time'] == '08:00-12:00':
            info['Deliver Time'] = '08:00 - 12:00'
        if info['Deliver Time'] == '14:00-18:00':
            info['Deliver Time'] = '14:00 - 18:00'
        return info







