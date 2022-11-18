""" thread queues demo """

import threading
import queue
import time
from random import randint

nums_queue: queue.Queue[int] = queue.Queue()
double_nums_queue: queue.Queue[int] = queue.Queue()

generate_nums_done = threading.Event()
double_nums_done = threading.Event()


# step 1
def generate_nums(
    number_of_nums: int,
    queue_nums: queue.Queue[int],
    done: threading.Event) -> None:
    """ generate_nums """

    for _ in range(number_of_nums):
        num = randint(0, 9)
        print("generate number: " + str(num))
        time.sleep(0.01)
        queue_nums.put(num)

    done.set()


# step 2
def double_nums(
    queue_nums: queue.Queue[int],
    queue_double_nums: queue.Queue[int],
    nums_done: threading.Event,
    done: threading.Event,
) -> None:
    """double_nums"""

    one_last_time = False

    while True:
        try:
            num = queue_nums.get(timeout=0.1)
            time.sleep(0.01)
            print("get num: " + str(num))
            double_num = num * 2
            queue_double_nums.put(double_num)
            time.sleep(0.01)
            print("calc double num: " + str(num) + " => " + str(double_num))
        except queue.Empty:
            time.sleep(0.01)
            if nums_done.is_set():
                if one_last_time:
                    # we ran it one last time, and the queue was empty
                    done.set()
                    break
                else:
                    # queue was empty, but we will check again
                    one_last_time = True
                    continue

# step 3
def output_nums(
    queue_double_nums: queue.Queue[int],
    done: threading.Event) -> None:
    """output_nums"""

    one_last_time = False

    while True:
        try:
            double_num = queue_double_nums.get(timeout=0.1)
            time.sleep(0.01)
            print("output num: " + str(double_num))
        except queue.Empty:
            print("output nums queue empty", done.is_set())
            if done.is_set():
                time.sleep(0.01)
                if one_last_time:
                    break
                else:
                    # queue was empty, but we will check again
                    one_last_time = True
                    continue


generate_nums_thread = threading.Thread(
    target=generate_nums, args=(10, nums_queue, generate_nums_done))

double_nums_thread = threading.Thread(
    target=double_nums,
    args=(nums_queue, double_nums_queue, generate_nums_done, double_nums_done))

output_nums_thread = threading.Thread(
    target=output_nums, args=(double_nums_queue, double_nums_done))


generate_nums_thread.start()
double_nums_thread.start()
output_nums_thread.start()


generate_nums_thread.join()
double_nums_thread.join()
output_nums_thread.join()