# Research Decisions: From Literature Review to Empirical Experiment

**Project**: Context-Window Degradation and Its Impact on Long-Document Research Synthesis  
**Author**: Mayank Waila  
**Course**: Post-Midsem Assignment — AI Tools for Research (PCL Course, IIIT Allahabad)  

---

## 1. Context and Problem Statement

In **Paper 1 (Literature Review)**, we conducted a systematic survey of context-window degradation in modern Transformer architectures. That review highlighted a persistent discrepancy: while contemporary Large Language Models advertise context windows ranging from 32k to over 1M tokens, empirical benchmarks (notably Liu et al., 2024; Bai et al., 2024; Hsieh et al., 2024) document severe performance degradation when relevant evidence resides in the interior of long prompt contexts—the canonical **"Lost in the Middle"** effect.

This empirical follow-up (**Paper 2**) was designed to transition from literature synthesis to controlled experimental validation.

---

## 2. Key Literature-to-Experiment Decisions

### Decision 1: Synthetic Needle-in-a-Haystack vs. Real Document Corpora
- **Literature Context**: LongBench (Bai et al., 2024) and Multi-document QA (Liu et al., 2024) utilize multi-article collections where distractors originate from Wikipedia or news articles.
- **Experimental Decision**: We implemented a parameterized synthetic retrieval framework with explicit signal tokens (`SIGNAL_X`, `SIGNAL_Y`, `SIGNAL_Z`) embedded in distractor haystacks.
- **Justification**: Using natural documents introduces non-uniform semantic overlap and token frequency variations across positions, confounding the measurement of positional bias itself. A synthetic corpus eliminates vocabulary confounds and guarantees known ground truth across thousands of trials.

### Decision 2: Theoretical Attention-Decay Parameterization
- **Literature Context**: Liu et al. (2024, Figure 2) demonstrated that retrieval accuracy exhibits a U-shaped or inverted bell curve, dropping by 15–25 percentage points when moving from context boundaries ($0\%$ and $100\%$) to the center ($50\%$).
- **Experimental Decision**: We formalized this attention decay mathematically as:
  $$w(i, N) = \max\left(0.05, 1.0 - \lambda \cdot \sin^2\left(\frac{\pi \cdot i}{N - 1}\right)\right)$$
- **Justification**: A $\sin^2$ function continuously models the symmetric boundary-to-center attention drop observed empirically across multiple commercial architectures. Setting $\lambda = 1.8$ with a small noise factor $\mathcal{N}(0, 0.015^2)$ reproduces the ~10–15 pp degradation reported in literature under identical signal conditions.

### Decision 3: Evaluated Mitigation Strategies
- **Literature Context**: Surveys on Retrieval-Augmented Generation (Gao et al., 2023; Lewis et al., 2020) and prompt compression (LLMLingua; Jiang et al., 2023) suggest that reducing the context size presented to the retriever restores high precision.
- **Experimental Decision**: We designed and compared four distinct retrieval paradigms:
  1. **FC-B1 (Full-Context Baseline)**: Single global pass over all $N=20$ chunks.
  2. **CS-B2 (Chunked Sequential)**: Partitioning the context into non-overlapping sliding windows ($W=5$).
  3. **OC-B3 (Overlapping Chunks)**: Stridden windows (window=5, stride=2) specifically mitigating chunk boundary truncation.
  4. **H2P (Hierarchical Two-Pass - Proposed)**: Coarse summary ranking followed by high-resolution fine-pass retrieval in the top candidates.

### Decision 4: Discovery of the Chunk-Boundary Problem
- **Observation during v1 experiment**: Fixed, non-overlapping windows revealed an acute edge failure: when the target chunk fell exactly on a partition boundary, evidence was truncated across windows, dropping recall to 0.08 for prime window sizes ($W=3, 7$).
- **Refinement**: Overlapping chunks (OC-B3) with stride 2 and Hierarchical 2-Pass (H2P) were explicitly added to solve boundary fragmentation, achieving 1.000 recall across all positions.
