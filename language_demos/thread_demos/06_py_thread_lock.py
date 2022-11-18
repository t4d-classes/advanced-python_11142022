""" py thread lock """

import threading
import time

counter = 2

counter_lock = threading.Lock()

def do_it() -> None:
    """ do it """

    global counter

    with counter_lock:
        x = counter
        time.sleep(1)
        x = x - 1
        counter = x

print(f"start counter: {counter}")

thread1 = threading.Thread(target=do_it)
thread1.start()
thread2 = threading.Thread(target=do_it)
thread2.start()

thread1.join()
thread2.join()

print(f"end counter: {counter}")