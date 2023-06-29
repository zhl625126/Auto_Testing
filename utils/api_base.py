import json
import logging
import allure


class APIBase:
    def __init__(self, session, url):
        self.response = None
        self.session = session
        self.url = url

    def api_request(self, method, **kwargs):
        logging.info(f'Request method: {method}')
        print(f'Request URL: {self.url}')
        json_body = kwargs.get("json", None)
        logging.info(f'Request Json body: {json.dumps(json_body, indent=4, ensure_ascii=False)}')
        logging.info(f'Request Cookies: {self.session.cookies}')
        logging.info(f'Request headers: {self.session.headers}')

        self.response = self.session.request(method, self.url, **kwargs)
        logging.info(f'url: {self.url}')
        logging.info(f'Response headers: {self.response.headers}')
        logging.info(f'Response code: {self.response.status_code}')
        try:
            json_body = self.response.json()
            logging.info(f'Response: {json.dumps(json_body, indent=4, sort_keys=True, ensure_ascii=False)}')
        except Exception as e:
            logging.info(f"Exception: {e}")
            logging.info("Response: No Json Response Body")

    @allure.step('return status code')
    def get_status_code(self):
        return self.response.status_code

    @allure.step('return response.json')
    def get_response_body(self):
        return self.response.json()

    @allure.step('return request body')
    def get_request_loads(self):
        return json.loads(self.response.request.body.decode('utf-8'))
