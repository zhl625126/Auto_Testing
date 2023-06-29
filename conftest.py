import pytest
import logging
import os
import pymysql
from dotenv import load_dotenv
#
if 'ENV_FILE' in os.environ:
    load_dotenv(os.environ['ENV_FILE'])
else:
    load_dotenv()
@pytest.fixture()
def conn_database():

    db_settings = {  # 設定db
        "host": os.getenv('db_host'),
        "port": int(os.getenv("db_port")),
        "user": os.getenv("db_user"),
        "password": os.getenv("db_password"),
        "db": os.getenv("schema"),
        "charset": os.getenv("charset")
    }
    # 建立Connection物件
    logging.info(f'Connecting db.......')
    conn = pymysql.connect(**db_settings)  # 與db建立連線
    logging.info('Connected')

    yield conn
    conn.close()
