from utils.api_base import APIBase
import os

class APISearch(APIBase):
    def __init__(self, session, keyword, page):
        url = f"{os.getenv('domain')}api/1.0/products/search?keyword={keyword}&paging={page}"
        super().__init__(session, url)

    def send_search(self):
        self.api_request('get')
        return self
