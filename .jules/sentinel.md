## 2026-09-14 - [Insecure SSL Fallback]
**Vulnerability:** Downloader had a try-except block that fell back to `verify=False` for SSL requests when downloading files, exposing the application to Man-in-the-Middle (MitM) attacks.
**Learning:** Never disable SSL verification in HTTP clients, as this bypasses the security guarantees of HTTPS and can lead to silent interception or modification of downloaded files.
**Prevention:** Remove the insecure fallback block and enforce `verify=True` in all HTTP client requests. Use appropriate custom CA bundles if self-signed certificates are necessary in internal environments, instead of disabling verification completely.

## 2026-09-15 - [SSRF Bypass in URL Validation]
**Vulnerability:** Downloader validated the domain of the scraped URL using `parsed.netloc.endswith("gov.br")`. This allowed SSRF/malicious downloads by bypass domains such as `attacker-gov.br` and URLs formatted as `https://attacker.com\\@www.gov.br/...`.
**Learning:** `netloc` contains both the hostname and optional authentication information. When checking domains, always extract the `.hostname` rather than the whole `netloc` to prevent `@` bypasses. Always ensure domain validation is strict by checking for an exact match or a `.domain` suffix, avoiding substring matches like `endswith("domain")`.
**Prevention:** Use `parsed.hostname` instead of `parsed.netloc`, and validate using exact matching or `.endswith(".gov.br")` rather than just `.endswith("gov.br")`.

## 2026-10-16 - [Strict CSP Breaking FastAPI Auto-Generated Documentation]
**Vulnerability:** Adding a strict Content-Security-Policy (CSP) that only allowed `default-src 'self'` broke the auto-generated documentation endpoints (Swagger UI / ReDoc) in FastAPI by blocking their required remote CSS/JS assets.
**Learning:** FastAPI's built-in interactive docs rely on external Content Delivery Networks (CDNs), specifically `https://cdn.jsdelivr.net` for CSS/JS, and `https://fastapi.tiangolo.com` for images, plus they require `unsafe-inline` scripts and styles.
**Prevention:** When implementing CSP headers on a FastAPI service that exposes documentation, ensure the policy explicitly whitelists the required CDNs (e.g. `script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net`) and uses `img-src` or similar directives to permit documentation assets, unless the docs are disabled or hosted entirely self-contained.
