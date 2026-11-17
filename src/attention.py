"""
Attention degradation formulations matching Liu et al. (2024) primacy-recency dynamics.
"""

import math

def attn_weight(pos: int, total: int, strength: float = 1.8) -> float:
    """
    Computes theoretical attention degradation weight using a U-shaped
    primacy-recency function:
    
        w(i, N) = max(0.05, 1.0 - lambda * sin^2(pi * i / (N - 1)))
        
    Args:
        pos: Zero-indexed position of chunk within the window.
        total: Total number of chunks in the current window.
        strength: Attenuation intensity parameter lambda.
        
    Returns:
        float: Effective attention weight clamped to [0.05, 1.0].
    """
    if total <= 1:
        return 1.0
    frac = pos / (total - 1)
    w = 1.0 - strength * (math.sin(math.pi * frac) ** 2)
    return max(0.05, w)
