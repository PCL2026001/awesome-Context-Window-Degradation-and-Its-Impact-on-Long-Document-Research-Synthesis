#!/usr/bin/env python3
"""
Ablation study entrypoint: evaluates attention-decay parameter lambda in [0.0, 3.0]
at the middle (50%) document position.
"""

import os
import sys
import json
import csv
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.attention import attn_weight
from src.data import build_query_evidence, build_document, bow_score

CONFIG_PATH = os.path.join(BASE_DIR, "configs", "config_v2.json")
with open(CONFIG_PATH, "r") as f:
    cfg = json.load(f)

RANDOM_SEED = cfg["random_seed"]
TOTAL_CHUNKS = cfg["total_chunks"]
CHUNK_SIZE = cfg["chunk_size"]
NUM_TRIALS = cfg["num_trials"]
MID_POS = cfg["positions"][2]

def main():
    print("=" * 60)
    print("AITR Lab 02: Attention-Decay Parameter Ablation")
    print(f"Target Position: Middle (Index {MID_POS}, 50%)")
    print("=" * 60)
    
    strengths = [0.0, 0.5, 1.0, 1.5, 1.8, 2.0, 2.5, 3.0]
    records = []
    
    for s in strengths:
        hits = []
        for t in range(NUM_TRIALS):
            rng = random.Random(RANDOM_SEED + 99999 + t)
            query, evidence = build_query_evidence(rng, chunk_size=CHUNK_SIZE)
            chunks = build_document(evidence, MID_POS, TOTAL_CHUNKS, CHUNK_SIZE, rng)
            n = len(chunks)
            scores = [
                bow_score(c, query) * attn_weight(i, n, strength=s) + rng.gauss(0, 0.015)
                for i, c in enumerate(chunks)
            ]
            pred = max(range(n), key=lambda i: scores[i])
            hits.append(int(pred == MID_POS))
        
        recall = sum(hits) / NUM_TRIALS
        records.append({"strength": s, "recall_at_1": round(recall, 4)})
        print(f"  lambda = {s:4.1f}  ->  Recall@1 = {recall:.4f}")
        
    out_csv = os.path.join(BASE_DIR, "results", "ablation_strength.csv")
    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["strength", "recall_at_1"])
        writer.writeheader()
        writer.writerows(records)
    print("=" * 60)
    print(f"Saved ablation results to: {out_csv}")

if __name__ == "__main__":
    main()
