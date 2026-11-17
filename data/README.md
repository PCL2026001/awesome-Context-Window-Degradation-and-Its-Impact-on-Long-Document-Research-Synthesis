# Data Access and Protocol Description

This document describes the synthetic data generation protocol, access rationale, and schema for the context-window degradation benchmark.

## Rationale for Synthetic Generation vs. Proprietary Corpora

To evaluate **positional attention degradation** in long-document synthesis in a strictly controlled manner without confounds from:
1. Lexical memorization or pretraining corpus contamination in open/closed-source LLMs,
2. Inconsistent document lengths or semantic topic biases across heterogeneous domains,
3. Non-deterministic API rate-limiting or non-reproducible model version updates,

the benchmark employs a parameterized synthetic needle-in-a-haystack retrieval corpus following the methodology established by Liu et al. (2024) and RULER (Hsieh et al., 2024).

## Data Generation Pipeline

The generation pipeline is implemented in `src/data.py` and executed dynamically during evaluation:

1. **Evidence Chunk Synthesis**:
   - Each trial creates an evidence chunk containing exact key signal tokens (`SIGNAL_X`, `SIGNAL_Y`, `SIGNAL_Z`) embedded within $C = 60$ words.
   - The corresponding query tests partial retrieval matching (`SIGNAL_X SIGNAL_Y`).

2. **Distractor Haystack Synthesis**:
   - $N - 1 = 19$ distractor chunks are sampled from a disjoint vocabulary pool ($V = 800$ tokens).
   - Distractors simulate semantic interference while guaranteeing zero overlap with target signal tokens.

3. **Positional Placement**:
   - The target evidence chunk is placed at exact normalized depths:
     - **Start**: Index $0$ ($0\%$)
     - **Early**: Index $5$ ($25\%$)
     - **Middle**: Index $10$ ($50\%$)
     - **Late**: Index $15$ ($75\%$)
     - **End**: Index $19$ ($100\%$)

## Schema

Every generated document in trial $t$ has:
- `query`: String containing query tokens.
- `evidence`: String containing ground-truth evidence chunk.
- `document`: Array of $N=20$ chunk strings.
- `target_pos`: Integer index of evidence in document $\in \{0, 5, 10, 15, 19\}$.

All generated artifacts and evaluated trial logs are stored in `results/`.
