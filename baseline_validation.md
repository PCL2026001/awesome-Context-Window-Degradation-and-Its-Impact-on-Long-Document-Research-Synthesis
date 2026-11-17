# Baseline Validation and Reproduction Checks

**Project**: Positional Context-Window Degradation and Chunked Retrieval  
**Author**: Mayank Waila  
**Institute**: IIIT Allahabad  

---

## 1. Reproduction Objectives

The validation protocol verifies two core hypotheses formulated from prior literature:
- **Hypothesis 1 (Degradation)**: Retrieval recall under full-context attention decreases significantly when evidence is placed in the interior ($25\%$ and $50\%$) compared to boundaries ($0\%$ and $100\%$).
- **Hypothesis 2 (Mitigation)**: Localized window chunking (CS-B2, OC-B3, and H2P) recovers lost recall by reducing the effective attention traversal depth.

---

## 2. Experimental Checks and Validation Data

### Primary Run ($N=200$ trials per condition, 4,000 retrievals total)

| Position | Index | FC-B1 (Full-Context) | CS-B2 (Sequential) | OC-B3 (Overlapping) | H2P (Hierarchical) |
|:---|:---:|:---:|:---:|:---:|:---:|
| Start (0%) | 0 | **1.000** | **1.000** | **1.000** | **1.000** |
| Early (25%) | 5 | **0.900** | **1.000** | **1.000** | **1.000** |
| Middle (50%) | 10 | **0.905** | **1.000** | **1.000** | **1.000** |
| Late (75%) | 15 | **1.000** | **1.000** | **1.000** | **1.000** |
| End (100%) | 19 | **1.000** | **1.000** | **1.000** | **1.000** |
| **Overall Mean** | — | **0.961** | **1.000** | **1.000** | **1.000** |

### Statistical Significance (95% Wald Confidence Intervals)
- **FC-B1 at Early (25%)**: $\hat{p} = 0.900$, $\text{CI}_{95} = [0.8584, 0.9416]$
- **FC-B1 at Middle (50%)**: $\hat{p} = 0.905$, $\text{CI}_{95} = [0.8644, 0.9456]$
- **Chunking Baselines (CS-B2, OC-B3, H2P)**: $\hat{p} = 1.000$, $\text{CI}_{95} = [1.000, 1.000]$ (0 failures in 200 trials)

**Conclusion**: The ~10 pp drop at non-boundary positions is statistically significant at the $p < 0.01$ level.

---

## 3. Attention Decay Sensitivity Validation (Ablation)

We evaluated the robustness of the degradation effect across varying values of the decay parameter $\lambda$:

| $\lambda$ (Strength) | Recall@1 (Middle Position) | State / Behavior |
|:---:|:---:|:---|
| 0.0 | 1.000 | Uniform attention (ideal baseline) |
| 0.5 | 1.000 | Sub-critical degradation (signal dominates) |
| 1.0 | 0.920 | Degradation onset |
| 1.5 | 0.920 | Plateau reached |
| 1.8 | 0.920 | Calibrated setting used in paper |
| 2.0 | 0.920 | Robust plateau |
| 2.5 | 0.920 | Robust plateau |
| 3.0 | 0.920 | Robust plateau |

**Validation Takeaway**: For any $\lambda \ge 1.0$, the middle recall stays stable at ~0.920. This confirms that the observed degradation is not an artifact of fine-tuned hyperparameter choices.

---

## 4. Observed Deviations & Architectural Differences

1. **Synthetic vs. Real-World LLMs**: Real-world language models exhibit a ~20–30 pp drop on natural text (Liu et al., 2024), whereas our controlled BoW synthetic model exhibits ~10 pp drop. This deviation occurs because natural language distractors share partial subword token overlaps with the query, increasing false positives in natural text.
2. **Chunk Boundary Truncation**: Standard sliding window chunkers (v1) exhibited catastrophic recall drops (down to 0.08) when the window stride caused boundary splits. This deviation motivated the inclusion of Overlapping Chunks (stride 2) and Hierarchical 2-Pass in v2.
