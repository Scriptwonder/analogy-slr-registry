# Broadened title-level query — full corpus period (run 2026-08-22)

Honors the rebuttal promise to iG8r: "the revision's broadened title-level query will cover the full corpus period." The original conjunct query (analog* AND generation/retrieval/evaluation stems) favors precision; the broadened query drops the second conjunct to catch analogy-central papers phrased as identifying/mining/mapping/solving/probing.

## Method (ready for §3 adaptation)

Query: title matches `\banalog` (analogy, analogies, analogical(ly), analogous, analog) over a fresh ACL Anthology bulk export, all venues, 1980–2026. Script: `scripts/title_query.py`; raw hits: `title-query-hits.csv` (193 hits). The snapshot is the fresh Anthology bib downloaded 2026-08-22 (see script header for URL; pin SHA256 in the release copy — the download landed in the session scratchpad; re-derive the hash when packaging).

## Results

- **193 title hits** total: 87 pre-2018 (never screened by any prior round) + 106 from 2018–2026.
- **2018–2026 partition (106): fully reconciled** — every hit maps to (a) a corpus member, (b) a class_screening.md decision (the 30-paper 2018–2024 recall check), (c) the 2025–26 ATK re-run candidates (rerun_results.txt), or (d) an existing registry/Tier-B/C exclusion (morphology/SIGMORPHON, TALN French EC2, workshop EC1, metaphor scope, application EC6). No new in-scope 2018+ papers.
- **Pre-2018 partition (87):** dominated by the formal/form-level analogy school — morphology, pronunciation-by-analogy, analogical/example-based MT, string-analogy solvers, plus analogy-as-means applications (QA, summarization, WSD, segmentation) → IC2/EC6 under the frozen scope rule. Several semantic-relational candidates were already screened and rejected in round 1 (verified against the registry pool: Turney 2013 TACL supervised analogy/paraphrase; Turney-line relation classification; "Revealing Analogous Themes" 2005; Drozd et al. 2016 "king − man + woman"). **Three candidates were never screened and are in-scope under the freeze rules:**

| Candidate | Backward-citation check (admit iff cited by ≥1 corpus member) | Decision |
|---|---|---|
| Rogers, Drozd & Li 2017, "The (too Many) Problems of Analogical Reasoning with Word Vectors" (*SEM) | **Cited by 3 corpus members** (czinczoll2022scan, fournier2020analogies, afantenos2026proportional) | **IN → rogers2017toomany** (critique cell: schluter2018/fournier2020) |
| Chiu, Poupart & DiMarco 2007, "Generating Lexical Analogies Using Dependency Relations" (EMNLP-CoNLL) | Forward link only (cites turney2006similarity-FP1); no corpus member cites it | OUT — context cite candidate for §4.2 history |
| "Syntactic Dependencies and Distributed Word Representations for Analogy Detection and Mining" (EMNLP 2015) | Forward link only | OUT — context cite candidate |

Two further team-calls defaulted OUT: Linzen 2016 "Issues in evaluating semantic spaces using word analogies" (RepEval → EC1 workshop rule, same as Communicative-Grounding 2021; strong §4.4 context cite) and "Discriminating Rhetorical Analogies in Social Media" (EACL 2014 → EC6 application-lean).

## Verdict

**1 new corpus member (rogers2017toomany).** Combined with snowball round 2 (1 find in 813 new candidates), the two promised protocol runs changed the corpus by +2 of 18 additions and altered no conclusion — the robustness statement nosy asked for (S3) can now be made with receipts.

## Residual limitation (for §7)

The broadened title query ran on the ACL Anthology only; the five non-ACL portals (IEEE, ScienceDirect, ACM, SpringerLink, Wiley) were not re-queried at title level for the full period, and the April 2025 portal boundary stands for those databases. Non-Anthology coverage since April 2025 relies on snowballing (rounds 1–2), which did surface non-ACL members (Nature Comms, ICDM, IEEE TCDS, Information Fusion, ICAART).
