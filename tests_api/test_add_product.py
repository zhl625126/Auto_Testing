import os
import pytest
import logging
import allure
from comm_function import comm_function
from api_objects import add_product_api, delete_product_api
from testdata import api_create_product
from database import db_product


path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.info(f'path is: {path}')

xlsx_file = os.path.join(path, 'testdata', 'Stylish_TestCase.xlsx')
image_file = os.path.join(path, 'testdata')


@allure.feature("api測試")
@allure.story("api add product testing")
@allure.title("add product with invalid value")
@pytest.mark.parametrize('product', api_create_product.modify_product_excel(xlsx_file, 'API Create Product Failed'))
def test_create_product_invalid(login, conn_database, product, request):

    add_product = add_product_api.CreateProductAPI(login[0], product, image_file)
    response = add_product.send()

    body = response.get_response_body()
    logging.info(f'response body is: {body}')

    comm_function.assert_check(response.get_status_code(), 400)
    comm_function.assert_check(body['errorMsg'], product['Error Msg'])

    def finalizer():
        try:
            logging.info(f"product_id is: {body['data']['product_id']}")
            delete_product = delete_product_api.DeleteProductAPI(login[0], body['data']['product_id'])
            delete_response = delete_product.send()
            comm_function.assert_check(delete_response.get_status_code(), 200)

            db_result = db_product.check_deleted_product(conn_database, body['data']['product_id'])
            comm_function.assert_check(db_result, ())
        except:
            logging.info(f'have no find product id')

    request.addfinalizer(finalizer)


@allure.feature("api測試")
@allure.story("api add product testing")
@allure.title("add product with valid value")
@pytest.mark.parametrize('product', api_create_product.modify_product_excel(xlsx_file, 'API Create Product Success'))
def test_create_product_valid(login, conn_database, product, request):

    add_product = add_product_api.CreateProductAPI(login[0], product, image_file)
    info = add_product.body

    response = add_product.send()
    body = response.get_response_body()
    logging.info(f'response body is: {body}')

    db_product_info = db_product.get_added_product_info(conn_database, body['data']['product_id'])
    db_color_id = db_product.get_added_product_variant(conn_database, body['data']['product_id'], 'color_id')
    db_size = db_product.get_added_product_variant(conn_database, body['data']['product_id'], 'size')
    db_other_image = db_product.get_added_product_otherimage(conn_database, body['data']['product_id'])

    comm_function.assert_check(response.get_status_code(), 200)
    comm_function.assert_check(info['category'], db_product_info[0]['category'])
    comm_function.assert_check(info['title'], db_product_info[0]['title'])
    comm_function.assert_check(info['description'], db_product_info[0]['description'])
    comm_function.assert_check(info['price'], db_product_info[0]['price'])
    comm_function.assert_check(info['texture'], db_product_info[0]['texture'])
    comm_function.assert_check(info['wash'], db_product_info[0]['wash'])
    comm_function.assert_check(info['place'], db_product_info[0]['place'])
    comm_function.assert_check(info['note'], db_product_info[0]['note'])
    comm_function.assert_check(info['story'], db_product_info[0]['story'])
    comm_function.assert_check(info['main_image'], db_product_info[0]['main_image'])
    comm_function.assert_check(info['color_ids'], str(db_color_id['color_id']) \
                                                       if isinstance(db_color_id, dict) else [str(item['color_id']) \
                                                                                              for item in db_color_id])
    comm_function.assert_check(info['sizes'], [item['size'] for item in db_size])
    comm_function.assert_check(info['sizes'], db_size['size'] \
                                                   if isinstance(db_size, dict) else [item['size'] for item in db_size])
    comm_function.assert_check(info['other_images'], [item['image'] for item in db_other_image])

    def finalizer():
        try:
            logging.info(f"product_id is: {body['data']['product_id']}")
            delete_product = delete_product_api.DeleteProductAPI(login[0], body['data']['product_id'])
            delete_response = delete_product.send()
            comm_function.assert_check(delete_response.get_status_code(), 200)

            db_result = db_product.check_deleted_product(conn_database, body['data']['product_id'])
            comm_function.assert_check(db_result, ())
        except:
            logging.info(f'have no find product id')

    request.addfinalizer(finalizer)


@allure.feature("api測試")
@allure.story("api add product testing")
@allure.title("add product with no login")
@pytest.mark.parametrize('product', api_create_product.modify_product_excel(xlsx_file, 'API Create Product Success'))
def test_create_no_login(sessions, conn_database, product):

    add_product = add_product_api.CreateProductAPI(sessions, product, image_file)
    response = add_product.send()

    body = response.get_response_body()
    logging.info(f'response body is: {body}')

    comm_function.assert_check(response.get_status_code(), 401)
    comm_function.assert_check(body['errorMsg'], 'Unauthorized')



