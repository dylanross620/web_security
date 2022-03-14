# Password Based

1. This lab has clearly different responses when the username is correct vs when it is not. As such, the username can be enumerated easily with a following brute force of the password. The code to do so is in `user_enum.py`
2. This lab had slightly different responses depending on if the username was correct (it was missing a period if the username was correct). I modified the previous code to look for the new tell and put it in `user_enum2.py`
3. This lab implements a brute force prevention mechanism and has identical responses when the username is right or wrong. To get around the brute force protection, we can use the `X-Forwarded-For` header to make the app think that we are an intermediary server for different original users. I couldn't find a way to reliably track the response time using `aiohttp`, so I performed the username enumeration using Burp Intruder instead with a very long password to make string comparisons take a long time. I found that the username of `affiliate` resulted in a longer response time, and as such appeared to be correct. From there, the previous programs can be modified to attempt the possible passwords in `user_enum3.py`
4. This lab implements brute force protection where the number of incorrect attempts is reset once a valid login is made. As such, I logged into a valid account after every other invalid attampt to prevent the lockout count from being reached. The code for this lab is in `brute_force.py`
5. This lab implements account locking if there are too many invalid login attempts for the same account. This fact can be used to enumerate usernames by trying potential passwords multiple times and seeing which ones lock. From there, the password can be brute forced by attempting to see which requests have a different error message, or in this case no error message at all. After waiting for the account to unlock, the found credentials can be used to sign into the compromised account. The code to do this is in `account_lock.py`
6. This lab has a user lock based on making too many HTTP requests from the same IP address. However, the sign in form uses JSON to encode the credentials and accepts a list for the password field. As such, you can provide the entire password list in a single HTTP request and avoid the lock. The code to do this is in `multiple_passwords.py`

# Multi-factor

1. This lab has the MFA check on a different page from the login form, and fails to ensure that the user actually completes the MFA when attempting to access other resources. As such, after logging in you can simply navigate directly to `/my-account` to bypass MFA entirely
2. This lab also has the MFA separate from the login page, and knows which user is being checked via the `verify` cookie. This cookie only contains the username and is unrelated to the password. As such, we can send a GET request to the `/login2` endpoint to generate a MFA code for the victim and then brute force the generated code as it is only 4 digits. The code to do this is in `mfa_cookie.py`
3. This lab consists of attempting to brute force the MFA code by repeatedly signing into the victim account until eventually the correct code is guessed. I skipped this lab as it cannot be made concurrent and as such takes a very long and non-deterministic amount of time to complete.

# Other

1. This lab has a cookie called `stay-logged-in` that is used for "Remember Me" functionality. The function is comprised of the following `base64(username:md5(password))`. As such, the cookie can be brute forced using an existing password list by generating the corresponding token for the victim user's account name. The code to do the brute force can be found in `login_cookie.py`
2. This lab also has a `stay-logged-in` cookie that is used the same as above. This lab also has a XSS vulnerability within the comment functionality of the posts. Combining these 2 and the fact that the `stay-logged-in` cookie is not marked as `HttpOnly`, the cookie can be extracted via the XSS. In my example, I had crafted the following payload to post a user's cookies within a comment on post ID 7 (I made sure to put the payload in a different post so I could actually read the automated comments):
```
<form action="/post/comment" method="POST" id=csrf>
<input required type="hidden" name="postId" value="7">
<input name=comment id="comment-field">
<input required type="text" name="name" value=asdf>
<input required type="email" name="email" value="asdf@asdf">
<input pattern="(http:|https:).+" type="text" name="website">
</form>
<script>
document.getElementById('comment-field').value = document.cookie;
document.getElementById('csrf').submit();
```
From there, taking over the account could be done by simply reading the comment created by the XSS and setting my own cookie to match it. The cookie's structture was the same as the previous lab, and the password could easily be cracked with online tools because it was not salted
3. This lab has a password reset form with the user's account name in it. Because the form does not ask for your current password, I changed the hidden field's value from my own username to `carlos` to reset that account's password instead
4. This lab has a password reset function that is vulnerable to middleware. The endpoint that generates the reset link supports the `X-Forwarded-Host` header, which is used by programs such as reverse proxies to change the destination of generated content. This header can be used to point a reset link for the `carlos` account to the exploit server, where the traffic can be viewed and the reset token can be stored. This same token can then be used on the actual reset page in order to reset the other account's password
5. This lab has a password changing endpoint where the username and password of the account are provided. Additionally, the error message for having an incorrect correct password provided and for having a correct password but 2 new passwords that don't match are different. By taking advantage of these, you can brute force a user's password by submitting password change requests with their username and 2 mismatched new passwords. The code to do this is in `change_password.py`
