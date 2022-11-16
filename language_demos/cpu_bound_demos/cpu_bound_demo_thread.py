""" cpu bound demo thread """

from typing import Generator
import itertools
import threading
import time

def fibonacci() -> Generator[int, None, None]:
    """ generate an infinite fibonacci sequence """

    num_1 = 0
    num_2 = 1

    yield 0

    while True:

        next_num = num_1 + num_2
        yield next_num
        num_1 = num_2
        num_2 = next_num

def calc_fib_total(p_results: list[int]) -> None:
    """ calc fib total """
    
    total = 0
    for num in itertools.islice(fibonacci(), 0, 500000):
        total += num
    p_results.append(total)

if __name__ == '__main__':

    start_time = time.time()

    results: list[int] = []    
    threads: list[threading.Thread] = []

    for _ in range(8):
        a_thread = threading.Thread(target=calc_fib_total, args=(results,))
        a_thread.start()
        threads.append(a_thread)

    for a_thread in threads:
        a_thread.join()

    print(len(results))

    print(time.time() - start_time)
