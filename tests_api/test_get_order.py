import json
import logging
import allure
from comm_function import comm_function
from api_objects import get_order
from database import db_order


@allure.feature("api測試")
@allure.story("api order testing")
@allure.title("checkout with valid value")
def test_get_right_order(login, conn_database):

    order = get_order.Getorder(login[0], '522122576982')
    order_response = order.get_order()
    response_body = order_response.get_response_body()['data']
    logging.info(f'response_body is: {response_body}')
    comm_function.assert_check(order_response.get_status_code(), 200)

    db_order_info = db_order.get_order_info(conn_database, '522122576982')
    details_info = json.loads(db_order_info['details'])

    comm_function.assert_check(response_body['id'], db_order_info['id'])
    comm_function.assert_check(response_body['number'], db_order_info['number'])
    comm_function.assert_check(response_body['time'], db_order_info['time'])
    comm_function.assert_check(response_body['user_id'], db_order_info['user_id'])
    comm_function.assert_check(int(response_body['total']), int(db_order_info['total']))
    comm_function.assert_check(response_body['details']['list'][0]['id'], details_info['list'][0]['id'])
    comm_function.assert_check(response_body['details']['list'][0]['qty'], details_info['list'][0]['qty'])
    comm_function.assert_check(response_body['details']['list'][0]['name'], details_info['list'][0]['name'])
    comm_function.assert_check(response_body['details']['list'][0]['size'], details_info['list'][0]['size'])
    comm_function.assert_check(response_body['details']['list'][0]['image'], details_info['list'][0]['image'])
    comm_function.assert_check(int(response_body['details']['list'][0]['price']), int(details_info['list'][0]['price']))
    comm_function.assert_check(response_body['details']['freight'], details_info['freight'])
    comm_function.assert_check(response_body['details']['total'], details_info['total'])
    comm_function.assert_check(response_body['details']['payment'], details_info['payment'])
    comm_function.assert_check(response_body['details']['shipping'], details_info['shipping'])
    comm_function.assert_check(response_body['details']['subtotal'], details_info['subtotal'])
    comm_function.assert_check(response_body['details']['recipient']['name'], details_info['recipient']['name'])
    comm_function.assert_check(response_body['details']['recipient']['time'], details_info['recipient']['time'])
    comm_function.assert_check(response_body['details']['recipient']['email'], details_info['recipient']['email'])
    comm_function.assert_check(response_body['details']['recipient']['phone'], details_info['recipient']['phone'])
    comm_function.assert_check(response_body['details']['recipient']['address'], details_info['recipient']['address'])


@allure.feature("api測試")
@allure.story("api order testing")
@allure.title("checkout with valid value")
def test_get_wrong_order(login, conn_database):

    order = get_order.Getorder(login[0], '123')
    order_response = order.get_order()
    response_body = order_response.get_response_body()
    logging.info(f'response_body is: {response_body}')
    comm_function.assert_check(order_response.get_status_code(), 400)

    comm_function.assert_check(response_body['errorMsg'], 'Order Not Found.')


@allure.feature("api測試")
@allure.story("api order testing")
@allure.title("checkout with valid value")
def test_get_order_without_login(sessions, conn_database):

    order = get_order.Getorder(sessions, '123')
    order_response = order.get_order()
    response_body = order_response.get_response_body()
    logging.info(f'response_body is: {response_body}')
    comm_function.assert_check(order_response.get_status_code(), 401)

    comm_function.assert_check(response_body['errorMsg'], 'Unauthorized')