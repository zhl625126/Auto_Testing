import os
import pytest
import allure
from testdata import get_data_from_excel
from page_objects.create_product_page import CreateProductPage


path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
xlsx_file = os.path.join(path, 'testdata', 'Stylish_TestCase.xlsx')

mainImage = os.path.join(path, 'testdata', 'mainImage.jpg')
otherImage0 = os.path.join(path, 'testdata', 'otherImage0.jpg')
otherImage1 = os.path.join(path, 'testdata', 'otherImage1.jpg')

@allure.feature("web測試")
@allure.story("Create product testing")
@allure.title("Create Product without invalid values")
@pytest.mark.parametrize('info', get_data_from_excel.create_product_info(xlsx_file, 'Create Product Failed'))
def test_create_with_invalid_value(launch_webdriver, login, info, request):
    create_product_page = CreateProductPage(launch_webdriver)

    launch_webdriver.get(f"{os.getenv('domain')}admin/products.html")
    create_product_page.click_new_product()
    msg = create_product_page.send_product_info(info, mainImage, otherImage0, otherImage1)

    assert msg == info['Alert Msg'], f"""msg display wrong, expected msg is: {info['Alert Msg']},\
                                        actual result is: {msg}"""

    def finalizer():
        create_product_page.delete_product(info['Title'])
        product_new_list = create_product_page.check_product()
        assert info['Title'] not in product_new_list, f'{info["Title"]} still in product list'

    request.addfinalizer(finalizer)


@allure.feature("web測試")
@allure.story("Create product testing")
@allure.title("Create Product without login")
@pytest.mark.parametrize('info', get_data_from_excel.create_product_info(xlsx_file, 'Create Product Success'))
def test_create_with_valid(launch_webdriver, login, info, request):
    create_product_page = CreateProductPage(launch_webdriver)

    launch_webdriver.get(f"{os.getenv('domain')}admin/products.html")
    create_product_page.click_new_product()
    msg = create_product_page.send_product_info(info, mainImage, otherImage0, otherImage1)
    product_list = create_product_page.check_product()
    assert msg == 'Create Product Success', f"""msg display wrong, expected msg is: Create Product Success,\
                                        actual result is: {msg}"""

    assert info['Title'] in product_list, 'add product failed'

    def finalizer():
        create_product_page.delete_product(info['Title'])
        product_new_list = create_product_page.check_product()
        assert info['Title'] not in product_new_list, f'{info["Title"]} still in product list, delete failed'

    request.addfinalizer(finalizer)


@allure.feature("web測試")
@allure.story("Create product testing")
@allure.title("Create Product without login")
def test_create_without_login(launch_webdriver):

    create_product_page = CreateProductPage(launch_webdriver)

    launch_webdriver.get(f"{os.getenv('domain')}admin/products.html")
    create_product_page.pop_msg()
    create_product_page.click_new_product()
    info = create_product_page.random_right_value(get_data_from_excel.create_product_info(xlsx_file, 'Create Product Success'))
    msg = create_product_page.send_product_info(info, mainImage, otherImage0, otherImage1)

    assert msg == 'Please Login First', f"""msg display wrong, expected msg is: Please Login First,\
                                        actual result is: {msg}"""

