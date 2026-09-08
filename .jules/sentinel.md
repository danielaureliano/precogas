## 2026-09-08 - [CRITICAL] Remove Insecure SSL Verification Fallback
**Vulnerability:** The application attempted to gracefully handle `SSLError` when downloading files from the ANP by falling back to `verify=False` using the `requests` library.
**Learning:** This approach completely defeats the purpose of SSL/TLS and allows attackers to perform Man-in-the-Middle (MitM) attacks to intercept and potentially modify the downloaded files. Such fallbacks are inherently unsafe, especially for operations involving downloading executable/data files.
**Prevention:** Never use `verify=False` in production code. If SSL errors occur, they must be resolved by fixing the underlying certificate issues on the server or the local trust store (e.g., updating `certifi`), rather than bypassing verification.
