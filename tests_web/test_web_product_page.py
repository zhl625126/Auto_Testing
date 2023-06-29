import pytest
import logging
from page_objects.product_page import ProductPage
import allure

@allure.feature("web測試")
@allure.story("選取產品顏色測試")
@allure.title("測試用例名稱: test_product_color")
def test_product_color(launch_webdriver,):
    logging.info(f'Test product page color')
    product_page = ProductPage(launch_webdriver)
    product_page.random_click_product()
    product_page.random_click_color()


@allure.feature("web測試")
@allure.story("選取產品尺寸測試")
@allure.title("測試用例名稱: test_product_size")
def test_product_size(launch_webdriver):
    logging.info(f'Test product page size')
    product_page = ProductPage(launch_webdriver)
    product_page.random_click_product()
    product_page.random_click_size()


@allure.feature("web測試")
@allure.story("產品數量disable測試")
@allure.title("測試用例名稱: test_quantity_disabled")
@pytest.mark.parametrize('quantity', [3])
def test_quantity_disabled(launch_webdriver, quantity):
    logging.info(f'Test product page quantity editor disable function, quantity is {quantity}')
    product_page = ProductPage(launch_webdriver)
    product_page.random_click_product()

    quantity_value = product_page.modify_quantity(quantity)
    assert quantity_value == 1, \
        f"""
        Quantity should be disabled, 
        Expected quantity is 1, 
        Actual quantity is {quantity_value}
        """

@allure.feature("web測試")
@allure.story("產品數量增加測試")
@allure.title("測試用例名稱: test_increase_quantity")
@pytest.mark.parametrize('quantity, second_qty', [(9, 11)])
def test_increase_quantity(launch_webdriver, quantity, second_qty):
    logging.info(f'Test product page  increase quantity function, quantity is {quantity}')
    product_page = ProductPage(launch_webdriver)
    product_page.random_click_product()
    product_page.random_click_size()

    quantity_value = product_page.modify_quantity(quantity)
    assert quantity_value == quantity, \
        f"""
        Quantity should be {quantity}, 
        Actual quantity is {quantity_value}
        """

    second_qty_value = product_page.modify_quantity(second_qty)
    assert second_qty_value == quantity,\
        f"""
        Quantity should be disabled, 
        Expected quantity is {quantity}, 
        Actual quantity is {second_qty_value}
        """

@allure.feature("web測試")
@allure.story("產品數量減少測試")
@allure.title("測試用例名稱: test_decrease_quantity")
@pytest.mark.parametrize('quantity, second_qty', [(9, 1)])
def test_decrease_quantity(launch_webdriver, quantity, second_qty):
    logging.info(f'Test product page  decrease quantity function, quantity is {quantity}')
    product_page = ProductPage(launch_webdriver)
    product_page.random_click_product()
    product_page.random_click_size()

    product_page.modify_quantity(quantity)
    second_qty_value = product_page.modify_quantity(second_qty)
    assert second_qty_value == second_qty,\
        f"""
        Quantity should be disabled, 
        Expected quantity is {second_qty}, 
        Actual quantity is {second_qty_value} 
        """

@allure.feature("web測試")
@allure.story("加入購物車測試")
@allure.title("測試用例名稱: test_add_cart_success")
@pytest.mark.parametrize('icon_number', [1])
def test_add_cart_success(launch_webdriver, icon_number):
    logging.info(f'Test add to cart success and pop up message')
    product_page = ProductPage(launch_webdriver)
    product_page.random_click_product()
    product_page.random_click_size()
    product_page.add_to_cart()
    msg = product_page.popup_msg()
    assert msg == "已加入購物車"
    product_page.check_cart(icon_number)


@allure.feature("web測試")
@allure.story("加入購物車失敗測試")
@allure.title("測試用例名稱: test_add_cart_fail")
def test_add_cart_fail(launch_webdriver):
    logging.info(f'Test add to cart fail and pop up message')
    product_page = ProductPage(launch_webdriver)
    product_page.random_click_product()
    product_page.add_to_cart()
    msg = product_page.popup_msg()
    assert msg == "請選擇尺寸"
