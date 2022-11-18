""" single async """

import asyncio
import time
from random import randint

def delay() -> float:
    """ delay """
    return randint(1,10) / 2


async def get_data() -> None: # Task<None>
    """ get data """
    print("start get data")
    await asyncio.sleep(delay())
    print("end get data")



async def main() -> None:
    """ main """
    await get_data()


if __name__ == "__main__":
    asyncio.run(main())
