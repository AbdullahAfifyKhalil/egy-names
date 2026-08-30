package com.afify.egynames.index;

import com.afify.egynames.model.Models;

import java.util.List;
import java.util.Set;

/**
 * Personal-name quality gate.
 *
 * <p>The book keeps some surface tokens so split and compounds still resolve.
 * Those tokens are not a person's name. Production APIs must not treat them
 * as one. Mirrors {@code python/src/egy_names/_quality.py}.
 */
public final class Quality {

    private Quality() {}

    /** True if this lemma may stand as a person's name. */
    public static boolean isPersonalEntry(Models.NameEntry entry) {
        return entry != null && !RulesConfig.nonPersonalAr().contains(entry.ar);
    }

    /**
     * True if this lemma is likely a fabricated/unverified filler row.
     *
     * <p>Zero real-world corpus share on its own just means "rare" — plenty
     * of genuine names are rare. But zero share combined with the catalog's
     * own gloss admitting the name's meaning/origin is unclear is a strong
     * signal the row was never attested, only guessed.
     */
    public static boolean isLowConfidenceEntry(Models.NameEntry entry) {
        if (entry == null) return true;
        if (isMalformedCompound(entry)) return true;
        if (entry.corpusShare > RulesConfig.lowConfidenceShareEpsilon()) return false;
        String meaning = entry.meaningAr != null ? entry.meaningAr : "";
        for (String marker : RulesConfig.uncertainMeaningMarkers()) {
            if (meaning.contains(marker)) return true;
        }
        return false;
    }

    /**
     * True if a multi-word lemma's first half is not a real name.
     *
     * <p>A well-formed two-word lemma is either a kunya ("أبو" + element) or
     * a name plus a compound. What is left after spacing fixes are corrupted
     * rows whose first half resolves to nothing, and they all sit at the
     * corpus noise floor.
     */
    public static boolean isMalformedCompound(Models.NameEntry entry) {
        if (entry == null || entry.ar == null) return false;
        String ar = entry.ar.trim();
        if (!ar.contains(" ")) return false;
        if (entry.corpusShare > RulesConfig.lowConfidenceShareEpsilon()) return false;
        String[] words = ar.split("\\s+");
        String first = words.length > 0 ? words[0] : "";
        if (RulesConfig.kunyaExemptPrefixes().contains(first)) return false;
        return LookupIndices.lookupAr(first, null) == null;
    }

    /** True if generate may emit this lemma as one token. */
    public static boolean isGeneratableEntry(Models.NameEntry entry) {
        return entry != null
                && isPersonalEntry(entry)
                && !isLowConfidenceEntry(entry)
                && !entry.ar.trim().contains(" ");
    }

    /** Family and tribal tokens are lineage, not the person. */
    public static boolean isLineageRole(Models.NameEntry entry) {
        return entry != null && entry.role == Models.NameRole.FAMILY;
    }
}
