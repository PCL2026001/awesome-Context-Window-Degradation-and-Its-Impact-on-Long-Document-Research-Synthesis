# Notebooks

This directory contains verified, runnable Jupyter and Google Colab notebooks for interactive exploration, visualization, and validation.

## Available Notebooks

### 1. `PCL_Context_Window_Degradation_Experiment.ipynb`
- **Purpose**: Full end-to-end interactive reproduction of all paper experiments, ablation studies, and figure generation.
- **Run in Colab**: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PCL2026001/awesome-Context-Window-Degradation-and-Its-Impact-on-Long-Document-Research-Synthesis/blob/main/notebooks/PCL_Context_Window_Degradation_Experiment.ipynb)
- **Features**:
  - Implements all 4 retrieval strategies (FC-B1, CS-B2, OC-B3, H2P).
  - Executes 4,000 empirical retrieval trials deterministically.
  - Generates publication-ready figures (Figures 1, 2, and 3).
  - Computes 95% Wald binomial confidence intervals.
  - Exports validated reproduction CSV files.
