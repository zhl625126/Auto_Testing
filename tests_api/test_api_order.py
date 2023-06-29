import json
import os
import pytest
import logging
import allure
from comm_function import comm_function
from api_objects import getprime, api_order
from testdata import api_checkout_invalid_value, data
from database import db_order

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.info(f'path is: {path}')
xlsx_file = os.path.join(path, 'testdata', 'Stylish_TestCase.xlsx')


@allure.feature("api測試")
@allure.story("api order testing")
@allure.title("checkout with invalid value")
@pytest.mark.parametrize('info', api_checkout_invalid_value.checkout_info(xlsx_file, 'API Checkout with Invalid Value'))
def test_order_with_invalid_checkout(login, info):

    order = api_order.Order(login[0])
    order_response = order.send_order(getprime.get_prime(), info).get_response_body()
    comm_function.assert_check(order_response['errorMsg'], info['Alert Msg'])

@allure.feature("api測試")
@allure.story("api order testing")
@allure.title("checkout with valid value")
@pytest.mark.parametrize('info', data.checkout_valid_value)
def test_order_with_valid_checkout(login, conn_database, info):

    order = api_order.Order(login[0])
    order_response = order.send_order(getprime.get_prime(), info)
    response_body = order_response.get_response_body()
    logging.info(f'response_body is: {response_body}')
    comm_function.assert_check(order_response.get_status_code(), 200)
    api_order_id = response_body['data']['number']
    logging.info(f'api_order_id is: {api_order_id}')

    db_order_info = db_order.get_order_info(conn_database, api_order_id)
    logging.info(f'db_search info is: {db_order_info}')
    db_details = json.loads(db_order_info['details'])
    comm_function.assert_check(api_order_id, db_order_info['number'])
    comm_function.assert_check(int(info['Total']), int(db_order_info['total']))
    comm_function.assert_check(info['Receiver'], db_details['recipient']['name'])
    comm_function.assert_check(info['Email'], db_details['recipient']['email'])
    comm_function.assert_check(info['Mobile'], db_details['recipient']['phone'])
    comm_function.assert_check(info['Address'], db_details['recipient']['address'])
    comm_function.assert_check(info['Deliver Time'], db_details['recipient']['time'])
    comm_function.assert_check(int(info['Subtotal']), int(db_details['subtotal']))
    comm_function.assert_check(info['Shipping'], db_details['shipping'])
    comm_function.assert_check(info['Payment'], db_details['payment'])
    comm_function.assert_check(data.cart_list['color']['code'], db_details['list'][0]['color']['code'])
    comm_function.assert_check(data.cart_list['color']['name'], db_details['list'][0]['color']['name'])
    comm_function.assert_check(data.cart_list['id'], db_details['list'][0]['id'])
    comm_function.assert_check(data.cart_list['image'], db_details['list'][0]['image'])
    comm_function.assert_check(data.cart_list['name'], db_details['list'][0]['name'])
    comm_function.assert_check(int(data.cart_list['price']), int(db_details['list'][0]['price']))
    comm_function.assert_check(int(data.cart_list['qty']), int(db_details['list'][0]['qty']))
    comm_function.assert_check(data.cart_list['size'], db_details['list'][0]['size'])
    comm_function.assert_check(data.cart_list['id'], db_details['list'][0]['id'])


@allure.feature("api測試")
@allure.story("api order testing")
@allure.title("checkout without login")
@pytest.mark.parametrize('info', data.checkout_valid_value)
def test_order_without_checkout(sessions, conn_database, info):

    order = api_order.Order(sessions)
    order_response = order.send_order(getprime.get_prime(), info)
    response_body = order_response.get_response_body()
    logging.info(f'response_body is: {response_body}')
    comm_function.assert_check(order_response.get_status_code(), 401)
    comm_function.assert_check(response_body['errorMsg'], 'Unauthorized')
