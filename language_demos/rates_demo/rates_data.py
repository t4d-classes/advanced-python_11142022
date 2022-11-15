""" rates data module """

from typing import Any
import csv
import pathlib
import math

def load_rates_from_history(
    rates_file_path: pathlib.Path) -> list[dict[str, Any]]:
    """ load rates from history """

    rates_history: list[dict[str, Any]] = []

    with open(rates_file_path, encoding="UTF-8") as rates_file:

        rates_file_csv = csv.DictReader(rates_file)

        for rate_row in rates_file_csv:

            rate_entry = { "Date": rate_row["Date"], "EUR": 1.0 }

            for rate_col in rate_row:

                if rate_col != "Date" and len(rate_col) > 0:
                    if rate_row[rate_col] == "N/A":
                        rate_entry[rate_col] = math.nan
                    else:
                        rate_entry[rate_col] = float(rate_row[rate_col])

            rates_history.append(rate_entry)

    return rates_history
