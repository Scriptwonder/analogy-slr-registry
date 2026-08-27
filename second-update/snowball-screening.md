# Snowball 2.0 — screening shortlist (2026-07-12)
# Source: snowball_candidates.csv (6,130 registry-deduplicated candidates from
# forward+backward citations of all 65 corpus papers, via Semantic Scholar).
# Ranked by n_links = how many corpus papers cite / are cited by the candidate.
# Preliminary IC/EC calls below are MINE from title+venue; final calls are the team's.
# Codes: IC2 in-scope NLP/AI/CS analogy gen+eval · EC1 grey-lit(workshop/poster/EA) ·
# EC3 non-archival · EC5 secondary/survey · EC6 analogy not the contribution.

## Headline
- The snowball independently recovered **all 4 papers the rebuttal already
  committed to adding** (Sultan&Shahaf "Life is a Circus" @8 links, Ushio "BERT
  is to NLP" @7, "In-Context Analogical Reasoning" @6, FAME @3) — confirms those
  promises are real and citation-reachable.
- It also recovered known corpus members (AnaloBench, Beneath-Surface, Counterfactual
  Tasks, Past-Meets-Present, etc.) as a sanity check that dedup + recall work.
- Priority set = 43 NEW analogy candidates with n_links≥3 and year≥2018 (below).
  Full graph (incl. older/classic + n_links 1–2) in snowball_candidates.csv.

## A. Already committed in rebuttal — confirm add (4)
| n | Year | Paper | Venue | Note |
|---|---|---|---|---|
| 8 | 2022 | Life is a Circus… Automatically Finding Analogies | EMNLP | Sultan & Shahaf; mining |
| 7 | 2021 | BERT is to NLP what AlexNet is to CV | ACL | Ushio; capability eval |
| 6 | 2023 | In-Context Analogical Reasoning with PLMs | ACL | LLM prompting |
| 3 | 2023 | FAME: Flexible, Scalable Analogy Mappings Engine | EMNLP | Sultan & Shahaf; mapping |

## B. NEW, strong IN candidates (computational, gen/eval, archival) — screen first
| n | Year | Paper | Venue | Prelim call |
|---|---|---|---|---|
| 3 | 2025 | Can Language Models Serve as Analogy Annotators? | Findings ACL | **IN** — LLM-as-judge eval; also in 2026 re-run M-set. Slots into the new LLM-eval table. |
| 5 | 2022 | Zero-shot visual reasoning through probabilistic analogical mapping | Nature Communications | **IN** — PAM computational model, visual analogy generation/solving. |
| 3 | 2022 | DeepGAR: Deep Graph Learning for Analogical Reasoning | ICDM | **IN** — neural method for analogical reasoning. |
| 4 | 2026 | CARV: Diagnostic Benchmark for Compositional Analogical Reasoning in MLLMs | arXiv | IN if archival lands (currently arXiv → EC3 check); compositional+multimodal eval benchmark. |
| 6 | 2026 | Enhancing Structural Mapping with LLM-derived Abstractions for Analogical… | arXiv | IN if archival (EC3 check); LLM+SME generation — directly feeds reshaped §4.1 fifth paradigm. |
| 3 | 2026 | Learning Proportional Analogies: Lightweight NN vs LLM | ICAART | IN — lexical generation/eval comparison. |
| 3 | 2025 | Evaluating the Tradeoff Between Analogical Reasoning Ability and Efficiency | IEEE TCDS | IN — evaluation study. |
| 3 | 2023 | Solving morphological analogies: from retrieval to generation | Ann. Math & AI | BORDERLINE — generation, but morphology (linguistic analogy); same IC2 scope question as the excluded inflection papers (class_screening.md Tier B). |

## C. Debate cluster (§4.5) — decide corpus membership consistently (plan WS1.8)
| n | Year | Paper | Venue | Note |
|---|---|---|---|---|
| 10 | 2022 | Emergent analogical reasoning in LLMs (Webb) | Nature Human Behaviour | anchor of the §4.5 debate; currently context-cite only |
| 8/5 | 2021/22 | Probabilistic Analogical Mapping (Webb/Holyoak) | Psych Review / Nat Comms | PAM; Psych Review venue → IC2 borderline |
| 4 | 2026 | Emergent Analogical Reasoning in Transformers | arXiv | mechanistic extension |
| 4 | 2026 | Transformer See, Transformer Do: Copying as Intermediate Step… | arXiv | mechanistic |
| 4 | 2023 | Response: Emergent analogical reasoning (Hodel) | arXiv | rebuttal to Webb; arXiv-only → EC3 |
→ If the debate papers stay context-cites, keep them out of the corpus uniformly
  and say so; if any enter, enter Webb 2023 too. Don't split the cluster.

## D. Excluded by existing rule — cite as context, not corpus
| n | Year | Paper | Rule |
|---|---|---|---|
| 3 | 2023 | Solving Hard Analogy Questions with Relation Embedding Chains (Kumar & Schockaert) | embedding-rule (§4), same as RelBERT — rebuttal already states this |

## E. Application / HCI — borderline (EC6: is analogy the contribution or a means?)
| n | Year | Paper | Venue | Prelim |
|---|---|---|---|---|
| 5 | 2026 | Beyond Input–Output: Design-by-Analogy in [creativity] | CHI | borderline; corpus already has CHI (cao2024, ju2025) |
| 3 | 2025 | BioSpark: LLM-augmented Transfer [analogical inspiration] | CHI | borderline |
| 3 | 2026 | AHAlogy: Agent-Supported In-Class Analogical Learning | CHI **Extended Abstract** | OUT — EC1 grey-lit |
| 3 | 2019 | Infer Creative Analogous Relationships from Wikidata | Interacción | borderline method |

## F. Formal analogical-proportions line (Prade & Richard et al.) — team call
Mostly theory; some computational (word-analogy classification). n_links 3 each:
Analogy between concepts (2019, Artif. Intel.); Analogical proportions I (2020) & II
(2024); Any four real numbers… (2024); A Galois Framework… (2022, IARML workshop→EC1);
Classifying/completing word analogies by ML (2021, IJAR). → If any enter, they land
in the lexical/automatic cells; most likely EC6/IC2-scope excluded as formal-logic
theory. Recommend: exclude the pure-theory ones, consider the ML word-analogy ones.

## G. Cognitive science / psychology — likely OUT (IC2: not primarily CS/AI method)
Modelling Analogies and Analogical Reasoning (2025, **TACL** — CS venue but reads as a
review → EC5 secondary; check); Analogical inferences mediated by relational categories
(2023, Cognitive Psychology); The Neural Correlates of Analogy… (2022, Cognitive Sci);
Verbal analogy problem sets: an inventory (2020, Behavior Research Methods — dataset,
borderline resource); Analogy & metareasoning: robot learning (2020); The Influence of
Analogy Instructions on Motor Skills (2018) → OUT.

## Recommended team actions
1. Confirm B additions (target ~5–7: Analogy-Annotators, Zero-shot-PAM, DeepGAR,
   CARV*, Enhancing-Structural-Mapping*, Learning-Proportional-Analogies, Efficiency-
   Tradeoff; *=pending archival). These join the rebuttal's committed 4.
2. Make the WS1.8 debate-cluster call once (C) and apply it uniformly.
3. For the full picture, sweep snowball_candidates.csv n_links≥2 (797 rows) later;
   the ≥3 set here is the high-yield core. Older classics (Gentner 1983 SMT @16 etc.)
   are theory/psychology and mostly out by IC2, but a few (Copycat, Mental Leaps) are
   already cited in §2/§4.
4. Re-run is cheap/idempotent: `python3 scripts/snowball.py --seeds seeds.csv` (cache
   in .snowball_cache/); re-run after adding the new papers as seeds to snowball round 2.
