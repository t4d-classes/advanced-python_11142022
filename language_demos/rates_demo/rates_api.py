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


def start_rates_api() -> None:
    """ start rates api """

    app.run(port=5050)


if __name__ == "__main__":
    start_rates_api()
