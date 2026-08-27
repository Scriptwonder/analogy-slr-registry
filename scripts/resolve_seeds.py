#!/usr/bin/env python3
"""Resolve corpus citekeys -> Semantic Scholar ids via the /paper/search/match
endpoint, with generous pacing so the rate-limited search pool doesn't 429.

Reads titles from FP.bib/FP-extended.bib/custom.bib, skips keys already in
seeds.csv, and appends newly resolved (id,label) rows. Idempotent: re-run to
pick up any that failed on a prior pass.

Env: S2_API_KEY (required for a usable rate limit).
"""
import re, csv, json, os, ssl, time, urllib.request, urllib.parse, urllib.error

try:
    import certifi
    SSLCTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    SSLCTX = ssl.create_default_context()
    SSLCTX.check_hostname = False
    SSLCTX.verify_mode = ssl.CERT_NONE

def _load_key():
    k = os.environ.get("S2_API_KEY") or os.environ.get("S2_KEY")
    if k:
        return k.strip()
    try:
        for line in open(".env"):
            if line.strip().startswith(("S2_API_KEY", "S2_KEY")):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return ""

KEY = _load_key()
BASE = "https://api.semanticscholar.org/graph/v1/paper/search/match"
SPACING = 3.0          # seconds between successful calls
BIBS = ["FP.bib", "FP-extended.bib", "custom.bib"]

def norm(s): return re.sub(r"[^a-z0-9]", "", str(s).lower())

def titles():
    blob = "".join(open(f, errors="ignore").read() for f in BIBS)
    out = {}
    for e in re.split(r"\n(?=@)", blob):
        m = re.match(r"@\w+\{([^,]+),", e)
        if not m: continue
        t = re.search(r"title\s*=\s*[{\"]+(.*?)[}\"]+,?\s*\n", e, re.I | re.S)
        y = re.search(r"year\s*=\s*[{\"]?(\d{4})", e, re.I)
        out[m.group(1).strip()] = (
            re.sub(r"[{}\\]|\s+", " ", t.group(1)).strip() if t else "",
            y.group(1) if y else "")
    return out

def call(title):
    url = BASE + "?query=" + urllib.parse.quote(title[:300]) + "&fields=title,year,externalIds"
    req = urllib.request.Request(url)
    if KEY: req.add_header("x-api-key", KEY)
    delay = 3.0
    last = "unknown"
    for _ in range(7):
        try:
            with urllib.request.urlopen(req, timeout=40, context=SSLCTX) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {"data": []}          # match endpoint: 404 = no title match
            if e.code in (429, 500, 502, 503):
                last = f"http{e.code}"; time.sleep(delay); delay = min(delay * 2, 90); continue
            return None
        except Exception as e:
            last = type(e).__name__; time.sleep(delay); delay = min(delay * 2, 90)
    return "FAIL:" + last

def main():
    meta = titles()
    have = {r["label"] for r in csv.DictReader(open("seeds.csv"))}
    corpus = sorted({k.strip() for g in re.findall(r"\\cite\{([^}]+)\}",
                     open("Sections/AppendixA.tex").read()) for k in g.split(",")})
    todo = [k for k in corpus if k not in have]
    ok, nf, fail = [], [], []
    for k in todo:
        title, year = meta.get(k, ("", ""))
        if not title:
            fail.append((k, "no-title")); continue
        data = call(title)
        if isinstance(data, str) and data.startswith("FAIL:"):
            fail.append((k, data)); continue
        hits = (data or {}).get("data") or []
        p = hits[0] if hits else None
        if p and norm(p["title"])[:55] == norm(title)[:55] and (
                not year or (p.get("year") and abs(int(p["year"]) - int(year)) <= 1)):
            ext = p.get("externalIds") or {}
            sid = ("DOI:" + ext["DOI"] if ext.get("DOI")
                   else "ACL:" + ext["ACL"] if ext.get("ACL")
                   else "ARXIV:" + ext["ArXiv"] if ext.get("ArXiv")
                   else p["paperId"])
            ok.append((sid, k))
            print(f"  OK   {k} -> {sid}", flush=True)
        else:
            nf.append((k, (p or {}).get("title", "zero-results")[:45]))
            print(f"  NF   {k} | {(p or {}).get('title','zero-results')[:45]}", flush=True)
        time.sleep(SPACING)
    if ok:
        with open("seeds.csv", "a", newline="") as f:
            csv.writer(f).writerows(ok)
    print(f"\nresolved {len(ok)} | not-found {len(nf)} | failed {len(fail)}", flush=True)
    for k, i in fail: print(f"  FAIL {k} | {i}", flush=True)

if __name__ == "__main__":
    main()
