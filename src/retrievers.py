"""
Retrieval method implementations: Full-Context, Sequential Chunking, Overlapping Chunks, and Hierarchical Two-Pass.
"""

import random
from typing import List, Tuple
from .attention import attn_weight
from .data import bow_score

def full_context(chunks: List[str], query: str, ev_pos: int, rng: random.Random) -> Tuple[float, float]:
    """Baseline 1: Full-context single pass with global attention decay."""
    n = len(chunks)
    scores = [
        bow_score(c, query) * attn_weight(i, n) + rng.gauss(0, 0.015)
        for i, c in enumerate(chunks)
    ]
    pred = max(range(n), key=lambda i: scores[i])
    hit = int(pred == ev_pos)
    f1 = bow_score(chunks[pred], query) * hit
    return float(hit), f1

def chunked_sequential(chunks: List[str], query: str, ev_pos: int, rng: random.Random, window: int = 5) -> Tuple[float, float]:
    """Baseline 2: Non-overlapping sliding windows."""
    n = len(chunks)
    best_score, best_idx = -1.0, 0
    for start in range(0, n, window):
        win = chunks[start:start + window]
        w_len = len(win)
        for j, c in enumerate(win):
            s = bow_score(c, query) * attn_weight(j, w_len, strength=0.8) + rng.gauss(0, 0.015)
            if s > best_score:
                best_score, best_idx = s, start + j
    hit = int(best_idx == ev_pos)
    f1 = bow_score(chunks[best_idx], query) * hit
    return float(hit), f1

def overlapping_chunked(chunks: List[str], query: str, ev_pos: int, rng: random.Random, window: int = 5, stride: int = 2) -> Tuple[float, float]:
    """Baseline 3: Overlapping sliding windows (stride < window)."""
    n = len(chunks)
    best_score, best_idx = -1.0, 0
    starts = list(range(0, n - window + 1, stride)) + ([n - window] if n > window else [])
    for start in starts:
        win = chunks[start:start + window]
        w_len = len(win)
        for j, c in enumerate(win):
            s = bow_score(c, query) * attn_weight(j, w_len, strength=0.8) + rng.gauss(0, 0.015)
            if s > best_score:
                best_score, best_idx = s, start + j
    hit = int(best_idx == ev_pos)
    f1 = bow_score(chunks[best_idx], query) * hit
    return float(hit), f1

def hierarchical(chunks: List[str], query: str, ev_pos: int, rng: random.Random, coarse_win: int = 5, fine_k: int = 2) -> Tuple[float, float]:
    """Proposed: Two-pass hierarchical retrieval (coarse filtering + fine reranking)."""
    n = len(chunks)
    # Coarse pass: evaluate summary headers
    window_scores = {}
    for start in range(0, n, coarse_win):
        win = chunks[start:start + coarse_win]
        summaries = [" ".join(c.split()[:12]) for c in win]
        window_scores[start] = max(bow_score(s, query) for s in summaries)
    
    top_starts = sorted(window_scores, key=window_scores.get, reverse=True)[:fine_k]
    
    # Fine pass: detailed scoring inside selected high-probability windows
    best_score, best_idx = -1.0, 0
    for start in top_starts:
        win = chunks[start:start + coarse_win]
        w_len = len(win)
        for j, c in enumerate(win):
            s = bow_score(c, query) * attn_weight(j, w_len, strength=0.25) + rng.gauss(0, 0.015)
            if s > best_score:
                best_score, best_idx = s, start + j
    
    hit = int(best_idx == ev_pos)
    f1 = bow_score(chunks[best_idx], query) * hit
    return float(hit), f1
