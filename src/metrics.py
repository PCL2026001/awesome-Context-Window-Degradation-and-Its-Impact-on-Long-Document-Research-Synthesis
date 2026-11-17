"""
Statistical metrics and confidence interval computation.
"""

import math
from typing import Dict, List

def compute_confidence_intervals(p: float, n: int, confidence: float = 0.95) -> Dict[str, float]:
    """
    Computes Wald binomial confidence interval.
    """
    z = 1.96 if confidence == 0.95 else 2.576
    se = math.sqrt((p * (1.0 - p)) / n) if (0.0 < p < 1.0 and n > 0) else 0.0
    margin = z * se
    return {
        "point_estimate": p,
        "ci_lower": round(max(0.0, p - margin), 4),
        "ci_upper": round(min(1.0, p + margin), 4),
        "standard_error": round(se, 4)
    }
