import os
from dotenv import load_dotenv

if 'ENV_FILE' in os.environ:
    load_dotenv(os.environ['ENV_FILE'])
else:
    load_dotenv()

fail_login = {
        "email": "testmail@mail.com",
        "password": "test",
    }

user_login = 'api/1.0/user/login'
user_logout = 'api/1.0/user/logout'
user_profile = 'api/1.0/user/profile'


def product_category(category, page):
    return f'api/1.0/products/{category}?paging={page}'


login_fail_info = [
    {'email': f'{os.getenv("email_gw0")}', 'password': 'wrong_password', 'msg': 'Login Failed'},
    {'email': 'wrong_email', 'password': f'{os.getenv("password_gw0")}', 'msg': 'Login Failed'},
    {'email': '', 'password': f'{os.getenv("password_gw0")}', 'msg': 'Email and password are required.'},
    {'email': f'{os.getenv("email_gw0")}', 'password': '', 'msg': 'Email and password are required.'},
    {'email': '', 'password': '', 'msg': 'Email and password are required.'}
]

checkout_valid_value = [{
        'Receiver': '陳大文',
        'Email': 'abc@abc.com',
        'Mobile': '0912345678',
        'Address': '台北市',
        'Deliver Time': 'anytime',
        'Subtotal': '1797',
        'Total': '1827',
        'cart list': '1 item',
        'Prime': 'prime',
        'Shipping': 'delivery',
        'Payment': 'credit_card',
    }]


cart_list = {
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

