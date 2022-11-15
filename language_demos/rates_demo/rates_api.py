""" rates api """

from typing import Any
import math
import pathlib
import time
from flask import Flask, Response, request, jsonify, abort

rates: list[dict[str,Any]] = []

app = Flask(__name__)

@app.route("/check") 
def check() -> Response:
    """ health check envdpoint """
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
    


def start_rates_api() -> None:
    """ start rates api """

    app.run(port=5050)


if __name__ == "__main__":
    start_rates_api()
