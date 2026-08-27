#!/usr/bin/env python3
"""Publication-trend figure (stacked bars), cloned from the submitted design.

Reads audit_v2_results.json (run scripts/audit.py --json first) so bars stay
in sync with the frozen corpus. Categories per paper:
  generation-only = in gen coding tables, in no eval-granularity row
  both            = in gen tables AND an eval row
  evaluation-only = everything else in the corpus
Outputs Figures/trend.pdf and Figures/trend.png.
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman", "Times", "DejaVu Serif"]

d = json.load(open("audit_v2_results.json"))
s = d["sets"]
gen = set(s["gen_lexical"]) | set(s["gen_compositional"])
ev = (set(s["auto_lexical"]) | set(s["auto_compositional"])
      | set(s["human_lexical"]) | set(s["human_compositional"]))
years = {r["bibkey"]: int(r["year"]) for r in d["corpus"]}

BINS = ["1980-1989", "1990-1999", "2000-2009", "2010-2019",
        "2020", "2021", "2022", "2023", "2024", "2025", "2026"]

def bin_of(y):
    if y < 1990: return 0
    if y < 2000: return 1
    if y < 2010: return 2
    if y < 2020: return 3
    return 4 + (y - 2020)

gen_only = np.zeros(len(BINS)); both = np.zeros(len(BINS)); ev_only = np.zeros(len(BINS))
for k, y in years.items():
    b = bin_of(y)
    if k in gen and k in ev:   both[b] += 1
    elif k in gen:             gen_only[b] += 1
    else:                      ev_only[b] += 1

assert gen_only.sum() + both.sum() + ev_only.sum() == len(years), "bin total != corpus"

fig, ax = plt.subplots(figsize=(8.9, 5.0), dpi=300)
x = np.arange(len(BINS))
c_gen, c_both, c_ev = "#1f6fd4", "#27a344", "#e8590c"
ax.bar(x, gen_only, color=c_gen, label="Generation only", width=0.62)
ax.bar(x, both, bottom=gen_only, color=c_both, label="Both", width=0.62)
ax.bar(x, ev_only, bottom=gen_only + both, color=c_ev, label="Evaluation only", width=0.62)

totals = gen_only + both + ev_only
for xi, t in zip(x, totals):
    if t > 0:
        ax.text(xi, t + 0.25, str(int(t)), ha="center", va="bottom",
                fontsize=11, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(BINS, rotation=30, ha="right", fontsize=12)
ax.set_ylabel("Number of Papers", fontsize=14, fontweight="bold")
ax.set_xlabel("Year", fontsize=14, fontweight="bold")
ax.set_ylim(0, max(totals) * 1.12)
ax.tick_params(axis="y", labelsize=12)
ax.yaxis.grid(True, color="#DDDDDD", linewidth=0.8)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.legend(loc="upper left", fontsize=12, frameon=False)

fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(f"Figures/trend.{ext}")
print("written Figures/trend.pdf/.png; bin totals:", [int(t) for t in totals])
