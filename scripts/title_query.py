#!/usr/bin/env python3
"""Broadened title-level query over an ACL Anthology bulk-export snapshot.

Revision-plan item WS1.6 (promised to reviewer iG8r): the original ATK query
required analog* AND a generation/retrieval/evaluation (G/R/E) stem; the
broadened query drops the second conjunct and matches every entry whose TITLE
contains the analog* stem family (analogy, analogies, analogical,
analogically, analogous, analogue, analog ...), regex r"\banalog"
(case-insensitive), over the FULL corpus period 1980-2026, all Anthology
venues.

Input:  an ACL Anthology bulk BibTeX export, ideally with abstracts
        (https://aclanthology.org/anthology+abstracts.bib.gz).  The snapshot
        used for the paper is pinned by download date + SHA256 in Section 3 /
        the search appendix.
Output: CSV with one row per hit: anthology id, year, title, venue, bibtype,
        and gre_stem (whether a G/R/E stem occurs in title or abstract --
        i.e., whether the ORIGINAL conjunct query could have retrieved the
        record; used to partition hits into previously-retrievable vs.
        newly-visible).

Usage:
  python3 scripts/title_query.py anthology+abstracts.bib[.gz] \
      [--out title-query-hits.csv] [--year-min 1980] [--year-max 2026]

@proceedings entries (front matter for whole volumes) are excluded; every
other entry type (inproceedings, article, ...) is kept.
"""

import argparse
import csv
import gzip
import re
import sys
from collections import Counter

TITLE_RE = re.compile(r"\banalog", re.IGNORECASE)
GRE_RE = re.compile(r"\b(generat|retriev|evaluat)", re.IGNORECASE)
FIELD_START_RE = re.compile(r"^\s*(\w+)\s*=\s*", re.MULTILINE)


def read_text(path):
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as fh:
        return fh.read()


def iter_entries(text):
    """Yield (bibtype, key, body) for each @entry in a bulk bib export."""
    for m in re.finditer(r"^@(\w+)\{([^,\n]*),", text, re.MULTILINE):
        bibtype = m.group(1).lower()
        key = m.group(2).strip()
        # scan to the matching closing brace
        depth = 1
        i = m.end()
        while i < len(text) and depth:
            c = text[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            i += 1
        yield bibtype, key, text[m.end():i - 1]


def fields(body):
    """Extract field->raw-value dict from an entry body (brace-delimited)."""
    out = {}
    for m in FIELD_START_RE.finditer(body):
        name = m.group(1).lower()
        i = m.end()
        if i >= len(body):
            continue
        if body[i] == "{":
            depth, j = 1, i + 1
            while j < len(body) and depth:
                if body[j] == "{":
                    depth += 1
                elif body[j] == "}":
                    depth -= 1
                j += 1
            out[name] = body[i + 1:j - 1]
        elif body[i] == '"':
            # quoted value; may contain brace-protected quotes like {\"u}
            depth, j = 0, i + 1
            while j < len(body):
                c = body[j]
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                elif c == '"' and depth == 0:
                    break
                j += 1
            out[name] = body[i + 1:j]
    return out


def detex(s):
    """Light LaTeX-to-text: drop braces, accents, commands; fold whitespace."""
    s = re.sub(r"\\[a-zA-Z]+\s*", " ", s)      # \textit etc.
    s = re.sub(r"\\[`'^\"~=.]", "", s)          # accent macros
    s = s.replace("{", "").replace("}", "")
    s = s.replace("\\", "")
    return re.sub(r"\s+", " ", s).strip()


def anthology_id(entry_fields, key):
    url = entry_fields.get("url", "")
    m = re.search(r"aclanthology\.org/([^\s/}]+)", url)
    return m.group(1) if m else key


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("bib", help="anthology(+abstracts).bib or .bib.gz")
    ap.add_argument("--out", default="title-query-hits.csv")
    ap.add_argument("--year-min", type=int, default=1980)
    ap.add_argument("--year-max", type=int, default=2026)
    args = ap.parse_args()

    text = read_text(args.bib)
    n_entries = 0
    hits = []
    out_of_range = skipped_proceedings = no_year = 0

    for bibtype, key, body in iter_entries(text):
        n_entries += 1
        f = fields(body)
        title = detex(f.get("title", ""))
        if not TITLE_RE.search(title):
            continue
        if bibtype == "proceedings":
            skipped_proceedings += 1
            continue
        ymatch = re.search(r"\d{4}", f.get("year", ""))
        if not ymatch:
            no_year += 1
            continue
        year = int(ymatch.group(0))
        if not (args.year_min <= year <= args.year_max):
            out_of_range += 1
            continue
        venue = detex(f.get("booktitle", "") or f.get("journal", ""))
        abstract = detex(f.get("abstract", ""))
        gre = bool(GRE_RE.search(title) or GRE_RE.search(abstract))
        hits.append({
            "id": anthology_id(f, key),
            "year": year,
            "title": title,
            "venue": venue,
            "bibtype": bibtype,
            "gre_stem": int(gre),
        })

    hits.sort(key=lambda h: (h["year"], h["id"]))
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "year", "title", "venue",
                                           "bibtype", "gre_stem"])
        w.writeheader()
        w.writerows(hits)

    by_decade = Counter((h["year"] // 10) * 10 for h in hits)
    gre_n = sum(h["gre_stem"] for h in hits)
    print(f"entries parsed: {n_entries}")
    print(f"title-level analog* hits {args.year_min}-{args.year_max}: "
          f"{len(hits)}  (G/R/E stem present: {gre_n}; absent: "
          f"{len(hits) - gre_n})")
    print(f"excluded: {skipped_proceedings} proceedings front-matter, "
          f"{out_of_range} outside year range, {no_year} without year")
    print("per-decade:", dict(sorted(by_decade.items())))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
