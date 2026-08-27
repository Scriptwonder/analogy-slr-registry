# Snowball 2.0 ROUND 2 — screening (2026-08-22)
# Source: snowball_round2_candidates.csv — forward+backward citations of the 16
# second-update (August 2026) corpus additions (seeds_round2.csv), via Semantic Scholar.
# Registry-deduplicated by scripts/snowball.py (Total.xlsx: 5,524 DOIs / 5,707 titles),
# then deduplicated here against (a) the 65-paper roster, (b) the 16 seeds themselves,
# (c) all 6,130 round-1 candidates (snowball_candidates.csv + snowball-screening.md
# decisions), (d) known exclusions (class_screening.md Tier B/C, RelBERT line, hodel/
# opielka/hofmann, CA-EHN, BATS-PT, MetaLadder, CHAIRO, Petersen & van der Plas).
# Codes as in round 1: IC2 scope · EC3 non-archival · EC5 secondary/survey ·
# EC6 analogy-as-means/not-the-contribution · DUP duplicate record.

## VERDICT — ANY NEW IN-SCOPE?
**1 strong new in-scope candidate + 2 borderline team-calls. Nothing else.**

1. **IN (strong)** — *Enhancing multimodal analogical reasoning with Logic Augmented
   Generation* (Information Fusion, DOI 10.1016/j.inffus.2026.104250; arXiv 2504.11190).
   Archival journal; primary contribution is a KG/logic-augmented method for multimodal
   analogical reasoning → joins the multimodal cells (MARVEL, VOILA, KiVA).
2. **BORDERLINE, lean IN** — *Learning from masked analogies between sentences at
   multiple levels of formality* (Wang & Lepage, Ann. Math. & AI 2023,
   DOI 10.1007/s10472-023-09918-2). Sentence-level analogy learning, NON-morphological
   (formality/style relations) — same school/genre as corpus members lepage1996 and
   wijesiriwardene2024sentence. The AMAI *morphological* sibling was excluded (IC2);
   this one does not trip the morphology rule.
3. **BORDERLINE, lean OUT** — *Analogies Explained: Towards Understanding Word
   Embeddings* (Allen & Hospedales, ICML 2019). Embedding-geometry THEORY of why
   analogies hold. Precedent split: fournier2020 (evaluation-methodology critique)
   was added, but Ethayarajh 2019 (embedding theory, class_screening Tier A) was not
   → by the Ethayarajh/§4-embedding-rule precedent this stays out. Team must confirm
   the split is intentional; if Ethayarajh ever enters, this enters with it.

If the team confirms all three leans: **corpus grows by 1–2; no promised addition was
missed** — the round-2 snowball surfaces no archival analogy generation/evaluation/
benchmark paper at n_links ≥ 2 that the corpus lacks.

## Counts / provenance
- 16 seeds, all resolved (seeds_round2.csv); forward+backward completed for ALL 16
  (no backward-only fallback needed; no rate-limit stalls).
- 1,140 candidates after the script's registry dedup → snowball_round2_candidates.csv.
- Dedup here: −17 roster papers, −14 seed self-matches, −294 already in round-1
  candidate set, −2 known exclusions → **813 genuinely new** (mostly n_links=1 tail).
- Screened per protocol: all 7 at n_links≥3 + all 9 at n_links=2 with analog* in
  title = 16 rows (2 are duplicate-record artifacts). Remaining 31 n=2 rows swept at
  title level: relational-reasoning architectures, RPM surveys, cognitive-science and
  LLM-capability papers — none analogy-primary (EC6/EC5 by inspection). 773 n=1 rows
  left unscreened in the CSV, same treatment as round 1's n=1 tail.

