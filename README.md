# Context-Window Degradation: A Controlled Retrieval Experiment

**Author**: Mayank Waila  
**Institute**: IIIT Allahabad, PCL Course  
**Assignment**: PCL-02 — Implementation & Experimental Paper

---

## Repository Structure

```
.
├── experiment.py          # v1 experiment (original design)
├── experiment_v2.py       # v2 experiment (refined, used in paper)
├── paper.tex              # LaTeX source of the paper (ACM sigconf)
├── references.bib         # BibTeX references
├── results.csv            # v1 results
├── results_v2.csv         # v2 results (all numbers in paper)
├── ablation_strength.csv  # ablation over attention-decay strength
├── ablation_window_size.csv # v1 ablation over window size
├── config_v2.json         # all hyper-parameters for full reproduction
└── README.md              # this file
```

---

## Research Question

> Does the positional placement of target evidence within a long document
> significantly degrade retrieval accuracy under a simulated LLM attention
> model, and can chunked or hierarchical retrieval strategies recover this loss?

---

## How to Reproduce

```bash
python3 experiment_v2.py
```

**Requirements**: Python 3.8+, no external dependencies.

This writes:
- `results_v2.csv` — main results (Recall@1 and Mean-F1 per method × position)
- `ablation_strength.csv` — ablation over attention-decay strength λ
- `config_v2.json` — all experimental parameters

---

## Key Results (Table 1 in paper)

| Evidence Position | FC-B1  | CS-B2  | OC-B3  | H2P    |
|------------------|--------|--------|--------|--------|
| Start (0%)       | 1.000  | 1.000  | 1.000  | 1.000  |
| Early (25%)      | 0.900  | 1.000  | 1.000  | 1.000  |
| Middle (50%)     | 0.905  | 1.000  | 1.000  | 1.000  |
| Late (75%)       | 1.000  | 1.000  | 1.000  | 1.000  |
| End (100%)       | 1.000  | 1.000  | 1.000  | 1.000  |

FC-B1 = Full-Context Baseline; CS-B2 = Chunked Sequential;  
OC-B3 = Overlapping Chunks; H2P = Hierarchical Two-Pass

---

## Experimental Config

```json
{
  "random_seed": 42,
  "total_chunks": 20,
  "chunk_size": 60,
  "window_size": 5,
  "positions": [0, 5, 10, 15, 19],
  "num_trials": 200,
  "distractor_pool": 800
}
```

---

## Connections to Paper 1

This experiment directly tests the **lost-in-the-middle phenomenon**
(Liu et al. 2023) described in my literature review (PCL-01).  
The attention-decay simulation in `experiment_v2.py` is parameterised to
match the ~20pp drop reported in Liu et al. Figure 2.

---

## AI Collaboration Transparency

| Task | AI Role | Author Role |
|------|---------|-------------|
| Research question | Feasibility check | Full authorship |
| Attention-decay equation | Shape suggestion (sin²) | Derivation, verification |
| Code scaffolding | ~40% of initial draft | Rewrote 60%, debugged all |
| Paper writing | Sentence rephrasing (2 paragraphs) | Full authorship of content |
| References | None | Manually verified against ACM DL |
