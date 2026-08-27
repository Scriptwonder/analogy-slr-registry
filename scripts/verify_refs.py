#!/usr/bin/env python3
"""Verify that every cited bib entry corresponds to a real, findable work.

Pass 1: parse custom.bib / FP.bib / FP-extended.bib, keep only entries cited
        in the compiled tex files.
Pass 2: for each entry:
          - if it has a DOI  -> Crossref lookup, compare titles
          - elif arXiv id    -> arXiv API, compare titles
          - else             -> Semantic Scholar title search (S2_KEY from .env)
Output: verify_refs_report.md + exit 1 if any NOT_FOUND/MISMATCH.

Results cached in .refcheck_cache/ so re-runs are cheap.
"""
import json
import os
import re
import sys
import time
import hashlib
import unicodedata
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".refcheck_cache")
os.makedirs(CACHE, exist_ok=True)

# ---------- env ----------
S2_KEY = ""
env_path = os.path.join(ROOT, ".env")
if os.path.exists(env_path):
    for line in open(env_path):
        line = line.strip()
        if line.startswith("S2_KEY="):
            S2_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")

# ---------- bib parsing ----------
def parse_bib(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    entries = {}
    # split on @type{key,
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        etype, key = m.group(1).lower(), m.group(2)
        if etype in ("comment", "string", "preamble"):
            continue
        # find balanced closing brace
        depth, i = 1, m.end()
        while i < len(text) and depth > 0:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        body = text[m.end():i - 1]
        fields = {}
        for fm in re.finditer(
            r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\"|\w+)", body
        ):
            val = fm.group(2).strip()
            if val.startswith("{") or val.startswith('"'):
                val = val[1:-1]
            fields[fm.group(1).lower()] = val
        entries[key] = {"type": etype, **fields}
    return entries


def norm_title(t):
    t = unicodedata.normalize("NFKD", t)
    t = re.sub(r"\\[a-zA-Z]+", " ", t)           # latex commands
    t = re.sub(r"[{}$\\]", "", t)
    t = re.sub(r"[^a-z0-9 ]", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def title_sim(a, b):
    """Token-level Jaccard on normalized titles."""
    ta, tb = set(norm_title(a).split()), set(norm_title(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


# ---------- HTTP with cache ----------
def fetch(url, headers=None, tag=""):
    h = hashlib.sha1((tag + url).encode()).hexdigest()
    cpath = os.path.join(CACHE, h + ".json")
    if os.path.exists(cpath):
        return json.load(open(cpath))
    req = urllib.request.Request(url, headers=headers or {})
    req.add_header("User-Agent", "ref-verifier/1.0 (mailto:swu85@ur.rochester.edu)")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        data = {"_http_error": e.code}
    except Exception as e:
        data = {"_error": str(e)}
    json.dump(data, open(cpath, "w"))
    time.sleep(1.1)  # polite: shared by crossref & S2
    return data


def check_crossref(doi, title):
    doi = doi.strip().replace("https://doi.org/", "").replace("http://dx.doi.org/", "")
    doi = urllib.parse.quote(doi, safe="")
    data = fetch(f"https://api.crossref.org/works/{doi}", tag="cr")
    if "_http_error" in data or "_error" in data:
        return None, f"DOI lookup failed ({data.get('_http_error', data.get('_error'))})"
    msg = data.get("message", {})
    cr_title = (msg.get("title") or [""])[0]
    sim = title_sim(title, cr_title)
    year = None
    for k in ("published-print", "published-online", "issued", "created"):
        parts = (msg.get(k) or {}).get("date-parts")
        if parts and parts[0] and parts[0][0]:
            year = parts[0][0]
            break
    return {"title": cr_title, "sim": sim, "year": year,
            "container": (msg.get("container-title") or [""])[:1]}, None


ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})", re.I)


def check_arxiv(aid, title):
    url = f"http://export.arxiv.org/api/query?id_list={aid}"
    h = hashlib.sha1(("ax" + url).encode()).hexdigest()
    cpath = os.path.join(CACHE, h + ".json")
    if os.path.exists(cpath):
        data = json.load(open(cpath))
    else:
        req = urllib.request.Request(url, headers={"User-Agent": "ref-verifier/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                xml = r.read().decode("utf-8", errors="replace")
            tm = re.search(r"<title>(.*?)</title>\s*", xml.split("<entry>")[-1], re.S)
            data = {"title": tm.group(1).strip() if tm else ""}
        except Exception as e:
            data = {"_error": str(e)}
        json.dump(data, open(cpath, "w"))
        time.sleep(1.1)
    if data.get("_error") or not data.get("title"):
        return None, "arXiv lookup failed"
    return {"title": data["title"], "sim": title_sim(title, data["title"])}, None


def check_s2(title, year):
    q = urllib.parse.quote(norm_title(title))
    url = (f"https://api.semanticscholar.org/graph/v1/paper/search/match"
           f"?query={q}&fields=title,year,externalIds,venue,authors")
    headers = {"x-api-key": S2_KEY} if S2_KEY else {}
    data = fetch(url, headers=headers, tag="s2")
    if data.get("_http_error") == 404:
        return None, "no S2 match"
    if "_http_error" in data or "_error" in data:
        return None, f"S2 lookup failed ({data.get('_http_error', data.get('_error'))})"
    hits = data.get("data") or []
    if not hits:
        return None, "no S2 match"
    hit = hits[0]
    return {"title": hit.get("title", ""), "sim": title_sim(title, hit.get("title", "")),
            "year": hit.get("year"),
            "authors": [a.get("name", "") for a in hit.get("authors", [])][:3]}, None


# Real works that Crossref/S2/arXiv cannot index (web resources, trade books).
# Each verified by hand 2026-08-23; the note records how.
MANUALLY_VERIFIED = {
    "dam2022affinity": "IxDF article; URL in bib entry returns the matching page",
    "hudson2013encyclopedia": "Encyclopedia of HCI 2nd ed. chapter; URL in bib entry returns the matching page",
    "spencer2009card": "Rosenfeld Media book, ISBN 978-1-933820-02-6 (publisher site blocks bots)",
    "sep-reasoning-analogy": "Stanford Encyclopedia of Philosophy, Fall 2024 archive URL returns the matching entry",
}


def main():
    cited_path = sys.argv[1] if len(sys.argv) > 1 else None
    cited = set()
    if cited_path and os.path.exists(cited_path):
        cited = {l.strip() for l in open(cited_path) if l.strip()}

    bib = {}
    for f in ("custom.bib", "FP.bib", "FP-extended.bib"):
        bib.update(parse_bib(os.path.join(ROOT, f)))

    keys = sorted(cited & set(bib)) if cited else sorted(bib)
    verified, warned, failed = [], [], []

    for i, key in enumerate(keys, 1):
        e = bib[key]
        title = e.get("title", "")
        year = re.sub(r"\D", "", e.get("year", ""))[:4]
        if not title:
            failed.append((key, "NO TITLE FIELD", ""))
            continue
        if key in MANUALLY_VERIFIED:
            verified.append((key, "manual: " + MANUALLY_VERIFIED[key], 1.0))
            print(f"[{i:3}/{len(keys)}] OK   {key} (manual)", flush=True)
            continue

        # choose verification route
        doi = e.get("doi", "")
        m = ARXIV_RE.search(e.get("url", "") + " " + e.get("journal", "") + " " + e.get("eprint", ""))
        if not m and e.get("eprint", "") and re.fullmatch(r"[0-9]{4}\.[0-9]{4,5}", e.get("eprint", "")):
            m = re.match(r"([0-9]{4}\.[0-9]{4,5})", e["eprint"])

        res, err = None, None
        route = ""
        if doi:
            route = "crossref"
            res, err = check_crossref(doi, title)
        if res is None and m:
            route = "arxiv"
            res, err = check_arxiv(m.group(1), title)
        if res is None:
            route = "s2"
            res, err = check_s2(title, year)

        if res is None:
            failed.append((key, f"NOT FOUND via {route}: {err}", title[:80]))
            status = "FAIL"
        elif res["sim"] >= 0.75:
            ry = res.get("year")
            if year and ry and abs(int(year) - int(ry)) > 1:
                warned.append((key, f"title OK ({route}, sim={res['sim']:.2f}) but year {year} vs {ry}", title[:80]))
                status = "WARN"
            else:
                verified.append((key, route, res["sim"]))
                status = "OK"
        elif res["sim"] >= 0.45:
            warned.append((key, f"partial title match ({route}, sim={res['sim']:.2f}): got '{res['title'][:70]}'", title[:80]))
            status = "WARN"
        else:
            failed.append((key, f"TITLE MISMATCH ({route}, sim={res['sim']:.2f}): got '{res['title'][:70]}'", title[:80]))
            status = "FAIL"
        print(f"[{i:3}/{len(keys)}] {status:4} {key}", flush=True)

    with open(os.path.join(ROOT, "verify_refs_report.md"), "w") as f:
        f.write(f"# Reference verification report\n\n")
        f.write(f"Checked {len(keys)} cited entries: "
                f"{len(verified)} verified, {len(warned)} warnings, {len(failed)} failures.\n\n")
        if failed:
            f.write("## FAILURES (must fix)\n\n")
            for k, why, t in failed:
                f.write(f"- **{k}** — {why}\n  - bib title: {t}\n")
            f.write("\n")
        if warned:
            f.write("## WARNINGS (manual check)\n\n")
            for k, why, t in warned:
                f.write(f"- **{k}** — {why}\n  - bib title: {t}\n")
            f.write("\n")
        f.write("## Verified\n\n")
        for k, route, sim in verified:
            f.write(f"- {k} ({route}, sim={sim:.2f})\n")

    print(f"\n{len(verified)} verified / {len(warned)} warnings / {len(failed)} failures")
    print("Report: verify_refs_report.md")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
