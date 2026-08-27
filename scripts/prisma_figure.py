#!/usr/bin/env python3
"""PRISMA flow figure (frozen 2026-08-22 funnel).

Numbers are the frozen funnel from corpus-freeze.md / audit_v2_results.txt.
Outputs Figures/PrismaFlowchart2026.pdf and .png (300 dpi), sized for a
single ACL column (~3.03 in): fonts here at 3.4 in render ~= 8 pt printed.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.family"] = ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]

INK = "#1A202C"; SUB = "#4A5568"; EDGE = "#98A4B5"
FILL = "#F1F5F9"; ACCENT_FILL = "#DFF0E4"; ACCENT_EDGE = "#2F855A"

# (headline, n-line, detail-lines)
MAIN = [
    ("Records identified", "n = 5,841",
     ["IEEE 2,076 · ScienceDirect 2,565 · ACM 734",
      "ACL Anthology 223 · SpringerLink 141 · Wiley 102"]),
    ("After de-duplication", "n = 5,680", []),
    ("Title–abstract–keyword screening", "n = 5,487", []),
    ("Full-text review", "n = 270", []),
    ("Round-1 corpus", "n = 44",
     ["31 from search + 13 backward snowballing"]),
    ("Submitted corpus", "n = 65",
     ["2026 update: +21 by forward and", "backward snowballing"]),
    ("Camera-ready update", "+18",
     ["Anthology re-run 2025–26 · snowball", "rounds 1–2 · title-level query"]),
    ("Final corpus", "N = 83", []),
]
# side boxes attached to the arrow gap after main box i: (after_idx, line1, line2)
SIDE = [
    (0, "Duplicates removed", "n = 161"),
    (1, "Pre-screening removals", "n = 193 (IC1 151 · EC1 23 · EC5 19)"),
    (2, "Records excluded", "n = 5,217"),
    (3, "Excluded with reasons", "n = 239"),
]

fig = plt.figure(figsize=(3.4, 7.3), dpi=300)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

MX, MW = 0.02, 0.555            # main column x / width
SX, SW = 0.605, 0.385           # side column x / width
GAP = 0.048                     # vertical gap between main boxes
y = 0.985                       # running top
centers = []

def box(x, ytop, w, h, fill, edge, lw=0.9):
    ax.add_patch(FancyBboxPatch((x, ytop - h), w, h,
                 boxstyle="round,pad=0.006,rounding_size=0.012",
                 fc=fill, ec=edge, lw=lw))

for i, (head, nval, details) in enumerate(MAIN):
    accent = (i == len(MAIN) - 1)
    h = 0.052 + 0.017 * len(details)
    box(MX, y, MW, h, ACCENT_FILL if accent else FILL,
        ACCENT_EDGE if accent else EDGE, 1.3 if accent else 0.9)
    cx = MX + MW / 2
    ty = y - 0.016
    ax.text(cx, ty, head, ha="center", va="center", fontsize=8.3, color=INK)
    ax.text(cx, ty - 0.020, nval, ha="center", va="center",
            fontsize=10 if not accent else 10.5, fontweight="bold",
            color=ACCENT_EDGE if accent else INK)
    for j, d in enumerate(details):
        ax.text(cx, ty - 0.038 - 0.0155 * j, d, ha="center", va="center",
                fontsize=6.1, color=SUB)
    centers.append((cx, y, y - h))
    y -= h + GAP

# arrows between main boxes
for i in range(len(MAIN) - 1):
    ax.add_patch(FancyArrowPatch((centers[i][0], centers[i][2] - 0.004),
                                 (centers[i][0], centers[i + 1][1] + 0.004),
                                 arrowstyle="-|>", mutation_scale=8,
                                 lw=1.0, color=SUB, shrinkA=0, shrinkB=0))

# side boxes on the arrow gaps
for after, l1, l2 in SIDE:
    gap_y = (centers[after][2] + centers[after + 1][1]) / 2
    h = 0.042
    box(SX, gap_y + h / 2, SW, h, "white", EDGE, 0.8)
    ax.text(SX + SW / 2, gap_y + 0.0075, l1, ha="center", va="center",
            fontsize=6.4, color=INK)
    ax.text(SX + SW / 2, gap_y - 0.0095, l2, ha="center", va="center",
            fontsize=5.9, color=SUB)
    ax.add_patch(FancyArrowPatch((centers[after][0], gap_y), (SX - 0.006, gap_y),
                                 arrowstyle="-|>", mutation_scale=7,
                                 lw=0.8, color=SUB, shrinkA=0, shrinkB=0))

ax.set_ylim(y + GAP - 0.02, 1.0)
for ext in ("pdf", "png"):
    fig.savefig(f"Figures/PrismaFlowchart2026.{ext}", bbox_inches="tight", pad_inches=0.03)
print("written Figures/PrismaFlowchart2026.pdf/.png")
