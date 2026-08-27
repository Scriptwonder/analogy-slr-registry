#!/usr/bin/env python3
"""Taxonomy figure (rebuttal promise I7, reviewer iG8r) — Figures/TaxonomyFigure2026.{pdf,png}.

Two-panel single-column figure for §4 (near the Model Type discussion):
  (top)    task x granularity matrix — Generation / Evaluation-automatic /
           Evaluation-human rows x Lexical / Compositional columns, cell = paper
           count. A paper can sit in several cells (e.g. wang2024know-FP15 is
           both gen-lexical and gen-compositional; most papers have an
           evaluation row membership too), so cells sum to more than N.
  (bottom) evaluation-model architecture membership as horizontal bars — the
           five explicit-representation paradigms from table:evaluation_model
           plus an "LLM prompting (no explicit repr.)" bar = the LLM-generation
           papers (multi-step ∪ single-prompt rows of table:llm_generation).
           This visualizes §4's finding that LLM-era work bypasses the
           explicit-representation paradigms.

EVERY number is derived at build time from Sections/AppendixA.tex via the
audit parser (scripts/audit.py: parse_appendix / trow) — nothing is hardcoded,
so the figure regenerates if the frozen coding changes. Matplotlib only.

Usage:  python3 scripts/taxonomy_figure.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from audit import parse_appendix, trow  # noqa: E402  (reuse, don't re-implement)

TEX = os.path.join(ROOT, "Sections", "AppendixA.tex")
OUT_PDF = os.path.join(ROOT, "Figures", "TaxonomyFigure2026.pdf")
OUT_PNG = os.path.join(ROOT, "Figures", "TaxonomyFigure2026.png")

# Colors: five explicit-representation paradigms in blue; the LLM-prompting
# bar in orange — it is NOT one of the explicit paradigms, it bypasses them.
PARADIGM_COLOR = "#4878A8"
LLM_COLOR = "#D8823C"


def derive_counts():
    tables = parse_appendix(TEX)
    gen_lex = trow(tables, "table:analogy_gen_granularity", "Lexical-level")
    gen_comp = trow(tables, "table:analogy_gen_granularity", "Compositional-level")
    multi = trow(tables, "table:llm_generation", "Multi-step")
    single = trow(tables, "table:llm_generation", "Single Prompt")
    hitl = trow(tables, "table:llm_generation", "Human-in-the-loop")
    nonllm = trow(tables, "table:llm_generation", "Non-LLM")
    auto_lex = trow(tables, "table:evaluation_by_granularity", "Automatic/Lexical")
    auto_comp = trow(tables, "table:evaluation_by_granularity", "Automatic/Compositional")
    hum_lex = trow(tables, "table:evaluation_by_granularity", "Human/Lexical")
    hum_comp = trow(tables, "table:evaluation_by_granularity", "Human/Compositional")
    dims = {d: trow(tables, "table:target_of_analogy_generation", d)
            for d in ("Accuracy", "Similarity", "Validity", "Novelty",
                      "Human Preference")}
    models = {d: trow(tables, "table:evaluation_model", d)
              for d in ("Relational Graph-based", "Distributional Semantic",
                        "Cognitive/architectural", "Transformation-based",
                        "Learned Relational Representations")}

    # corpus N — same union as scripts/audit.py builds (filter F2)
    corpus = set().union(gen_lex, gen_comp, hitl, multi, single, nonllm,
                         auto_lex, auto_comp, hum_lex, hum_comp,
                         *dims.values(), *models.values())

    matrix = {
        "Generation": (len(gen_lex), len(gen_comp)),
        "Evaluation\n(automatic)": (len(auto_lex), len(auto_comp)),
        "Evaluation\n(human)": (len(hum_lex), len(hum_comp)),
    }
    bars = [
        ("LLM prompting (no explicit representation)", len(multi | single), LLM_COLOR),
        ("Distributional semantic", len(models["Distributional Semantic"]), PARADIGM_COLOR),
        ("Relational graph-based", len(models["Relational Graph-based"]), PARADIGM_COLOR),
        ("Cognitive/architectural", len(models["Cognitive/architectural"]), PARADIGM_COLOR),
        ("Transformation-based", len(models["Transformation-based"]), PARADIGM_COLOR),
        ("Learned relational representations", len(models["Learned Relational Representations"]), PARADIGM_COLOR),
    ]
    return len(corpus), matrix, bars


def main():
    n_corpus, matrix, bars = derive_counts()
    print(f"corpus N = {n_corpus}")
    print("matrix  =", {k.replace(chr(10), " "): v for k, v in matrix.items()})
    print("bars    =", [(l.replace(chr(10), " "), n) for l, n, _ in bars])

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.titlesize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "pdf.fonttype": 42,  # embed TrueType fonts (publisher requirement)
        "ps.fonttype": 42,
    })

    fig = plt.figure(figsize=(3.3, 4.4))

    # ---- top panel: task x granularity matrix -------------------------------
    # [left, bottom, width, height] fractions; top panel needs a wide left
    # margin for the row labels, the bottom panel spans nearly full width.
    ax = fig.add_axes([0.345, 0.625, 0.615, 0.275])
    rows = list(matrix)
    vals = [list(matrix[r]) for r in rows]
    vmax = max(max(v) for v in vals)
    ax.imshow(vals, cmap="Blues", vmin=0, vmax=vmax * 1.25, aspect="auto")
    ax.set_xticks(range(2), ["Lexical", "Compositional"])
    ax.set_yticks(range(len(rows)), rows)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    # white grid between cells
    ax.set_xticks([x - 0.5 for x in range(1, 2)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(rows))], minor=True)
    ax.grid(which="minor", color="white", linewidth=1.6)
    ax.tick_params(which="minor", length=0)
    for i, row in enumerate(vals):
        for j, v in enumerate(row):
            dark = v > 0.55 * vmax
            ax.text(j, i, str(v), ha="center", va="center", fontsize=11,
                    fontweight="bold", color="white" if dark else "#1a3a5c")
    ax.set_title(f"Task × granularity ($N$ = {n_corpus})", pad=6)

    # ---- bottom panel: architecture membership bars --------------------------
    # Labels sit ABOVE each bar (full panel width, single line) so long
    # paradigm names never collide; counts are annotated at the bar ends,
    # which makes an x-axis redundant.
    ax2 = fig.add_axes([0.035, 0.03, 0.925, 0.475])
    counts = [b[1] for b in bars]
    cmax = max(counts)
    for i, (label, count, color) in enumerate(bars):
        ax2.barh(i, count, color=color, height=0.46)
        ax2.text(0, i - 0.52, label, ha="left", va="center", fontsize=10)
        ax2.text(count + cmax * 0.022, i, str(count), va="center",
                 ha="left", fontsize=10)
    ax2.set_ylim(len(bars) - 0.55, -0.95)  # inverted: LLM prompting on top
    ax2.set_xlim(0, cmax * 1.12)
    ax2.set_yticks([])
    ax2.set_xticks([])
    for spine in ax2.spines.values():
        spine.set_visible(False)
    ax2.set_title("Evaluation-model architecture", pad=6)

    os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
    fig.savefig(OUT_PDF)
    fig.savefig(OUT_PNG, dpi=300)
    print(f"wrote {OUT_PDF}")
    print(f"wrote {OUT_PNG}")


if __name__ == "__main__":
    main()
