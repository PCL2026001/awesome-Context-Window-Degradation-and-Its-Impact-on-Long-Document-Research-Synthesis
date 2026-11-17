"""
Generate TikZ/PGFPlots figure code for the paper.
Outputs figures.tex which is \input{} into paper.tex.
Uses only Python standard library — no matplotlib/numpy needed.
"""

import csv, os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Load actual results ───────────────────────────────────────────────────────
def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

results    = load_csv(os.path.join(OUTPUT_DIR, "results_v2.csv"))
ablation   = load_csv(os.path.join(OUTPUT_DIR, "ablation_strength.csv"))

# ── Figure 1: Recall@1 vs Position (line chart) ──────────────────────────────
POSITIONS = ["Start\n(0%)", "Early\n(25%)", "Middle\n(50%)", "Late\n(75%)", "End\n(100%)"]
POS_LABELS = ["Start (0%)", "Early (25%)", "Middle (50%)", "Late (75%)", "End (100%)"]
METHODS = [
    ("Full-Context (Baseline 1)",       "fc",  "red!70!black",   "square*",      "solid"),
    ("Chunked Sequential (Baseline 2)", "cs",  "blue!70!black",  "triangle*",    "dashed"),
    ("Overlapping Chunks (Baseline 3)", "oc",  "teal!80!black",  "diamond*",     "dotted"),
    ("Hierarchical 2-Pass (Proposed)",  "h2p", "green!50!black", "pentagon*",    "densely dashdotted"),
]

def recall(method_name, pos_label):
    for r in results:
        if r["method"] == method_name and r["position_label"] == pos_label:
            return float(r["recall_at_1"])
    return 0.0

# Build coordinates for each method
fig1_coords = {}
for mname, mid, color, mark, style in METHODS:
    coords = " ".join(f"({i+1},{recall(mname, pl)})" for i, pl in enumerate(POS_LABELS))
    fig1_coords[mid] = (coords, color, mark, style, mname)

# ── Figure 2: Ablation — strength vs Recall@1 (bar chart) ───────────────────
abl_data = [(float(r["strength"]), float(r["recall_at_1"])) for r in ablation]

# ── TikZ output ───────────────────────────────────────────────────────────────
tikz = r"""\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{pgfplotstable}
"""

# Figure 1 TikZ
fig1 = r"""
% ── Figure 1: Recall@1 vs Evidence Position ──────────────────────────────────
\begin{figure}[t]
\centering
\begin{tikzpicture}
\begin{axis}[
  width=\columnwidth, height=5.5cm,
  xlabel={Evidence Position in Document},
  ylabel={Recall@1},
  ymin=0.80, ymax=1.02,
  xtick={1,2,3,4,5},
  xticklabels={Start\\(0\%),Early\\(25\%),Middle\\(50\%),Late\\(75\%),End\\(100\%)},
  legend style={at={(0.5,-0.28)}, anchor=north, legend columns=2,
                font=\footnotesize, draw=none},
  grid=major, grid style={gray!25},
  tick label style={font=\footnotesize},
  label style={font=\footnotesize},
  ymajorgrids=true,
  cycle list name=color list,
]
"""

for mid, (coords, color, mark, style, mname) in fig1_coords.items():
    short = mname.replace(" (Baseline 1)", " B1").replace(" (Baseline 2)", " B2") \
                 .replace(" (Baseline 3)", " B3").replace(" (Proposed)", "")
    fig1 += f"""\\addplot[color={color}, mark={mark}, {style}, line width=1.2pt,
  mark size=2.5pt] coordinates {{{coords}}};
\\addlegendentry{{{short}}}
"""

fig1 += r"""\end{axis}
\end{tikzpicture}
\caption{Recall@1 vs.\ evidence position for all four retrieval methods
  ($N=200$ trials per cell, random seed~42). The full-context baseline (FC-B1)
  drops to 0.900--0.905 at Early and Middle positions; all chunking methods
  maintain perfect recall across all positions.}
\label{fig:main}
\end{figure}
"""

