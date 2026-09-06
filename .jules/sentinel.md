## 2023-10-27 - [CRITICAL] Prevent Insecure SSL Fallbacks
**Vulnerability:** Code in `app/services/downloader.py` explicitly fell back to `verify=False` during an `SSLError`.
**Learning:** Fallbacks intended to handle minor misconfigurations can completely bypass security mechanisms, making the system vulnerable to Man-in-the-Middle (MitM) attacks. Never disable SSL verification as an error recovery strategy in production code.
**Prevention:** Fail securely. Let `SSLError` propagate or be handled safely via standard error logging without degrading connection security. Implement strict code review checks targeting `verify=False` in HTTP clients.
