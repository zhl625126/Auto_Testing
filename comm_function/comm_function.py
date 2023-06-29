import datetime
import logging
import allure


@allure.step('Check assert')
def assert_check(actual_value, expected_value):
    assert actual_value == expected_value, f"""Test failed, expected value is: {expected_value},
                                                actual value is: {actual_value}"""


@allure.step('Change UTC time format')
def change_utc_time(utc_time):
    logging.info('change utc time format')

    dt = datetime.datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    formatted_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_dt
