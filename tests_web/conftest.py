import pytest
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import logging
import allure
import os
from dotenv import load_dotenv, dotenv_values
from page_objects import login_page, product_page

if 'ENV_FILE' in os.environ:
    load_dotenv(os.environ['ENV_FILE'])
else:
    load_dotenv()

@pytest.fixture()
def launch_webdriver(request):

    service = Service(executable_path=ChromeDriverManager().install())

    options = webdriver.ChromeOptions()  # 設定chrome參數
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=service, options=options)
    logging.info('open browser')
    driver.get(os.getenv('domain'))
    log_content = driver.get_log("browser")

    yield driver
    def finalizer():

        allure.attach(driver.get_screenshot_as_png(), name='screenshot', attachment_type=allure.attachment_type.PNG)
        allure.attach(str(log_content), name="Browser Log", attachment_type=allure.attachment_type.TEXT)

        driver.quit()

    request.addfinalizer(finalizer)

@pytest.fixture()
def login(launch_webdriver, worker_id):

    page_product = product_page.ProductPage(launch_webdriver)
    page_login = login_page.LoginPage(launch_webdriver)
    page_login.click_member_icon()
    logging.info(f'worker_id is {worker_id}')
    email = os.getenv(f'email_{worker_id}')
    password = os.getenv(f'password_{worker_id}')
    logging. info(f"test mail is {email}, password is {password}")

    page_login.send_info(email, password)
    page_login.click_login()
    msg = page_product.popup_msg()

    yield msg
