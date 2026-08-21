"""Spelling correction for Egyptian names.

Uses the 54K-entry correction index plus Arabic orthographic normalization
and compound name resolution to map misspelled or variant-form names
to their canonical form.
"""

from __future__ import annotations

from typing import Optional

from ._index import (
    correct as _correction_lookup,
    lookup_ar,
    normalize_ar,
    get_ar_forms,
    get_ar_norm_forms,
    is_arabic,
)


def correct_token(token: str) -> str:
    """Correct a single name token to its canonical form."""
    if not token or not token.strip():
        return ""

    t = token.strip()

    # 1. Exact AR entry match (already canonical)
    entry = lookup_ar(t)
    if entry and entry.ar:
        return entry.ar

    # 2. Correction index (surface_form -> canonical)
    canonical = _correction_lookup(t)
    if canonical:
        return canonical

    # 3. Normalized match
    norm = normalize_ar(t)
    ar_norm = get_ar_norm_forms()
    entry = ar_norm.get(norm)
    if entry:
        return entry.ar

    # 4. Trailing alif / alif maqsura check
    if norm.endswith("\u0627"):
        alt = norm[:-1] + "\u064A"
        alt_entry = ar_norm.get(alt)
        if alt_entry:
            return alt_entry.ar
    elif norm.endswith("\u064A"):
        alt = norm[:-1] + "\u0627"
        alt_entry = ar_norm.get(alt)
        if alt_entry:
            return alt_entry.ar

    return t


def correct(name: str) -> str:
    """Correct a full name (including compound and multi-word names)."""
    if not name or not name.strip():
        return ""

    tokens = name.strip().split()
    result = []
    i = 0
    n = len(tokens)

    while i < n:
        current = tokens[i]

        # Check if current and next token form a compound name (e.g. "عبد" + "الرحيم" -> "عبدالرحيم")
        if i < n - 1:
            next_tok = tokens[i + 1]
            compound = f"{current} {next_tok}"
            compound_no_space = f"{current}{next_tok}"
            compound_entry = lookup_ar(compound) or lookup_ar(compound_no_space)
            if compound_entry:
                result.append(compound_entry.ar)
                i += 2
                continue

        result.append(correct_token(current))
        i += 1

    return " ".join(result)
