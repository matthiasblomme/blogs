# ACE on Windows:  Disable Weak TLS Ciphers and Verify with OpenSSL

Let’s be real: if your App Connect Enterprise (ACE) instance still accepts weak TLS ciphers, you're inviting problems. 
Here’s how to disable them, verify they’re gone, and avoid getting roasted in your next security audit.

## The Goal
Kill insecure TLS ciphers in ACE. Then prove they’re dead.

This walkthrough uses ACE in the server role, handling inbound TLS traffic. But the `java.security` config applies just as 
much when ACE acts as a client making outbound HTTPS calls. So if ACE is calling external APIs, brokers, or cloud endpoints—weak 
ciphers still get blocked. That’s exactly what you want.

## Set Up a Test HTTPS Endpoint in ACE
Just need something dumb and HTTPS-enabled:
- Use a simple HTTPInput or REST API flow that returns a static response.
- Example: [HelloWorld_https](https://github.com/matthiasblomme/Ace_test_cases/tree/64d32256864391e330d1d1482fd412c80957998e/HelloWorld_https)
- Create a standalone Integration Server (default HTTPS port is 7843).
- Deploy the simple flow to that Integration Server (this starts the https listener)

Verify the endpoint is reachable.
```powershell
> Test-NetConnection localhost -Port 7843

ComputerName     : localhost
RemoteAddress    : ::1
RemotePort       : 7843
InterfaceAlias   : Loopback Pseudo-Interface 1
SourceAddress    : ::1
TcpTestSucceeded : True
```

If that doesn’t work, your setup’s broken. Fix that first.


## Install OpenSSL on Windows
No, not OpenSSH. OpenSSL.
- Download [Win64 OpenSSL v3.5.2 Light](https://slproweb.com/products/Win32OpenSSL.html)
- Or grab the portable ZIP if you're not into installers
- Choose the "Windows system directory" so you can call it from anywhere
![img.png](img.png)
- Open a new terminal and check that you have OpenSSL available

```powershell
> openssl version
OpenSSL 3.5.0 8 Apr 2025 (Library: OpenSSL 3.5.0 8 Apr 2025)
```

## Baseline Test 1 — Known Good Cipher
Before locking stuff down, let's prove that a strong cipher still works

```powershell
> $TARGET="localhost:7843"
> openssl s_client -connect $TARGET -tls1_2 -cipher "ECDHE-RSA-AES256-GCM-SHA384" -servername localhost
Connecting to ::1
CONNECTED(00000200)
depth=0 C=US, CN=IBM App Connect Enterprise v13.0 HTTPSConnector self signed, O=IBM, OU=IBM App Connect

...

SSL handshake has read 2457 bytes and written 250 bytes
Verification error: self-signed certificate
---
New, TLSv1.2, Cipher is ECDHE-RSA-AES256-GCM-SHA384
Protocol: TLSv1.2

...
---
```

WAs you can see from the output, the command gives us `New, TLSv1.2, Cipher is ECDHE-RSA-AES256-GCM-SHA384`, showing we had a successful TLS handshake. This is our "known good".



## Baseline Test 2 — Known Weak Cipher
Now let's try something weaker

```powershell
> openssl s_client -connect $TARGET -tls1_2 -cipher "AECDH-AES128-SHA" -servername localhost
Connecting to ::1
CONNECTED(0000020C)
1CD30C00:error:0A0000B5:SSL routines:ssl_cipher_list_to_bytes:no ciphers available:ssl\statem\statem_clnt.c:4157:No ciphers enabled for max supported SSL/TLS version
---
no peer certificate available
---
No client certificate CA names sent
---
SSL handshake has read 0 bytes and written 7 bytes
Verification: OK
---
New, (NONE), Cipher is (NONE)
Protocol: TLSv1.2
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
SSL-Session:
Protocol  : TLSv1.2
Cipher    : 0000
Session-ID:
Session-ID-ctx:
Master-Key:
PSK identity: None
PSK identity hint: None
SRP username: None
Start Time: 1755152168
Timeout   : 7200 (sec)
Verify return code: 0 (ok)
Extended master secret: no
---
```

This is a completely different output than before, and it tells us two things
- No matching cipher was AECDH-AES128-SHA, indicated by `no ciphers available` and `New, (NONE), Cipher is (NONE)`
- The SSL handshake did not complete, indicated by `no peer certificate available` and `Cipher    : 0000`

Conclusion: the handshake failed, and cipher was rejected, as it should.


## Why This Still Matters Behind a Firewall

Before you skip the next step, I get it. ACE might be behind SSL-terminating firewalls or proxies, that’s not only normal, 
but should be the standard. However, relying on a single upstream component is a risk. If something manages to bypass 
those layers, ACE still needs to shut these weaknesses. Not all threats come from outside. They can originate from inside 
your network too. Think compromised internal servers, misconfigured apps, or legacy systems...
Your security is only as strong as it's weakest link. Don't let that be ACE!


## Harden ACE by Editing `java.security`
Now that we've got all that foreplay out of the way, let's be serious

Locate your ACE JRE java.security file. The default location is
```
<ACE_INSTALL_DIR>\common\jdk\jre\lib\security\java.security
```

If you used the default ACE install options (like I did), that translates to
```
C:\Program Files\IBM\ACE\13.0.4.0\common\jdk\jre\lib\security\java.security
```

Find the line starting with jdk.tls.disabledAlgorithms, and add your disallowed ciphers there.

The original property (from ACE 13.0.4.0)
```properties
jdk.tls.disabledAlgorithms=SSLv3, TLSv1, TLSv1.1, RC4, DES, MD5withRSA, DH keySize < 1024, DESede, \
    EC keySize < 224, 3DES_EDE_CBC, anon, NULL, ECDH, \
    include jdk.disabled.namedCurves
```

Modified
```properties
jdk.tls.disabledAlgorithms=SSLv3, TLSv1, TLSv1.1, RC4, DES, MD5withRSA, DH keySize < 1024, DESede, \
    EC keySize < 224, 3DES_EDE_CBC, anon, NULL, ECDH, \
    include jdk.disabled.namedCurves \
	AECDH, ECDH_ECDSA_WITH_AES_128_CBC_SHA2562, ECDH_RSA_WITH_AES_128_CBC_SHA2562, \
    ECDH_ECDSA_WITH_AES_256_CBC_SHA384, ECDH_RSA_WITH_AES_256_CBC_SHA384, \
    ECDH_ECDSA_WITH_AES_128_GCM_SHA2562, ECDH_RSA_WITH_AES_128_GCM_SHA2562, \
    ECDH_ECDSA_WITH_AES_256_GCM_SHA384, ECDH_RSA_WITH_AES_256_GCM_SHA384
```

Tips:
- Keep it one logical line or use backslashes for continuation.
- Restart the Integration Server (or Integration Node, if you are using a Node based setup) after changes.



## Verify Ciphers Post-Hardening
Time to check if our changes are working

**Blocked examples:**
```powershell
# RC4 - blocked by openssl itself
> openssl s_client -connect $TARGET -tls1_2 -cipher "RC4-SHA" -servername localhost
Call to SSL_CONF_cmd(-cipher, RC4-SHA) failed
D0EF0C00:error:0A0000B9:SSL routines:SSL_CTX_set_cipher_list:no cipher match:ssl\ssl_lib.c:3399:

# Anonymous - blocked by the integration server
> openssl s_client -connect $TARGET -tls1_2 -cipher "AECDH-AES128-SHA" -servername localhost
Connecting to ::1
CONNECTED(00000208)
08CA0D00:error:0A0000B5:SSL routines:ssl_cipher_list_to_bytes:no ciphers available:ssl\statem\statem_clnt.c:4157:No ciphers enabled for max supported SSL/TLS version
---
no peer certificate available
---
No client certificate CA names sent
---
SSL handshake has read 0 bytes and written 7 bytes
Verification: OK
---
New, (NONE), Cipher is (NONE)
Protocol: TLSv1.2
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
SSL-Session:
    Protocol  : TLSv1.2
    Cipher    : 0000
    Session-ID:
    Session-ID-ctx:
    Master-Key:
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    Start Time: 1755152775
    Timeout   : 7200 (sec)
    Verify return code: 0 (ok)
    Extended master secret: no
---
```

**Allowed example (for control):**
```powershell
> openssl s_client -connect $TARGET -tls1_2 -cipher "ECDHE-RSA-AES256-GCM-SHA384" -servername localhost
Connecting to ::1
CONNECTED(000001F8)
depth=0 C=US, CN=IBM App Connect Enterprise v13.0 HTTPSConnector self signed, O=IBM, OU=IBM App Connect

...

SSL handshake has read 2457 bytes and written 250 bytes
Verification error: self-signed certificate
---
New, TLSv1.2, Cipher is ECDHE-RSA-AES256-GCM-SHA384
Protocol: TLSv1.2

...

---
```

**Optional TLS 1.3 control (if enabled):**
```powershell
>  openssl s_client -connect $TARGET -tls1_3 -ciphersuites "TLS_AES_256_GCM_SHA384" -servername localhost

...

New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Protocol: TLSv1.3

...

---
```




## Keep `java.security` Under Control
Don't harden one server and forget about the rest. Think disaster recovery. Think rebuilds. Think repeatability. 
Or simply automate your server installs.
What do these have in common? They all need to have a single source of truth for your `java.security` file.
So, simply put:
- Store the `java.security` file, or at least the diffs, in version control
- Use pull requests for changes, think Infrastructure as Code (IaaC) and treat this like code.
- Enforce config with Ansible, DSC, ..., or whatever keeps your setup sane

And don't forget, after each update
- Restart the Integration Server
- Verify one of the disabled ciphers
 


Harden it, test it, version it, automate it. Then sleep better, knowing your runtime environment isn’t the weakest link.

---

## References

* [ACE Test Cases Repo](https://github.com/matthiasblomme/Ace_test_cases)
* [Download OpenSSL for Windows](https://slproweb.com/products/Win32OpenSSL.html)
* [ACE default cipher list](https://www.ibm.com/docs/en/sdk-java-technology/8?topic=suites-cipher)

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)

\#IBMChampion \
\#AppConnectEnterprise(ACE) \
\#OpenSSL \
\#Certificates \
\#TLS \
\#HowTo
