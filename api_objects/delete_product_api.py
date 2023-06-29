import logging
import os
from utils.api_base import APIBase
from dotenv import load_dotenv

if 'ENV_FILE' in os.environ:
    load_dotenv(os.environ['ENV_FILE'])
else:
    load_dotenv()


class DeleteProductAPI(APIBase):
    def __init__(self, session, product_id):

        url = f"{os.getenv('domain')}api/1.0/admin/product/{product_id}"
        logging.info(f'url is: {url}')
        super().__init__(session, url)


    def send(self):
        self.api_request('delete')
        return self

