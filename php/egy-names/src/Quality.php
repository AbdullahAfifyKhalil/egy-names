<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * Personal-name quality gate.
 *
 * The book keeps some surface tokens so split and compounds still resolve.
 * Those tokens are not a person's name. Production APIs must not treat them
 * as one.
 */
final class Quality
{
    /** @var list<string>|null */
    private static ?array $nonPersonalAr = null;

    /** @var list<string>|null */
    private static ?array $uncertainMeaningMarkers = null;

    /** @var list<string>|null */
    private static ?array $kunyaExemptPrefixes = null;

    /**
     * @return list<string>
     */
    public static function nonPersonalAr(): array
    {
        if (self::$nonPersonalAr === null) {
            self::$nonPersonalAr = RulesConfig::nonPersonalAr();
        }
        return self::$nonPersonalAr;
    }

    /** True if this lemma may stand as a person's name. */
    public static function isPersonal(NameEntry $entry): bool
    {
        return !in_array($entry->ar, self::nonPersonalAr(), true);
    }

    /** Alias kept for readability at call sites that mirror the Python API name. */
    public static function isPersonalEntry(NameEntry $entry): bool
    {
        return self::isPersonal($entry);
    }

    /**
     * True if this lemma is likely a fabricated/unverified filler row.
     *
     * Zero real-world corpus share on its own just means "rare" — plenty
     * of genuine names are rare. But zero share combined with the
     * catalog's own gloss admitting the name's meaning or origin is
     * unclear is a strong signal the row was never attested, only
     * guessed to fill out a role/pattern. Those rows should not surface
     * from isValid, generate, or the detectors.
     */
    public static function isLowConfidenceEntry(NameEntry $entry): bool
    {
        if (self::isMalformedCompound($entry)) {
            return true;
        }
        if ($entry->corpusShare > RulesConfig::lowConfidenceShareEpsilon()) {
            return false;
        }
        if (self::$uncertainMeaningMarkers === null) {
            self::$uncertainMeaningMarkers = RulesConfig::uncertainMeaningMarkers();
        }
        $meaning = $entry->meaningAr ?? '';
        foreach (self::$uncertainMeaningMarkers as $marker) {
            if ($marker !== '' && str_contains($meaning, $marker)) {
                return true;
            }
        }
        return false;
    }

    /**
     * True if a multi-word lemma's first half is not a real name.
     *
     * A well-formed two-word lemma is either a kunya ("أبو" + element) or
     * a name plus a compound ("احمد سعدالدين"). What is left after the
     * spacing fixes are corrupted rows: truncated fragments ("د الدين"),
     * doubled-letter typos ("عببد الله"), and three-name chains glued into
     * two words ("محمدسميرسعد الدين"). Their first half resolves to
     * nothing, and they all sit at the corpus noise floor. Cheap to
     * detect structurally, so no hardcoded blocklist.
     */
    public static function isMalformedCompound(NameEntry $entry): bool
    {
        $ar = trim($entry->ar);
        if (!str_contains($ar, ' ')) {
            return false;
        }
        if ($entry->corpusShare > RulesConfig::lowConfidenceShareEpsilon()) {
            return false;
        }

        $parts = preg_split('/\s+/u', $ar) ?: [];
        $first = $parts[0] ?? '';

        if (self::$kunyaExemptPrefixes === null) {
            self::$kunyaExemptPrefixes = RulesConfig::kunyaExemptPrefixes();
        }
        // "أبو"/"ابو" kunya lemmas are well-formed by construction even
        // when the element after them is not an independent name.
        if (in_array($first, self::$kunyaExemptPrefixes, true)) {
            return false;
        }

        return Lookup::lookupAr($first) === null;
    }

    /** True if generate may emit this lemma as one token. */
    public static function isGeneratable(NameEntry $entry): bool
    {
        return self::isGeneratableEntry($entry);
    }

    /** True if generate may emit this lemma as one token. */
    public static function isGeneratableEntry(NameEntry $entry): bool
    {
        return self::isPersonal($entry)
            && !self::isLowConfidenceEntry($entry)
            && !str_contains(trim($entry->ar), ' ');
    }

    /** Family and tribal tokens are lineage, not the person. */
    public static function isLineage(NameEntry $entry): bool
    {
        return $entry->role->isFamilyLike();
    }
}
