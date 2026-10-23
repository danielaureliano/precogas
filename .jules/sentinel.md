## 2026-09-14 - [Insecure SSL Fallback]
**Vulnerability:** Downloader had a try-except block that fell back to `verify=False` for SSL requests when downloading files, exposing the application to Man-in-the-Middle (MitM) attacks.
**Learning:** Never disable SSL verification in HTTP clients, as this bypasses the security guarantees of HTTPS and can lead to silent interception or modification of downloaded files.
**Prevention:** Remove the insecure fallback block and enforce `verify=True` in all HTTP client requests. Use appropriate custom CA bundles if self-signed certificates are necessary in internal environments, instead of disabling verification completely.

## 2026-09-15 - [SSRF Bypass in URL Validation]
**Vulnerability:** Downloader validated the domain of the scraped URL using `parsed.netloc.endswith("gov.br")`. This allowed SSRF/malicious downloads by bypass domains such as `attacker-gov.br` and URLs formatted as `https://attacker.com\\@www.gov.br/...`.
**Learning:** `netloc` contains both the hostname and optional authentication information. When checking domains, always extract the `.hostname` rather than the whole `netloc` to prevent `@` bypasses. Always ensure domain validation is strict by checking for an exact match or a `.domain` suffix, avoiding substring matches like `endswith("domain")`.
**Prevention:** Use `parsed.hostname` instead of `parsed.netloc`, and validate using exact matching or `.endswith(".gov.br")` rather than just `.endswith("gov.br")`.

## 2026-10-19 - [XML External Entity (XXE) Vulnerability]
**Vulnerability:** The application was missing `defusedxml` in its `requirements.txt`. The `openpyxl` library, which `pandas` uses to parse the downloaded `.xlsx` files, is vulnerable to XXE attacks if `defusedxml` is not installed to safely parse the underlying XML structure of Excel files.
**Learning:** Always ensure `defusedxml` is included when parsing potentially untrusted XML-based formats (like `.xlsx` via `openpyxl`). Python's standard library XML parsers are vulnerable to XXE by default.
**Prevention:** Include `defusedxml` in project dependencies when using `openpyxl` or dealing with XML processing from untrusted sources.

## 2026-11-20 - [Path Traversal in URL Extraction]
**Vulnerability:** Downloader used `url.split('/')[-1]` to extract the filename from a URL. This was susceptible to path traversal, as a malicious URL (like `https://.../.../etc/passwd`) would result in a filename of `passwd` or a path attempting to escape the output directory.
**Learning:** Never trust paths or filenames extracted from user-controlled input (like URLs) without strict validation. Always resolve the final path and ensure it is confined to the intended directory using path relative checks.
**Prevention:** Use `os.path.basename(urllib.parse.unquote(urllib.parse.urlparse(url).path))` to extract just the base filename, and use `Path.resolve()` combined with `Path.is_relative_to(base_dir)` to ensure the path cannot escape the intended directory.
