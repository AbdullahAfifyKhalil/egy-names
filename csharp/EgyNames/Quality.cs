using System.Collections.Generic;
using System.Linq;

namespace EgyptianNames
{
    /// <summary>
    /// Personal-name quality gate.
    ///
    /// The book keeps some surface tokens so split and compounds still resolve.
    /// Those tokens are not a person's name. Production APIs must not treat them
    /// as one.
    /// </summary>
    public static class Quality
    {
        /// <summary>
        /// Proven non-names from the 100-lemma labeling review, plus their twins.
        /// Kept in the index. Excluded from IsValid, Generate, and detect.
        /// Sourced from data/logic_config.json — every SDK reads the same list.
        /// </summary>
        public static HashSet<string> NonPersonalAr => RulesConfig.NonPersonalAr;

        /// <summary>True if this lemma may stand as a person's name.</summary>
        public static bool IsPersonalEntry(NameEntry? entry) =>
            entry != null && !NonPersonalAr.Contains(entry.Ar);

        /// <summary>
        /// True if this lemma is likely a fabricated/unverified filler row.
        ///
        /// Zero real-world corpus share on its own just means "rare" — plenty of
        /// genuine names are rare. But zero share *combined with* the catalog's
        /// own gloss admitting the name's meaning or origin is unclear is a
        /// strong signal the row was never attested, only guessed to fill out a
        /// role/pattern. Those rows should not surface from IsValid, Generate,
        /// or the detectors.
        /// </summary>
        public static bool IsLowConfidenceEntry(NameEntry? entry)
        {
            if (entry == null) return false;
            if (IsMalformedCompound(entry)) return true;
            if (entry.CorpusShare > RulesConfig.LowConfidenceShareEpsilon) return false;
            var meaning = entry.MeaningAr ?? string.Empty;
            return RulesConfig.UncertainMeaningMarkers.Any(marker => meaning.Contains(marker));
        }

        /// <summary>
        /// True if a multi-word lemma's first half is not a real name.
        ///
        /// A well-formed two-word lemma is either a kunya ("أبو" + element) or a
        /// name plus a compound ("احمد سعدالدين"). What is left after the
        /// spacing fixes are corrupted rows: truncated fragments ("د الدين"),
        /// doubled-letter typos ("عببد الله"), and three-name chains glued into
        /// two words ("محمدسميرسعد الدين"). Their first half resolves to
        /// nothing, and they all sit at the corpus noise floor. Cheap to detect
        /// structurally, so no hardcoded blocklist.
        /// </summary>
        public static bool IsMalformedCompound(NameEntry? entry)
        {
            if (entry == null) return false;
            var ar = entry.Ar.Trim();
            if (!ar.Contains(" ")) return false;
            if (entry.CorpusShare > RulesConfig.LowConfidenceShareEpsilon) return false;

            var first = ar.Split(' ')[0];
            // "أبو"/"ابو" kunya lemmas are well-formed by construction even
            // when the element after them is not an independent name.
            if (RulesConfig.KunyaExemptPrefixes.Contains(first)) return false;

            return LookupIndices.LookupAr(first) == null;
        }

        /// <summary>True if generate may emit this lemma as one token.</summary>
        public static bool IsGeneratableEntry(NameEntry? entry) =>
            entry != null
            && IsPersonalEntry(entry)
            && !IsLowConfidenceEntry(entry)
            && !entry.Ar.Trim().Contains(" ");

        /// <summary>Family and tribal tokens are lineage, not the person.</summary>
        public static bool IsLineageRole(NameEntry? entry) =>
            entry != null && entry.Role == NameRole.Family;

        // Backwards-compatible aliases kept for existing call sites.
        public static bool IsPersonal(NameEntry? entry) => IsPersonalEntry(entry);
        public static bool IsGeneratable(NameEntry? entry) => IsGeneratableEntry(entry);
        public static bool IsLineage(NameEntry? entry) => IsLineageRole(entry);
    }
}
