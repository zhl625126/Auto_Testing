import logging
import allure
import requests
from dotenv import load_dotenv
import os

if 'ENV_FILE' in os.environ:
    load_dotenv(os.environ['ENV_FILE'])
else:
    load_dotenv()

@allure.step('get prime with api')
def get_prime():
    sessions = requests.Session()
    url = 'https://js.tappaysdk.com/tpdirect/sandbox/getprime'
    header = {
                "Content-Type": "application/x-www-form-urlencoded",
                "x-api-key": os.getenv("x-api-key"),
            }
    data = {
            "cardnumber": os.getenv("cardnumber"),
            "cardduedate": os.getenv("cardduedate"),
            "cardccv": "123",
            "appid": os.getenv("appid"),
            "appkey": os.getenv("x-api-key"),
            "appname": os.getenv("db_host"),
            "url": os.getenv("domain"),
            "port": "",
            "protocol": "http:",
            "fraudid": ""}

    response = sessions.post(url=url, headers=header, data=f'jsonString={data}')
    response_body = response.json()

    return response_body['card']['prime']
