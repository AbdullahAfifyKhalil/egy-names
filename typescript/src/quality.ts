import { NameEntry, NameRole } from "./types";
import { lookupAr } from "./lookupIndices";
import {
  kunyaExemptPrefixes,
  lowConfidenceShareEpsilon,
  nonPersonalAr,
  uncertainMeaningMarkers,
} from "./rulesConfig";

/**
 * Personal-name quality gate.
 *
 * The book keeps some surface tokens so split and compounds still resolve.
 * Those tokens are not a person's name. Production APIs must not treat
 * them as one.
 */

/**
 * Proven non-names from the 100-lemma labeling review, plus their twins.
 * Kept in the index. Excluded from isValid, generate, and detect.
 * Sourced from data/logic_config.json — every SDK reads the same list.
 */
export const NON_PERSONAL_AR: Set<string> = nonPersonalAr();

export function isPersonalEntry(entry: NameEntry): boolean {
  return !NON_PERSONAL_AR.has(entry.ar);
}

/**
 * True if a multi-word lemma's first half is not a real name.
 *
 * A well-formed two-word lemma is either a kunya ("أبو" + element) or a
 * name plus a compound ("احمد سعدالدين"). What is left after the spacing
 * fixes are corrupted rows: truncated fragments, doubled-letter typos,
 * and multi-name chains glued into two words. Their first half resolves
 * to nothing, and they all sit at the corpus noise floor. Cheap to
 * detect structurally, so no hardcoded blocklist.
 */
export function isMalformedCompound(entry: NameEntry): boolean {
  const ar = entry.ar.trim();
  if (!ar.includes(" ")) return false;
  if (entry.corpusShare > lowConfidenceShareEpsilon()) return false;
  const first = ar.split(/\s+/)[0];
  // "أبو"/"ابو" kunya lemmas are well-formed by construction even when
  // the element after them is not an independent name.
  if (kunyaExemptPrefixes().includes(first)) return false;
  return lookupAr(first) === undefined;
}

/**
 * True if this lemma is likely a fabricated/unverified filler row.
 *
 * Zero real-world corpus share on its own just means "rare" — plenty of
 * genuine names are rare. But zero share *combined with* the catalog's
 * own gloss admitting the name's meaning or origin is unclear is a
 * strong signal the row was never attested, only guessed to fill out a
 * role/pattern. Those rows should not surface from isValid, generate,
 * or the detectors.
 */
export function isLowConfidenceEntry(entry: NameEntry): boolean {
  if (isMalformedCompound(entry)) return true;
  // "tp" (total corpus percentage) at this floor is a couple of raw
  // hits out of tens of millions of records — noise, not attestation.
  if (entry.corpusShare > lowConfidenceShareEpsilon()) return false;
  const meaning = entry.meaningAr || "";
  return uncertainMeaningMarkers().some((marker) => meaning.includes(marker));
}

export function isGeneratableEntry(entry: NameEntry): boolean {
  return (
    isPersonalEntry(entry) &&
    !isLowConfidenceEntry(entry) &&
    !entry.ar.trim().includes(" ")
  );
}

export function isLineageRole(entry: NameEntry): boolean {
  return entry.role === NameRole.FAMILY;
}
