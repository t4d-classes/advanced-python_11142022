"""  rate demo package """

import time

from rates_demo.rates_api_server import rates_api_server
from rates_demo.get_rates import get_rates, get_rates_threaded

if __name__ == "__main__":

    health_check_url = "http://localhost:5050/check"

    with rates_api_server(health_check_url):

        start_time = time.time()
        get_rates()
        print(f"non-threaded: {time.time() - start_time}")

        start_time = time.time()
        get_rates_threaded()
        print(f"threaded: {time.time() - start_time}")