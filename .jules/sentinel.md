## 2026-09-14 - [Insecure SSL Fallback]
**Vulnerability:** Downloader had a try-except block that fell back to `verify=False` for SSL requests when downloading files, exposing the application to Man-in-the-Middle (MitM) attacks.
**Learning:** Never disable SSL verification in HTTP clients, as this bypasses the security guarantees of HTTPS and can lead to silent interception or modification of downloaded files.
**Prevention:** Remove the insecure fallback block and enforce `verify=True` in all HTTP client requests. Use appropriate custom CA bundles if self-signed certificates are necessary in internal environments, instead of disabling verification completely.

## 2026-09-15 - [SSRF Bypass in URL Validation]
**Vulnerability:** Downloader validated the domain of the scraped URL using `parsed.netloc.endswith("gov.br")`. This allowed SSRF/malicious downloads by bypass domains such as `attacker-gov.br` and URLs formatted as `https://attacker.com\\@www.gov.br/...`.
**Learning:** `netloc` contains both the hostname and optional authentication information. When checking domains, always extract the `.hostname` rather than the whole `netloc` to prevent `@` bypasses. Always ensure domain validation is strict by checking for an exact match or a `.domain` suffix, avoiding substring matches like `endswith("domain")`.
**Prevention:** Use `parsed.hostname` instead of `parsed.netloc`, and validate using exact matching or `.endswith(".gov.br")` rather than just `.endswith("gov.br")`.
