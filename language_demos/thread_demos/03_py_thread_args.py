""" py thread """

import time
import threading


def some_task(msg: str, msg2: str) -> None:
    """ some task """
    print(msg, msg2)
    print("task name: " + threading.current_thread().getName())
    print("start some task: " + str(threading.get_native_id()))
    time.sleep(2)
    print ("end some task: " + str(threading.get_native_id()))


print("main name: " + threading.current_thread().getName())
print("start main thread: " + str(threading.get_native_id()))

thread1 = threading.Thread(
    target=some_task, args=('hello1', 'goodbye1'), name="threadA")
thread1.start()

thread2 = threading.Thread(
    target=some_task, args=('hello2', 'goodbye2'), name="threadB")
thread2.start()

thread1.join()
thread2.join()

print("end main thread: " + str(threading.get_native_id()))
