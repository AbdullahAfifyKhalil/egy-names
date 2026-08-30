"""Personal-name quality gate.

The book keeps some surface tokens so split and compounds still resolve.
Those tokens are not a person's name. Production APIs must not treat them
as one.
"""

from __future__ import annotations

from typing import FrozenSet

from ._types import NameEntry, NameRole
from . import _rules_config as _cfg

# Proven non-names from the 100-lemma labeling review, plus their twins.
# Kept in the index. Excluded from is_valid, generate, and detect.
# Sourced from data/logic_config.json — every SDK reads the same list.
NON_PERSONAL_AR: FrozenSet[str] = _cfg.non_personal_ar()


def is_personal_entry(entry: NameEntry) -> bool:
    """True if this lemma may stand as a person's name."""
    return entry.ar not in NON_PERSONAL_AR


# Phrases the catalog itself uses when a lemma's authenticity is
# uncertain (likely a typo, a dialectal one-off, or an unverified
# guess rather than an attested Egyptian name). Also from the shared config.
_UNCERTAIN_MEANING_MARKERS = _cfg.uncertain_meaning_markers()


def is_low_confidence_entry(entry: NameEntry) -> bool:
    """True if this lemma is likely a fabricated/unverified filler row.

    Zero real-world corpus share on its own just means "rare" — plenty
    of genuine names are rare. But zero share *combined with* the
    catalog's own gloss admitting the name's meaning or origin is
    unclear is a strong signal the row was never attested, only
    guessed to fill out a role/pattern. Those rows should not surface
    from is_valid, generate, or the detectors.
    """
    # "tp" (total corpus percentage) at this floor is a couple of raw
    # hits out of tens of millions of records — noise, not attestation.
    # Real rare surnames (e.g. Farghal, Dogheidy, El-Sisi) sit an order
    # of magnitude above this even when their gloss also hedges on
    # etymology, so the threshold stays tight on purpose.
    if is_malformed_compound(entry):
        return True
    if entry.corpus_share > _cfg.low_confidence_share_epsilon():
        return False
    meaning = entry.meaning_ar or ""
    return any(marker in meaning for marker in _UNCERTAIN_MEANING_MARKERS)


def is_malformed_compound(entry: NameEntry) -> bool:
    """True if a multi-word lemma's first half is not a real name.

    A well-formed two-word lemma is either a kunya ("أبو" + element) or
    a name plus a compound ("احمد سعدالدين"). What is left after the
    spacing fixes are corrupted rows: truncated fragments ("د الدين"),
    doubled-letter typos ("عببد الله"), and three-name chains glued into
    two words ("محمدسميرسعد الدين"). Their first half resolves to
    nothing, and they all sit at the corpus noise floor. Cheap to
    detect structurally, so no hardcoded blocklist.
    """
    ar = entry.ar.strip()
    if " " not in ar:
        return False
    if entry.corpus_share > _cfg.low_confidence_share_epsilon():
        return False
    first = ar.split()[0]
    # "أبو"/"ابو" kunya lemmas are well-formed by construction even
    # when the element after them is not an independent name.
    if first in _cfg.kunya_exempt_prefixes():
        return False
    from ._index import lookup_ar

    return lookup_ar(first) is None


def is_generatable_entry(entry: NameEntry) -> bool:
    """True if generate may emit this lemma as one token."""
    return (
        is_personal_entry(entry)
        and not is_low_confidence_entry(entry)
        and " " not in entry.ar.strip()
    )


def is_lineage_role(entry: NameEntry) -> bool:
    """Family and tribal tokens are lineage, not the person."""
    return entry.role in (NameRole.FAMILY, NameRole.TRIBAL)
