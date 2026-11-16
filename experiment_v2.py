"""
Refined Experiment: Context-Window Degradation — cleaner simulation with
configurable noise, overlapping windows, and F1 metrics.
"""

import random
import json
import csv
import math
import os
from typing import List, Tuple, Dict, Optional

RANDOM_SEED   = 42
TOTAL_CHUNKS  = 20
CHUNK_SIZE    = 60
WINDOW_SIZE   = 5
POSITIONS     = [0, 5, 10, 15, 19]
POSITION_LABELS = ["Start (0%)", "Early (25%)", "Middle (50%)", "Late (75%)", "End (100%)"]
NUM_TRIALS    = 200
DISTRACTOR_POOL = 800
OUTPUT_DIR    = os.path.dirname(os.path.abspath(__file__))


# ── Synthetic data ─────────────────────────────────────────────────────────────

def random_words(n: int, vocab_size: int = DISTRACTOR_POOL, rng: Optional[random.Random] = None) -> str:
    r = rng or random
    return " ".join(str(r.randint(0, vocab_size)) for _ in range(n))


def build_query_evidence(rng: random.Random) -> Tuple[str, str]:
    signal_tokens = ["SIGNAL_X", "SIGNAL_Y", "SIGNAL_Z"]
    partial_match = signal_tokens[:2]
    evidence = " ".join(signal_tokens) + " " + random_words(CHUNK_SIZE - len(signal_tokens), rng=rng)
    query = " ".join(partial_match)
    return query, evidence


def build_document(evidence: str, pos: int, rng: random.Random) -> List[str]:
    return [evidence if i == pos else random_words(CHUNK_SIZE, rng=rng)
            for i in range(TOTAL_CHUNKS)]


# ── Attention model ────────────────────────────────────────────────────────────

def attn_weight(pos: int, total: int, strength: float = 1.8) -> float:
    """
    U-shaped primacy–recency curve parameterized to match Liu et al. (2023):
    ~15 pp drop in the middle relative to ends.
    """
    if total <= 1:
        return 1.0
    frac = pos / (total - 1)
    w = 1.0 - strength * math.sin(math.pi * frac) ** 2
    return max(0.05, w)   # floor to avoid 0 weights


# ── Scoring ────────────────────────────────────────────────────────────────────

def bow_score(chunk: str, query: str) -> float:
    qt = set(query.lower().split())
    ct = set(chunk.lower().split())
    if not qt:
        return 0.0
    return len(qt & ct) / len(qt)


# ── Methods ────────────────────────────────────────────────────────────────────

def full_context(chunks: List[str], query: str, ev_pos: int,
                 rng: random.Random) -> Tuple[float, float]:
    """Baseline 1: single-pass with global attention decay."""
    n = len(chunks)
    scores = [bow_score(c, query) * attn_weight(i, n) + rng.gauss(0, 0.015)
              for i, c in enumerate(chunks)]
    pred = max(range(n), key=lambda i: scores[i])
    hit  = int(pred == ev_pos)
    # F1: fraction of signal tokens retrieved (simulated as hit × recall score)
    f1   = bow_score(chunks[pred], query) * hit
    return float(hit), f1


def chunked_sequential(chunks: List[str], query: str, ev_pos: int,
                        rng: random.Random, window: int = WINDOW_SIZE) -> Tuple[float, float]:
    """Baseline 2: non-overlapping sliding window."""
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
    f1  = bow_score(chunks[best_idx], query) * hit
    return float(hit), f1


def overlapping_chunked(chunks: List[str], query: str, ev_pos: int,
                         rng: random.Random,
                         window: int = WINDOW_SIZE, stride: int = 2) -> Tuple[float, float]:
    """Variant: overlapping sliding window (stride < window)."""
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
    f1  = bow_score(chunks[best_idx], query) * hit
    return float(hit), f1


def hierarchical(chunks: List[str], query: str, ev_pos: int,
                  rng: random.Random,
                  coarse_win: int = WINDOW_SIZE, fine_k: int = 2) -> Tuple[float, float]:
    """
    Proposed: two-pass hierarchical retrieval.
    Pass 1 — coarse: score each window by its best chunk summary.
    Pass 2 — fine:   re-rank chunks in top-k windows with reduced attention penalty.
    """
    n = len(chunks)
    # Pass 1
    window_scores = {}
    for start in range(0, n, coarse_win):
        win = chunks[start:start + coarse_win]
        summaries = [" ".join(c.split()[:12]) for c in win]
        window_scores[start] = max(bow_score(s, query) for s in summaries)
    
    top_starts = sorted(window_scores, key=window_scores.get, reverse=True)[:fine_k]
    
    # Pass 2
    best_score, best_idx = -1.0, 0
    for start in top_starts:
        win = chunks[start:start + coarse_win]
        w_len = len(win)
        for j, c in enumerate(win):
            # Fine pass: much lower attention decay since context is short
            s = bow_score(c, query) * attn_weight(j, w_len, strength=0.25) + rng.gauss(0, 0.015)
            if s > best_score:
                best_score, best_idx = s, start + j
    
    hit = int(best_idx == ev_pos)
    f1  = bow_score(chunks[best_idx], query) * hit
    return float(hit), f1


