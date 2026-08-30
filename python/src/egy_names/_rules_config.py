"""Loader for the shared, cross-SDK rule config.

``data/logic_config.json`` (synced by scripts/sync-catalog.sh, same as
names.json.gz) is the single source of truth for every threshold and
rule list that used to be hardcoded per language: non-personal
surfaces, low-confidence detection, ML abstention thresholds, and the
gender/religion/role prefix-suffix rule tables. Only pure algorithms
(compound-token lookahead, first-personal-token-wins, corpus-share
tie-break) stay as code, because they cannot be expressed as data.

If the config file is missing or malformed, fall back to the values
last known correct from this session's audits, so the library never
hard-fails on a packaging mistake — but log-free, since this is a
library, not an app with a logger configured.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Tuple

_CONFIG_PATH = Path(__file__).parent / "data" / "logic_config.json"

_FALLBACK: Dict[str, Any] = {
    "quality": {
        "non_personal_ar": [
            "الله", "الرجل", "الرجال", "شربه", "لافندي", "لفندي", "ماء", "البيت",
        ],
        "uncertain_meaning_markers": [
            "غير واضح", "لا يوجد معنى", "غير معروف",
            "قد يكون تحريف", "تحريفاً", "تحريفًا",
        ],
        "low_confidence_share_epsilon": 0.0001,
        "kunya_exempt_prefixes": ["أبو", "ابو", "أم", "ام"],
    },
    "infer_thresholds": {
        "gender_min_p": 0.70,
        "muslim_min_p": 0.85,
        "christian_min_p": 0.90,
        "role_min_p": 0.88,
    },
    "infer_rules": {"gender": [], "religion": [], "role": []},
}

_config: Dict[str, Any] = {}


def _load() -> Dict[str, Any]:
    global _config
    if _config:
        return _config
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            _config = json.load(f)
    except (OSError, json.JSONDecodeError, KeyError):
        _config = _FALLBACK
    return _config


def non_personal_ar() -> FrozenSet[str]:
    return frozenset(_load().get("quality", {}).get("non_personal_ar", []))


def uncertain_meaning_markers() -> Tuple[str, ...]:
    return tuple(_load().get("quality", {}).get("uncertain_meaning_markers", []))


def low_confidence_share_epsilon() -> float:
    return float(_load().get("quality", {}).get("low_confidence_share_epsilon", 0.0001))


def kunya_exempt_prefixes() -> Tuple[str, ...]:
    return tuple(_load().get("quality", {}).get("kunya_exempt_prefixes", []))


def infer_thresholds() -> Dict[str, float]:
    return _load().get("infer_thresholds", _FALLBACK["infer_thresholds"])


def infer_rules(kind: str) -> List[Dict[str, Any]]:
    """Rule table for 'gender' | 'religion' | 'role'."""
    return _load().get("infer_rules", {}).get(kind, [])


def _as_list(v: Any) -> List[str]:
    if v is None:
        return []
    return [v] if isinstance(v, str) else list(v)


def match_rule(rule: Dict[str, Any], surface: str, normalized: str) -> bool:
    """Evaluate one rule against a token.

    prefix/suffix test the normalized form; contains tests the raw
    surface (diacritics-sensitive, matching the original hand-written
    checks this config replaced). match='all' requires every listed
    condition; default ('any') requires just one.
    """
    conditions: List[bool] = []
    for p in _as_list(rule.get("prefix")):
        conditions.append(normalized.startswith(p))
    for s in _as_list(rule.get("suffix")):
        conditions.append(normalized.endswith(s))
    for c in _as_list(rule.get("contains")):
        conditions.append(c in surface)
    if not conditions:
        return False
    return all(conditions) if rule.get("match") == "all" else any(conditions)
