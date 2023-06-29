import json
import os
import pytest
import logging
import allure
from comm_function import comm_function
from api_objects import api_category
from database import db_category, db_search


@allure.feature("API測試")
@allure.story("product category api test")
@allure.title("right search testing")
@pytest.mark.parametrize('category', ['men', 'women', 'accessories', 'all'])
def test_api_category_success(sessions, conn_database, category):
    logging.info('Testing category api')
    count = db_category.get_category_count(conn_database, category)

    for i in range(int(count[0]['total'] / 6)+1):
        product_category = api_category.APICategory(sessions, category, i)

        api_data = product_category.send_category().get_response_body()
        logging.info(f'api_data is: {api_data}')
        db_data = db_category.get_product_info(conn_database, category, i)
        status_code = product_category.get_status_code()
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

        db_variant = db_category.get_variants(conn_database, category, i)
        db_variants = db_search.sorted_variant_by_db(db_variant)

        def compare_dict_by_name(variant):
            return variant["color_code"], variant["size"], variant["stock"]

        api_list = []
        for item in api_data['data']:
            for j in item['variants']:
                api_list.append(compare_dict_by_name(j))

        #comm_function.assert_check(api_list, db_variants)


def test_api_wrong_category(sessions, conn_database):

    product_category = api_category.APICategory(sessions, 'category', 0)
    api_data = product_category.send_category().get_response_body()
    db_data = db_category.get_product_info(conn_database, "category", 0)
    status_code = product_category.get_status_code()
    comm_function.assert_check(status_code, 400)
    comm_function.assert_check(api_data['errorMsg'], "Invalid Category")
    comm_function.assert_check(db_data, ())


def test_api_wrong_page(sessions, conn_database):

    product_category = api_category.APICategory(sessions, 'men', 3)
    api_data = product_category.send_category().get_response_body()
    db_data = db_category.get_product_info(conn_database, "men", 3)
    status_code = product_category.get_status_code()
    comm_function.assert_check(status_code, 200)
    comm_function.assert_check(api_data['data'], [])
    comm_function.assert_check(db_data, ())

