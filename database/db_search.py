import json
import logging
from pymysql.cursors import DictCursor


def get_product_search(conn, keyword, page):
    logging.info('search product id from db')
    with conn.cursor(cursor=DictCursor) as cursor:
        limit = 6
        offset = page * limit

        command = f"SELECT * FROM product WHERE title LIKE '%{keyword}%' LIMIT {limit} OFFSET {offset}"
        cursor.execute(command)

        all_id = cursor.fetchall()
        logging.info(f'search_result is : {all_id}')
        return all_id

def get_variant_by_title(conn, keyword, page):
        limit = 6
        offset = page * limit

        cursor = conn.cursor(cursor=DictCursor)

        if keyword != '':
            add_line = f" WHERE product.title like '%{keyword}%'"
        else:
            add_line = ''
        command = f"""SELECT
                        variant.product_id, 
                        JSON_ARRAYAGG(JSON_OBJECT('color_code', color.code, 'size', variant.size, 'stock', variant.stock)) AS variants
                        FROM product
                        LEFT JOIN variant ON product.id = variant.product_id
                        LEFT JOIN color ON variant.color_id = color.id {add_line}
                        GROUP BY variant.product_id LIMIT {limit} OFFSET {offset} """

        cursor.execute(command)
        result = cursor.fetchall()
        return result


def sorted_variant_by_db(db_variant):
    def compare_dict_by_name(variant):
        return variant["color_code"], variant["size"], variant["stock"]

    list = []
    for item in db_variant:
        item_variant = json.loads(item['variants'])

        for i in item_variant:
            list.append(compare_dict_by_name(i))
    return list
