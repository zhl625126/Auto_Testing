import logging
from utils.api_base import APIBase
import os

class Getorder(APIBase):
    def __init__(self, session, number):
        url = f"{os.getenv('domain')}api/1.0/order/{number}"
        super().__init__(session, url)

    def get_order(self):
        self.api_request('get')
        return self
