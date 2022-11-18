""" file async """

import asyncio
import aiofiles


async def main() -> None:
    """ main """

    async with aiofiles.open(
        "requirements.txt", "r", encoding="UTF-8") as the_file:
        async for line in the_file:
            print(line.strip())

asyncio.run(main())
