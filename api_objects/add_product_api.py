import logging
import os
from utils.api_base import APIBase
from dotenv import load_dotenv

if 'ENV_FILE' in os.environ:
    load_dotenv(os.environ['ENV_FILE'])
else:
    load_dotenv()

class CreateProductAPI(APIBase):

    def __init__(self, session, product, path):

        url = f"{os.getenv('domain')}api/1.0/admin/product"
        super().__init__(session, url)

        info = {
            'category': product['Category'],
            'title': product['Title'],
            'description': product['Description'],
            'price': int(product['Price']) if product['Price'] and product['Price'] != 'text' else product['Price'],
            'texture': product['Texture'],
            'wash': product['Wash'],
            'place': product['Place of Product'],
            'note': product['Note'],
            'color_ids': product['ColorIDs'],
            'sizes': product['Sizes'],
            'story': product['Story'],
            'main_image': product['Main Image'],
            'other_images': product['other_images']
        }

        self.body = info
        logging.info(f'product body is: {info}')

        self.files = []
        if self.body['main_image'] != "":
            main_image = f"{path}\\{self.body['main_image']}"
            self.files.append(('main_image', open(main_image, 'rb')))

        for image in self.body['other_images']:
            image_path = f"{path}\\{image}"
            self.files.append(('other_images', open(image_path, 'rb')))
        logging.info(f'image is: {self.files}')

    def send(self):
        self.api_request('post', data=self.body, files=self.files)
        return self
