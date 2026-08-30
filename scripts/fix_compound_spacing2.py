#!/usr/bin/env python3
"""Generalized fix for misplaced spaces in two-word compound lemmas.

The catalog fused a leading given name onto the FIRST half of a
compound second name, then kept the compound's second half as a
separate word:

    'احمدسعد الدين'  ->  'احمد سعدالدين'   (Ahmed + Saad-El-Din)
    'احمدنصر الله'   ->  'احمد نصرالله'    (Ahmed + Nasrallah)

Only rewrites when BOTH halves independently verify: the prefix must be
a real book name, and the remainder fused with the trailing word must
also be a real book name. Ambiguous leftovers (typos like 'عببد الله',
or three-name chains like 'محمداحمدعبد الله') are left untouched rather
than guessed at.

Supersedes fix_compound_spacing.py, which only handled the 'عبد' case.
"""
from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python" / "src"))

from egy_names._index import lookup_ar  # noqa: E402

PATHS = [
    "data/names.json.gz",
    "python/src/egy_names/data/names.json.gz",
]


def find_fix(ar: str):
    parts = ar.strip().split()
    if len(parts) != 2:
        return None
    a, b = parts
    if lookup_ar(a) is not None:
        return None
    for i in range(2, len(a) - 1):
        prefix, rest = a[:i], a[i:]
        if lookup_ar(prefix) is None:
            continue
        fused = rest + b
        if lookup_ar(fused) is not None or lookup_ar(f"{rest} {b}") is not None:
            return f"{prefix} {fused}"
    return None


def main() -> None:
    # Resolve fixes once against the live index so both files get the
    # identical rewrite regardless of iteration order.
    plan: dict[str, str] = {}
    with gzip.open(ROOT / PATHS[0], "rt", encoding="utf-8") as f:
        for n in json.load(f)["names"]:
            new = find_fix(n["a"])
            if new and new != n["a"]:
                plan[n["a"]] = new

    print(f"planned rewrites: {len(plan)}")

    for rel in PATHS:
        path = ROOT / rel
        with gzip.open(path, "rt", encoding="utf-8") as f:
            raw = json.load(f)
        n_fixed = 0
        for n in raw["names"]:
            new = plan.get(n["a"])
            if new:
                n["a"] = new
                n_fixed += 1
        with gzip.open(path, "wt", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False)
        print(f"{path}: fixed {n_fixed} entries")


if __name__ == "__main__":
    main()
