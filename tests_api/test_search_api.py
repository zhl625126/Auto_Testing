import json
import os
import pytest
import logging
import allure
from comm_function import comm_function
from api_objects import api_search
from database import db_search,db_category


@allure.feature("API測試")
@allure.story("product search api test")
@allure.title("right search testing")
@pytest.mark.parametrize('keyword, page', [('襯衫', 0)])
def test_get_search(sessions, conn_database, keyword, page):
    logging.info('Testing search api')

    product_search = api_search.APISearch(sessions, keyword, page)

    api_data = product_search.send_search().get_response_body()
    db_data = db_search.get_product_search(conn_database, keyword, page)
    status_code = product_search.get_status_code()
    comm_function.assert_check(status_code, 200)
    for api_datas, db_datas in zip(api_data['data'], db_data):
        comm_function.assert_check(api_datas['id'], db_datas['id'])
        comm_function.assert_check(api_datas['category'], db_datas['category'])
        comm_function.assert_check(api_datas['title'], db_datas['title'])
        comm_function.assert_check(api_datas['description'], db_datas['description'])
        comm_function.assert_check(api_datas['price'], db_datas['price'])
        comm_function.assert_check(api_datas['texture'], db_datas['texture'])
        comm_function.assert_check(api_datas['wash'], db_datas['wash'])
        comm_function.assert_check(api_datas['place'], db_datas['place'])
        comm_function.assert_check(api_datas['story'], db_datas['story'])
        comm_function.assert_check(api_datas['note'], db_datas['note'])
        comm_function.assert_check(os.path.basename(api_datas['main_image']), db_datas['main_image'])
        db_images = db_category.get_product_image(conn_database, api_datas['id'])
        comm_function.assert_check(api_datas['images'], db_images[0]['images'])

    db_variant = db_search.get_variant_by_title(conn_database, keyword, page)
    db_variants = db_search.sorted_variant_by_db(db_variant)

    def compare_dict_by_name(variant):
        return variant["color_code"], variant["size"], variant["stock"]

    api_list = []
    for item in api_data['data']:
        for i in item['variants']:
            api_list.append(compare_dict_by_name(i))

    comm_function.assert_check(api_list, db_variants)

@allure.step('send null keyword for search')
def test_get_product_search_no_keyword(sessions, conn_database):
    logging.info('Testing category api')
    product_search = api_search.APISearch(sessions, '', 0)

    api_data = product_search.send_search().get_response_body()
    status_code = product_search.get_status_code()
    comm_function.assert_check(status_code, 400)
    comm_function.assert_check(api_data['errorMsg'], "Search Keyword is required.")

@allure.step('send wrong page for search')
def test_get_product_search_wrong_page(sessions, conn_database):
    logging.info('Testing category api')
    product_search = api_search.APISearch(sessions, '襯衫', 3)

    api_data = product_search.send_search().get_response_body()
    status_code = product_search.get_status_code()
    comm_function.assert_check(status_code, 200)
    comm_function.assert_check(api_data['data'], [])