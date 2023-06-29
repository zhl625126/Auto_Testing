import pytest
import logging
from page_objects.product_search import SearchPage
from database.db_command import get_db_products
import allure


@allure.feature("web測試")
@allure.story("主頁面搜尋結果測試")
@allure.title("測試用例名稱: search case")
@pytest.mark.parametrize('keyword', ['洋裝','','Hello'])
def test_search_case(launch_webdriver, conn_database, keyword):

    logging.info(f'Test search case, search keyword is {keyword}')
    search_page = SearchPage(launch_webdriver)
    search_page.input_values(keyword)
    actual_list = search_page.get_all_products()
    expect_list = get_db_products(keyword, conn_database)

    assert actual_list == expect_list, f'Search result is different, test fail\n, \
    expect list is {expect_list},\n \
    actual list is {actual_list}'
