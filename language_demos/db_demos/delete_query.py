""" params query """

import pyodbc

from db_demos.conn_info import conn_string


with pyodbc.connect(conn_string) as con:

    rates = con.execute("delete from rates where ratesid = ?", (2,))
