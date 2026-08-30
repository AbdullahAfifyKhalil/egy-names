"""ML fallback for names that are not in the book.

The book is the product. This module only runs when lookup misses.
Every field is labeled inferred. Rank, dallaa, figures, and official
passport spelling are never invented.

The classifier abstains unless the posterior is high. A wrong male
default is worse than saying unknown.
"""

from __future__ import annotations

import gzip
import json
import math
import threading
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Union

from ._index import (
    get_all,
    is_arabic,
    lookup,
    normalize_ar,
    normalize_en,
)
from ._quality import is_low_confidence_entry, is_personal_entry
from ._types import InferredName, NameEntry, NameRole
from . import _rules_config

_MODEL_PATH = Path(__file__).parent / "data" / "infer_model.json.gz"
_NOTE_INFERRED = (
    "Not in the book. Inferred. Do not treat as verified."
)
_NOTE_BOOK = "In the book. Use lookup() for the full verified row."
_NOTE_NEAREST = (
    "Not in the book. Closest verified name: {ar} ({en}). Inferred."
)

# Holdout-tuned to a consistent ~93-97% precision-at-threshold target,
# measured directly (not picked by feel): scripts/calibrate_thresholds.py
# reports precision/coverage per class per threshold. The role and
# christian thresholds moved up from an earlier pass that measured
# only accuracy, not actual precision-at-threshold — that pass gave
# "given" 81.8% precision and "christian" 89.4% precision at their old
# cutoffs, well under what "speak only when precision holds" promises.
# Sourced from data/logic_config.json (re-run scripts/calibrate_thresholds.py
# after any retrain, then update that file — every SDK reads the same cuts).
_THRESH = _rules_config.infer_thresholds()
_GENDER_MIN_P = _THRESH["gender_min_p"]
_MUSLIM_MIN_P = _THRESH["muslim_min_p"]
_CHRISTIAN_MIN_P = _THRESH["christian_min_p"]
_ROLE_MIN_P = _THRESH["role_min_p"]

_AR_EN = {
    "ا": "a", "أ": "a", "إ": "e", "آ": "a", "ء": "a", "ؤ": "o", "ئ": "e",
    "ب": "b", "ت": "t", "ث": "th", "ج": "g", "ح": "h", "خ": "kh",
    "د": "d", "ذ": "z", "ر": "r", "ز": "z", "س": "s", "ش": "sh",
    "ص": "s", "ض": "d", "ط": "t", "ظ": "z", "ع": "a", "غ": "gh",
    "ف": "f", "ق": "q", "ك": "k", "ل": "l", "م": "m", "ن": "n",
    "ه": "h", "ة": "a", "و": "w", "ي": "y", "ى": "a",
}
_EN_AR = {
    "kh": "خ", "sh": "ش", "gh": "غ", "th": "ث", "ph": "ف",
    "aa": "ا", "ee": "ي", "oo": "و",
    "a": "ا", "b": "ب", "c": "ك", "d": "د", "e": "ي", "f": "ف",
    "g": "ج", "h": "ه", "i": "ي", "j": "ج", "k": "ك", "l": "ل",
    "m": "م", "n": "ن", "o": "و", "p": "ب", "q": "ق", "r": "ر",
    "s": "س", "t": "ت", "u": "و", "v": "ف", "w": "و", "x": "كس",
    "y": "ي", "z": "ز",
}

_lock = threading.Lock()
_model: Optional[dict] = None
_nn_ar: Optional[List[Tuple[str, NameEntry]]] = None
_nn_en: Optional[List[Tuple[str, NameEntry]]] = None


