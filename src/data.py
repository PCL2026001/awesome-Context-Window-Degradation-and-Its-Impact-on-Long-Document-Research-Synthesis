"""
Synthetic data generation and scoring utilities for controlled retrieval experiments.
"""

import random
from typing import List, Tuple, Optional

def random_words(n: int, vocab_size: int = 800, rng: Optional[random.Random] = None) -> str:
    r = rng or random
    return " ".join(str(r.randint(0, vocab_size)) for _ in range(n))

def build_query_evidence(rng: random.Random, chunk_size: int = 60) -> Tuple[str, str]:
    signal_tokens = ["SIGNAL_X", "SIGNAL_Y", "SIGNAL_Z"]
    partial_match = signal_tokens[:2]
    evidence = " ".join(signal_tokens) + " " + random_words(chunk_size - len(signal_tokens), rng=rng)
    query = " ".join(partial_match)
    return query, evidence

def build_document(evidence: str, pos: int, total_chunks: int, chunk_size: int, rng: random.Random) -> List[str]:
    return [evidence if i == pos else random_words(chunk_size, rng=rng) for i in range(total_chunks)]

def bow_score(chunk: str, query: str) -> float:
    qt = set(query.lower().split())
    ct = set(chunk.lower().split())
    if not qt:
        return 0.0
    return len(qt & ct) / len(qt)
