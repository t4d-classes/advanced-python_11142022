""" simple query """

import pyodbc

from db_demos.conn_info import conn_string


with pyodbc.connect(conn_string) as con:

    rates = con.execute("select currencysymbol as currency_symbol from rates")

    for rate_row in rates:
        print(rate_row.currency_symbol)