def morph_flags(surface: str) -> List[int]:
    """Fixed-order morphological flags. Train and runtime must match."""
    n = normalize_ar(surface) if is_arabic(surface) else normalize_en(surface)
    ar = is_arabic(surface)
    if ar:
        return [
            int(surface.endswith("ة")),
            int(surface.endswith("ى")),
            int(n.startswith("عبد")),
            int(n.startswith("ابو")),
            int(n.startswith("ال")),
            int(n.endswith("وي") or n.endswith("اوي") or n.endswith("اني")),
            int(n.endswith("وس") or n.endswith("يس") or n.endswith("يوس")),
            int("ائيل" in surface or n.endswith("ئيل")),
            int(any(x in surface for x in ("جرجس", "مينا", "بطرس", "شنودة", "كيرلس", "ميخائيل"))),
            int(len(n) <= 3),
            int(len(n) >= 8),
        ]
    return [
        int(n.endswith(("a", "ah", "ya", "ia", "na"))),
        int(n.startswith(("abdel", "abdul", "abd"))),
        int(n.startswith(("abu", "abo"))),
        int(n.startswith(("el", "al"))),
        int(n.endswith(("awy", "awi", "any", "ani"))),
        int(n.endswith(("os", "ius", "yos"))),
        int(n.endswith(("el", "iel"))),
        int(any(x in n for x in ("gerges", "mina", "botros", "shenouda", "cyril", "michael"))),
        int(len(n) <= 3),
        int(len(n) >= 10),
        0,
    ]


def _char_ngrams(text: str, lo: int, hi: int) -> List[str]:
    grams: List[str] = []
    for n in range(lo, hi + 1):
        if len(text) < n:
            continue
        for i in range(len(text) - n + 1):
            grams.append(text[i : i + n])
    return grams


def _tfidf_vector(text: str, vocab: Dict[str, int], idf: List[float], lo: int, hi: int) -> Dict[int, float]:
    grams = _char_ngrams(text, lo, hi)
    tf: Dict[str, int] = {}
    for g in grams:
        if g in vocab:
            tf[g] = tf.get(g, 0) + 1
    vec: Dict[int, float] = {}
    for g, c in tf.items():
        i = vocab[g]
        vec[i] = (1.0 + math.log(c)) * idf[i]
    norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
    return {i: v / norm for i, v in vec.items()}


def _softmax(scores: List[float]) -> List[float]:
    m = max(scores)
    ex = [math.exp(s - m) for s in scores]
    z = sum(ex) or 1.0
    return [e / z for e in ex]


def _score_linear(vec: Dict[int, float], morph: Sequence[int], pack: dict) -> Dict[str, float]:
    classes: List[str] = pack["classes"]
    coef: List[List[float]] = pack["coef"]
    intercept: List[float] = pack["intercept"]
    n_ngram = pack["n_ngram"]
    scores = []
    for c in range(len(classes)):
        s = intercept[c]
        row = coef[c]
        for i, v in vec.items():
            s += row[i] * v
        for j, flag in enumerate(morph):
            if flag:
                s += row[n_ngram + j] * float(flag)
        scores.append(s)
    probs = _softmax(scores)
    return {classes[i]: probs[i] for i in range(len(classes))}


def _load_model() -> dict:
    global _model
    if _model is not None:
        return _model
    with _lock:
        if _model is not None:
            return _model
        with gzip.open(_MODEL_PATH, "rt", encoding="utf-8") as f:
            _model = json.load(f)
        return _model


def _nn_tables() -> Tuple[List[Tuple[str, NameEntry]], List[Tuple[str, NameEntry]]]:
    global _nn_ar, _nn_en
    if _nn_ar is not None and _nn_en is not None:
        return _nn_ar, _nn_en
    with _lock:
        if _nn_ar is not None and _nn_en is not None:
            return _nn_ar, _nn_en
        ar: List[Tuple[str, NameEntry]] = []
        en: List[Tuple[str, NameEntry]] = []
        for e in get_all():
            if not is_personal_entry(e) or is_low_confidence_entry(e):
                continue
            ar.append((normalize_ar(e.ar), e))
            en.append((normalize_en(e.en), e))
        _nn_ar, _nn_en = ar, en
        return _nn_ar, _nn_en


