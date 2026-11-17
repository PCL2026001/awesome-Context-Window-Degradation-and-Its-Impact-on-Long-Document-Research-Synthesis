# AI Assistance and Human Verification Log

**Student**: Mayank Waila  
**Course**: AI Tools for Research (PCL Course)  
**Institution**: Indian Institute of Information Technology Allahabad (IIITA)  
**Assignment**: Lab 02 — Implementation & Empirical Research Paper  

---

## 1. Transparency Statement

In compliance with the **AI Tools for Research (AITR)** course policy and ACM publication ethics guidelines, this log records the significant interactions, prompts, AI contributions, human reviews, and verification steps performed throughout this project.

---

## 2. Interaction Log

### Entry 1: Problem Formulation & Hypothesis Generation
- **User Prompt / Intent**: Formulate an experimental methodology continuing from the literature review on context-window degradation (Lost in the Middle, Liu et al., 2024), defining testable hypotheses and controlled experimental conditions.
- **AI Contribution**: Suggested formulating two distinct hypotheses:
  - $H_1$: Retrieval degradation as a function of normalized evidence depth.
  - $H_2$: Chunked/hierarchical mitigation strategies.
- **Human Verification & Decision**: Verified that $H_1$ and $H_2$ are empirically falsifiable without relying on non-deterministic external proprietary APIs. Constrained the evaluation to a synthetic controlled protocol ensuring 100% reproducible trials.

### Entry 2: Attention Degradation Formulation
- **User Prompt / Intent**: Develop a continuous mathematical function modeling the U-shaped primacy and recency attention attenuation observed in Transformer architectures.
- **AI Contribution**: Proposed a sinusoidal decay model:
  $$w(i, N) = 1.0 - \lambda \cdot \sin^2\left(\frac{\pi \cdot i}{N - 1}\right)$$
- **Human Verification & Decision**: Added a clamped floor ($\max(0.05, w)$) to prevent non-physical negative attention weights. Calibrated $\lambda = 1.8$ against the 15–20 pp degradation figures in Liu et al. (2024).

### Entry 3: Code Implementation & Edge Case Debugging
- **User Prompt / Intent**: Implement baseline and proposed retrieval methods in a zero-dependency Python script, plus Google Colab interactive notebook.
- **AI Contribution**: Provided initial draft implementations of Full-Context, Sequential Chunking, Overlapping Chunking, and Hierarchical Two-Pass methods.
- **Human Verification & Decision**: Discovered chunk-boundary edge cases during v1 experimentation (fixed non-overlapping windows caused evidence truncation at boundary indices). Designed overlapping windows ($W=5$, stride $2$) and hierarchical 2-pass ranking to eliminate boundary failure modes.

### Entry 4: LaTeX Formatting & TikZ Figure Compilation
- **User Prompt / Intent**: Embed publication figures into ACM Sigconf `paper.tex` without relying on external raster images.
- **AI Contribution**: Generated PGFPlots/TikZ code for line charts and bar charts.
- **Human Verification & Decision**: Debugged Overleaf compilation errors:
  - Removed newline `\\` commands inside `xticklabels` that caused LaTeX LR-mode errors.
  - Replaced unsupported markers (`pentagon*`) with standard `pgfplots` markers (`mark=o`).
  - Added label rotation to prevent visual overlap in ACM two-column layout.

### Entry 5: Google Colab Notebook & Project Structure Refactoring
- **User Prompt / Intent**: Organize project files to strictly follow the recommended AITR Lab 02 project tree (`configs/`, `data/`, `notebooks/`, `src/`, `scripts/`, `results/`, `paper/`, etc.).
- **AI Contribution**: Created package structure, modularized reusable code into `src/`, entrypoints into `scripts/`, and generated `PCL_Context_Window_Degradation_Experiment.ipynb`.
- **Human Verification & Decision**: Verified all paths, ensured `requirements.txt` accurately documents all optional analysis dependencies, verified reproducible execution across CLI and Colab.

---

## 3. Human-AI Responsibility Breakdown

| Lifecycle Phase | AI Contribution | Human Oversight & Verification |
|:---|:---|:---|
| Literature Grounding | Summarized Liu et al. & LongBench benchmarks | Manually verified papers and DOIs against ACM Digital Library |
| Math Formulation | Suggested sinusoidal decay equation | Verified derivative, bounds, and clamping parameters |
| Implementation | Initial code scaffolding and boilerplate | Debugged boundary condition, rewrote scoring loop, ensured reproducibility |
| Figure Generation | Generated TikZ & Matplotlib scripts | Visual validation and Overleaf LaTeX compilation verification |
| Analysis & Writing | Formatting assistance and drafting suggestions | Authored discussion, validated interpretations, verified statistical claims |
