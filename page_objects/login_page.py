import logging
import allure
from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class LoginPage(PageBase):

    email = (By.ID, 'email')
    pwd = (By.ID, 'pw')
    login_btn = (By.XPATH, '//button[text()="Login"]')
    member = (By.CSS_SELECTOR, '.header__link-icon-profile')
    logout_btn = (By.XPATH, '//button[text()="登出"]')


    @allure.step("切換 login 頁面")
    def click_member_icon(self):
        logging.info("進入 login 頁面")
        self.find_element(self.member).click()


    @allure.step("input email and password")
    def send_info(self, email, password):
        print(f"password2: {password}")
        logging.info(f"輸入 email 以及 password, email is: {email}, password is: {password}")
        self.send_key(self.email, email)
        self.send_key(self.pwd, password)


    @allure.step("click login button")
    def click_login(self):
        logging.info("click login button....")
        self.find_element(self.login_btn).click()


    @allure.step("check JWT token in localstorage")
    def get_jwt_token(self):
        logging.info("get JWT token")

        jwt_token = self.driver.execute_script('return localStorage.getItem("jwtToken");')
        logging.info(f"jwtToken is: {jwt_token}")

        return jwt_token


    @allure.step("Click Logout button")
    def click_logout(self):
        logging.info("click logout button")
        self.find_element(self.logout_btn).click()


    @allure.step("send jwtToken to localstorage")
    def send_jwtToken(self, token):
        logging.info("set JWT token")

        self.driver.execute_script(f"window.localStorage.setItem('jwtToken', '{token}');")












