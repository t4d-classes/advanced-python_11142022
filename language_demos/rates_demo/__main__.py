"""  rate demo package """

from datetime import date, timedelta
import requests

from rates_demo.business_days import business_days

def get_rates() -> None:

    rates_list = []

    start_date = date(2021, 1, 1)
    end_date = start_date + timedelta(days=20)

    for current_date in business_days(start_date, end_date):

        rates_url = (
            "http://127.0.0.1:5050/api/"
            f"{current_date}"
            "?base=INR&symbols=USD,EUR"
        )

        resp = requests.get(rates_url)
        rates_list.append(resp.text)

    print(rates_list)

if __name__ == "__main__":

    get_rates()


