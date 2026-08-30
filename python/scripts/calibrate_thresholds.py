#!/usr/bin/env python3
"""Measure precision-at-threshold for each class the ML fallback can
predict, so abstention cutoffs in _infer.py are set from evidence
instead of a single accuracy number or a guess.

Accuracy alone hides which classes the model is actually reliable on;
a threshold that looks fine on paper can deliver much weaker precision
than "abstain unless confident" is supposed to guarantee. Re-run this
after any retrain and re-check _infer.py's thresholds still hold.

Run:
    PYTHONPATH=src python3 scripts/calibrate_thresholds.py
"""
from __future__ import annotations

import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from egy_names._index import get_all, normalize_ar  # noqa: E402
from egy_names._infer import morph_flags  # noqa: E402
from egy_names._quality import is_low_confidence_entry, is_personal_entry  # noqa: E402

SEED = 20260830
THRESHOLDS = [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.88, 0.90, 0.92, 0.95]


def stratified_split(entries, keyfn, frac=0.15, rng=None):
    rng = rng or random.Random(SEED)
    buckets = defaultdict(list)
    for e in entries:
        buckets[keyfn(e)].append(e)
    train, test = [], []
    for rows in buckets.values():
        rng.shuffle(rows)
        n = max(1, int(len(rows) * frac))
        test.extend(rows[:n])
        train.extend(rows[n:])
    return train, test


def build_matrix(entries, vec, fit=False):
    texts = [normalize_ar(e.ar) for e in entries]
    morph = np.array([morph_flags(e.ar) for e in entries], dtype=float)
    X = vec.fit_transform(texts) if fit else vec.transform(texts)
    return hstack([X, csr_matrix(morph)]).tocsr()


def calibrate(name: str, entries, yfn) -> None:
    train, test = stratified_split(entries, yfn, rng=random.Random(SEED))
    vec = TfidfVectorizer(analyzer="char", ngram_range=(2, 5), min_df=2, sublinear_tf=True)
    Xtr = build_matrix(train, vec, fit=True)
    Xte = build_matrix(test, vec, fit=False)
    ytr = [yfn(e) for e in train]
    yte = [yfn(e) for e in test]

    clf = LogisticRegression(max_iter=500, class_weight="balanced", C=1.5)
    clf.fit(Xtr, ytr)
    probs = clf.predict_proba(Xte)
    classes = list(clf.classes_)

    print(f"\n--- {name} (test n={len(test)}) ---")
    for cls in classes:
        if cls == "neutral":
            continue
        ci = classes.index(cls)
        for t in THRESHOLDS:
            idx = [i for i in range(len(test)) if probs[i][ci] >= t]
            if not idx:
                continue
            correct = sum(1 for i in idx if yte[i] == cls)
            precision = correct / len(idx)
            coverage = len(idx) / len(test)
            flag = "  <-- weak" if precision < 0.90 else ""
            print(
                f"  class={cls:10s} t={t:.2f} n={len(idx):4d} "
                f"precision={precision:.3f} coverage={coverage:.3f}{flag}"
            )


def main() -> None:
    book = [
        e
        for e in get_all()
        if is_personal_entry(e) and not is_low_confidence_entry(e) and " " not in e.ar.strip()
    ]
    given = [e for e in book if e.role.value == "given"]

    calibrate("gender", given, lambda e: e.gender.value)
    calibrate("religion", given, lambda e: e.religion.value)
    calibrate("role", book, lambda e: "family" if e.role.value == "family" else "given")


if __name__ == "__main__":
    main()
