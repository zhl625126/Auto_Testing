import json
import logging
import os

import allure
import pymysql
from dotenv import load_dotenv
from pymysql.cursors import DictCursor


@allure.step('get add_product info')
def get_added_product_info(conn, product_id):
    logging.info('get info from db')

    with conn.cursor(cursor=DictCursor) as cursor:
        command = f"""SELECT * FROM product where id='{product_id}'"""
        cursor.execute(command)

        datas = cursor.fetchall()
        logging.info(f'db product info is: {datas}')

        return datas


@allure.step('get add_product variant info')
def get_added_product_variant(conn, product_id, variant):
    logging.info('get info from db')

    with conn.cursor(cursor=DictCursor) as cursor:
        command = f"""SELECT {variant} FROM variant where product_id='{product_id}' group by {variant};"""
        cursor.execute(command)

        datas = cursor.fetchall()
        logging.info(f'db product variant {variant} info is: {datas}')

        return datas


@allure.step('get add_product other image')
def get_added_product_otherimage(conn, product_id):
    logging.info('get info from db')

    with conn.cursor(cursor=DictCursor) as cursor:
        command = f"""SELECT image FROM product_images where product_id='{product_id}' group by image;"""
        cursor.execute(command)

        datas = cursor.fetchall()
        logging.info(f'db product other image info is: {datas}')
        print(datas)
        return datas


@allure.step('get add_product other image')
def check_deleted_product(conn, product_id):
    logging.info('get info from db')
    try:
        with conn.cursor(cursor=DictCursor) as cursor:
            command = f"""SELECT * FROM product where id='{product_id}';"""
            cursor.execute(command)

            datas = cursor.fetchall()
            logging.info(f'db product other image info is: {datas}')

            return datas
    except:
        logging.info('Can not find product id in db')

