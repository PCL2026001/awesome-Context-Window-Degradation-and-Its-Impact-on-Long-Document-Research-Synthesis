# Datasets for Long-Document Research Synthesis

This document lists publicly available datasets used to evaluate long-context reasoning, retrieval, summarization, and document synthesis.

---

## 1. LongBench

**Source:** ACL Anthology

Purpose:

- Long-context QA.
- Summarization.
- Few-shot learning.
- Code completion.
- Multi-document reasoning.

Used for evaluating context utilization across many tasks.

---

## 2. RULER Benchmark

**Source:** arXiv

Purpose:

- Effective context-length evaluation.
- Needle-in-haystack retrieval.
- Retrieval under distractors.
- Context scaling.

Useful for measuring degradation as context length grows.

---

## 3. LooGLE

Purpose:

- Long-document reasoning.
- Cross-document synthesis.
- Evidence retrieval.

Designed for realistic long-document tasks.

---

## 4. NarrativeQA

Source:

DeepMind.

Purpose:

Reading comprehension over books and movie scripts.

Useful for testing long-range understanding.

---

## 5. HotpotQA

Purpose:

Multi-hop question answering requiring evidence from multiple documents.

---

## 6. MultiDoc2Dial

Purpose:

Dialogue grounded in multiple documents.

---

## 7. Qasper

Purpose:

Question answering over scientific papers.

Useful for research synthesis evaluation.

---

## Dataset Summary

| Dataset | Task | Domain |
|---------|------|--------|
| LongBench | Long-context understanding | General |
| RULER | Context-length evaluation | General |
| LooGLE | Long document reasoning | General |
| NarrativeQA | Reading comprehension | Books |
| HotpotQA | Multi-hop QA | Wikipedia |
| Qasper | Scientific QA | Research papers |
| MultiDoc2Dial | Multi-document dialogue | Documents |

---

## Why These Datasets Matter

These datasets collectively evaluate:

- evidence retrieval,
- reasoning across documents,
- summarization quality,
- retrieval robustness,
- long-context degradation,
- evidence completeness.

They complement the literature discussed in the accompanying research paper.
