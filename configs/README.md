# Experimental Configurations

This directory contains frozen, versioned configuration settings used across all empirical evaluations in the study.

## Configuration Files

- `config_v2.json`: Primary frozen hyperparameter configuration for Paper 2 results.
- `default_config.json`: Canonical configuration specification for reproducibility.

## Schema & Parameters

```json
{
  "random_seed": 42,
  "total_chunks": 20,
  "chunk_size": 60,
  "window_size": 5,
  "positions": [0, 5, 10, 15, 19],
  "num_trials": 200,
  "distractor_pool": 800
}
```

### Parameter Semantics
- `random_seed`: Deterministic pseudo-random seed ensuring 100% bitwise replication.
- `total_chunks`: Document length expressed in discrete semantic chunks ($N=20$).
- `chunk_size`: Word count per chunk (60 words $\approx$ 80 tokens, yielding 1,600-token total document lengths).
- `window_size`: Local context window size for sliding chunkers ($W=5$ chunks).
- `positions`: Discrete indices evaluating target evidence placement across the context:
  - `0`: Start (0%) — extreme primacy boundary.
  - `5`: Early (25%) — intermediate pre-center region.
  - `10`: Middle (50%) — maximum attention attenuation center.
  - `15`: Late (75%) — intermediate post-center region.
  - `19`: End (100%) — extreme recency boundary.
- `num_trials`: Monte Carlo trials per condition ($T=200$, yielding $4 \times 5 \times 200 = 4,000$ simulated retrievals).
- `distractor_pool`: Vocabulary cardinality used to synthesize non-matching distractor chunks.
