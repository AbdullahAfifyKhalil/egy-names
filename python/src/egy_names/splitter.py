"""Dictionary-based full-name splitting with DP segmentation for
concatenated Arabic text.

For space-separated input:  simple whitespace split.
For concatenated Arabic:    weighted dynamic programming using the 90K+
                            name dictionary for optimal segmentation.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

from ._index import (
    get_ar_forms,
    get_ar_norm_forms,
    is_arabic,
    lookup,
    normalize_ar,
)
from ._types import NameEntry


# ── Cost parameters for DP segmentation ──
_BASE_SEGMENT_COST = 1.0
_UNKNOWN_PENALTY = 8.0
_FREQ_BONUS = {"c": -0.6, "n": -0.2, "r": 0.0}  # common > normal > rare
_LENGTH_BONUS_PER_CHAR = -0.05  # prefer longer tokens (fewer segments)


def _dp_segment(text: str) -> List[str]:
    """Segment concatenated Arabic into individual name tokens using DP.

    Uses a weighted shortest-path algorithm where cost is minimized
    to find the segmentation that produces the most likely sequence
    of known Egyptian names.

    Args:
        text: Concatenated Arabic text with no spaces.

    Returns:
        List of name tokens forming the optimal segmentation.
    """
    ar_index = get_ar_forms()
    ar_norm = get_ar_norm_forms()

    n = len(text)
    # dp[i] = (cost_to_reach_i, backpointer_j, is_known)
    INF = float("inf")
    dp: List[Tuple[float, int, bool]] = [(INF, -1, False)] * (n + 1)
    dp[0] = (0.0, 0, True)

    for i in range(1, n + 1):
        # Try all possible last-tokens S[j:i]
        for j in range(max(0, i - 30), i):  # max name length ~30 chars
            if dp[j][0] == INF:
                continue

            substr = text[j:i]
            if len(substr) < 2 and j > 0:
                continue  # skip single-char segments (except at start)

            # Check if this substring is a known name
            entry = ar_index.get(substr)
            if entry is None:
                entry = ar_norm.get(normalize_ar(substr))

            if entry is not None:
                # Known name → low cost
                cost = (
                    dp[j][0]
                    + _BASE_SEGMENT_COST
                    + _FREQ_BONUS.get(entry.frequency.value[0], 0.0)
                    + _LENGTH_BONUS_PER_CHAR * len(substr)
                )
                if cost < dp[i][0]:
                    dp[i] = (cost, j, True)
            else:
                # Unknown segment → high cost (only if no better option)
                cost = dp[j][0] + _UNKNOWN_PENALTY + len(substr)
                if cost < dp[i][0]:
                    dp[i] = (cost, j, False)

    # Backtrack to recover the optimal segmentation
    if dp[n][0] == INF:
        return [text]  # couldn't segment at all

    segments: List[str] = []
    pos = n
    while pos > 0:
        prev = dp[pos][1]
        segments.append(text[prev:pos])
        pos = prev

    segments.reverse()
    return segments


def split(full_name: str) -> List[str]:
    """Split a full name into individual name parts.

    Handles:
      - Space-separated names (trivial split)
      - Concatenated Arabic text (DP segmentation)
      - English names (whitespace split)

    Args:
        full_name: A full name string.

    Returns:
        List of individual name tokens.
    """
    if not full_name or not full_name.strip():
        return []

    text = full_name.strip()

    # If spaces exist, use simple whitespace splitting
    if " " in text:
        return text.split()

    # Single token — is it Arabic with potential concatenation?
    if is_arabic(text):
        # Check if the whole string is a known single name first
        entry = lookup(text)
        if entry is not None:
            return [text]

        # Try DP segmentation for concatenated Arabic
        segments = _dp_segment(text)
        return segments

    # English single token — can't split further
    return [text]
