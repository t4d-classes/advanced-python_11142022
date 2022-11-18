""" single async """

import asyncio
from random import randint

def delay() -> float:
    """ delay """
    return randint(1,10) / 2


async def get_data() -> None:
    """ get data """
    print("start get data")
    await asyncio.sleep(delay())
    print("end get data")


async def main() -> None:
    """ main """
    coroutine_obj = get_data()
    print(type(coroutine_obj))

    task_obj = asyncio.create_task(coroutine_obj)
    print(type(task_obj))

    await task_obj


if __name__ == "__main__":
    asyncio.run(main())
