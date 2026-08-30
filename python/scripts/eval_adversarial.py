#!/usr/bin/env python3
"""Adversarial input stress test.

Every public method gets fed hostile input: empty, whitespace, huge,
mixed-script, emoji, control characters, injection-looking strings,
RTL/LTR marks, numbers, and lone diacritics. Nothing may raise, hang,
or return a nonsense type. A library people trust in production must
degrade politely, not crash.

Run:
    PYTHONPATH=src python3 scripts/eval_adversarial.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from egy_names import EgyNames  # noqa: E402

HOSTILE = [
    ("empty", ""),
    ("space only", "   "),
    ("tab/newline", "\t\n\r "),
    ("single letter ar", "م"),
    ("single letter en", "m"),
    ("lone diacritic", "\u064e"),
    ("tashkeel only", "\u064e\u0651\u064f\u0652"),
    ("emoji", "🙂🎉"),
    ("name + emoji", "محمد🙂"),
    ("digits", "1234567890"),
    ("name + digits", "محمد123"),
    ("punctuation", "!@#$%^&*()_+-=[]{}|;':\",./<>?"),
    ("sql-ish", "'; DROP TABLE names; --"),
    ("html-ish", "<script>alert(1)</script>"),
    ("path-ish", "../../etc/passwd"),
    ("null-ish", "\x00\x01\x02"),
    ("rtl/ltr marks", "\u200f\u200eمحمد\u200f"),
    ("zero width", "مح\u200bمد"),
    ("nbsp separated", "محمد\u00a0أحمد"),
    ("mixed script", "محمدMohamed"),
    ("mixed with space", "محمد Mohamed"),
    ("very long ar", "محمد" * 500),
    ("very long en", "Mohamed" * 500),
    ("many tokens", " ".join(["محمد"] * 300)),
    ("only spaces between", "محمد     أحمد"),
    ("leading/trailing space", "   محمد   "),
    ("unicode combining", "م\u0300\u0301"),
    ("surrogate-ish", "\ud83d\ude00".encode("utf-16", "surrogatepass").decode("utf-16")),
    ("cyrillic", "Мохамед"),
    ("hebrew", "מוחמד"),
    ("chinese", "穆罕默德"),
    ("mixed dialect spelling", "محمّد"),
    ("hamza variants", "أحمد احمد إحمد آحمد"),
    ("repeated diacritics", "مُُُحَ" * 50),
]


def main() -> None:
    en = EgyNames()
    failures = []
    slow = []

    methods = [
        ("lookup", lambda s: en.lookup(s)),
        ("info", lambda s: en.info(s)),
        ("is_valid", lambda s: en.is_valid(s)),
        ("translate", lambda s: en.translate(s)),
        ("split", lambda s: en.split(s)),
        ("detect_gender", lambda s: en.detect_gender(s)),
        ("detect_religion", lambda s: en.detect_religion(s)),
        ("annotate", lambda s: en.annotate(s)),
        ("tashkeel", lambda s: en.tashkeel(s)),
        ("tashkeel_eg", lambda s: en.tashkeel_eg(s)),
        ("rank", lambda s: en.rank(s)),
        ("identify", lambda s: en.identify(s)),
        ("identify_all", lambda s: en.identify_all(s)),
        ("correct", lambda s: en.correct(s)),
        ("search", lambda s: en.search(contains=s)),
    ]

    for label, payload in HOSTILE:
        for mname, fn in methods:
            t0 = time.time()
            try:
                out = fn(payload)
            except Exception as exc:  # noqa: BLE001
                failures.append((label, mname, f"{type(exc).__name__}: {exc}"))
                continue
            elapsed = time.time() - t0
            if elapsed > 2.0:
                slow.append((label, mname, round(elapsed, 2)))

            # Type sanity: these must never return None where a
            # container/primitive is promised.
            if mname in ("is_valid",) and not isinstance(out, bool):
                failures.append((label, mname, f"expected bool, got {type(out).__name__}"))
            if mname in ("translate", "tashkeel", "tashkeel_eg") and not isinstance(out, str):
                failures.append((label, mname, f"expected str, got {type(out).__name__}"))
            if mname in ("split", "identify_all") and not isinstance(out, list):
                failures.append((label, mname, f"expected list, got {type(out).__name__}"))
            if mname in ("detect_gender",) and out.gender not in (
                "male",
                "female",
                "neutral",
            ):
                failures.append((label, mname, f"bad gender value {out.gender!r}"))
            if mname in ("detect_religion",) and out.religion not in (
                "muslim",
                "christian",
                "neutral",
            ):
                failures.append((label, mname, f"bad religion value {out.religion!r}"))

    total = len(HOSTILE) * len(methods)
    print(f"Adversarial cases run: {total} ({len(HOSTILE)} payloads x {len(methods)} methods)")
    print(f"Failures: {len(failures)}")
    print(f"Slow (>2s): {len(slow)}")

    if failures:
        print("\n=== FAILURES ===")
        for label, mname, msg in failures:
            print(f"  [{label}] {mname}: {msg}")
    if slow:
        print("\n=== SLOW ===")
        for label, mname, secs in slow:
            print(f"  [{label}] {mname}: {secs}s")


if __name__ == "__main__":
    main()
