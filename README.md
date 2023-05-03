# Proxy for editing http requests


General execution steps of the program described below:
1. Firstly the accepting_requests.py accept http requests and write the request body to file by name "http_requests.log".
2. editing_requests.py replace strings which is between two '$' sign with strings from wordlist and send http requests to given url.

For example:

```
POST /login2 HTTP/1.1
Host: 0a3500960335e87ec07ca5ae004a00ae.web-security-academy.net
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Origin: https://0a3500960335e87ec07ca5ae004a00ae.web-security-academy.net
Referer: https://0a3500960335e87ec07ca5ae004a00ae.web-security-academy.net/login2
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Te: trailers
Connection: close

mfa-code=$0195$
```

The program will change `mfa-code` value with string from wordlist and send http requests.