## Screened candidates
| n | Year | Title | Venue | Decision | Reason |
|---|---|---|---|---|---|
| 3 | 2024 | Language Model Behavior: A Comprehensive Survey | Computational Linguistics | OUT EC5 | Survey/secondary, not a primary analogy contribution. |
| 3 | 2022 | Language models show human-like content effects on reasoning | arXiv (PNAS Nexus version exists) | OUT EC6 | Content effects on syllogistic/Wason logical reasoning; analogy not the contribution (S2 record also arXiv-only → EC3). |
| 3 | 2021 | Emergent Symbols through Binding in External Memory (ESBN) | ICLR | OUT EC6 | Memory-binding architecture for abstract rule induction; not analogy gen/eval — mechanism context for §4.5 debate cluster, cite-as-context. |
| 3 | 2019 | Analogies Explained: Towards Understanding Word Embeddings | ICML | TEAM-CALL (lean OUT, EC6/§4 embedding rule) | Embedding-geometry theory; Ethayarajh-precedent keeps it out, fournier-precedent lets it in — decide once, apply to both. |
| 3 | 2018 | Relation Induction in Word Embeddings Revisited | COLING | OUT EC6 | Relation-embedding/induction line — same §4 rule as RelBERT and Kumar & Schockaert. |
| 3 | 1984 | Analogical thinking and human intelligence | Psychology of human intelligence (chapter) | OUT IC2 | Psychology book chapter, not a computational method/benchmark. |
| 3 | n/a | UvA-DARE record: LMs…Syntactic Structure…Brain Activity | repository stub | OUT EC6 | Syntax/neuro topic, repository artifact; not analogy. |
| 2 | 2026 | LLMs provide support for the parallelogram theory of analogy | arXiv 2603.19066 | OUT EC3 | arXiv-only; watch for archival landing (would join §4.5 evaluation-methodology line). |
| 2 | 2025 | Generalizing Analogical Inference from Boolean to Continuous Domains | AAAI | OUT IC2/EC6 | Formal analogical-proportions theory — round-1 section-F rule (exclude pure theory). |
| 2 | 2026 | Enhancing multimodal analogical reasoning with Logic Augmented Generation | Information Fusion | **IN** | Archival; primary contribution = logic/KG-augmented multimodal analogical-reasoning method. |
| 2 | 2024 | Hierarchical Perceptual and Predictive Analogy-Inference Network (HP²AI) | ACM Multimedia | OUT EC6/IC2 | RPM abstract-visual-reasoning solver; corpus consistently excludes the RPM-solver genre (analogy is internal naming). |
| 2 | 2023 | Learning from masked analogies between sentences at multiple levels of formality | Ann. Math & AI | TEAM-CALL (lean IN) | Wang & Lepage; sentence-level (non-morphological) analogy learning — matches lepage1996/wijesiriwardene2024sentence genre. |
| 2 | 1980 | Developmental Patterns in the Solution of Verbal Analogies | Child Development | OUT IC2 | Developmental psychology, not computational. |
| 2 | n/a | UvA-DARE record: Do LLMs solve verbal analogies like children do? | repository stub | DUP | Repository copy of seed johnson2025children. |
| 2 | n/a | Which Pairs to Choose? Exploring Analogical Competency for KG Pruning | none in S2 | OUT EC6 | Analogy as means for KG pruning; no archival venue verifiable in S2. |
| 2 | n/a | "2022. Scientific and creative analogies in pretrained language models" | mis-parsed ref | DUP | Citation-string artifact of seed czinczoll2022scan. |

## Seed resolution notes (seeds_round2.csv)
- 6 ACL external-ids 404'd on S2 (`ACL:` prefix not indexed); resolved via
  `DOI:10.18653/v1/…` (wang2025anascore, qiu2025annotators) or title match
  (jacob2023fame, czinczoll2022scan → arXiv DOIs of the merged records;
  prototypical2025relational → bare S2 id d1a1a97b…, no DOI/ACL id in S2).
- johnson2025children (2025.conll-1.40): S2's merged record carries the arXiv DOI
  10.48550/arXiv.2310.20384 and year 2023, but venue = "Proceedings of the 29th
  CoNLL" — correct paper (Stevenson, ter Veen, Choenni, van der Maas, Shutova).
- webb2023pam-natcomms and webb2023emergent-nhb show S2 year 2022 (preprint year);
  DOIs verified as the 2023 journal versions.
- yang2025symbolic matched to DOI 10.48550/arXiv.2502.20332, S2 venue = ICML (2025).

## Recommended actions
1. Confirm the Information Fusion LAG paper (full-text screen → multimodal cells).
2. Make the paired call: Wang & Lepage AMAI 2023 (lean in) and Allen & Hospedales
   ICML 2019 vs Ethayarajh 2019 (decide the embedding-theory rule once).
3. If any of these enter the corpus, snowball round 3 from them (cache makes it
   cheap: `python3 scripts/snowball.py --seeds <new-seeds.csv> --out …`).
