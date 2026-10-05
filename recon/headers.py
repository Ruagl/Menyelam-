#!/usr/bin/env python3
"""
MENYELAM recon toolkit — security header + CORS misconfiguration quick check.
Usage: python3 headers.py <url> [evil-origin]
"""
import sys, urllib.request, ssl

def check(url, evil="https://evil.example.com"):
    ctx = ssl.create_default_context()
    out = {}
    for origin in (None, evil):
        h = {"User-Agent": "menyelam-recon"}
        if origin: h["Origin"] = origin
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=10, context=ctx)
            out[origin or "no-origin"] = {
                "status": r.status,
                "acao": r.headers.get("Access-Control-Allow-Origin"),
                "acac": r.headers.get("Access-Control-Allow-Credentials"),
                "csp": (r.headers.get("Content-Security-Policy") or "")[:80],
                "xfo": r.headers.get("X-Frame-Options"),
                "hsts": r.headers.get("Strict-Transport-Security"),
            }
        except Exception as ex:
            out[origin or "no-origin"] = {"error": str(ex)[:60]}
    return out

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 headers.py <url>"); sys.exit(1)
    import json
    print(json.dumps(check(sys.argv[1]), indent=2))

if __name__ == "__main__":
    main()
