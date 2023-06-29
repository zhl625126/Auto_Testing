import json
import logging
import allure
from pymysql.cursors import DictCursor


@allure.step('from db get order number')
def get_order_info(conn, number):
    logging.info('search product id from db')
    with conn.cursor(cursor=DictCursor) as cursor:

        command = f"SELECT * FROM order_table WHERE number='{number}'"
        cursor.execute(command)

        order_id = cursor.fetchone()
        logging.info(f'search_result is : {order_id}')
        return order_id

