# CORPUS FREEZE — Findings of EMNLP 2026 (frozen 2026-08-22)

**Final N = 83** = 31 (round-1 database search) + 13 (round-1 snowball) + 21 (2026 update) + **18 second-update (August 2026) additions**.
Ground truth for coding = the five tables in `Sections/AppendixA.tex`; QA gate = `scripts/audit.py` (CLAIMS dict), **exit 0 as of this freeze** (51 PASS / 0 FAIL / 7 WARN). Roster + per-year histogram: `audit_v2_results.txt` / `.json`.

## Headline frozen numbers (old → new)

| Metric | Submitted (65) | Frozen (83) |
|---|---|---|
| Corpus | 65 | **83** |
| Generation papers | 29 = 18 lex / 12 comp / 1 both | **35 = 19 lex / 17 comp / 1 both** (both = wang2024know-FP15) |
| LLM generation | 18 = 11 multi / 7 single | **19 = 12 multi / 7 single** |
| HITL (of LLM gen) | 10/18 (56%) | **11/19 (58%)** |
| Non-LLM generation | 11 | **16** |
| Automatic evaluation | 51 = 33 lex / 18 comp | **69 = 42 lex / 27 comp** |
| Human evaluation | 3 lex / 24 comp | **4 lex / 26 comp** |
| Both auto + human | 13 | **16** |
| No formal eval | 1 (salu1994-FP23) | 1 |
| Model-type taxonomy | 17 = 6/7/2/2 (4 paradigms) | **20 = 6 relational / 9 distributional / 2 cognitive / 2 transformation / 1 learned** (5th paradigm) |
| Eval dimensions | 28 acc / 20 sim / 20 val / 4 nov / 19 pref | **42 acc / 23 sim / 22 val / 4 nov / 20 pref** |
| Since 2021 | "≈ half" (was actually 60%) | **55/83 = 66% — "about two-thirds"** |
| Initial-round prose | "45 papers" | **44 (31 + 13)** — the 45th FP.bib key is the excluded Gentner 2001 book |
| Screened (ATK) | 5,488 | **5,487** (ledger's 5,488 counted the header row; pool verified clean, 0 dup DOIs/titles) |

## The 18 additions (provenance → keys)

**Committed in rebuttal (7):** ushio2021bert (ACL 2021; eval auto/lex/acc) · sultan2022life (EMNLP 2022; mining, comp, non-LLM; eval both) · jacob2023fame (EMNLP 2023 — authors Jacob/Shani/Shahaf, rebuttal misattributed to Sultan; gen comp non-LLM) · czinczoll2022scientificcreativeanalogiespretrained (Findings EMNLP 2022; eval auto/lex/acc) · hu2023incontext (ACL 2023; **capability-evaluation** per freeze decision, auto/comp/acc) · fournier2020analogies (CoNLL 2020; eval-critique, auto/lex/sim, distributional paradigm) · johnson2025analogies (CoNLL 2025; eval auto+human/lex/acc).

**2026-update re-run, M-set (3):** wang2025anascore (NAACL 2025; eval-method, auto/lex, sim+val) · zhang2025annotators (Findings ACL 2025; LLM-as-judge, auto/lex, val) · das2025prototypical (INLG 2025; capability eval, auto/comp/acc).

**Snowball 2.0 round 1 (4):** webb2023zeroshot (Nature Comms 2023; PAM mapping model, gen comp non-LLM, auto/comp/acc) · ling2022deepgar (ICDM 2022; gen comp, **learned-relational paradigm**, auto/comp/acc) · afantenos2026proportional (ICAART 2026; gen lex non-LLM, auto/lex/acc) · combs2025tradeoff (IEEE TCDS 2025; eval auto/comp/acc).

**Debate-cluster rule (2):** webb2023emergent (Nature Human Behaviour 2023; capability eval, auto/comp/acc) · yang2025emergent (ICML 2025; mechanistic capability eval, auto/lex/acc).

**Snowball 2.0 round 2 (1):** lippolis2026multimodal (Information Fusion 133:104250, 2026; logic/KG-augmented multimodal analogical reasoning; eval auto/comp/acc — joins the KiVA/MARVEL/VOILA multimodal cells).

**Full-period title query (1):** rogers2017toomany (*SEM 2017; Rogers, Drozd & Li, "The (too Many) Problems of Analogical Reasoning with Word Vectors"; evaluation-methodology critique — schluter2018/fournier2020 cell: auto/lex, similarity, distributional paradigm). Admitted under the first-author backward-citation criterion (2026-08-22): a title-query find enters iff cited by ≥1 existing corpus member — Rogers 2017 is cited by three (czinczoll2022scan, fournier2020analogies, afantenos2026proportional; snowball_round2_candidates.csv).

## Coding decisions applied (2026-08-22, first-author sign-off)

1. **cam/cao Option 2**: bhavya2023cam-FP11 = Multi-step only, NOT HITL (its filter is automatic scorers; the §4.2 prose example must be fixed — text agent). cao2024llm-FP43 ADDED to generation coding: LLM + Multi-step + HITL + compositional (peer-consistent with ju2025toward, chen2024analogymate). Result: HITL 11/19.
2. **hu2023incontext = capability-evaluation**, not generation (precedent: lewis2024counterfactual, webb2025counterfactual, qin2025relevant, stevenson2026children). Keeps the rebuttal's 10-of-18-family claim true in spirit; codebook worked example.
3. **gentner2001analogical-FP40 adjudicated OUT** (EC5 — book/secondary source; snowball-accepted in 2025 but never coded; the posted rebuttal funnel says 65, consistent with exclusion). FP.bib key remains but is not corpus.
4. **Debate-cluster membership rule** (state in §3/codebook): a paper enters the corpus iff (i) archival (journal or refereed proceedings; arXiv-only → EC3), and (ii) its primary contribution is a computational analogy generation/evaluation method, benchmark/resource, or an empirical/mechanistic evaluation of computational systems' analogical capability on semantic-relational (non-morphological) tasks. Replies without archival status and analogy-as-explanans linguistics = context citations.

## Explicit exclusions (logged; cite as context where useful)

| Paper | Code | Reason |
|---|---|---|
| MetaLadder (Findings EMNLP 2025) | EC6 | analogy as means for math solving |
| CHAIRO (ACL 2026) | EC6 | analogy as means for content moderation |
| hodel2024response | EC3 | arXiv-only; context cite in §4.5 |
| opielka2025conceptvectors | EC3 | arXiv-only; context cite |
| hofmann2025derivational (PNAS) | IC2 | derivational morphology, not semantic-relational |
| CA-EHN, BATS-PT, BATS-translation, string-analogy context encoder, analogical grids, neural word inflection (Tier-B six) | EC6/IC2 | embedding-benchmark line / form-level; consistent with RelBERT & Kumar–Schockaert rule |
| CARV; Enhancing-Structural-Mapping (arXiv 2026) | EC3 | not archival at freeze date; re-screen post-publication |
| Wang & Lepage 2023 masked analogies (Ann. Math & AI) | IC2 | formal proportional analogy at sentence level (form-level school); round-2 screener leaned IN — overridden for rule consistency, flagged to team |
| Chiu, Poupart & DiMarco 2007 lexical-analogy generation (EMNLP) | context | title-query find; fails backward-citation criterion (no corpus member cites it — forward link to Turney 2006 only) |
| "Analogy Detection and Mining" (EMNLP 2015) | context | title-query find; fails backward-citation criterion (forward link only) |
| Linzen 2016 "Issues in evaluating semantic spaces" (RepEval) | EC1 | workshop venue (same rule as Communicative-Grounding 2021); context cite in §4.4 |
| "Discriminating Rhetorical Analogies" (EACL 2014) | EC6 | application-lean detection; team-call defaulted out |
| Allen & Hospedales 2019 "Analogies Explained" (ICML) | context | embedding-geometry theory; same class as Ethayarajh 2019 (Tier-A, not taken) |
| zhou2023 "Learning by Analogy" MWP generation | EC6 (retroactive) | registry Accept was a silent drop; adjudicated: contribution is math-word-problem augmentation — repairs the MetaLadder-consistency hole |
| gentner2001analogical-FP40 | EC5 | book (secondary) |

## Protocol runs honoring the rebuttal promises

- **Re-run (promised, done pre-freeze):** July 2026 Anthology ATK re-run → M-set 3 (rerun_results.txt).
- **Snowball round 2 from every addition (promised, done 2026-08-22):** 16 seeds → 1,140 candidates → 813 new after dedup → all n≥2 screened → **exactly 1 new in-scope (lippolis2026multimodal)**. Saturation signal. Files: seeds_round2.csv, snowball_round2_candidates.csv, snowball-round2-screening.md.
- **Broadened title-level query, full period (promised, run 2026-08-22):** fresh Anthology snapshot, analog* in title 1980–2026 → 193 hits (title-query-hits.csv; scripts/title_query.py) → 87 pre-2018 never-screened + 106 post-2018 (all reconciled to prior decisions) → 3 in-scope candidates → **1 admitted (rogers2017toomany)** under the backward-citation criterion. Screening report: title-query-fullperiod.md.

## Still open (not blockers for freeze)

- FR-Snowball sheet has 11 analogy Accepts vs the funnel's +13 (FP45/46/47 lack provenance rows) — registry hygiene before release.
- FullPaperReading(Analogy) duplicate Paper ID 23; tag column off-by-one rows 42–45 — fix in release copy.
- 198 reviewer-name cells (R1/R2/R3/R4) to scrub in the release copy of the registry.
