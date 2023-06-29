import logging

from utils.api_base import APIBase
import os

class Order(APIBase):
    def __init__(self, session):
        url = f"{os.getenv('domain')}api/1.0/order"
        super().__init__(session, url)

    def send_order(self, prime, info):
        self.api_request('post', json=self.set_order_payload(prime, info))
        return self

    def set_order_payload(self, prime, info):
        if info['cart list'] == '0 item':
            cart_list = []

        if info['cart list'] == '1 item':
            cart_list = [
                {
                    "color": {
                        "code": "FFFFFF",
                        "name": "白色"
                    },
                    "id": "201807201824",
                    "image": "http://abc.com/assets/3456789/main.jpg",
                    "name": "洋裝",
                    "price": 599,
                    "qty": 3,
                    "size": "S"
                }
            ]
        if info['Prime'] == 'prime':
            new_prime = prime
        elif info['Prime'] == 'invalid':
            new_prime = info['Prime']
        else:
            new_prime = ''

        logging.info('組合payload結構')
        pay_load = {
            "prime": new_prime,
            "order": {
                "shipping": info["Shipping"],
                "payment": info["Payment"],
                "subtotal": int(info["Subtotal"]),
                "freight": 30,
                "total": int(info["Total"]),
                "recipient": {
                    "name": info["Receiver"],
                    "phone": info["Mobile"],
                    "email": info["Email"],
                    "address": info["Address"],
                    "time": info["Deliver Time"]
                },
                "list": cart_list
            }
        }
        logging.info(f'pay load is: {pay_load}')

        return pay_load


    def get_order(self, number):
        
        self.api_request('get', json=self.set_order_payload(prime, info))
        return self