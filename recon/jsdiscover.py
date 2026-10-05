#!/usr/bin/env python3
"""
MENYELAM recon toolkit — JS bundle endpoint discovery.
Usage: python3 jsdiscover.py <url>
Extracts API endpoints, paths and interesting strings from JS files.
"""
import sys, re, urllib.request, ssl

ENDPOINT_RE = re.compile(r'["\'`](/(?:api|v\d|graphql)[^"\'`\s]*)["\'`]', re.I)
PATH_RE = re.compile(r'["\'`](/[a-zA-Z0-9_\-/]{3,80})["\'`]')
SECRET_RE = re.compile(r'(api[_-]?key|secret|token|password)\s*[:=]\s*["\'][^"\']{4,}["\']', re.I)

def fetch(url):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "menyelam-recon"})
    return urllib.request.urlopen(req, timeout=15, context=ctx).read().decode("utf-8", "ignore")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 jsdiscover.py <url>"); sys.exit(1)
    url = sys.argv[1]
    print(f"[*] Fetching {url}")
    html = fetch(url)
    js_urls = set(re.findall(r'(?:src="|href=")([^"]+\.js[^"]*)"', html))
    print(f"[*] Found {len(js_urls)} JS files")
    endpoints, paths = set(), set()
    for j in js_urls:
        if j.startswith("/"):
            j = url.rstrip("/") + j
        elif not j.startswith("http"):
            continue
        try:
            js = fetch(j)
            endpoints.update(ENDPOINT_RE.findall(js))
            paths.update(p for p in PATH_RE.findall(js) if "." not in p.split("/")[-1])
            for m in SECRET_RE.findall(js):
                print(f"  [!] possible secret pattern in {j}: {m[:40]}")
        except Exception as ex:
            print(f"  [!] skip {j}: {ex}")
    print("\n=== API endpoints ===")
    for e in sorted(endpoints)[:50]: print(" ", e)
    print("\n=== Paths ===")
    for p in sorted(paths)[:50]: print(" ", p)

if __name__ == "__main__":
    main()