# Figure 2 TikZ — ablation bar chart
abl_coords = " ".join(f"({s},{r})" for s, r in abl_data)
fig2 = r"""
% ── Figure 2: Ablation — attention-decay strength ────────────────────────────
\begin{figure}[t]
\centering
\begin{tikzpicture}
\begin{axis}[
  width=\columnwidth, height=5cm,
  xlabel={Attention-Decay Strength $\lambda$},
  ylabel={Recall@1 (Middle Position)},
  ymin=0.90, ymax=1.02,
  xtick={0,0.5,1,1.5,1.8,2,2.5,3},
  xticklabel style={font=\scriptsize, rotate=45, anchor=east},
  grid=major, grid style={gray!25},
  tick label style={font=\footnotesize},
  label style={font=\footnotesize},
  ybar, bar width=0.18cm,
  fill=blue!40, draw=blue!60!black,
]
""" + f"\\addplot coordinates {{{abl_coords}}};\n" + r"""
\end{axis}
\end{tikzpicture}
\caption{Ablation: Recall@1 of the Full-Context baseline at the Middle~(50\%)
  position as a function of attention-decay strength $\lambda$
  (Equation~\ref{eq:attn}, $N=200$ trials).
  Degradation is negligible below $\lambda=1.0$ and plateaus at 0.920 for
  all $\lambda \geq 1.0$, confirming robustness of the main result.}
\label{fig:ablation}
\end{figure}
"""

# Figure 3 TikZ — method comparison bar chart (avg recall)
method_avgs = {}
for mname, mid, color, mark, style in METHODS:
    vals = [recall(mname, pl) for pl in POS_LABELS]
    method_avgs[mid] = (sum(vals)/len(vals), color, mname)

short_names = {
    "fc":  "FC-B1",
    "cs":  "CS-B2",
    "oc":  "OC-B3",
    "h2p": "H2P",
}
avg_coords = " ".join(f"({i+1},{method_avgs[mid][0]:.4f})"
                      for i, (_, mid, *_rest) in enumerate(METHODS))
bar_colors = [c for _, _, c, _, _ in METHODS]

fig3 = r"""
% ── Figure 3: Average Recall across positions ────────────────────────────────
\begin{figure}[t]
\centering
\begin{tikzpicture}
\begin{axis}[
  width=\columnwidth, height=5cm,
  xlabel={Retrieval Method},
  ylabel={Average Recall@1},
  ymin=0.94, ymax=1.005,
  xtick={1,2,3,4},
  xticklabels={FC-B1, CS-B2, OC-B3, H2P},
  grid=major, grid style={gray!25},
  tick label style={font=\footnotesize},
  label style={font=\footnotesize},
  nodes near coords, nodes near coords style={font=\scriptsize},
  ybar, bar width=0.6cm,
]
"""
for i, (mname, mid, color, mark, style) in enumerate(METHODS):
    avg = method_avgs[mid][0]
    fig3 += f"\\addplot[fill={color}!60, draw={color}!80!black] coordinates {{({i+1},{avg:.4f})}};\n"

fig3 += r"""\end{axis}
\end{tikzpicture}
\caption{Average Recall@1 across all five evidence positions per method.
  FC-B1 scores 0.961 due to degradation at non-boundary positions;
  all three chunking methods achieve a perfect average of 1.000.}
\label{fig:avgrecall}
\end{figure}
"""

# ── Write figures.tex ─────────────────────────────────────────────────────────
figures_tex = "% Auto-generated by generate_figures.py — do not edit manually\n"
figures_tex += "% Include in preamble: \\input{figures_preamble}\n"
figures_tex += "% Include in body:     \\input{figures}\n\n"
figures_tex += fig1 + "\n" + fig2 + "\n" + fig3

preamble_tex = tikz

with open(os.path.join(OUTPUT_DIR, "figures.tex"), "w") as f:
    f.write(figures_tex)

with open(os.path.join(OUTPUT_DIR, "figures_preamble.tex"), "w") as f:
    f.write(preamble_tex)

print("Written: figures.tex")
print("Written: figures_preamble.tex")
print("\nFigure 1 — Recall@1 vs Position (line chart)")
print("Figure 2 — Ablation: decay strength vs Recall@1 (bar chart)")
print("Figure 3 — Average Recall@1 per method (grouped bar chart)")
