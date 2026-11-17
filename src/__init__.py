"""
AITR Lab 02 Source Package: Context-Window Degradation and Retrieval Mitigation.
"""

from .attention import attn_weight
from .data import build_query_evidence, build_document, bow_score
from .retrievers import full_context, chunked_sequential, overlapping_chunked, hierarchical
from .metrics import compute_confidence_intervals

__all__ = [
    "attn_weight",
    "build_query_evidence",
    "build_document",
    "bow_score",
    "full_context",
    "chunked_sequential",
    "overlapping_chunked",
    "hierarchical",
    "compute_confidence_intervals",
]
