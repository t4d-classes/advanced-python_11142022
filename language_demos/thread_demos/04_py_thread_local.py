""" py thread local """

import time
import threading

my_data = threading.local()

def fn2() -> None:
    """ fn2 """

    time.sleep(1)
    print(f"thread id: {threading.get_native_id()}, msg: {my_data.msg}")


def fn1(msg: str) -> None:
    """ fn1 """

    time.sleep(1)
    print((
            f"thread id: {threading.get_native_id()}, "
            f"assign {msg} to thread local"
        ))
    my_data.msg = msg
    time.sleep(1)
    fn2()


thread1 = threading.Thread(target=fn1, args=("python threads are cool 1",))
thread1.start()
thread2 = threading.Thread(target=fn1, args=("python threads are cool 2",))
thread2.start()


thread1.join()
thread2.join()

