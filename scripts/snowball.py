#!/usr/bin/env python3
"""Snowball 2.0 — forward+backward citation snowballing via Semantic Scholar.

Usage:
  python3 scripts/snowball.py --seeds seeds.csv [--registry Total.xlsx] [--out snowball_candidates.csv]

seeds.csv: one seed per line, column 'id' (header required), using Semantic
Scholar external-id syntax: DOI:10.18653/v1/2024.naacl-long.54, ACL:2023.acl-long.109,
ARXIV:2310.00000, or a bare S2 paperId. Optional column 'label' for your own bookkeeping.

Output: candidates CSV with columns
  n_links, directions, seed_labels, title, year, venue, doi, s2_id, abstract_head
sorted by n_links (papers cited-by/citing multiple seeds first — screen those first).
Candidates already present in the registry (matched by DOI or normalized title) are dropped.

Set S2_API_KEY in the environment for higher rate limits; unauthenticated works but is slow.
Re-runnable: responses are cached in .snowball_cache/ so interrupted runs resume cheaply.
"""
import argparse, csv, json, os, re, sys, time, hashlib
import urllib.request, urllib.error
import ssl

try:
    import certifi
    SSLCTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    SSLCTX = ssl.create_default_context()
    SSLCTX.check_hostname = False
    SSLCTX.verify_mode = ssl.CERT_NONE

API = "https://api.semanticscholar.org/graph/v1/paper/"
FIELDS = "title,year,venue,externalIds,abstract"
CACHE = ".snowball_cache"

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

S2_KEY = _load_key()

def norm_title(t):
    return re.sub(r"[^a-z0-9]", "", str(t).lower())

def fetch(url):
    os.makedirs(CACHE, exist_ok=True)
    key = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest() + ".json")
    if os.path.exists(key):
        return json.load(open(key))
    req = urllib.request.Request(url)
    if S2_KEY:
        req.add_header("x-api-key", S2_KEY)
    delay = 1.2
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=60, context=SSLCTX) as r:
                data = json.load(r)
            json.dump(data, open(key, "w"))
            time.sleep(0.35 if S2_KEY else 1.1)
            return data
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503):
                time.sleep(delay); delay = min(delay * 2, 60)
            elif e.code == 404:
                return None
            else:
                raise
    print(f"  !! giving up on {url}", file=sys.stderr)
    return None

def edges(seed_id, endpoint):
    """endpoint: 'references' (backward) or 'citations' (forward)."""
    out, offset = [], 0
    while True:
        url = f"{API}{seed_id}/{endpoint}?fields={FIELDS}&limit=500&offset={offset}"
        data = fetch(url)
        # data["data"] is null when the publisher elides the list (e.g. paywalled
        # Elsevier references) — treat as empty, not an error.
        rows = (data or {}).get("data") or []
        for row in rows:
            p = row.get("citedPaper") or row.get("citingPaper")
            if p and p.get("title"):
                out.append(p)
        if not data or data.get("next") is None or not rows:
            break
        offset = data["next"]
    return out

def load_registry_keys(path):
    """DOIs + normalized titles already screened, from the registry workbook."""
    dois, titles = set(), set()
    try:
        import pandas as pd
    except ImportError:
        print("pandas not available — skipping registry dedup", file=sys.stderr)
        return dois, titles
    xl = pd.ExcelFile(path)
    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        for col in df.columns:
            c = str(col).lower()
            if c == "doi":
                dois |= {str(v).lower().replace("https://doi.org/", "").strip()
                         for v in df[col].dropna()}
            if c == "title":
                titles |= {norm_title(v) for v in df[col].dropna()}
    return dois, titles

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", required=True)
    ap.add_argument("--registry", default="Total.xlsx")
    ap.add_argument("--out", default="snowball_candidates.csv")
    args = ap.parse_args()

    seeds = list(csv.DictReader(open(args.seeds)))
    reg_dois, reg_titles = (set(), set())
    if os.path.exists(args.registry):
        reg_dois, reg_titles = load_registry_keys(args.registry)
        print(f"registry keys: {len(reg_dois)} DOIs, {len(reg_titles)} titles")

    cand = {}  # key -> record
    for i, s in enumerate(seeds, 1):
        sid, label = s["id"].strip(), s.get("label", s["id"]).strip()
        print(f"[{i}/{len(seeds)}] {label}")
        for endpoint, direction in (("references", "back"), ("citations", "fwd")):
            for p in edges(sid, endpoint):
                doi = (p.get("externalIds") or {}).get("DOI", "")
                key = doi.lower() if doi else norm_title(p["title"])
                if key in reg_dois or norm_title(p["title"]) in reg_titles:
                    continue
                r = cand.setdefault(key, {
                    "title": p["title"], "year": p.get("year"),
                    "venue": p.get("venue"), "doi": doi,
                    "s2_id": p.get("paperId"),
                    "abstract_head": (p.get("abstract") or "")[:300],
                    "seed_labels": set(), "directions": set()})
                r["seed_labels"].add(label)
                r["directions"].add(direction)

    rows = sorted(cand.values(), key=lambda r: -len(r["seed_labels"]))
    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n_links", "directions", "seed_labels", "title", "year",
                    "venue", "doi", "s2_id", "abstract_head"])
        for r in rows:
            w.writerow([len(r["seed_labels"]), "+".join(sorted(r["directions"])),
                        "; ".join(sorted(r["seed_labels"])), r["title"], r["year"],
                        r["venue"], r["doi"], r["s2_id"], r["abstract_head"]])
    print(f"\n{len(rows)} candidates -> {args.out} (screen high n_links first)")

if __name__ == "__main__":
    main()