def _levenshtein(a: str, b: str, limit: int = 2) -> int:
    if abs(len(a) - len(b)) > limit:
        return limit + 1
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        row_min = i
        for j, cb in enumerate(b, 1):
            ins = cur[j - 1] + 1
            delete = prev[j] + 1
            sub = prev[j - 1] + (0 if ca == cb else 1)
            v = min(ins, delete, sub)
            cur.append(v)
            if v < row_min:
                row_min = v
        if row_min > limit:
            return limit + 1
        prev = cur
    return prev[-1]


def _nearest(surface: str) -> Optional[Tuple[NameEntry, int]]:
    arabic = is_arabic(surface)
    q = normalize_ar(surface) if arabic else normalize_en(surface)
    if not q:
        return None
    ar_tbl, en_tbl = _nn_tables()
    rows = ar_tbl if arabic else en_tbl
    best: Optional[NameEntry] = None
    best_d = 3
    qlen = len(q)
    for key, entry in rows:
        if abs(len(key) - qlen) > 2:
            continue
        d = _levenshtein(q, key, limit=2)
        if d < best_d:
            best_d = d
            best = entry
            if d == 1:
                break
    if best is None or best_d > 2:
        return None
    return best, best_d


def romanize_ar(ar: str) -> str:
    out: List[str] = []
    i = 0
    while i < len(ar):
        ch = ar[i]
        if ch == " ":
            out.append(" ")
            i += 1
            continue
        out.append(_AR_EN.get(ch, ch))
        i += 1
    en = "".join(out)
    if en:
        en = en[0].upper() + en[1:]
    return en


def arabize_en(en: str) -> str:
    s = normalize_en(en)
    if s.startswith("el"):
        s = "ال" + s[2:]
        # remaining latin after ال
        rest = normalize_en(en)[2:]
        return "ال" + _arabize_body(rest)
    if s.startswith("al") and len(s) > 3:
        return "ال" + _arabize_body(s[2:])
    return _arabize_body(s)


def _arabize_body(s: str) -> str:
    out: List[str] = []
    i = 0
    while i < len(s):
        if i + 1 < len(s) and s[i : i + 2] in _EN_AR:
            out.append(_EN_AR[s[i : i + 2]])
            i += 2
            continue
        out.append(_EN_AR.get(s[i], s[i]))
        i += 1
    return "".join(out)


def _apply_rule_table(kind: str, surface: str) -> Optional[Tuple[str, float]]:
    """Check surface against data/logic_config.json's ordered rule table.

    First matching rule for the token's script wins, exactly like the
    hand-written prefix/suffix checks this replaced — but the rule
    values themselves now live in one JSON file every SDK reads.
    """
    script = "ar" if is_arabic(surface) else "en"
    normalized = normalize_ar(surface) if script == "ar" else normalize_en(surface)
    for rule in _rules_config.infer_rules(kind):
        if rule.get("script") != script:
            continue
        if _rules_config.match_rule(rule, surface, normalized):
            return rule["value"], float(rule["confidence"])
    return None


def _rule_gender(surface: str) -> Optional[Tuple[str, float]]:
    return _apply_rule_table("gender", surface)


def _rule_religion(surface: str) -> Optional[Tuple[str, float]]:
    return _apply_rule_table("religion", surface)


def _rule_role(surface: str) -> Optional[Tuple[str, float]]:
    return _apply_rule_table("role", surface)


def _predict(surface: str, pack: dict) -> Dict[str, float]:
    arabic = is_arabic(surface)
    text = normalize_ar(surface) if arabic else normalize_en(surface)
    vec = _tfidf_vector(text, pack["vocab"], pack["idf"], pack["ngram"][0], pack["ngram"][1])
    return _score_linear(vec, morph_flags(surface), pack)


def _from_book(entry: NameEntry, surface: str) -> InferredName:
    return InferredName(
        surface=surface,
        inferred=False,
        source="book",
        note=_NOTE_BOOK,
        is_valid=is_personal_entry(entry),
        ar=entry.ar,
        en=entry.en,
        gender=entry.gender.value,
        gender_confidence=1.0,
        religion=entry.religion.value,
        religion_confidence=1.0,
        role=entry.role.value,
        role_confidence=1.0,
        tashkeel=entry.tashkeel,
        nearest_book_ar=entry.ar,
        nearest_book_en=entry.en,
        nearest_distance=0,
        script="ar" if is_arabic(surface) else "en",
    )


