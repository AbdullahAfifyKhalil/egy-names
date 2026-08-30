/// Personal-name quality gate.
///
/// The book keeps some surface tokens so split and compounds still resolve.
/// Those tokens are not a person's name. Production APIs must not treat them
/// as one.
library;

import 'lookup_indices.dart';
import 'rules_config.dart';
import 'types.dart';

/// Proven non-names from the 100-lemma labeling review, plus their twins.
/// Kept in the index. Excluded from isValid, generate, and detect.
/// Sourced from data/logic_config.json — every SDK reads the same list.
Set<String> get nonPersonalAr => RulesConfigLoader.load().nonPersonalAr;

/// True if this lemma may stand as a person's name.
bool isPersonalEntry(NameEntry entry) => !nonPersonalAr.contains(entry.ar);

/// Phrases the catalog itself uses when a lemma's authenticity is
/// uncertain (likely a typo, a dialectal one-off, or an unverified
/// guess rather than an attested Egyptian name). Also from the shared config.
List<String> get _uncertainMeaningMarkers =>
    RulesConfigLoader.load().uncertainMeaningMarkers;

/// True if this lemma is likely a fabricated/unverified filler row.
///
/// Zero real-world corpus share on its own just means "rare" — plenty
/// of genuine names are rare. But zero share *combined with* the
/// catalog's own gloss admitting the name's meaning or origin is
/// unclear is a strong signal the row was never attested, only
/// guessed to fill out a role/pattern. Those rows should not surface
/// from isValid, generate, or the detectors.
bool isLowConfidenceEntry(NameEntry entry) {
  // "tp" (total corpus percentage) at this floor is a couple of raw
  // hits out of tens of millions of records — noise, not attestation.
  // Real rare surnames sit an order of magnitude above this even when
  // their gloss also hedges on etymology, so the threshold stays tight
  // on purpose.
  if (isMalformedCompound(entry)) return true;
  if (entry.corpusShare > RulesConfigLoader.load().lowConfidenceShareEpsilon) {
    return false;
  }
  final meaning = entry.meaningAr;
  return _uncertainMeaningMarkers.any((marker) => meaning.contains(marker));
}

/// True if a multi-word lemma's first half is not a real name.
///
/// A well-formed two-word lemma is either a kunya ("أبو" + element) or
/// a name plus a compound ("احمد سعدالدين"). What is left after the
/// spacing fixes are corrupted rows: truncated fragments, doubled-letter
/// typos, and three-name chains glued into two words. Their first half
/// resolves to nothing, and they all sit at the corpus noise floor.
/// Cheap to detect structurally, so no hardcoded blocklist.
bool isMalformedCompound(NameEntry entry) {
  final ar = entry.ar.trim();
  if (!ar.contains(' ')) return false;
  if (entry.corpusShare > RulesConfigLoader.load().lowConfidenceShareEpsilon) {
    return false;
  }
  final first = ar.split(RegExp(r'\s+')).first;
  // "أبو"/"ابو" kunya lemmas are well-formed by construction even
  // when the element after them is not an independent name.
  if (RulesConfigLoader.load().kunyaExemptPrefixes.contains(first)) {
    return false;
  }
  return LookupIndices.lookupAr(first) == null;
}

/// True if generate may emit this lemma as one token.
bool isGeneratableEntry(NameEntry entry) =>
    isPersonalEntry(entry) &&
    !isLowConfidenceEntry(entry) &&
    !entry.ar.trim().contains(' ');

/// Family and tribal tokens are lineage, not the person.
bool isLineageRole(NameEntry entry) => entry.role == NameRole.family;
