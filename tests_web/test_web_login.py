import os
import pytest
import logging
from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
import allure
from testdata import data

@allure.feature("web測試")
@allure.story("login and logout success 測試")
@allure.title("測試用例名稱: test_login_logout")
@pytest.mark.login_info(email=os.getenv('email'), password=os.getenv('pwd'))
def test_login_logout(launch_webdriver, login):

    logging.info("test login success and then logout")
    login_page = LoginPage(launch_webdriver)
    product_page = ProductPage(launch_webdriver)

    token = login_page.get_jwt_token()

    assert login == "Login Success", f"""
                                        pop up msg display wrong, expected msg is: Login Success,
                                        actual msg is: {login}"""
    assert token, f"""
                                        Login success have no jwt_token, test fail"""

    login_page.click_logout()
    msg = product_page.popup_msg()
    logout_token = login_page.get_jwt_token()

    assert msg == "Logout Success", f"""
                                        pop up msg display wrong, expected msg is: Logout Success,
                                        actual msg is: {msg}"""
    assert logout_token == None, f"""
                                    Logout jwt_token should be deleted, test fail"""


@allure.feature("web測試")
@allure.story("login fail 測試")
@allure.title("測試用例名稱: test_login_failed")
def test_login_failed(launch_webdriver):
    logging.info("test login fail with incorrect email and password")
    page_login = LoginPage(launch_webdriver)
    product_page = ProductPage(launch_webdriver)

    page_login.click_member_icon()
    page_login.send_info(data.fail_login['email'], data.fail_login['password'])
    page_login.click_login()

    msg = product_page.popup_msg()
    login_token = page_login.get_jwt_token()

    assert msg == "Login Failed", f"""
                                    pop up msg display wrong, expected msg is: Login Success,
                                    actual msg is: {msg}"""
    assert login_token == None, f"""
                                    Login failed should no jwt_token, test fail"""


@allure.feature("web測試")
@allure.story("send invalid token 測試")
@allure.title("測試用例名稱: test_invalid_token")
@pytest.mark.login_info(email=os.getenv('email'), password=os.getenv('pwd'))
def test_invalid_token(launch_webdriver, login):

    logging.info("test invalid token")
    login_page = LoginPage(launch_webdriver)
    product_page = ProductPage(launch_webdriver)
    valid_token = login_page.get_jwt_token()

    login_page.click_logout()
    msg = product_page.popup_msg()

    no_token = login_page.get_jwt_token()
    assert msg == "Logout Success", f"""
                                        pop up msg display wrong, expected msg is: Logout Success,
                                        actual msg is: {msg}"""
    assert no_token == None, f"""
                                     Logout jwt_token should be deleted, test fail"""

    login_page.send_jwtToken(valid_token)

    login_page.click_member_icon()
    popup_msg = product_page.popup_msg()
    token_msg = login_page.get_jwt_token()
    assert popup_msg == "Invalid Access Token", f"""
                                                    pop up msg display wrong, expected msg is: Invalid Access Token,
                                                    actual msg is: {popup_msg}"""
    assert token_msg == None, f"""
                                invalid token have not be clear, test fail"""
