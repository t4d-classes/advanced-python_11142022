
""" http async """

import asyncio
import aiohttp

url = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin%2Clitecoin%2Cethereum&vs_currencies=usd%2Ceur"
)

async def main() -> None:
    """ main """

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            prices = await resp.json()
            print(prices)


asyncio.run(main())
