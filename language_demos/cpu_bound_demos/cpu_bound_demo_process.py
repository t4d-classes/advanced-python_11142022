""" cpu bound demo multi"""

from typing import Generator
import itertools
import multiprocessing
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

    with multiprocessing.Manager() as manager:

        results = manager.list()

        processes: list[multiprocessing.Process] = []

        for _ in range(8):
            a_process = multiprocessing.Process(
                target=calc_fib_total, args=(results,))
            a_process.start()
            processes.append(a_process)

        for a_process in processes:
            a_process.join()

        print(len(results))

    print(time.time() - start_time)
