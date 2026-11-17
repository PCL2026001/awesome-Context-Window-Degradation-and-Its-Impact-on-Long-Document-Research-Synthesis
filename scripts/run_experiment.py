#!/usr/bin/env python3
"""
Main evaluation entrypoint for context-window degradation experiment.
Runs all 4 methods across 5 positions with N=200 trials per cell (4,000 retrievals).
"""

import os
import sys
import json
import csv
import random

# Add root project directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.data import build_query_evidence, build_document
from src.retrievers import full_context, chunked_sequential, overlapping_chunked, hierarchical

CONFIG_PATH = os.path.join(BASE_DIR, "configs", "config_v2.json")
with open(CONFIG_PATH, "r") as f:
    cfg = json.load(f)

RANDOM_SEED = cfg["random_seed"]
TOTAL_CHUNKS = cfg["total_chunks"]
CHUNK_SIZE = cfg["chunk_size"]
WINDOW_SIZE = cfg["window_size"]
POSITIONS = cfg["positions"]
NUM_TRIALS = cfg["num_trials"]
POSITION_LABELS = ["Start (0%)", "Early (25%)", "Middle (50%)", "Late (75%)", "End (100%)"]

methods = {
    "Full-Context (Baseline 1)": full_context,
    "Chunked Sequential (Baseline 2)": chunked_sequential,
    "Overlapping Chunks (Baseline 3)": overlapping_chunked,
    "Hierarchical 2-Pass (Proposed)": hierarchical,
}

def main():
    print("=" * 80)
    print("AITR Lab 02: Positional Retrieval Evaluation Entrypoint")
    print(f"Total Trials: {len(POSITIONS) * len(methods) * NUM_TRIALS} across {len(POSITIONS)} document positions")
    print("=" * 80)
    
    results = []
    print(f"{'Position':<22} {'Method':<35} {'R@1':>6} {'F1':>6} {'Trials':>6}")
    print("-" * 80)
    
    for pos_i, (pos, label) in enumerate(zip(POSITIONS, POSITION_LABELS)):
        for mname, mfn in methods.items():
            hits, f1s = [], []
            for t in range(NUM_TRIALS):
                rng = random.Random(RANDOM_SEED + pos_i * 10000 + t)
                query, evidence = build_query_evidence(rng, chunk_size=CHUNK_SIZE)
                chunks = build_document(evidence, pos, TOTAL_CHUNKS, CHUNK_SIZE, rng)
                h, f = mfn(chunks, query, pos, rng)
                hits.append(h)
                f1s.append(f)
            
            recall = sum(hits) / NUM_TRIALS
            mean_f1 = sum(f1s) / NUM_TRIALS
            results.append({
                "position_label": label,
                "evidence_pos": pos,
                "method": mname,
                "recall_at_1": round(recall, 4),
                "mean_f1": round(mean_f1, 4),
                "num_trials": NUM_TRIALS
            })
            print(f"{label:<22} {mname:<35} {recall:>6.3f} {mean_f1:>6.3f} {NUM_TRIALS:>6}")
            
    out_csv = os.path.join(BASE_DIR, "results", "results_v2.csv")
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
        
    print("-" * 80)
    print(f"Saved primary results to: {out_csv}")

if __name__ == "__main__":
    main()
