""" rate server module """
from typing import Optional, Any
from multiprocessing.sharedctypes import Synchronized
from decimal import Decimal
import multiprocessing as mp
import sys
import socket
import threading
import re
import decimal
import pyodbc
import requests

from rates_shared.utils import read_config, parse_command


config = read_config()


def create_conn_string(app_config: Any) -> str:
    """ create_conn_string """

    database_server = app_config["database"]["server"]
    database_name = app_config["database"]["database"]
    database_username = app_config["database"]["username"]
    database_password = app_config["database"]["password"]

    conn_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={database_server};"
        f"DATABASE={database_name};"
        f"UID={database_username};"
        f"PWD={database_password};"
    )

    return conn_string


def get_rate_from_api(
        closing_date: str,
        currency_symbol: str,
        currency_rates: list[tuple[str, str, Decimal]]) -> None:
    """ get_rate_from_api """

    decimal.getcontext().prec = 4

    resp = requests.get((
        "http://127.0.0.1:5060"
        f"/api/{closing_date}"
        f"?base=USD&symbols={currency_symbol}"), timeout=60)

    currency_rates.append(
        (closing_date,
         currency_symbol,
         round(float(resp.json()["rates"][currency_symbol]), 4)))


class ClientConnectionThread(threading.Thread):
    """ client connection thread """

    def __init__(self, conn: socket.socket, client_count: Synchronized):
        threading.Thread.__init__(self)
        self.conn = conn
        self.client_count = client_count

    def run(self) -> None:

        try:

            self.conn.sendall(b"Connected to the Rates Server")

            while True:

                command = self.conn.recv(2048).decode("UTF-8")

                command_parts = parse_command(command)

                if not command_parts:
                    self.conn.sendall(b"Invalid Command Format")
                    continue

                self.process_client_command(*command_parts)

        except ConnectionAbortedError:
            pass

        finally:
            with self.client_count.get_lock():
                self.client_count.value -= 1

    def process_client_command(
            self, command_name: str,
            currency_date: str, currency_symbol_str: str) -> None:
        """ process client command """

        if command_name != "GET":
            self.conn.sendall(b"Invalid Command")
            return

        with pyodbc.connect(create_conn_string(config)) as con:

            # parse the currency symbols

            currency_symboles_re = re.compile(r"[,:|;]")
            currency_symbols = currency_symboles_re.split(currency_symbol_str)
            placeholders = ",".join("?" * len(currency_symbols))

            # query the cache for the currency symbols for a given date

            rates_sql = (
                "select closingdate as closing_date, "
                "currencysymbol as currency_symbol, "
                "exchangerate as exchange_rate from rates "
                f"where closingdate = ? and currencysymbol in ({placeholders})"
            )

            cached_currency_symbols: set[str] = set()
            rate_responses = []

            rates_sql_param = [currency_date]
            rates_sql_param.extend(currency_symbols)

            rates = con.execute(rates_sql, rates_sql_param)

            for rate in rates:
                cached_currency_symbols.add(rate.currency_symbol)
                rate_responses.append(
                    f"{rate.currency_symbol}: {rate.exchange_rate}")

            # getting the rates of the uncached currency symbols

            currency_rate_from_api_threads: list[threading.Thread] = []
            currency_rates: list[tuple[str, str, Decimal]] = []

            for currency_symbol in currency_symbols:
                if currency_symbol not in cached_currency_symbols:
                    a_thread = threading.Thread(
                        target=get_rate_from_api,
                        args=(currency_date, currency_symbol, currency_rates))

                    a_thread.start()
                    currency_rate_from_api_threads.append(a_thread)

            for a_thread in currency_rate_from_api_threads:
                a_thread.join()

            # add rates from the api to the cache and response

            if len(currency_rates) > 0:

                decimal.getcontext().prec = 4

                with con.cursor() as cur:

                    insert_rates_sql = (
                        "insert into rates "
                        "(closingdate, currencysymbol, exchangerate) "
                        "values (?, ?, ?)"
                    )

                    print(currency_rates)

                    cur.executemany(insert_rates_sql, currency_rates)

                    for currency_rate in currency_rates:
                        rate_responses.append(
                            f"{currency_rate[1]}: {currency_rate[2]}")

            self.conn.sendall("\n".join(rate_responses).encode("UTF-8"))


def rate_server(host: str, port: int, client_count: Synchronized) -> None:
    """rate server"""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:

        socket_server.bind((host, port))
        socket_server.listen()

        print(f"server is listening on {host}:{port}")

        while True:
            conn, addr = socket_server.accept()
            print(f"client at {addr[0]}:{addr[1]} connected")

            with client_count.get_lock():
                client_count.value += 1

            a_thread = ClientConnectionThread(conn, client_count)
            a_thread.start()


def command_start_server(
        server_process: Optional[mp.Process],
        host: str,
        port: int,
        client_count: Synchronized) -> mp.Process:
    """ command start server """

    if server_process and server_process.is_alive():
        print("server is already running")
    else:
        server_process = mp.Process(
            target=rate_server,
            args=(host, port, client_count))
        server_process.start()
        print("server started")

    return server_process


def command_stop_server(
        server_process: Optional[mp.Process]) -> Optional[mp.Process]:
    """ command stop server """

    if not server_process or not server_process.is_alive():
        print("server is not running")
    else:
        server_process.terminate()
        print("server stopped")

    server_process = None

    return server_process


def command_status(
        server_process: Optional[mp.Process]) -> None:
    """ command status """

    if server_process and server_process.is_alive():
        print("server is running")
    else:
        print("server is stopped")


def command_count(client_count: Synchronized) -> None:
    """ command count """

    print(client_count.value)


def command_clear_cache() -> None:
    """ command clear cache """

    with pyodbc.connect(create_conn_string(config)) as con:
        con.execute("delete from rates")

    print("cache cleared")


def command_exit(
        server_process: Optional[mp.Process]) -> Optional[mp.Process]:
    """ command exit """

    if server_process and server_process.is_alive():
        server_process.terminate()

    server_process = None

    return server_process


def main() -> None:
    """Main Function"""

    try:

        server_process: Optional[mp.Process] = None
        client_count: Synchronized = mp.Value('i', 0)

        host = config["server"]["host"]
        port = int(config["server"]["port"])

        while True:

            command = input("> ")

            if command == "start":
                server_process = command_start_server(
                    server_process, host, port, client_count)
            elif command == "stop":
                server_process = command_stop_server(server_process)
            elif command == "status":
                command_status(server_process)
            elif command == "count":
                command_count(client_count)
            elif command == "clear":
                command_clear_cache()
            elif command == "exit":
                server_process = command_exit(server_process)
                break

    except KeyboardInterrupt:
        server_process = command_exit(server_process)

    sys.exit(0)


if __name__ == '__main__':

    main()
