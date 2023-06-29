import logging
import allure
from comm_function import comm_function
from api_objects import delete_product_api


@allure.feature("api測試")
@allure.story("api add product testing")
@allure.title("add product with invalid value")
def test_delete_product_invalid_id(login):

    delete_product = delete_product_api.DeleteProductAPI(login[0], '123456')
    response = delete_product.send()

    body = response.get_response_body()
    logging.info(f'response body is: {body}')

    comm_function.assert_check(response.get_status_code(), 400)
    comm_function.assert_check(body['errorMsg'], 'Product ID not found.')


@allure.feature("api測試")
@allure.story("api add product testing")
@allure.title("add product with invalid value")
def test_delete_product_without_login(sessions):

    delete_product = delete_product_api.DeleteProductAPI(sessions, '201807201824')
    response = delete_product.send()

    body = response.get_response_body()
    logging.info(f'response body is: {body}')

    comm_function.assert_check(response.get_status_code(), 401)
    comm_function.assert_check(body['errorMsg'], 'Unauthorized')



