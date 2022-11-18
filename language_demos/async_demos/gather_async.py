""" single async """

import asyncio
from random import randint

def delay() -> float:
    """ delay """
    return randint(1,10) / 2


async def get_data(task_num: int) -> int:
    """ get data """
    print(f"start get data: {task_num}")
    await asyncio.sleep(delay())
    print(f"end get data: {task_num}")
    return task_num

async def main() -> None:
    """ main """

    coroutines = [get_data(1), get_data(2), get_data(3)]

    results = await asyncio.gather(*coroutines)
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
