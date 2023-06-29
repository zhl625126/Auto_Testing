import logging
import allure
from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class CategoryPage(PageBase):

    product = (By.CSS_SELECTOR, "div[class='product__title']")
    active_btn = (By.XPATH, '//*[contains(@class,"header__category--active")')
    def category_btn(self, category):
        return (By.XPATH, f"//a[text()='{category}']")


    def btn_status(self):
        web_element = self.find_element(self.active_btn)
        assert web_element, f'btn should be focus, test failed.'


    @allure.step("點選category")
    def click_category(self, category):
        logging.info(f'Click category {category}')
        self.find_element(self.category_btn(category), clickable=True).click()


    allure.step("拿到全部category的產品")
    def get_all_category(self):
        logging.info(f'Get all category list...')
        num = 0
        while True:
            self.scroll_down()
            try:
                self.find_element((By.XPATH, f"//div[@class='products' and count(a) > {num}]"))
                products = self.find_elements(self.product)
                num = len(products)
                product_list = []
                for i in products:
                    product_list.append(i.text)
                logging.info(f'Get list is {product_list}')
            except:
                return product_list

    @allure.step("按照選擇的category返回product list")
    def product_list(self, category):

        logging.info(f'Return category {category} to check with category list ')
        woman = ['前開衩扭結洋裝', '透肌澎澎防曬襯衫', '小扇紋細織上衣', '活力花紋長筒牛仔褲', '精緻扭結洋裝', '透肌澎澎薄紗襯衫', '小扇紋質感上衣', '經典修身長筒牛仔褲']
        man = ['純色輕薄百搭襯衫', '時尚輕鬆休閒西裝', '經典商務西裝']
        accessory = ['夏日海灘戶外遮陽帽', '經典牛仔帽', '卡哇伊多功能隨身包', '柔軟氣質羊毛圍巾']
        if category == "女裝":
            logging.info(f'return product list is {woman}')
            return woman
        if category == "男裝":
            logging.info(f'return product list is {man}')
            return man
        if category == "配件":
            logging.info(f'return product list is {accessory}')
            return accessory





