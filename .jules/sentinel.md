## 2024-05-24 - Disabling SSL Verification Fallback
**Vulnerability:** The `baixar_arquivo` function in `app/services/downloader.py` was falling back to disabling SSL verification (`verify=False`) when an `SSLError` occurred while fetching the ANP spreadsheet.
**Learning:** This is a Man-in-the-Middle (MitM) vulnerability that allows attackers to intercept and potentially modify the data downloaded from the ANP website. We should never intentionally disable SSL validation on HTTP requests, particularly when connecting to external sources to gather data.
**Prevention:** Never use `verify=False` in `requests.get()` or similar HTTP clients to bypass SSL errors. Handle SSL errors securely, logging them as failures rather than skipping verification.
