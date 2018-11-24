import aiohttp
import asyncio

async def fetch(session, url, proxy=None):
    async with session.get(url, proxy=proxy) as response:
        return await response.text()


if __name__ == "__main__":
    url = 'https://www.instagram.com/p/BqiS7RaFzuD/?utm_source=ig_share_sheet&igshid=1hdpp1m0gs7li'
    proxy = 'http://127.0.0.1:1087'
    async def main():
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url, proxy)
            print(html)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
