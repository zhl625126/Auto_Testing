import json
import os
import pytest
import logging
import allure
from comm_function import comm_function
from api_objects import api_detail
from database import db_detail, db_category, db_search


@allure.feature("API測試")
@allure.story("product detail api test")
@allure.title("right id search detail testing")
@pytest.mark.parametrize('product_id', ['201807242222', '201807242216'])
def test_get_product_detail(sessions, conn_database, product_id):
    logging.info('Testing detail api')

    product_detail = api_detail.APIDetail(sessions, product_id)
    api_data = product_detail.send_detail().get_response_body()
    logging.info(f'api_data is: {api_data}')
    db_data = db_detail.get_product_detail(conn_database, product_id)
    logging.info(f'db_data is: {db_data}')
    status_code = product_detail.get_status_code()
    comm_function.assert_check(status_code, 200)

    comm_function.assert_check(api_data['data']['id'], db_data['id'])
    comm_function.assert_check(api_data['data']['category'], db_data['category'])
    comm_function.assert_check(api_data['data']['title'], db_data['title'])
    comm_function.assert_check(api_data['data']['description'], db_data['description'])
    comm_function.assert_check(api_data['data']['price'], db_data['price'])
    comm_function.assert_check(api_data['data']['texture'], db_data['texture'])
    comm_function.assert_check(api_data['data']['wash'], db_data['wash'])
    comm_function.assert_check(api_data['data']['place'], db_data['place'])
    comm_function.assert_check(api_data['data']['story'], db_data['story'])
    comm_function.assert_check(api_data['data']['note'], db_data['note'])
    comm_function.assert_check(os.path.basename(db_data['main_image']), db_data['main_image'])
    db_images = db_category.get_product_image(conn_database, db_data['id'])
    comm_function.assert_check(api_data['data']['images'], db_images[0]['images'])

    db_variant = db_detail.get_variants(conn_database, product_id)
    db_variants = db_search.sorted_variant_by_db(db_variant)

    def compare_dict_by_name(variant):
        return variant["color_code"], variant["size"], variant["stock"]

    api_list = []
    for item in api_data['data']['variants']:
        logging.info(f'item is: {item}')
        api_list.append(compare_dict_by_name(item))
    comm_function.assert_check(api_list, db_variants)


@allure.step('send null id for search detail')
def test_get_product_profile_no_id(sessions, conn_database):
    logging.info('Testing detail api')
    product_detail = api_detail.APIDetail(sessions, '')

    api_data = product_detail.send_detail().get_response_body()
    status_code = product_detail.get_status_code()
    comm_function.assert_check(status_code, 400)
    comm_function.assert_check(api_data['errorMsg'], "Invalid Category")

@allure.step('send wrong id for search detail')
def test_get_product_detail_wrong_id(sessions, conn_database):
    logging.info('Testing detail api')
    product_detail = api_detail.APIDetail(sessions, '1231231231231')

    api_data = product_detail.send_detail().get_response_body()
    status_code = product_detail.get_status_code()
    comm_function.assert_check(status_code, 400)
    comm_function.assert_check(api_data['errorMsg'], 'Invalid Product ID')