# Boolean Search Queries

## Canonical Query

```
(analogy OR analogous OR analogical OR metaphor) AND (generation OR evaluation OR retrieval OR generate OR evaluate)
```

Executed: April 2025

## Per-Database Results

| Database | Count |
|----------|-------|
| IEEE Xplore | 2076 |
| ScienceDirect | 2565 |
| ACM Digital Library | 734 |
| ACL Anthology | 223 |
| SpringerLink | 67 |
| Springer (Secondary) | 74 |
| Wiley | 102 |
| **Total** | **5841** |

## Reproducing the Searches

The original point-and-click portal sessions (April 2025) were not retained;
database vendors do not provide stable URLs for such sessions. The searches are
reproducible from the canonical Boolean query above, entered in each portal's
advanced-search interface over title, abstract, and keyword fields, with the
date range 1980--2025. Note that IEEE Xplore, ScienceDirect, ACM DL,
SpringerLink, and Wiley continuously re-index content, so re-running the query
today will return supersets of the April 2025 hit counts; the record-level
exports in `/registry/` are the authoritative snapshot that the review screened.

The ACL Anthology leg and the second-update queries are exactly reproducible
with the released scripts (`scripts/title_query.py`, `scripts/snowball.py`)
against a dated Anthology snapshot; see `/second-update/` for the executed
protocols and their hit lists.
