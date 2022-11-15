""" rates api server """

from contextlib import contextmanager
from collections.abc import Generator
import multiprocessing as mp

import requests
from requests.exceptions import RequestException

from rates_demo.rates_api import start_rates_api

@contextmanager
def rates_api_server(health_check_url: str) -> Generator[None, None, None]:
    """ rates api server """

    print("start server")
    rates_api_process = mp.Process(target=start_rates_api)
    rates_api_process.start()

    while True:

        try:
            requests.get(health_check_url, timeout=2)
            break
        except ConnectionError:
            continue
        except RequestException:
            continue

    yield

    rates_api_process.terminate()
    print("terminate server")