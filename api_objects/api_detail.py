from utils.api_base import APIBase
import os

class APIDetail(APIBase):
    def __init__(self, session, product_id):
        url = f"{os.getenv('domain')}api/1.0/products/details?id={product_id}"
        super().__init__(session, url)

    def send_detail(self):
        self.api_request('get')
        return self
