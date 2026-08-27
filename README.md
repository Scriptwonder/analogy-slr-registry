# Search Registry and Analysis Artifacts

Companion repository for:

> **A Systematic Review of Analogy Generation and Evaluation: Methods, Metrics, and Challenges.**
> Shutong Wu, Tianyu Zhang, Yang Lu, Jiankun Yang, Jiamu Tang, Hecong Wang, and Zhen Bai.
> *Findings of the Association for Computational Linguistics: EMNLP 2026.*

This repository contains the search registry, screening decisions, and
analysis scripts behind the review (final corpus N = 83). It is the
record-level counterpart to the PRISMA funnel and the coding tables reported
in the paper: 5,841 records identified across six databases, 5,680 after
de-duplication, 5,487 screened, 270 full-text reviewed, 31 included from the
database search, plus 13 from snowballing and 39 from two dated protocol
updates (April 2026 and August 2026).

## Contents

### `/registry/`
Database export CSVs (limited columns: DOI, type, year, source, title — no
abstracts) and the screening/filtering sheets with reviewer identities
anonymized.

- `acl.csv`, `ieee.csv`, `sd.csv`, `Wiley.csv`, `acm.csv`, `SpringerLink.csv`, `springer3.csv` — per-database exports
- `Total_Random.csv` — the pilot screening sample
- `FR-Filtering.csv`, `FR-Filtering(Count).csv` — title/abstract/keyword screening decisions
- `FPAnalogy.csv`, `FullPaperReading(Analogy).csv` — full-text screening and reading decisions
- `FR-Snowball.csv` — round-1 snowball screening
- `KNOWN-ISSUES.md` — data-quality notes

### `/second-update/`
Executed protocol and hit lists for the August 2026 update (Appendix C of the
paper): seed lists, two snowballing rounds, the Anthology re-run, the
broadened title-level query, and the corpus-freeze record.

### `/evidence-table/`
`analogy-evidence-table.csv` — the per-paper characteristics table
(N = 83) as published in the paper's appendix, in machine-readable form.

### `/scripts/`
Python tooling (no external dependencies beyond `matplotlib` for figures):

- `audit.py` — consistency gate: re-derives every count reported in the paper from the registry sheets and coding tables, and fails on any mismatch
- `verify_refs.py` — verifies every cited reference against Crossref / arXiv / Semantic Scholar / the ACL Anthology
- `snowball.py`, `resolve_seeds.py`, `title_query.py` — search-update tooling (Semantic Scholar API, ACL Anthology snapshot)
- `prisma_figure.py`, `taxonomy_figure.py`, `trend_figure.py` — figure generation from the audit output

Note: `audit.py` and `verify_refs.py` run against the paper source tree
(LaTeX coding tables, bib files, and the internal master sheet); they are
released for transparency of the QA procedure. The search and figure scripts
run standalone. Scripts that call the Semantic Scholar API read an `S2_KEY`
environment variable.

## Reproducing the searches

See `queries.md` for the canonical Boolean query, per-database hit counts,
and reproduction notes. Original portal sessions from April 2025 were not
retained (vendors provide no stable session URLs); the record-level exports
in `/registry/` are the authoritative snapshot that was screened. The ACL
Anthology and update-protocol queries are exactly reproducible with the
released scripts.

## Data notes

- **No abstracts.** Database-export abstracts are excluded for licensing
  reasons; only bibliographic metadata is redistributed.
- **Anonymized screeners.** Reviewer identities in screening sheets are
  coded R1–R4.

## License

- **Code** (`/scripts/`): MIT — see `LICENSE`.
- **Data** (everything else): CC BY 4.0 — see `LICENSE-DATA`.

## Citation

```bibtex
@inproceedings{wu2026analogy-slr,
  title     = {A Systematic Review of Analogy Generation and Evaluation:
               Methods, Metrics, and Challenges},
  author    = {Wu, Shutong and Zhang, Tianyu and Lu, Yang and Yang, Jiankun
               and Tang, Jiamu and Wang, Hecong and Bai, Zhen},
  booktitle = {Findings of the Association for Computational Linguistics:
               EMNLP 2026},
  year      = {2026},
  publisher = {Association for Computational Linguistics}
}
```
