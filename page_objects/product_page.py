import logging
import random
import allure
from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class ProductPage(PageBase):

    logo = (By.CSS_SELECTOR, '.header__logo')
    add_quantity = (By.CSS_SELECTOR, '.product__quantity-add')
    quantity_value = (By.CSS_SELECTOR, '.product__quantity-value')
    minus_quantity = (By.CSS_SELECTOR, '.product__quantity-minus')
    add_cart_btn = (By.CSS_SELECTOR, '.product__add-to-cart-button')
    cart_icon_num = (By.CSS_SELECTOR, 'div[class="header__link-icon-cart"]>div')
    all_product = (By.CSS_SELECTOR, 'div[class="product__title"]')
    all_color = (By.XPATH, '//*[contains(@class, "product__color") and contains(@data_id, "color_code")]')
    all_size = (By.CSS_SELECTOR, 'div[class="product__size"]')
    cart_icon = (By.CSS_SELECTOR, '.header__link-icon-cart')
    product_id = (By.CSS_SELECTOR, '.product__id')
    product_price = (By.CSS_SELECTOR, '.product__price')
    product_details = (By.XPATH, '//div[@class="product__detail"]/child::div')

    @allure.step("隨機點選一個產品")
    def random_click_product(self):
        logging.info(f'Get all products list...')
        num = 0
        products = []
        while True:
            self.scroll_down()
            try:
                self.find_element((By.XPATH, f"//div[@class='products' and count(a) > {num}]"))
                products = self.find_elements(self.all_product)
                num = len(products)
                logging.info(f'Get list is {products}')
            except:
                break
        one_product = random.choice(products)
        self.driver.execute_script("arguments[0].click();", one_product)
        return one_product

    @allure.step('進入全部產品頁面')
    def click_logo(self):
        logging.info("點選 logo 切換到全部商品頁面")
        self.find_element(self.logo).click()

    @allure.step('隨機點選另一個產品')
    def random_click_another_product(self, product):
        logging.info("點選 logo 切換到全部商品頁面")
        self.find_element(self.logo).click()

        logging.info("搜尋全部商品....")
        num = 0
        products = []
        products_name = []
        while True:
            self.scroll_down()
            try:
                self.find_element((By.XPATH, f"//div[@class='products' and count(a) > {num}]"))
                products = self.find_elements(self.all_product)
                num = len(products)
                logging.info(f'Get list is {products}')
            except:
                break

        logging.info("列出全部商品的名稱")
        for i in products:
            products_name.append(i.text)
        logging.info(f"全部商品的名稱: {products_name}")

        logging.info("剔除已經存在的產品名稱...")
        if product in products_name:
            products_name.remove(product)
        logging.info((f"商品名稱: {products_name}"))

        logging.info("任意點選一個商品")
        another_product = self.find_element((By.XPATH, f'//div[text()="{random.choice(products_name)}"]'))
        self.driver.execute_script("arguments[0].click();", another_product)


    @allure.step("隨機點選一個顏色")
    def random_click_color(self):
        logging.info(f'Random select color and click it')
        random_color = random.choice(self.find_elements(self.all_color))
        self.driver.execute_script("arguments[0].click();", random_color)
        class_value = random_color.get_attribute('class')
        logging.info(f'class_value is: {class_value}')
        color_id = random_color.get_attribute('data_id')
        assert 'selected' in class_value, 'Selected color does not have "selected" class'
        logging.info(f'return color_id: {color_id}')
        self.save_snapshot()
        return color_id


    @allure.step("隨機點選一個尺寸")
    def random_click_size(self):
        logging.info(f'Random select size and click it')
        random_size = random.choice(self.find_elements(self.all_size))
        self.driver.execute_script("arguments[0].click();", random_size)
        class_value = random_size.get_attribute('class')
        assert 'selected' in class_value, 'Selected size does not have "selected" class'
        logging.info(f'return size: {random_size.text}')
        self.save_snapshot()
        return random_size.text


    @allure.step("修改產品數量")
    def modify_quantity(self, quantity):
        # quantity = int(quantity)
        logging.info(f"Change quantity, want modify quantity is {quantity}")
        current_value = int(self.find_element(self.quantity_value).text)
        if current_value < quantity:
            for _ in range(quantity-current_value):
                self.find_element(self.add_quantity).click()
        elif current_value > quantity:
            for _ in range(current_value-quantity):
                self.find_element(self.minus_quantity).click()
        return int(self.find_element(self.quantity_value).text)


    @allure.step("加入購物車")
    def add_to_cart(self):
        logging.info((f'Click add to cart button'))
        self.find_element(self.add_cart_btn).click()


    @allure.step("檢查購物車icon")
    def check_cart(self, num):
        logging.info(f'Check cart icon number should be {num}')
        cart_value = self.find_element(self.cart_icon_num).text
        assert int(cart_value) == num, f"""
        Cart icon number display wrong, 
        Expected number is {num}, 
        Actual number is {cart_value}
        """

    @allure.step("抓取popup訊息")
    def popup_msg(self):
        logging.info(f'Check pop up message....')
        pop_msg = self.confirm_popup()
        return pop_msg


    @allure.step("點選購物車icon")
    def click_cart_icon(self):
        logging.info(f'點選購物車icon')
        self.find_element(self.cart_icon).click()


    @allure.step("Get product info: 名稱, ID, 價錢,並返回dict")
    def get_product_info(self):
        logging.info('find all info on product page')

        product_dict = dict()
        product_dict['product name'] = self.find_element(self.all_product).text
        product_dict['ID'] = self.find_element(self.product_id).text
        product_dict['price'] = self.find_element(self.product_price).text

        logging.info(f"product_dict is: {product_dict}")
        logging.info('修改價錢只保留數字部分')
        if "." in product_dict['price']:
            product_dict['price'] = product_dict['price'].split('.', 1)[1]
        logging.info(f'product price is: {product_dict["price"]}')
        logging.info(f"return product detail: {product_dict}")
        return product_dict

    @allure.step("拿到產品頁面的產品名稱回傳")
    def get_product_name(self):

        logging.info('拿到產品頁面的產品名稱回傳')
        name = self.find_element(self.all_product).text
        logging.info(f"產品名稱為: {name}")
        return name






