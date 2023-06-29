import logging
import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class SearchPage(PageBase):

    search_field = (By.CSS_SELECTOR, 'input[class="header__search-input"]')
    product = (By.CSS_SELECTOR, "div[class='product__title']")

    @allure.step("輸入搜尋value")
    def input_values(self, keyword):
        self.send_key(self.search_field, keyword)
        self.send_key(self.search_field, Keys.ENTER)

    @allure.step("get product list")
    def get_all_products(self):
        logging.info(f'Get all category list...')
        num = 0
        product_list = []
        while True:
            self.scroll_down()
            try:
                self.find_element((By.XPATH, f"//div[@class='products' and count(a) > {num}]"))
                products = self.find_elements(self.product)
                num = len(products)

                for i in products:
                    product_list.append(i.text)
                logging.info(f'Get list is {product_list}')
            except:
                if len(self.find_elements((By.XPATH, "//div[@class='products']/child::*"))) == 0:
                    return []
                else:
                    return set(product_list)
