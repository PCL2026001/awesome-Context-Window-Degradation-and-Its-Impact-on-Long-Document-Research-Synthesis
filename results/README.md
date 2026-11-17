# Experimental Results and Metric Artifacts

This directory contains verified experimental outputs, raw metric logs, and generated visual artifacts.

## Files

- `results_v2.csv`: Primary experimental results measuring Recall@1 and Mean-F1 across all 4 retrieval methods and 5 positions ($N=4,000$ trials).
- `ablation_strength.csv`: Attention-decay sensitivity ablation across $\lambda \in [0.0, 3.0]$ at Middle (50%) position.
- `results_v1.csv`: Baseline validation run outputs from initial system iteration.
- `ablation_window_size.csv`: Window size ablation across $W \in \{2, 3, 5, 7, 10\}$.
- `figures/`: High-resolution figures and TikZ code matching the paper.

## Primary Results Summary (Recall@1)

| Evidence Position | FC-B1 (Full-Context) | CS-B2 (Chunked Seq) | OC-B3 (Overlapping) | H2P (Hierarchical) |
|:------------------|:--------------------:|:-------------------:|:-------------------:|:------------------:|
| Start (0%)        | 1.000                | 1.000               | 1.000               | 1.000              |
| Early (25%)       | 0.900                | 1.000               | 1.000               | 1.000              |
| Middle (50%)      | 0.905                | 1.000               | 1.000               | 1.000              |
| Late (75%)        | 1.000                | 1.000               | 1.000               | 1.000              |
| End (100%)        | 1.000                | 1.000               | 1.000               | 1.000              |
| **Average**       | **0.961**            | **1.000**           | **1.000**           | **1.000**          |
