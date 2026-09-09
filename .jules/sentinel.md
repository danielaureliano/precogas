## 2024-05-24 - Remove Insecure SSL Fallback in Downloader
**Vulnerability:** In `app/services/downloader.py`, the HTTP client intentionally fell back to `verify=False` if the initial request to download the spreadsheet failed with an `SSLError`.
**Learning:** This architectural gap means any network adversary could execute a Man-in-the-Middle (MitM) attack by intercepting the SSL connection and serving malicious files when the application automatically retried without verifying the certificate.
**Prevention:** Never disable SSL verification (`verify=False`) in HTTP requests. Retrying without SSL verification defeats the purpose of encryption and validation. The application should fail securely if the certificate is invalid.
