## 2026-01-09 - [Scraping on Every Request]
**Learning:** The application was scraping an external government website on *every single request* to `/precos` to find the latest file URL, causing severe latency and potential IP blocking.
**Action:** Implemented caching for the scraped URL using Redis (TTL 1 hour). Always check for expensive external calls in hot paths and cache them.
