from datetime import date
from concurrent.futures import ThreadPoolExecutor
from rates_demo.business_days import business_days

import threading
import time
import aiohttp
import asyncio
import requests

start_date = date(2020, 8, 1)
end_date = date(2021, 3, 20) # date(2020, 8, 20)
base_currency = 'INR'
currency_symbols = ['USD', 'CAD', 'GBP']

def get_rate_url(business_day):
    return "".join([
        "http://127.0.0.1:5060/api/",
        str(business_day),
        f"?base={base_currency}&symbols=",
        ",".join(currency_symbols)
    ])


def get_rates_sync(start_date, end_date):

    rate_responses = []

    for business_day in business_days(start_date, end_date):
        response = requests.get(get_rate_url(business_day), timeout=60)
        rate_responses.append(response.text)

    return rate_responses


def get_rate_thread(business_day, rate_responses):
    response = requests.get(get_rate_url(business_day), timeout=60)
    rate_responses.append(response.text)


def get_rates_thread(start_date, end_date):
    rate_responses = []
    threads: list[threading.Thread] = []

    for business_day in business_days(start_date, end_date):
        a_thread = threading.Thread(target=get_rate_thread, args=(business_day, rate_responses))
        a_thread.start()
        threads.append(a_thread)

    for a_thread in threads:
        a_thread.join()
    return rate_responses


async def get_rate_async(session, business_day):
    async with session.get(get_rate_url(business_day)) as resp:
        return str(await resp.json())


async def get_rates_async(start_date, end_date):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*[
            get_rate_async(session, business_day)
            for business_day in business_days(start_date, end_date)
        ])


def get_rate_threadpool(business_day):
    response = requests.get(get_rate_url(business_day), timeout=60)
    return response.text


def get_rates_threadpool(start_date, end_date):
    with ThreadPoolExecutor(max_workers=20) as executor:
        return list(executor.map(
            get_rate_threadpool,
            list(business_days(start_date, end_date))
        ))


get_rates_funcs = [
    ("Sync", get_rates_sync, False),
    ("Thread", get_rates_thread, False),
    ("Async", get_rates_async, True),
    ("ThreadPool", get_rates_threadpool, False),
]

async def main():

    for (func_name, get_rates, is_async) in get_rates_funcs:

        start_time = time.time()
        print(f"Running {func_name}")

        rates = []

        if is_async:
            rates = await get_rates(start_date, end_date)
        else:
            rates = get_rates(start_date, end_date)

        # for rate in rates:
        #     print(rate)
        end_time = time.time()

        print(f"{func_name} time elapsed: {end_time - start_time}")

if __name__ == "__main__":
    asyncio.run(main())

