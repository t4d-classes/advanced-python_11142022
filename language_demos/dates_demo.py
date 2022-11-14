""" date demo """

from datetime import datetime, timedelta, date
import time

# wall time performance measurement
# start_time = time.time()
# time.sleep(3)
# end_time = time.time()
# print(end_time - start_time) # time elapsed

start = datetime.now()
print(start)
end = start + timedelta(days=40)
print(end)

print((end - start).days)

independence_day = date(1776, 7, 4)
print(type(independence_day))
print(independence_day + timedelta(days=365.25 * 300))

print(datetime.now().strftime("%B %A"))

tax_day_str = "04-2022-18"

tax_day = datetime.strptime(tax_day_str, "%m-%Y-%d")
print(tax_day)

print(datetime.now().weekday())



