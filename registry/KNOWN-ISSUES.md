# Known Issues in Registry Export

## Data Quality Notes

### FullPaperReading(Analogy)
- **Duplicate Paper ID 23**: appears in rows 42–45; rows are exported as-is
- **Column alignment**: rows 42–45 exhibit off-by-one column shift in source data

### FR-Snowball
- **Provenance gap**: 11 analogy accepts recorded vs. 13 in funnel (+3 untracked)
- **Missing rows**: Papers FP45–47 lack corresponding provenance rows in FullPaperReading(Analogy)
- **Exported as-is**: gaps preserved to maintain traceability

## Export Details

- Abstracts dropped from registry sheets (acl, ieee, sd, Wiley, acm, SpringerLink, springer3) for licensing compliance
- Reviewer identities in full-column sheets are anonymized to codes R1–R4.
- Empty rows removed from all exports
- Timestamp: 2026-08-23
