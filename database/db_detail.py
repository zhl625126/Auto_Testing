import json
import logging
import os
from pymysql.cursors import DictCursor
import allure


@allure.step('get color, size, stock')
def get_variants(conn, product_id):
    logging.info('search variants from db')

    with conn.cursor(cursor=DictCursor) as cursor:
        command = f"""SELECT
                        variant.product_id, 
                        JSON_ARRAYAGG(JSON_OBJECT('color_code', color.code, 'size', variant.size, 'stock', variant.stock)) AS variants
                        FROM product
                        LEFT JOIN variant ON product.id = variant.product_id
                        LEFT JOIN color ON variant.color_id = color.id 
                        WHERE variant.product_id = {product_id}
                        GROUP BY variant.product_id """
        cursor.execute(command)

        datas = cursor.fetchall()
        logging.info(f'db variants is: {datas}')
        print(type(datas))
        return datas


@allure.step('get color, size, stock')
def get_product_detail(conn, product_id):
    logging.info('get product detail with product id')

    with conn.cursor(cursor=DictCursor) as cursor:
        command = f"""SELECT * FROM product WHERE id = {product_id} """
        cursor.execute(command)

        datas = cursor.fetchone()
        logging.info(f'db info by id is: {datas}')
        return datas
