# Under-retrieval class — screening worksheet for the team
# Class definition: archival ACL Anthology papers 2018–2024 with analog* in the TITLE
# whose title+abstract contain NO generation/retrieval/evaluation stem — i.e., papers
# the original ATK query could not retrieve by construction. 30 members found.
# My abstract/title-level pre-screen below; FINAL EC6/IC2 calls are yours.
# Goal: decide K (how many enter the corpus) before posting the rebuttal.

## Tier A — likely ELIGIBLE (screen first; my guess: most enter)
| Year | Paper | Venue | Why likely in |
|---|---|---|---|
| 2021 | BERT is to NLP what AlexNet is to CV: Can PLMs Identify Analogies? (Ushio+) | ACL | capability evaluation, lexical — same cell as lewis/qin/stevenson line (already conceded in draft) |
| 2022 | Life is a Circus and We are the Clowns: Automatically Finding Analogies… (Sultan & Shahaf) | EMNLP | analogy MINING method — corpus already includes analogy mining (CAM, Hope+ 2017); RQ1 |
| 2023 | FAME: Flexible, Scalable Analogy Mappings Engine (Sultan & Shahaf) | EMNLP | mapping engine — modern descendant of corpus members SME/ACME/LISA; RQ1 |
| 2022 | Scientific and Creative Analogies in Pretrained Language Models (Czinczoll+) | Findings EMNLP | SCAN dataset — PLM analogy-evaluation benchmark; RQ2 |
| 2022 | Probing Relational Knowledge in Language Models via Word Analogies (Rezaee & Camacho-Collados) | Findings EMNLP | probing/capability evaluation, lexical |
| 2023 | In-Context Analogical Reasoning with Pre-Trained Language Models | ACL | LLM prompting for analogy tasks — cf. corpus member Yasunaga+ 2024. NOTE: if coded as LLM-generation single-prompt, HITL stat becomes 10/19 (53%) — still a majority; keep "over half" wording |
| 2019 | Towards Understanding Linear Word Analogies (Ethayarajh+) | ACL | critique of word-analogy evaluation — same genre as corpus member Schluter 2018 |
| 2020 | Analogies minus analogy test: measuring regularities in word embeddings | CoNLL | same genre as Schluter 2018 (evaluation-methodology critique) |
| 2021 | Paraphrases do not explain word analogies | EACL | same genre |

## Tier B — borderline (team call)
| Year | Paper | Venue | Consideration |
|---|---|---|---|
| 2020 | CA-EHN: Commonsense Analogy from E-HowNet | LREC | analogy resource/KB — is a dataset-only contribution in scope? cf. E-KAR (in) |
| 2024 | BATS-PT: Portuguese MLMs on Lexico-Semantic Analogy | LREC-COLING? | multilingual eval dataset (paper in English) |
| 2018 | Context Encoder for Analogies on Strings | PACLIC | formal string analogies — Lepage school; corpus includes Lepage 1996 |
| 2018 | Tools for Production of Analogical Grids + N-gram resource | LREC | Lepage school tooling/resource |
| 2020 | Analogy Models for Neural Word Inflection | COLING | analogy-based generation of inflections — linguistic analogy (morphology), may fail IC2 scope |
| 2023 | Validation of BATS Translation into Croatian/Lithuanian… | RANLP? | resource translation |

## Tier C — likely OUT (EC code noted)
| Year | Paper | Why out |
|---|---|---|
| 2023 | Solving Hard Analogy Questions with Relation Embedding Chains (Kumar & Schockaert) | EC6 — relation-embedding contribution (same rule as RelBERT; already handled in draft) |
| 2018 | Analogies in Complex Verb Meaning Shifts | linguistics analysis, EC6 |
| 2018 | Can Domain Adaptation be Handled as Analogies? | application uses analogy, EC6 |
| 2018 | Sound Analogies with Phoneme Embeddings | phonology, EC6/IC2 |
| 2020 | Réseaux de neurones pour la résolution d'analogies… (TALN) | EC2 non-English |
| 2021 | Caractérisation des relations sémantiques… (TALN) | EC2 non-English |
| 2021 | Communicative Grounding of Analogical Explanations in Dialogue | workshop venue → EC1 |
| 2023 | Analogy in Contact: Maltese Plural Inflection | morphology, EC6/IC2 |
| 2023 | Improving Continual RE by Distinguishing Analogous Semantics | application, EC6 |
| 2023 | MEAN: Metaphoric Erroneous ANalogies dataset | metaphor exclusion (§3.1) |
| 2024 | Mind Your Neighbours… Rhetorical Role Labelling | application, EC6 |
| 2024 | Semantic Exploration of Textual Analogies for Plagiarism Detection | application, EC6 |

## Already recovered by your own snowballing (evidence the protocol self-corrects)
- ARN: Analogical Reasoning on Narratives (TACL 2024) — in corpus
- AnaloBench (EMNLP 2024) — in corpus
- Sentence Analogy Identification & Structure Encoding (Findings EACL 2024) — in corpus

## What this means for the rebuttal (proposed language shape)
Do NOT post "two bounded misses." Post the class story:
1. Cause: the G/R/E conjunct trades recall for precision; it cannot retrieve analogy
   papers described with mining/mapping/solving/probing vocabulary.
2. Quantification: 30 title-level class members on the Anthology 2018–2024; 3 already
   recovered by snowballing; after eligibility screening, K = ⟦team fills: expect ~6–10⟧
   enter the corpus (list them).
3. Robustness: additions concentrate in lexical/automatic/accuracy and
   evaluation-methodology cells → Observation 1 strengthened; Observation 2 unchanged
   or 10/19 "majority"; Observation 3 enriched (Ethayarajh line supports the
   accuracy-confound argument).
4. Remediation commitment: report both analyses in the search appendix and adopt a
   TARGETED update protocol (completed Anthology re-run + snowballing from all
   additions) — NOT a six-portal re-run. Justification: every admitted paper is an
   Anthology publication, and recent non-Anthology corpus members (CHI 2025 etc.)
   entered via snowballing, not portal queries. State the scope in Limitations;
   corrected PRISMA figure.