def infer_token(surface: str) -> Optional[InferredName]:
    """Infer one token. Returns None only for empty input."""
    if not surface or not surface.strip():
        return None
    token = surface.strip()

    entry = lookup(token)
    if entry is not None:
        return _from_book(entry, token)

    model = _load_model()
    arabic = is_arabic(token)
    script = "ar" if arabic else "en"

    nearest = _nearest(token)
    nearest_ar = nearest[0].ar if nearest else None
    nearest_en = nearest[0].en if nearest else None
    nearest_d = nearest[1] if nearest else None

    gender, g_conf = "unknown", 0.0
    religion, r_conf = "unknown", 0.0
    role, role_conf = "unknown", 0.0

    # A distance-1 neighbour is usually a typo of a real lemma.
    if arabic:
        ar, en = token, romanize_ar(token)
    else:
        en, ar = token, arabize_en(token)
    classify_on = ar

    if nearest is not None and nearest_d == 1 and nearest[0].role == NameRole.GIVEN:
        nb = nearest[0]
        gender, g_conf = nb.gender.value, 0.78
        religion, r_conf = nb.religion.value, 0.72
        role, role_conf = nb.role.value, 0.80
    else:
        rg = _rule_gender(classify_on)
        if rg:
            gender, g_conf = rg
        else:
            gp = _predict(classify_on, model["gender"])
            best_g = max(gp, key=gp.get)
            if gp[best_g] >= _GENDER_MIN_P:
                gender, g_conf = best_g, gp[best_g]

        rr = _rule_religion(classify_on)
        if rr:
            religion, r_conf = rr
        else:
            rp = _predict(classify_on, model["religion"])
            if rp.get("christian", 0.0) >= _CHRISTIAN_MIN_P and rp["christian"] >= rp.get("muslim", 0):
                religion, r_conf = "christian", rp["christian"]
            elif rp.get("muslim", 0.0) >= _MUSLIM_MIN_P and rp["muslim"] >= rp.get("christian", 0):
                religion, r_conf = "muslim", rp["muslim"]

        rrole = _rule_role(classify_on)
        if rrole:
            role, role_conf = rrole
        else:
            rop = _predict(classify_on, model["role"])
            best_ro = max(rop, key=rop.get)
            if rop[best_ro] >= _ROLE_MIN_P:
                role, role_conf = best_ro, rop[best_ro]

    tashkeel = None
    if nearest is not None and nearest_d is not None and nearest_d <= 1:
        if normalize_ar(ar) == normalize_ar(nearest[0].ar):
            tashkeel = nearest[0].tashkeel

    if nearest is not None and nearest_d == 1:
        note = _NOTE_NEAREST.format(ar=nearest_ar, en=nearest_en)
    else:
        note = _NOTE_INFERRED

    return InferredName(
        surface=token,
        inferred=True,
        source="model",
        note=note,
        is_valid=False,
        ar=ar,
        en=en,
        gender=gender,
        gender_confidence=g_conf,
        religion=religion,
        religion_confidence=r_conf,
        role=role,
        role_confidence=role_conf,
        tashkeel=tashkeel,
        nearest_book_ar=nearest_ar,
        nearest_book_en=nearest_en,
        nearest_distance=nearest_d,
        script=script,
    )


def infer(name: str) -> Optional[Union[InferredName, List[Optional[InferredName]]]]:
    """Fallback for a name the book does not have.

    One token → one result. Several tokens → one result each.
    Empty → None. A book hit is marked source=book, not inferred.
    """
    if not name or not name.strip():
        return None
    tokens = name.strip().split()
    if len(tokens) == 1:
        return infer_token(tokens[0])
    return [infer_token(t) for t in tokens]
