""" single async """

import asyncio
from random import randint

def delay() -> float:
    """ delay """
    return randint(1,10) / 2


async def get_data(task_num: int) -> None:
    """ get data """
    print(f"start get data: {task_num}")
    await asyncio.sleep(delay())
    print(f"end get data: {task_num}")



async def main() -> None:
    """ main """
    await get_data(1)
    await get_data(2)
    await get_data(3)


if __name__ == "__main__":
    asyncio.run(main())
