#!/usr/bin/env python3
"""
MENYELAM recon toolkit — passive subdomain enumeration + basic web probing.
Usage: python3 recon.py <domain>
Rate: polite by default. Only use against in-scope targets you are authorized to test.
"""
import sys, socket, json, urllib.request, ssl

def passive_subdomains(domain):
    """crt.sh passive enumeration."""
    subs = set()
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "menyelam-recon"})
        data = json.loads(urllib.request.urlopen(req, timeout=20).read())
        for e in data:
            for n in e["name_value"].split("\n"):
                n = n.strip().lower()
                if n and "*" not in n and n.endswith(domain):
                    subs.add(n)
    except Exception as ex:
        print(f"[!] crt.sh failed: {ex}", file=sys.stderr)
    return sorted(subs)

def probe(host):
    """Basic HTTPS probe: status, server header, title."""
    out = {"host": host, "status": None, "server": None, "title": None}
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(f"https://{host}", headers={"User-Agent": "menyelam-recon"})
        r = urllib.request.urlopen(req, timeout=10, context=ctx)
        out["status"] = r.status
        out["server"] = r.headers.get("Server")
        html = r.read(50000).decode("utf-8", "ignore")
        if "<title>" in html.lower():
            t = html.lower().split("<title>", 1)[1].split("</title>", 1)[0]
            out["title"] = t.strip()[:80]
    except Exception as ex:
        out["status"] = f"ERR {type(ex).__name__}"
    return out

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 recon.py <domain>"); sys.exit(1)
    domain = sys.argv[1].lower()
    print(f"[*] Enumerating subdomains for {domain} ...")
    subs = passive_subdomains(domain)
    print(f"[*] Found {len(subs)} subdomains")
    results = []
    for s in subs[:50]:
        r = probe(s)
        results.append(r)
        print(f"  {r['status']}  {r['host']}  [{r['server'] or '-'}]  {r['title'] or ''}")
    with open(f"recon_{domain}.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"[*] Saved recon_{domain}.json")

if __name__ == "__main__":
    main()
