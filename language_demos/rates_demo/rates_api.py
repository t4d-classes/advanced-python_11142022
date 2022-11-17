""" rates api """

from typing import Any
import math
import pathlib
import time
from flask import Flask, Response, request, jsonify, abort

from rates_demo.rates_data import load_rates_from_history

rates: list[dict[str,Any]] = []

app = Flask(__name__)

@app.route("/check")
def check() -> Response:
    """ health check endpoint """
    return "READY"


# URL: http://127.0.0.1:5050/api/2021-04-08?base=INR&symbols=USD,EUR
# {
#     "date": "2021-04-08",
#     "base": "INR",
#     "rates": {
#         "USD": 70,
#         "EUR": 80,
#     }
# }

@app.route("/api/<rate_date>")
def rates_by_date(rate_date: str) -> Response:
    """ rates by date endpoint """

    time.sleep(0.5)

    for rate in rates:

        if rate["Date"] == rate_date:

            base_country = request.args.get("base", "EUR")

            if "symbols" in request.args:
                country_symbols = request.args["symbols"].split(",")
            else:
                country_symbols = [ col for col in rate if col != "Date" ]

            country_rates = {
                country_code: country_rate / rate[base_country]
                for (country_code, country_rate) in rate.items()
                if country_code != "Date" and
                country_code in country_symbols and
                not math.isnan(country_rate)
            }

            return jsonify({
                "date": rate["Date"],
                "base": base_country,
                "rates": country_rates
            })

    abort(404)


def start_rates_api() -> None:
    """ start rates api """

    global rates

    rates_file_path = pathlib.Path("data", "eurofxref-hist.csv")

    rates = load_rates_from_history(rates_file_path)

    app.run(port=5060)


if __name__ == "__main__":
    start_rates_api()
