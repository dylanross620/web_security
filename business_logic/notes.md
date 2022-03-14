1. This lab has the price embedded in the "add to cart" POST request. This value is not verified, so you can change the value using a MITM proxy (as an example, I changed it to 1 which resulted in a price of $0.01)
2. This lab is the same as one from the MFA section
3. This lab incorrectly allows a negative number of items to be added to your cart. However, it does not allow the cart total to be less than $0. As such, you can add the expensive item that you can't afford, then add an appropriate negative number of a cheaper item to mostly cancel out the price, getting a significant discount. You cannot add negative quantities through the UI, however, so a proxy or manual requests are required
4. This lab has an overflow in the cart price, but only allows 99 items to be ordered at a time. This can be exploited by ordering jackets until the price is as close to 0 as possible, then ordering other items to get the price to be at least 0. This ordering can be automated, as shown in `overflow.py`
5. This lab truncates email addresses, and has a `/admin` endpoint that is accessible to users with a `@dontwannacry.com` email address. Addresses are truncated to 255 characters so using an email address of `<'A'*238>@dontwannacry.com.<actual email>` tricks the admin page
6. This lab has the same `/admin` endpoint as the previous. To exploit this lab, you can create a normal account using the provided email client, then change the email associated with the account from its settings page. This new email will not be verified, so you can set it to something such as `test@dontwannacry.com` in order to gain access to the `/admin` page and solve the lab
7. This lab has a vulnerable password change feature, where it will continue to work if a current password is not provided. As such, you can change the `administrator` user's password by changing the username in the request and entirely removing the `current-password` parameter (including its name)
8. This lab has a flaw in the checkout logic. By purchasing a normal item, you can find out about the `/cart/order-confirmation?order-confirmed=true` endpoint, which is where the checkout button takes you after checking that you can afford your cart. By navigating to that page directly, the price check can be skipped, so any item can be bought by putting it in the cart and navigating directly to the page
9. For this lab, you are taken to a page to select a role after signing in with valid credentials. While the available roles for the provided account are `User` and `Content Author`, there is a time between sending the login POST request and sending the GET request for the role selection page where the role defaults to being an administrator. As such, a MITM proxy can be used to drop the GET request, leaving the account in the administrator setting indefinitely
10. This lab has a bug where a coupon code cannot be used twice in a row, but can be used multiple times if another one has been used since. As such, by alternating the input order of 2 coupon codes, you can use both codes infinitely and therefore get an infinite discount. The first code is `NEWCUST5` and is shown on the home page, and the second code can be found by signing up for the newsletter on the bottom of the homepage (it's `SIGNUP30`). As such, you can add a jacket to your cart, then use `coupon_code.py` to automatically send enough alternating requests to make the total be 0
11. This lab has a flaw in that you can get a 30% coupon code and use it to buy a $10 gift card to $7, effectively gaining $3. By doing this repeatedly, you can gain an infinite amount of money. The process is shown in `infinite_money.py`, but it takes a *very* long time to the point where my laptop kept falling asleep and the server started timing out. This can be made faster by buying more than 1 card at a time, but my exploit code shows a working proof of concept so I am calling the lab solved
12. This lab has an encryption oracle that can be used to generate a valid `stay-logged-in` cookie for the administrator user. This can be done by noting that the cookie is encrypted, then Base64 and URL encoded. When you attempt to comment on a post using an invalid email address, the error message is stored encrypted and encoded in the same message within a `notification` cookie. This cookie is then decrypted and displayed in plaintext as an error message when sending a GET request to a post page (where you attempted to submit an invalid comment to). As such, the login cookie can be decrypted and is found to be of the form `<username>:<timestamp>`. By taking that timestamp and sending a comment POST request where the email parameter is `administrator:<timestamp>`, we can get the encrypted message `Invalid email address: administrator:<timestamp>`. After experimentation with padding and modifying ciphertexts, it can be found that by prepending the desired cookie value with 9 bytes (for example, `AAAAAAAAAadministrator:<timestamp>`) and removing the first 32 bytes of the provided ciphertext, the result will then be a correctly padded ciphertext that decrypts to just `administrator:<timestamp>`. At this point, you can log in as the `administrator` user by logging out and manually setting the `stay-logged-in` cookie to equal the calculated ciphertext and refreshing the page