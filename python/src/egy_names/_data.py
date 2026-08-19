"""Lazy, thread-safe data loader for the bundled names corpus."""

from __future__ import annotations

import gzip
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional

from ._types import NameEntry

_DATA_FILE = Path(__file__).parent / "data" / "names.json.gz"

_lock = threading.Lock()
_cache: Optional[dict] = None


def _load_raw(path: Optional[Path] = None) -> dict:
    """Decompress and parse the JSON bundle."""
    p = path or _DATA_FILE
    with gzip.open(p, "rt", encoding="utf-8") as f:
        return json.load(f)


def get_bundle(path: Optional[Path] = None) -> dict:
    """Return the parsed bundle, loading it once and caching."""
    global _cache
    if _cache is not None and path is None:
        return _cache
    with _lock:
        if _cache is not None and path is None:
            return _cache
        bundle = _load_raw(path)
        if path is None:
            _cache = bundle
        return bundle


def get_entries(path: Optional[Path] = None) -> List[NameEntry]:
    """Return all name entries as NameEntry objects."""
    bundle = get_bundle(path)
    return [NameEntry._from_raw(r) for r in bundle["names"]]


def get_corrections(path: Optional[Path] = None) -> Dict[str, str]:
    """Return the correction index (surface_form → canonical)."""
    bundle = get_bundle(path)
    return bundle.get("corrections", {})


def get_metadata(path: Optional[Path] = None) -> dict:
    """Return corpus metadata (version, size, years)."""
    bundle = get_bundle(path)
    return {
        "version": bundle.get("version", "0.0.0"),
        "corpus_tokens": bundle.get("corpus_tokens", 0),
        "corpus_students": bundle.get("corpus_students", 0),
        "cohort_years": bundle.get("cohort_years", []),
    }


def clear_cache() -> None:
    """Clear the cached data (for testing or memory management)."""
    global _cache
    with _lock:
        _cache = None
