import logging
import random

import allure
from selenium.webdriver.common.by import By
from utils.page_base import PageBase
from page_objects.product_page import ProductPage


class CreateProductPage(PageBase):

    create_btn = (By.XPATH, '//button[text()="Create New Product"]')
    all_product = (By.ID, 'product_title')
    select_list = (By.XPATH, "//*[@name='category']")
    title = (By.CSS_SELECTOR, 'input[name="title"]')
    description = (By.CSS_SELECTOR, 'textarea[name="description"]')
    price = (By.CSS_SELECTOR, 'input[name="price"]')
    texture = (By.CSS_SELECTOR, 'input[name="texture"]')
    wash = (By.CSS_SELECTOR, 'input[name="wash"]')
    place = (By.CSS_SELECTOR, 'input[name="place"]')
    note = (By.CSS_SELECTOR, 'input[name="note"]')
    story = (By.CSS_SELECTOR, 'input[name="story"]')
    main_image = (By.CSS_SELECTOR, 'input[name="main_image"]')
    create = (By.CSS_SELECTOR, 'input[value="Create"]')
    color_all = (By.XPATH, '//input[@id="color_ids"]/following-sibling::label')
    size_all = (By.XPATH, '//input[@name="sizes"]/following-sibling::label')
    other_image1 = (By.XPATH, '//input[@name="other_images"][1]')
    other_image2 = (By.XPATH, '//input[@name="other_images"][2]')

    def delete_btn(self, delete):
        return (By.XPATH, f'//td[text()="{delete}"]/parent::tr/descendant::button')

    def color(self, color):
        return (By.XPATH, f'//label[contains(text(), "{color}")]/preceding-sibling::input')

    def size(self, size):
        return (By.XPATH, f'//label[contains(text(), "{size}")]/preceding-sibling::input')

    def click_new_product(self):
        self.find_element(self.create_btn).click()

    @allure.step('Send product info to page')
    def send_product_info(self, info, main_image, image1, image2):
        logging.info('send create information...')
        logging.info(f"send info is: {info}")
        original_page = self.switch_page()
        self.select_dropdown(self.select_list, info['Category'])
        self.send_key(self.title, info['Title'])
        self.send_key(self.description, info['Description'])
        self.send_key(self.price, info['Price'])
        self.send_key(self.texture, info['Texture'])
        self.send_key(self.wash, info['Wash'])
        self.send_key(self.place, info['Place of Product'])
        self.send_key(self.note, info['Note'])
        self.send_key(self.story, info['Story'])

        logging.info('判斷colors如果為全選,則全部勾選, 為空則跳過, 否則按照顏色點選')
        if '全選' in info['Colors']:
            colors = self.find_elements(self.color_all)
            logging.info(f'colors is: {colors} ')
            for i in colors:
                color = i.text
                self.find_element(self.color(color)).click()
                logging.info(f'{color} be clicked')
        elif info['Colors']:
            for i in info['Colors']:
                self.find_element(self.color(f' {i} ')).click()
                logging.info(f'{i} be clicked')

        if '全選' in info['Sizes']:
            sizes = self.find_elements(self.size_all)
            sizes.pop()
            logging.info(f'sizes is: {sizes} ')
            for j in sizes:
                size = j.text
                self.find_element(self.size(size)).click()
                logging.info(f'{size} be clicked')
        elif info['Sizes']:
            for j in info['Sizes']:
                self.find_element(self.size(j)).click()
                logging.info(f'{j} be clicked')

        if info['Main Image']:
            self.send_key(self.main_image, main_image)
            logging.info('main image send successful')

        if info['Other Image 1']:
            self.send_key(self.other_image1, image1)
            logging.info('image1 send successful')

        if info['Other Image 2']:
            self.send_key(self.other_image2, image2)
            logging.info('image2 send successful')

        self.find_element(self.create).click()

        msg = self.confirm_popup()
        self.driver.switch_to.window(original_page)
        logging.info('switch to original page')
        return msg

    @allure.step('Check create product')
    def check_product(self):
        self.refresh_page()
        product_list = []
        logging.info('Get all products.....')
        all_product = self.find_elements(self.all_product)
        for i in all_product:
            product = i.text
            product_list.append(product)
        logging.info(f'all product is: {product_list}')
        return product_list

    @allure.step('Delete new product')
    def delete_product(self, product):
        try:
            logging.info('find delete button and click it')
            self.find_element(self.delete_btn(product)).click()
            logging.info('click completed then confirm pop up msg')
            self.confirm_popup()
        except:
            logging.info(f'Can not find element: {product}')


    @allure.step('隨機拿一組正確資料')
    def random_right_value(self, info):
        random_list = random.choice(info)
        logging.info(f'random right value is: {random_list}')
        return random_list

    @allure.step('Return pop msg')
    def pop_msg(self):
        return self.confirm_popup()
