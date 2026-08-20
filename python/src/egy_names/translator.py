"""Arabic ↔ English name translation using the 134K+ variant lookup index."""

from __future__ import annotations

from typing import Optional

from ._index import is_arabic, lookup_ar, lookup_en, normalize_ar, normalize_en


def translate_token(token: str, *, to: Optional[str] = None) -> str:
    """Translate a single name token.

    Args:
        token: A single name (Arabic or English).
        to: Force target language ("ar" or "en"). If None, auto-detect
            source language and translate to the other.

    Returns:
        The translated token, or the original if no translation found.
    """
    src_is_arabic = is_arabic(token)

    if to is None:
        to = "en" if src_is_arabic else "ar"

    if to == "en":
        entry = lookup_ar(token)
        return entry.en if entry else token
    else:  # to == "ar"
        entry = lookup_en(token)
        return entry.ar if entry else token


def translate(
    full_name: str,
    *,
    to: Optional[str] = None,
) -> str:
    """Translate a full name (one or more parts) between Arabic and English.

    Each whitespace-separated token is translated independently.

    Args:
        full_name: A name or full name string (e.g., "محمد أحمد علي").
        to: Force target language ("ar" or "en"). If None, auto-detect.

    Returns:
        The translated full name.
    """
    if not full_name or not full_name.strip():
        return full_name

    tokens = full_name.strip().split()
    translated = [translate_token(t, to=to) for t in tokens]
    return " ".join(translated)
