"""Name annotation — returns full metadata for any Egyptian name."""

from __future__ import annotations

from typing import List, Optional

from ._index import lookup, lookup_ar, lookup_en, is_arabic
from ._types import NameEntry, NameInfo


def annotate_single(name: str) -> Optional[NameInfo]:
    """Get full metadata for a single name token.

    Args:
        name: A single name in Arabic or English.

    Returns:
        NameInfo if found, None otherwise.
    """
    entry = lookup(name)
    if entry is None:
        return None
    return NameInfo._from_entry(entry)


def annotate(name: str) -> Optional[NameInfo] | List[Optional[NameInfo]]:
    """Get metadata for a name (single token) or full name (multiple tokens).

    For a single token, returns a single NameInfo (or None).
    For multiple space-separated tokens, returns a list of NameInfo.

    Args:
        name: One or more name tokens separated by spaces.

    Returns:
        NameInfo, list of NameInfo, or None.
    """
    if not name or not name.strip():
        return None

    tokens = name.strip().split()
    if len(tokens) == 1:
        return annotate_single(tokens[0])

    return [annotate_single(t) for t in tokens]
