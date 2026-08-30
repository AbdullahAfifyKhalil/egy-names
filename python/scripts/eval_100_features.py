#!/usr/bin/env python3
"""100-name validation across every public library feature.

Different from eval_500.py (which stress-tests detection logic hard):
this exercises breadth — every public method on EgyNames — across a
fresh stratified 100-name sample, and reports pass/fail per feature so
gaps are visible per capability, not just per name.

Run:
    PYTHONPATH=src python3 scripts/eval_100_features.py
"""
from __future__ import annotations

import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from egy_names import EgyNames  # noqa: E402
from egy_names._index import get_all  # noqa: E402
from egy_names._quality import is_low_confidence_entry, is_personal_entry  # noqa: E402

SEED = 20260901
N = 100


def stratified_sample(entries, n, rng):
    buckets = defaultdict(list)
    for e in entries:
        buckets[(e.role.value, e.gender.value, e.religion.value)].append(e)
    keys = list(buckets.keys())
    rng.shuffle(keys)
    per_bucket = max(1, n // max(1, len(keys)))
    out = []
    seen = set()
    for k in keys:
        rows = buckets[k][:]
        rng.shuffle(rows)
        for r in rows[:per_bucket]:
            out.append(r)
            seen.add(r.ar)
    # Stratified quota often under-fills small buckets; top up from the
    # remaining pool so the sample is always exactly n.
    if len(out) < n:
        leftover = [e for e in entries if e.ar not in seen]
        rng.shuffle(leftover)
        out.extend(leftover[: n - len(out)])
    rng.shuffle(out)
    return out[:n]


def main() -> None:
    rng = random.Random(SEED)
    en = EgyNames()

    book = [e for e in get_all() if is_personal_entry(e) and not is_low_confidence_entry(e)]
    sample = stratified_sample(book, N, rng)

    checks = defaultdict(lambda: {"pass": 0, "fail": 0, "errors": []})

    def check(feature, cond, e, detail=""):
        d = checks[feature]
        if cond:
            d["pass"] += 1
        else:
            d["fail"] += 1
            d["errors"].append((e.ar, e.en, detail))

    for e in sample:
        # lookup / info
        info = en.lookup(e.ar)
        check("lookup(ar)", info is not None and info.ar == e.ar, e)
        check("info(ar) alias", en.info(e.ar) is not None, e)
        check("lookup(en)", en.lookup(e.en) is not None, e, f"lookup({e.en!r}) failed")

        # is_valid
        check("is_valid", en.is_valid(e.ar) is True, e)

        # translate
        t_en = en.translate(e.ar)
        check("translate ar->en nonempty", bool(t_en), e)
        t_ar = en.translate(e.en)
        check("translate en->ar nonempty", bool(t_ar), e)

        # split
        parts = en.split(e.ar)
        check("split(single token)", parts == [e.ar], e, f"got {parts}")

        # tashkeel
        tk = en.tashkeel(e.ar)
        check("tashkeel nonempty", bool(tk), e)
        tk_eg = en.tashkeel_eg(e.ar)
        check("tashkeel_eg nonempty", bool(tk_eg), e)

        # rank
        rk = en.rank(e.ar)
        check("rank returns for book entry", rk is not None, e)

        # detect_gender / detect_religion on the single token
        if e.role.value == "given":
            gd = en.detect_gender(e.ar)
            check(
                "detect_gender matches book (given)",
                e.gender.value == "neutral" or gd.gender == e.gender.value,
                e,
                f"got {gd.gender}",
            )
            rd = en.detect_religion(e.ar)
            check(
                "detect_religion matches book (given)",
                e.religion.value == "neutral" or rd.religion == e.religion.value,
                e,
                f"got {rd.religion}",
            )

        # annotate
        ann = en.annotate(e.ar)
        check("annotate returns", ann is not None, e)

        # correct (identity on a real name should return the same or a
        # sane suggestion, never crash / never empty)
        try:
            corrected = en.correct(e.ar)
            check("correct doesn't crash", True, e)
        except Exception as exc:  # noqa: BLE001
            check("correct doesn't crash", False, e, str(exc))

        # identify (book path)
        idn = en.identify(e.ar)
        check("identify book path", idn is not None and idn.source == "book", e)

    # identify_all on a full name built from real entries
    givens = [e for e in book if e.role.value == "given"][:20]
    for g in givens[:10]:
        full = f"{g.ar} أحمد"
        toks = en.identify_all(full)
        check("identify_all returns per-token list", len(toks) == 2, g, f"got {len(toks)}")

    # search + generate: feature-level smoke, not per-name
    try:
        results = en.search(gender="male", religion="muslim", max_results=10)
        check("search", isinstance(results, list) and len(results) > 0, sample[0])
    except Exception as exc:  # noqa: BLE001
        check("search", False, sample[0], str(exc))

    try:
        gen = en.generate(count=10, seed=SEED)
        check("generate", isinstance(gen, list) and len(gen) == 10, sample[0])
    except Exception as exc:  # noqa: BLE001
        check("generate", False, sample[0], str(exc))

    # ---- Report ----
    total_pass = sum(d["pass"] for d in checks.values())
    total_fail = sum(d["fail"] for d in checks.values())
    total = total_pass + total_fail
    print(f"Sample size: {len(sample)} names")
    print(f"Total checks: {total}  Pass: {total_pass}  Fail: {total_fail}")
    print(f"Overall: {100 * total_pass / total:.1f}%\n")

    print(f"{'Feature':45s} {'Pass':>6s} {'Fail':>6s} {'Rate':>7s}")
    print("-" * 68)
    for feature, d in sorted(checks.items()):
        n_total = d["pass"] + d["fail"]
        rate = 100 * d["pass"] / n_total if n_total else 0.0
        flag = "  <-- FAIL" if d["fail"] else ""
        print(f"{feature:45s} {d['pass']:6d} {d['fail']:6d} {rate:6.1f}%{flag}")

    if total_fail:
        print("\n=== FAILURE DETAILS ===")
        for feature, d in checks.items():
            if d["fail"]:
                print(f"\n[{feature}]")
                for ar, en_name, detail in d["errors"][:10]:
                    print(f"  {ar} / {en_name}: {detail}")


if __name__ == "__main__":
    main()
