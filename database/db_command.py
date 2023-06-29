import logging
from pymysql.cursors import DictCursor
import allure

@allure.step("從db拿到關鍵字的搜尋結果")
def get_db_products(keyword, conn):

    logging.info(f'search database with keyword: {keyword}')
    with conn.cursor(cursor=DictCursor) as cursor:
        command = f"SELECT title from product where title like '%{keyword}%'"
        cursor.execute(command)

        search_result = cursor.fetchall()
        print(search_result)
        if len(search_result) != 0:
            logging.info(f'search_result is: {search_result}')
            return set(item['title'] for item in search_result)
        else:
            logging.info(f'search_result is: {search_result}')

            return list(search_result)

def get_colors(conn, color):

    logging.info(f'拿到所有產品的顏色名稱遇十六進制對照資訊')
    with conn.cursor(cursor=DictCursor) as cursor:
        command = f"SELECT name, code from color "
        cursor.execute(command)

        search_result = cursor.fetchall()
        print(search_result)

        color_dict = {}

        for result in search_result:
            color_name = result['name']
            color_code = result['code']
            color_key = f"color_code_{color_code}"
            color_dict[color_name] = color_key

        logging.info(f"color_dict is: {color_dict}")

        if color in color_dict:
            logging.info(f"返回code_code: {color_dict[color]}")
            return color_dict[color]


@allure.step("get login info from db")
def get_user_info(conn, email):
    logging.info('search user info from db')
    with conn.cursor(cursor=DictCursor) as cursor:
        command = f"SELECT * FROM user WHERE email = '{email}'"
        cursor.execute(command)

        search_result = cursor.fetchone()
        logging.info(f'search_result is : {search_result}')
        return search_result
