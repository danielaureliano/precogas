## 2024-05-24 - Remove Insecure SSL Fallback
**Vulnerability:** The application was falling back to `verify=False` when SSL verification failed during file downloads, leaving it vulnerable to Man-in-the-Middle (MITM) attacks.
**Learning:** Security controls like SSL verification should never have insecure fallbacks. If a certificate is invalid, the connection should fail securely.
**Prevention:** Never disable SSL verification (`verify=False`) in HTTP clients for production code. Always enforce strict certificate validation.
