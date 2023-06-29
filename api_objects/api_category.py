from utils.api_base import APIBase
import os
from testdata import data

class APICategory(APIBase):
    def __init__(self, session, category, page):
        url = f"{os.getenv('domain')}{data.product_category(category, page)}"
        super().__init__(session, url)

    def send_category(self):
        self.api_request('get')
        return self


