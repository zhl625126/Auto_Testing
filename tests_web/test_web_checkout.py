import os
import pytest
from page_objects.product_page import ProductPage
import allure
from page_objects.cart_page import CartPage
from testdata import get_data_from_excel

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
xlsx_file = os.path.join(path, 'testdata', 'Stylish_TestCase.xlsx')

@allure.feature("web測試")
@allure.story("Checkout testing")
@allure.title("Checkout with empty cart")
def test_checkout_empty_cart(launch_webdriver, login):

    product_page = ProductPage(launch_webdriver)
    cart_page = CartPage(launch_webdriver)
    product_page.click_cart_icon()
    cart_page.click_checkout()
    msg = product_page.popup_msg()

    assert msg == '尚未選購商品', f"""msg display wrong, expected msg is: 尚未選購商品,\
                                    actual result is: {msg}"""


@allure.feature("web測試")
@allure.story("Checkout testing")
@allure.title("Checkout with invalid values")
@pytest.mark.parametrize('info', get_data_from_excel.checkout_info(xlsx_file, 'Checkout with Invalid Value'))
def test_checkout_invalid_values(launch_webdriver, login, info):

    product_page = ProductPage(launch_webdriver)
    cart_page = CartPage(launch_webdriver)
    product_page.click_logo()
    product_page.random_click_product()
    product_page.random_click_color()
    product_page.random_click_size()
    product_page.add_to_cart()
    product_page.popup_msg()
    product_page.click_cart_icon()
    cart_page.send_checkout_info(info)

    msg = product_page.popup_msg()
    assert msg == info['Alert Msg'], f"""msg display wrong, expected msg is: {info['Alert Msg']},\
                                        actual result is: {msg}"""

@allure.feature("web測試")
@allure.story("Checkout testing")
@allure.title("Checkout with valid values")
@pytest.mark.parametrize('info', get_data_from_excel.checkout_info(xlsx_file, 'Checkout with Valid Value'))
def test_checkout_valid_values(launch_webdriver, login, info):

    product_page = ProductPage(launch_webdriver)
    cart_page = CartPage(launch_webdriver)
    product_page.click_logo()
    product_page.random_click_product()
    product_page.random_click_color()
    product_page.random_click_size()
    product_page.add_to_cart()
    product_page.popup_msg()
    product_page.click_cart_icon()
    cart_page.send_checkout_info(info)

    msg = product_page.popup_msg()
    assert msg == '付款成功', f"""msg display wrong, expected msg is: 付款成功,\
                                actual result is: {msg}"""
    modify_info = cart_page.modify_success_time(info)
    cart_page.check_success_info(modify_info)
