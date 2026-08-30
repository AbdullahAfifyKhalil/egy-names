#!/usr/bin/env python3
"""One-time fix: 'X+عبد الله' -> 'X عبدالله' spacing.

The catalog fused a leading title/name onto 'عبد' and then split before
'الله' (e.g. 'اميرعبد الله'), instead of keeping the leading name as its
own word and fusing the classic 'عبدالله' compound the way it is
conventionally written (e.g. 'امير عبدالله'). Only touches rows where
stripping the trailing 'عبد' from the first word leaves a real,
independently attested book name — multi-name chains where that is not
true (e.g. 'محمداحمدعبد الله') are left alone rather than guessed at.

Run against the master file, then re-sync to every SDK with
sync-catalog.sh once you are ready to propagate it beyond Python.
"""
from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python" / "src"))
DIVINE = {"الله", "اللة"}


def normalize_ar(text: str) -> str:
    # Match egy_names._index.normalize_ar: fold hamza/alef variants and
    # a handful of common letter-shape differences so "اميرعبد" and
    # "أميرعبد" resolve to the same standalone-name check.
    table = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ة": "ه", "ى": "ي"})
    return text.translate(table)


def build_ar_index(names):
    idx = {}
    for n in names:
        idx[normalize_ar(n["a"])] = n
    return idx


def main(paths: list[str]) -> None:
    for rel in paths:
        path = ROOT / rel if not rel.startswith("/") else Path(rel)
        with gzip.open(path, "rt", encoding="utf-8") as f:
            raw = json.load(f)
        names = raw["names"]
        ar_index = build_ar_index(names)

        n_fixed = 0
        for n in names:
            ar = n["a"].strip()
            if " " not in ar:
                continue
            parts = ar.split()
            if len(parts) != 2:
                continue
            a, b = parts
            if b not in DIVINE or not a.endswith("عبد"):
                continue
            prefix = a[:-3]
            if len(prefix) < 2 or normalize_ar(prefix) not in ar_index:
                continue

            new_ar = f"{prefix} عبد{b}"
            if new_ar == ar:
                continue
            n["a"] = new_ar
            # Keep en/meaning as-is: they already describe the correct
            # "prefix + Abdallah" reading, only the ar spacing was off.
            n_fixed += 1

        with gzip.open(path, "wt", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False)

        print(f"{path}: fixed {n_fixed} entries")


if __name__ == "__main__":
    main(
        [
            "data/names.json.gz",
            "python/src/egy_names/data/names.json.gz",
        ]
    )
