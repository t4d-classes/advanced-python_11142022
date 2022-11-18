""" single async """

import asyncio
import time
from random import randint

def delay() -> float:
    """ delay """
    return randint(1,10) / 2


async def get_data_async() -> int:
    """ get data """
    print("start async get data")
    await asyncio.sleep(delay())
    print("end async get data")
    return 1


def get_data_sync() -> int:
    """ get data """
    print("start sync get data")
    time.sleep(delay())
    print("end sync get data")
    return 2


async def main() -> None:
    """ main """
    result = await asyncio.gather(
        get_data_async(),
        asyncio.to_thread(get_data_sync))
    print(result)

    


if __name__ == "__main__":
    asyncio.run(main())
