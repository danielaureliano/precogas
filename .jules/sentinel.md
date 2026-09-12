## 2026-09-12 - [CRITICAL] Insecure SSL Certificate Validation Fallback
**Vulnerability:** The application had a fallback mechanism that disabled SSL certificate validation (`verify=False`) when an `SSLError` occurred during file downloads. This allowed potential Machine-in-the-Middle (MitM) attacks.
**Learning:** Never bypass SSL verification in production environments, even as a fallback for connectivity issues. This undermines the security guarantees of HTTPS and exposes data in transit to interception or tampering.
**Prevention:** Always enforce strict SSL validation (`verify=True`). If SSL errors occur, they must be treated as security incidents or configuration errors (e.g., outdated CA bundles) and handled accordingly, not bypassed.
