#!/usr/bin/env python3
"""Hard 500-name evaluation for the Python SDK.

Stratified sample across role x gender x religion x frequency class,
plus synthetic full-name chains built from real book entries. Every
check is a hard pass/fail against the book's own ground truth — no
"looks plausible" grading. A single wrong answer on a confident claim
is a failure, full stop.

Run:
    PYTHONPATH=src python3 scripts/eval_500.py
"""
from __future__ import annotations

import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from egy_names import EgyNames  # noqa: E402
from egy_names._index import get_all  # noqa: E402
from egy_names._quality import is_low_confidence_entry, is_personal_entry  # noqa: E402

SEED = 20260830
N_SINGLE = 350
N_CHAINS = 150


def stratified_sample(entries, n, rng):
    buckets = defaultdict(list)
    for e in entries:
        buckets[(e.role.value, e.gender.value, e.religion.value)].append(e)
    keys = list(buckets.keys())
    rng.shuffle(keys)
    per_bucket = max(1, n // max(1, len(keys)))
    out = []
    for k in keys:
        rows = buckets[k][:]
        rng.shuffle(rows)
        out.extend(rows[:per_bucket])
    rng.shuffle(out)
    return out[:n]


def build_chains(clean, rng, n):
    """Build synthetic 'full name' chains: given + given + family."""
    givens = [e for e in clean if e.role.value == "given"]
    families = [e for e in clean if e.role.value == "family"]
    chains = []
    for _ in range(n):
        person = rng.choice(givens)
        father = rng.choice(givens)
        family = rng.choice(families) if families else rng.choice(givens)
        full = f"{person.ar} {father.ar} {family.ar}"
        # Ground truth: one part per chosen entry (3), even when a
        # chosen part is itself a legitimate two-word compound lemma
        # (e.g. kunya "Abu X") — naive whitespace count would be wrong.
        chains.append((full, person, 3))
    return chains


def main() -> None:
    rng = random.Random(SEED)
    en = EgyNames()

    book = [e for e in get_all() if is_personal_entry(e)]
    clean = [e for e in book if not is_low_confidence_entry(e)]

    singles = stratified_sample(clean, N_SINGLE, rng)
    chains = build_chains(clean, rng, N_CHAINS)

    results = {"solid": [], "wrong": [], "unsure": []}

    # ---- Single-token hard checks ----
    for e in singles:
        problems = []

        info = en.lookup(e.ar)
        if info is None:
            problems.append("lookup(ar) returned None for a book entry")
        else:
            if info.ar != e.ar:
                problems.append(f"lookup ar mismatch: {info.ar!r} != {e.ar!r}")
            if info.gender != e.gender.value:
                problems.append(f"lookup gender mismatch: {info.gender} != {e.gender.value}")
            if info.religion != e.religion.value:
                problems.append(f"lookup religion mismatch: {info.religion} != {e.religion.value}")

        if en.lookup(e.en) is None:
            problems.append(f"lookup(en={e.en!r}) returned None")

        if not en.is_valid(e.ar):
            problems.append("is_valid(ar) is False for a clean book entry")

        # translate should round-trip through a real variant, not necessarily
        # back to this exact lemma (many-to-one is expected), but must not
        # crash or return empty.
        t = en.translate(e.ar)
        if not t:
            problems.append("translate(ar) returned empty")

        # Single-token full-name detection must match the entry itself.
        if e.role.value == "given":
            gd = en.detect_gender(e.ar)
            if e.gender.value != "neutral" and gd.gender != e.gender.value:
                problems.append(f"detect_gender single-token: {gd.gender} != {e.gender.value}")
            rd = en.detect_religion(e.ar)
            if e.religion.value != "neutral" and rd.religion != e.religion.value:
                problems.append(f"detect_religion single-token: {rd.religion} != {e.religion.value}")

        if problems:
            results["wrong"].append((e.ar, e.en, problems))
        else:
            results["solid"].append((e.ar, e.en))

    # ---- Full-chain checks: gender/religion must follow the FIRST token ----
    for full, person, expected_parts in chains:
        problems = []
        gd = en.detect_gender(full)
        if person.gender.value != "neutral" and gd.gender != person.gender.value:
            problems.append(
                f"chain gender: got {gd.gender} (conf {gd.confidence}), "
                f"expected {person.gender.value} from first token {person.ar!r}"
            )
        rd = en.detect_religion(full)
        if person.religion.value != "neutral" and rd.religion != person.religion.value:
            problems.append(
                f"chain religion: got {rd.religion} (conf {rd.confidence}), "
                f"expected {person.religion.value} from first token {person.ar!r}"
            )
        split = en.split(full)
        if len(split) != expected_parts:
            problems.append(
                f"split token count mismatch: {split} (expected {expected_parts} parts)"
            )

        if problems:
            results["wrong"].append((full, person.en, problems))
        else:
            results["solid"].append((full, person.en))

    total = len(results["solid"]) + len(results["wrong"])
    print(f"Total cases: {total} ({N_SINGLE} single + {N_CHAINS} chains)")
    print(f"Solid: {len(results['solid'])} ({100*len(results['solid'])/total:.1f}%)")
    print(f"Wrong: {len(results['wrong'])} ({100*len(results['wrong'])/total:.1f}%)")

    if results["wrong"]:
        print("\n=== FAILURES ===")
        for surface, en_name, problems in results["wrong"]:
            print(f"\n{surface} / {en_name}")
            for p in problems:
                print(f"  - {p}")


if __name__ == "__main__":
    main()
