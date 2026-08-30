import Foundation

/// Personal-name quality gate.
///
/// The book keeps some surface tokens so split and compounds still resolve.
/// Those tokens are not a person's name. Production APIs must not treat them
/// as one. Mirrors `python/src/egy_names/_quality.py`.
enum Quality {
    /// Proven non-names from the 100-lemma labeling review, plus their twins.
    /// Kept in the index. Excluded from isValid, generate, and detect.
    /// Sourced from data/logic_config.json — every SDK reads the same list.
    static var nonPersonalAr: Set<String> {
        RulesConfig.nonPersonalAr
    }

    /// True if this lemma may stand as a person's name.
    static func isPersonalEntry(_ entry: NameEntry) -> Bool {
        !nonPersonalAr.contains(entry.ar)
    }

    /// True if this lemma is likely a fabricated/unverified filler row.
    ///
    /// Zero real-world corpus share on its own just means "rare" — plenty
    /// of genuine names are rare. But zero share *combined with* the
    /// catalog's own gloss admitting the name's meaning or origin is
    /// unclear is a strong signal the row was never attested, only
    /// guessed to fill out a role/pattern.
    static func isLowConfidenceEntry(_ entry: NameEntry) -> Bool {
        if isMalformedCompound(entry) {
            return true
        }
        if entry.corpusShare > RulesConfig.lowConfidenceShareEpsilon {
            return false
        }
        let meaning = entry.meaningAr
        return RulesConfig.uncertainMeaningMarkers.contains { meaning.contains($0) }
    }

    /// True if a multi-word lemma's first half is not a real name.
    ///
    /// A well-formed two-word lemma is either a kunya ("أبو" + element) or
    /// a name plus a compound ("احمد سعدالدين"). What is left after the
    /// spacing fixes are corrupted rows: truncated fragments, doubled-letter
    /// typos, and multi-name chains glued into two words. Their first half
    /// resolves to nothing, and they all sit at the corpus noise floor.
    static func isMalformedCompound(_ entry: NameEntry) -> Bool {
        let ar = entry.ar.trimmingCharacters(in: .whitespacesAndNewlines)
        guard ar.contains(" ") else { return false }
        if entry.corpusShare > RulesConfig.lowConfidenceShareEpsilon {
            return false
        }
        guard let first = ar.split(separator: " ").first.map(String.init) else {
            return false
        }
        // "أبو"/"ابو" kunya lemmas are well-formed by construction even
        // when the element after them is not an independent name.
        if RulesConfig.kunyaExemptPrefixes.contains(first) {
            return false
        }
        return LookupIndices.lookupAr(first) == nil
    }

    /// True if generate may emit this lemma as one token.
    static func isGeneratableEntry(_ entry: NameEntry) -> Bool {
        isPersonalEntry(entry)
            && !isLowConfidenceEntry(entry)
            && !entry.ar.trimmingCharacters(in: .whitespacesAndNewlines).contains(" ")
    }

    /// Family and tribal tokens are lineage, not the person.
    static func isLineageRole(_ entry: NameEntry) -> Bool {
        entry.role == .family
    }
}
