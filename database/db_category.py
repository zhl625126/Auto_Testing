import json
import logging
import os
from pymysql.cursors import DictCursor
import allure


@allure.step('get product id')
def get_product_id(conn, category, page):
    logging.info('search product id from db')
    with conn.cursor(cursor=DictCursor) as cursor:
        limit = 6
        offset = page * limit
        if category != 'all':
            add_line = f"WHERE category = '{category}'"
        else:
            add_line = ''

        command = f"SELECT id FROM product {add_line} LIMIT {limit} OFFSET {offset}"
        cursor.execute(command)

        all_id = cursor.fetchall()
        logging.info(f'search_result is : {all_id}')
        print(all_id)
        return all_id


@allure.step('get product info')
def get_product_info(conn, category, page):
    logging.info('search product info from db')
    with conn.cursor(cursor=DictCursor) as cursor:
        limit = 6
        offset = page * limit
        if category != 'all':
            add_line = f"WHERE category = '{category}'"
        else:
            add_line = ''

        command = f"SELECT * FROM product {add_line} LIMIT {limit} OFFSET {offset}"
        cursor.execute(command)

        datas = cursor.fetchall()
        logging.info(f'search_result is : {datas}')

        return datas


@allure.step('get color, size')
def get_variants(conn, category, page):
    logging.info('search variants from db')
    limit = 6
    offset = page * limit
    if category != 'all':
        add_line = f"WHERE category = '{category}'"
    else:
        add_line = ''
    with conn.cursor(cursor=DictCursor) as cursor:
        command = f"""SELECT
                        variant.product_id, 
                        JSON_ARRAYAGG(JSON_OBJECT('color_code', color.code, 'size', variant.size, 'stock', variant.stock)) AS variants
                        FROM product
                        LEFT JOIN variant ON product.id = variant.product_id
                        LEFT JOIN color ON variant.color_id = color.id {add_line}
                        GROUP BY variant.product_id LIMIT {limit} OFFSET {offset} """
        cursor.execute(command)

        datas = cursor.fetchall()
        logging.info(f'db variants is: {datas}')
        return datas


@allure.step('get product images by product id')
def get_product_image(conn, product_id):
    logging.info('search variants from db')
    with conn.cursor(cursor=DictCursor) as cursor:
        command = f"""SELECT product_images.product_id, JSON_ARRAYAGG(product_images.image) AS images
                        FROM product
                        LEFT JOIN
                        product_images ON product.id = product_images.product_id WHERE product.id = {product_id}"""
        cursor.execute(command)

        datas = cursor.fetchall()

        def add_prefix_to_images(product_id, images):
            prefix = f'{os.getenv("domain")}assets/{product_id}/'
            return [prefix + image for image in images]

        images_with_prefix = add_prefix_to_images(product_id, json.loads(datas[0]['images']))
        datas[0]['images'] = images_with_prefix
        logging.info(f'{datas}')
        return datas

def get_category_count(conn, category):
    logging.info('get category數量')
    if category != 'all':
        add_line = f"WHERE category = '{category}'"
    else:
        add_line = ''
    with conn.cursor(cursor=DictCursor) as cursor:
        command = f"SELECT COUNT(*) AS total FROM product {add_line};"
        cursor.execute(command)

        datas = cursor.fetchall()
        return datas
