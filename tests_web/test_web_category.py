import pytest
import logging
from page_objects.category_page import CategoryPage
import allure

@allure.feature("web測試")
@allure.story("主頁面分類結果測試")
@allure.title("測試用例名稱: category test")
@pytest.mark.parametrize('category', ['女裝', '男裝', '配件'])
def test_category_case(launch_webdriver, category):

    logging.info(f'Test category case, category is {category}')
    category_page = CategoryPage(launch_webdriver)
    category_page.click_category(category)
    actual_list = category_page.get_all_category()
    expect_list = category_page.product_list(category)
    assert actual_list == expect_list, f'Product display wrong\n, \
    expect list is {expect_list},\n \
    actual list is {actual_list}'


