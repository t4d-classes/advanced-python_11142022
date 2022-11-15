"""  rate demo package """

from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor

import requests

from rates_demo.business_days import business_days


def get_rate(current_date: date) -> str:
    """ get rate """

    rates_url = (
        "http://127.0.0.1:5050/api/"
        f"{current_date}"
        "?base=INR&symbols=USD,EUR"
    )

    return requests.get(rates_url, timeout=60).text


def get_rates_threaded() -> None:
    """ get rates """

    rates_list = []

    start_date = date(2021, 1, 1)
    end_date = start_date + timedelta(days=20)

    the_business_days = business_days(start_date, end_date)

    with ThreadPoolExecutor() as executor:
        rates_list = list(executor.map(get_rate, the_business_days))

    print(rates_list)


def get_rates() -> None:
    """ get rates """

    rates_list = []

    start_date = date(2021, 1, 1)
    end_date = start_date + timedelta(days=20)

    for current_date in business_days(start_date, end_date):

        rates_url = (
            "http://127.0.0.1:5050/api/"
            f"{current_date}"
            "?base=INR&symbols=USD,EUR"
        )

        resp = requests.get(rates_url, timeout=60)
        rates_list.append(resp.text)

    print(rates_list)