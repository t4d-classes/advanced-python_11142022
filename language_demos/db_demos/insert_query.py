""" params query """

import pyodbc

from db_demos.conn_info import conn_string


with pyodbc.connect(conn_string) as con:

    closing_date = '2021-10-03'
    currency_symbol = 'HKD'
    exchange_rate = 2.34


    rates = con.execute((
        "insert into rates (closingdate, currencysymbol, exchangerate) "
        "values (?, ?, ?)"
        ), (closing_date, currency_symbol, exchange_rate))
