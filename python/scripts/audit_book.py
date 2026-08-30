#!/usr/bin/env python3
"""Broad structural integrity audit of the whole book.

Not reacting to a reported pattern — scanning every field of every
entry for internal inconsistency: encoding/whitespace defects, script
contamination, numeric field sanity, cross-field consistency, and
duplicate/overlap problems in variant lists. Prints counts per check
plus samples, so real problems can be triaged and fixed deliberately
instead of guessed at.

Run:
    PYTHONPATH=src python3 scripts/audit_book.py
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from egy_names._index import get_all, lookup_ar  # noqa: E402
from egy_names._quality import is_personal_entry  # noqa: E402

ARABIC_RE = re.compile(r"[\u0600-\u06FF]")
LATIN_RE = re.compile(r"[A-Za-z]")
DIGIT_RE = re.compile(r"\d")
DOUBLE_SPACE_RE = re.compile(r"  +")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def report(title: str, items, limit=12, fmt=lambda x: x):
    print(f"\n=== {title}: {len(items)} ===")
    for it in items[:limit]:
        print("  ", fmt(it))
    if len(items) > limit:
        print(f"   ... and {len(items) - limit} more")


def main() -> None:
    book = [e for e in get_all() if is_personal_entry(e)]
    print(f"Auditing {len(book)} personal entries\n")

    # ---- 1. Whitespace defects ----
    leading_trailing = [e for e in book if e.ar != e.ar.strip()]
    double_space = [e for e in book if DOUBLE_SPACE_RE.search(e.ar)]
    report("ar has leading/trailing whitespace", leading_trailing, fmt=lambda e: repr(e.ar))
    report("ar has double-space", double_space, fmt=lambda e: repr(e.ar))

    # ---- 2. Control characters / encoding defects ----
    control_chars = [e for e in book if CONTROL_RE.search(e.ar) or CONTROL_RE.search(e.en)]
    report("ar/en has control characters", control_chars, fmt=lambda e: (repr(e.ar), repr(e.en)))

    # ---- 3. Script contamination ----
    ar_has_latin = [e for e in book if LATIN_RE.search(e.ar)]
    ar_has_digit = [e for e in book if DIGIT_RE.search(e.ar)]
    en_has_arabic = [e for e in book if ARABIC_RE.search(e.en)]
    en_empty = [e for e in book if not e.en.strip()]
    ar_empty = [e for e in book if not e.ar.strip()]
    report("ar contains Latin letters", ar_has_latin, fmt=lambda e: (e.ar, e.en))
    report("ar contains digits", ar_has_digit, fmt=lambda e: (e.ar, e.en))
    report("en contains Arabic letters", en_has_arabic, fmt=lambda e: (e.ar, e.en))
    report("en is empty", en_empty, fmt=lambda e: e.ar)
    report("ar is empty", ar_empty, fmt=lambda e: e.en)

    # ---- 4. Numeric field sanity ----
    bad_share = [e for e in book if not (0.0 <= e.corpus_share <= 100.0)]
    bad_slots = []
    for e in book:
        if len(e.slot_pcts) != 8:
            bad_slots.append(e)
            continue
        total = sum(e.slot_pcts)
        if total > 0 and not (85.0 <= total <= 115.0):
            bad_slots.append(e)
    report("corpus_share out of [0,100]", bad_share, fmt=lambda e: (e.ar, e.corpus_share))
    report(
        "slot_pcts don't sum to ~100 (or wrong length)",
        bad_slots,
        fmt=lambda e: (e.ar, len(e.slot_pcts), round(sum(e.slot_pcts), 1)),
    )

    # ---- 5. Frequency-class vs corpus_share mismatch ----
    freq_mismatch = []
    for e in book:
        fc = e.frequency.value
        share = e.corpus_share
        if fc == "common" and share < 0.001:
            freq_mismatch.append((e, "common but tiny share"))
        elif fc == "rare" and share > 0.5:
            freq_mismatch.append((e, "rare but huge share"))
    report(
        "frequency_class disagrees sharply with corpus_share",
        freq_mismatch,
        fmt=lambda t: (t[0].ar, t[0].frequency.value, t[0].corpus_share, t[1]),
    )

    # ---- 6. Missing meaning / tashkeel for real entries ----
    no_meaning = [e for e in book if not (e.meaning_ar or "").strip()]
    no_tashkeel = [e for e in book if not (e.tashkeel or "").strip()]
    report("meaning_ar is empty", no_meaning, fmt=lambda e: (e.ar, e.en))
    report("tashkeel is empty", no_tashkeel, fmt=lambda e: (e.ar, e.en))

    # ---- 7. Variant list problems ----
    empty_variant = [
        e for e in book if any(not v.strip() for v in e.ar_variants + e.en_variants)
    ]
    dup_variant = [
        e
        for e in book
        if len(e.ar_variants) != len(set(e.ar_variants))
        or len(e.en_variants) != len(set(e.en_variants))
    ]
    report("has an empty variant string", empty_variant, fmt=lambda e: (e.ar, e.ar_variants))
    report("has a duplicate variant", dup_variant, fmt=lambda e: (e.ar, e.ar_variants))

    # ---- 8. Cross-entry variant collisions (one variant claimed by two lemmas) ----
    variant_owner: dict[str, list[str]] = {}
    for e in book:
        for v in e.ar_variants:
            v = v.strip()
            if not v:
                continue
            variant_owner.setdefault(v, []).append(e.ar)
    contested = {v: owners for v, owners in variant_owner.items() if len(set(owners)) > 1}
    report(
        "ar_variant string claimed by >1 distinct lemma",
        list(contested.items()),
        fmt=lambda kv: (kv[0], kv[1][:4]),
    )

    # ---- 9. root field sanity ----
    bad_root = [
        e
        for e in book
        if e.root not in ("N/A",) and not re.fullmatch(r"[\u0600-\u06FF\-\|]+", e.root)
    ]
    report("root field has unexpected characters", bad_root, fmt=lambda e: (e.ar, repr(e.root)))

    # ---- 10. Multi-word (3+) entries: same malformed-compound risk ----
    three_plus = [e for e in book if len(e.ar.strip().split()) >= 3]
    bad_three = [e for e in three_plus if lookup_ar(e.ar.strip().split()[0]) is None]
    report(
        "3+-word lemma whose first word is not a known name",
        bad_three,
        fmt=lambda e: (e.ar, e.en, e.corpus_share),
    )

    # ---- 11. gender/role sanity: family/tribal entries with a gendered name-only meaning that reads like a given name ----
    family_but_short = [
        e
        for e in book
        if e.role.value in ("family", "tribal")
        and " " not in e.ar.strip()
        and len(e.ar.strip()) <= 3
    ]
    report(
        "very short single-word family/tribal lemma (surface plausibility check)",
        family_but_short,
        fmt=lambda e: (e.ar, e.en, e.meaning_ar[:50]),
    )

    # ---- 12. ar/en both consist of the exact same repeated single letter (garbage row) ----
    repeated_char = [e for e in book if len(set(e.ar.replace(" ", ""))) == 1]
    report("ar is a single repeated character", repeated_char, fmt=lambda e: (e.ar, e.en))

    print("\nDone.")


if __name__ == "__main__":
    main()