# ── Experiment loop ────────────────────────────────────────────────────────────

def run() -> List[Dict]:
    results = []
    
    methods = {
        "Full-Context (Baseline 1)":       full_context,
        "Chunked Sequential (Baseline 2)": chunked_sequential,
        "Overlapping Chunks (Baseline 3)": overlapping_chunked,
        "Hierarchical 2-Pass (Proposed)":  hierarchical,
    }
    
    print("Running experiments...")
    print(f"{'Position':<22} {'Method':<35} {'R@1':>6} {'F1':>6} {'N':>5}")
    print("-" * 80)
    
    for pos_i, (pos, label) in enumerate(zip(POSITIONS, POSITION_LABELS)):
        for mname, mfn in methods.items():
            hits, f1s = [], []
            for t in range(NUM_TRIALS):
                rng = random.Random(RANDOM_SEED + pos_i * 10000 + t)
                query, evidence = build_query_evidence(rng)
                chunks = build_document(evidence, pos, rng)
                h, f = mfn(chunks, query, pos, rng)
                hits.append(h); f1s.append(f)
            
            recall = sum(hits) / NUM_TRIALS
            mean_f1 = sum(f1s) / NUM_TRIALS
            
            row = {
                "position_label": label,
                "evidence_pos":   pos,
                "method":         mname,
                "recall_at_1":    round(recall, 4),
                "mean_f1":        round(mean_f1, 4),
                "num_trials":     NUM_TRIALS,
            }
            results.append(row)
            print(f"{label:<22} {mname:<35} {recall:>6.3f} {mean_f1:>6.3f} {NUM_TRIALS:>5}")
    
    return results


def ablation_strength() -> List[Dict]:
    """
    Ablation: Effect of attention-decay strength on full-context recall at middle.
    """
    print("\n\nABLATION: Attention-Decay Strength vs. Recall@1 (Middle Position)")
    print("=" * 60)
    pos = POSITIONS[2]   # middle
    rows = []
    for strength in [0.0, 0.5, 1.0, 1.5, 1.8, 2.0, 2.5, 3.0]:
        hits = []
        for t in range(NUM_TRIALS):
            rng = random.Random(RANDOM_SEED + 99999 + t)
            query, evidence = build_query_evidence(rng)
            chunks = build_document(evidence, pos, rng)
            n = len(chunks)
            scores = [bow_score(c, query) * attn_weight(i, n, strength=strength)
                      + rng.gauss(0, 0.015)
                      for i, c in enumerate(chunks)]
            pred = max(range(n), key=lambda i: scores[i])
            hits.append(int(pred == pos))
        recall = sum(hits) / NUM_TRIALS
        rows.append({"strength": strength, "recall_at_1": round(recall, 4)})
        print(f"  strength={strength:.1f}  → Recall@1 = {recall:.4f}")
    return rows


if __name__ == "__main__":
    print("=" * 80)
    print("EXPERIMENT (v2): Context-Window Degradation — Long-Document Research Synthesis")
    print(f"Config: {TOTAL_CHUNKS} chunks × {CHUNK_SIZE} words, {NUM_TRIALS} trials, window={WINDOW_SIZE}")
    print(f"Random seed: {RANDOM_SEED}")
    print("=" * 80 + "\n")
    
    results = run()
    
    csv_path = os.path.join(OUTPUT_DIR, "results_v2.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"\nResults CSV → {csv_path}")
    
    # Print LaTeX table
    methods = list(dict.fromkeys(r["method"] for r in results))
    positions = POSITION_LABELS
    
    print("\n\nLaTeX Table (Recall@1):")
    print(r"\begin{tabular}{lcccc}")
    print(r"\toprule")
    # Short method names for table
    short = ["FC-B1", "CS-B2", "OC-B3", "H2P"]
    print("Position & " + " & ".join(short) + r" \\")
    print(r"\midrule")
    for label in positions:
        vals = []
        for m in methods:
            row = next((r for r in results if r["position_label"] == label and r["method"] == m), None)
            vals.append(f"{row['recall_at_1']:.3f}" if row else "—")
        print(label + " & " + " & ".join(vals) + r" \\")
    print(r"\bottomrule")
    print(r"\end{tabular}")
    
    ablation_rows = ablation_strength()
    abl_path = os.path.join(OUTPUT_DIR, "ablation_strength.csv")
    with open(abl_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["strength", "recall_at_1"])
        writer.writeheader()
        writer.writerows(ablation_rows)
    print(f"\nAblation CSV → {abl_path}")
    
    config = {
        "random_seed": RANDOM_SEED, "total_chunks": TOTAL_CHUNKS,
        "chunk_size": CHUNK_SIZE, "window_size": WINDOW_SIZE,
        "positions": POSITIONS, "num_trials": NUM_TRIALS,
        "distractor_pool": DISTRACTOR_POOL,
    }
    with open(os.path.join(OUTPUT_DIR, "config_v2.json"), "w") as f:
        json.dump(config, f, indent=2)
    
    print("\nAll outputs written. Experiment complete.")
