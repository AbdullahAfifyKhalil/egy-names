#!/usr/bin/env python3
"""Train the ML fallback used by egy_names._infer.

Trains char-ngram + morphology logistic models for gender, religion,
and role on the book's given-name-role subset (where those signals are
strongest), with a stratified holdout to report real accuracy before
anything ships. Writes a compact JSON.gz the runtime can load without
scikit-learn or numpy as a runtime dependency.

Run:
    PYTHONPATH=src python3 scripts/train_infer_model.py
"""
from __future__ import annotations

import gzip
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from egy_names._index import get_all, normalize_ar  # noqa: E402
from egy_names._quality import is_low_confidence_entry, is_personal_entry  # noqa: E402
from egy_names._infer import morph_flags  # noqa: E402

from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402
from sklearn.metrics import classification_report  # noqa: E402
from scipy.sparse import hstack, csr_matrix  # noqa: E402
import numpy as np  # noqa: E402

SEED = 20260830
NGRAM = (2, 5)
OUT_PATH = ROOT / "src" / "egy_names" / "data" / "infer_model.json.gz"


def stratified_split(items, keyfn, frac=0.15, rng=None):
    rng = rng or random.Random(SEED)
    buckets = defaultdict(list)
    for e in items:
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
    ngram_X = vec.fit_transform(texts) if fit else vec.transform(texts)
    return hstack([ngram_X, csr_matrix(morph)]).tocsr()


def export_vectorizer(vec: TfidfVectorizer) -> dict:
    vocab = {k: int(v) for k, v in vec.vocabulary_.items()}
    idf = [float(x) for x in vec.idf_]
    return {"vocab": vocab, "idf": idf, "ngram": list(NGRAM)}


def export_classifier(clf: LogisticRegression) -> dict:
    """Export coef/intercept with one row per class.

    scikit-learn collapses binary logistic regression to a single row
    (the positive-class direction). Expand it to two rows so the
    runtime softmax scorer does not need a binary special case.
    """
    classes = [str(c) for c in clf.classes_]
    coef = clf.coef_.tolist()
    intercept = clf.intercept_.tolist()
    if len(classes) == 2 and len(coef) == 1:
        coef = [[-x for x in coef[0]], coef[0]]
        intercept = [-intercept[0], intercept[0]]
    return {"classes": classes, "coef": coef, "intercept": intercept}


def train_task(name, entries, yfn, rng):
    train, test = stratified_split(entries, yfn, frac=0.15, rng=rng)
    vec = TfidfVectorizer(analyzer="char", ngram_range=NGRAM, min_df=2, sublinear_tf=True)
    Xtr = build_matrix(train, vec, fit=True)
    Xte = build_matrix(test, vec, fit=False)
    ytr = [yfn(e) for e in train]
    yte = [yfn(e) for e in test]

    clf = LogisticRegression(max_iter=500, class_weight="balanced", C=1.5)
    clf.fit(Xtr, ytr)

    pred = clf.predict(Xte)
    print(f"\n==== {name} (n={len(entries)}, train={len(train)}, test={len(test)}) ====")
    print(classification_report(yte, pred, digits=3))

    pack = export_vectorizer(vec)
    pack["n_ngram"] = len(pack["vocab"])
    pack.update(export_classifier(clf))

    # Retrain on 100% of the data for the shipped artifact (holdout above
    # is only to print honest numbers).
    vec_full = TfidfVectorizer(analyzer="char", ngram_range=NGRAM, min_df=2, sublinear_tf=True)
    Xfull = build_matrix(entries, vec_full, fit=True)
    yfull = [yfn(e) for e in entries]
    clf_full = LogisticRegression(max_iter=500, class_weight="balanced", C=1.5)
    clf_full.fit(Xfull, yfull)

    pack_full = export_vectorizer(vec_full)
    pack_full["n_ngram"] = len(pack_full["vocab"])
    pack_full.update(export_classifier(clf_full))
    return pack_full


def main() -> None:
    rng = random.Random(SEED)
    book = [
        e
        for e in get_all()
        if is_personal_entry(e)
        and not is_low_confidence_entry(e)
        and " " not in e.ar.strip()
    ]
    given = [e for e in book if e.role.value == "given"]

    print(f"book (personal, single-token): {len(book)}")
    print(f"given-role subset for gender/religion training: {len(given)}")

    gender_pack = train_task("gender (given names)", given, lambda e: e.gender.value, rng)
    religion_pack = train_task("religion (given names)", given, lambda e: e.religion.value, rng)
    role_pack = train_task(
        "role (all personal)", book, lambda e: "family" if e.role.value == "family" else "given", rng
    )

    bundle = {
        "version": 1,
        "trained_on": len(book),
        "gender": gender_pack,
        "religion": religion_pack,
        "role": role_pack,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(OUT_PATH, "wt", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False)

    size_kb = OUT_PATH.stat().st_size / 1024
    print(f"\nWrote {OUT_PATH} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
