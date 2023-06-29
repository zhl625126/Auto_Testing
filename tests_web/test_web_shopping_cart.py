import logging
from page_objects.product_page import ProductPage
import allure
from page_objects.cart_page import CartPage
from database.db_command import get_colors


@allure.feature("web測試")
@allure.story("購物車產品資訊測試")
@allure.title("測試用例名稱: test_cart_info")
def test_cart_info(launch_webdriver, conn_database):

    msg = "已加入購物車"
    logging.info(f'Test product page color')
    product_page = ProductPage(launch_webdriver)
    cart_page = CartPage(launch_webdriver)

    product_page.random_click_product()
    color = product_page.random_click_color()
    size = product_page.random_click_size()

    product_info = product_page.get_product_info()
    product_page.add_to_cart()
    pop_msg = product_page.popup_msg()
    assert pop_msg == msg, f"""Message display wrong, 
                            expected message is: {msg},
                            actual message is: {pop_msg}"""

    product_page.click_cart_icon()
    cart_info = cart_page.get_cart_info()
    price = cart_page.get_product_price()
    cart_color = cart_page.get_color()
    color_code = get_colors(conn_database, cart_color)


    assert color == color_code, f"顏色顯示不正確, expected color is: {color}, actual color is: {color_code}"
    assert size == cart_info['size'], f"尺寸顯示不正確, expected size is: {size}, actual size is: {cart_info['size']}"
    assert product_info['product name'] == cart_info['car product name'], f"""
                                                            產品名稱不正確, expected name is: {product_info['product name']}, 
                                                            actual size is: {cart_info['cart product name']}"""
    assert product_info['ID'] == cart_info['ID'], f"""
                                                    產品名稱不正確, expected name is: {product_info['ID']}, 
                                                    actual size is: {cart_info['ID']}"""
    assert product_info['price'] == price, f"""
                                            產品名稱不正確, expected name is: {product_info['price']}, 
                                            actual size is: {price}"""


@allure.feature("web測試")
@allure.story("移除購物車產品資訊測試")
@allure.title("測試用例名稱: test_remove_product")
def test_remove_product(launch_webdriver):

    msg = "已刪除商品"
    logging.info(f'Test remove random cart product...')
    product_page = ProductPage(launch_webdriver)
    cart_page = CartPage(launch_webdriver)

    for i in range(2):
        product_page.click_logo()
        product_page.random_click_product()
        product_page.random_click_color()
        product_page.random_click_size()
        product_page.add_to_cart()
        product_page.popup_msg()

    product_page.click_cart_icon()

    cart_page.random_delete_product()
    pop_msg = product_page.popup_msg()
    assert pop_msg == msg, f"""
                            Pop msg display wrong, expected msg is: {msg},
                            actual msg is: {pop_msg}"""

    items = cart_page.get_items()
    assert items == 1, f"""
                        cart items display wrong, expected item is: 1,
                        actual item is: {items}"""


@allure.feature("web測試")
@allure.story("移除購物車產品資訊測試")
@allure.title("測試用例名稱: test_modify_quantity")
def test_modify_quantity(launch_webdriver):

    msg = "已修改數量"
    num = '3'
    logging.info(f'Test modify quantity of cart product....')
    product_page = ProductPage(launch_webdriver)
    cart_page = CartPage(launch_webdriver)

    product_page.random_click_product()
    product_page.random_click_color()
    product_page.random_click_size()
    product_page.add_to_cart()
    product_page.popup_msg()
    product_page.click_cart_icon()

    cart_page.modify_quantity(num)
    pop_msg = product_page.popup_msg()
    assert pop_msg == msg, f"""
                            Pop msg display wrong, expected msg is: {msg},
                            actual msg is: {pop_msg}"""

    price = cart_page.get_product_price()
    sub_total = cart_page.get_sub_total_price()
    assert int(price) * int(num) == sub_total, f"""
                                        subtotal display wrong, expected subtotal is: {price * num},
                                        actual subtotal is: {sub_total}"""




