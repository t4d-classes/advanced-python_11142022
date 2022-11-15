""" business days module """

from collections.abc import Generator
from datetime import date, timedelta
import holidays

def business_days(start_date: date, end_date: date) -> list[date]:
    """ business days """

    us_holidays = holidays.UnitedStates()

    days: list[date] = []

    for day in range((end_date - start_date).days + 1):
        the_date = start_date + timedelta(day)
        if (the_date.weekday() < 5) and (the_date not in us_holidays):
            days.append(the_date)

    return days


def business_days_gen(
    start_date: date, end_date: date) -> Generator[date,None,None]:
    """ business days """

    us_holidays = holidays.UnitedStates()

    for day in range((end_date - start_date).days + 1):
        the_date = start_date + timedelta(day)
        if (the_date.weekday() < 5) and (the_date not in us_holidays):
            yield the_date