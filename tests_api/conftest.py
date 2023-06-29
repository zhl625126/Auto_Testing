import pytest
import logging
import allure
import os
import requests
from testdata import data
from dotenv import load_dotenv

if 'ENV_FILE' in os.environ:
    load_dotenv(os.environ['ENV_FILE'])
else:
    load_dotenv()


@pytest.fixture()
def sessions():
    session = requests.Session()

    yield session


@pytest.fixture()
def login(sessions, worker_id):

    login_url = f"{os.getenv('domain')}{data.user_login}"
    logging.info(f'login url is: {login_url}')
    login_payload = {
        "provider": "native",
        "email": os.getenv(f'email_{worker_id}'),
        "password": os.getenv(f'password_{worker_id}')
    }
    logging.info(f'login_payload is : {login_payload}')

    response = sessions.post(
                url=login_url,
                data=login_payload
    )
    logging.info(f'login status code is: {response.status_code}')
    sessions.headers = {"Authorization": f'Bearer {response.json()["data"]["access_token"]}'}
    yield sessions, login_payload, response
