import os
import pytest
import logging
import allure
import requests
from database import db_command
from testdata import data
from comm_function import comm_function


@allure.feature("API測試")
@allure.story("user api test")
@allure.title("login api test")
def test_api_login_success(login, conn_database):
    logging.info('testing login api success')
    pay_load, response = login[1:]
    result_json = response.json()
    actual_user_info = result_json['data']['user']
    logging.info(f'result json is: {result_json}')

    db_info = db_command.get_user_info(conn_database, pay_load['email'])

    comm_function.assert_check(response.status_code, 200)
    comm_function.assert_check(actual_user_info['id'], db_info['id'])
    comm_function.assert_check(actual_user_info['name'], db_info['name'])
    comm_function.assert_check(result_json['data']['access_token'], db_info['access_token'])
    #comm_function.assert_check(comm_function.change_utc_time(result_json['data']['login_at']), db_info['login_at'].strftime("%Y-%m-%d %H:%M:%S"))
    comm_function.assert_check(int(result_json['data']['access_expired']), db_info['access_expired'])

@allure.feature("API測試")
@allure.story("user api test")
@allure.title("login api test with login fail")
@pytest.mark.parametrize('login_fail', data.login_fail_info)
def test_api_login_fail(sessions, login_fail):

    login_url = f"{os.getenv('domain')}{data.user_login}"
    logging.info(f'login url is: {login_url}')
    login_payload = {
        "provider": "native",
        "email": f'{login_fail["email"]}',
        "password": f'{login_fail["password"]}'
    }
    logging.info(f'login_payload is : {login_payload}')

    response = sessions.post(
        url=login_url,
        data=login_payload
    )
    response_json = response.json()

    comm_function.assert_check(response.status_code, 400)
    comm_function.assert_check(response_json['errorMsg'], login_fail['msg'])



@allure.feature("API測試")
@allure.story("user api test")
@allure.title("logout api testing")
def test_api_logout(login, conn_database):
    with allure.step('Testing logout success'):
        logout_url = f"{os.getenv('domain')}{data.user_logout}"
        logging.info(f'logout url is: {logout_url}')

        sessions, pay_load = login[:2]

        logging.info(f'session is: {sessions}')
        response = sessions.post(url=logout_url)
        response_json = response.json()
        logging.info(f'response is : {response_json}')

        db_info = db_command.get_user_info(conn_database, pay_load['email'])

        comm_function.assert_check(response.status_code, 200)
        comm_function.assert_check(response_json['message'], 'Logout Success')
        comm_function.assert_check(db_info['access_token'], '')
        comm_function.assert_check(db_info['login_at'], None)

    with allure.step('Testing logout with invalid token'):
        logging.info('Logout again, should show 403 code')
        response = sessions.post(url=logout_url)
        response_json = response.json()
        logging.info(f'response is : {response_json}')

        comm_function.assert_check(response.status_code, 403)
        comm_function.assert_check(response_json['errorMsg'], 'Invalid Access Token')

    with allure.step('Testing logout without token'):
        logging.info('test logout without token, should show 401 code')
        sessions.close()
        logging.info('disconnect session success...')

        new_session = requests.Session()
        response_without_token = new_session.post(url=logout_url)
        response_json = response_without_token.json()
        logging.info(f'response is : {response_json}')

        comm_function.assert_check(response_without_token.status_code, 401)
        comm_function.assert_check(response_json['errorMsg'], 'Unauthorized')


@allure.feature("API測試")
@allure.story("user api test")
@allure.title("user profile api testing")
def test_api_user_profile(login, conn_database):
    with allure.step('Testing profile with valid token'):
        logging.info('testing user profile api ')
        session, pay_load = login[:2]

        db_result = db_command.get_user_info(conn_database, pay_load['email'])
        logging.info(f'db_result is : {db_result}')

        profile_url = f'{os.getenv("domain")}{data.user_profile}'
        logging.info(f'profile url is: {profile_url}')

        response = session.get(profile_url)
        response_json = response.json()
        logging.info(f'response is: {response_json}')

        comm_function.assert_check(response.status_code, 200)
        comm_function.assert_check(response_json['data']['name'], db_result['name'])
        comm_function.assert_check(response_json['data']['email'], db_result['email'])
        comm_function.assert_check(response_json['data']['picture'], db_result['picture'])


    with allure.step('Testing profile without token'):
        session.headers.pop('Authorization')
        response = session.get(profile_url)
        response_json = response.json()
        logging.info(f'response is: {response_json}')

        comm_function.assert_check(response.status_code, 401)
        comm_function.assert_check(response_json['errorMsg'], 'Unauthorized')


    with allure.step('Testing profile with invalid token'):
        response = session.get(headers={"Authorization": 'Bearer invalidtokentest'}, url=profile_url)
        response_json = response.json()
        logging.info(f'response is: {response_json}')

        comm_function.assert_check(response.status_code, 403)
        comm_function.assert_check(response_json['errorMsg'], 'Forbidden')
