<?php

declare(strict_types=1);

namespace Afify\FakerEgyNames;

/**
 * Personal-name quality gate — same semantics as php/egy-names's Quality,
 * python/src/egy_names/_quality.py's is_generatable_entry, and the
 * generate()-side filter in every other egy-names SDK.
 *
 * The generate catalog otherwise contains a handful of non-personal
 * tokens ("الله", "البيت", ...), malformed compounds ("د الدين", glued
 * three-name chains), and low-confidence filler rows. None of those
 * are a real person's name and generate() must never emit them.
 */
final class Quality
{
    /** @var array<string, mixed>|null */
    private static ?array $config = null;

    /** @var array<string, true>|null keyed by 'a' across the whole catalog */
    private static ?array $arLookup = null;

    /**
     * @param list<array{a: string, e: string, g: string, r: string, l: string, fc: string, ma?: string, p: list<float>, tp: float}> $entry
     */
    public static function isGeneratableEntry(array $entry): bool
    {
        $ar = trim($entry['a']);

        return !self::isNonPersonal($ar)
            && !self::isLowConfidence($entry)
            && !str_contains($ar, ' ');
    }

    private static function isNonPersonal(string $ar): bool
    {
        return in_array($ar, self::config()['quality']['non_personal_ar'], true);
    }

    /**
     * @param array{a: string, ma?: string, tp: float} $entry
     */
    private static function isLowConfidence(array $entry): bool
    {
        if (self::isMalformedCompound($entry)) {
            return true;
        }
        $epsilon = self::config()['quality']['low_confidence_share_epsilon'];
        if (($entry['tp'] ?? 0.0) > $epsilon) {
            return false;
        }
        $meaning = $entry['ma'] ?? '';
        foreach (self::config()['quality']['uncertain_meaning_markers'] as $marker) {
            if ($marker !== '' && str_contains($meaning, $marker)) {
                return true;
            }
        }
        return false;
    }

    /**
     * True if a multi-word lemma's first half is not a real name.
     *
     * Well-formed two-word lemmas are either a kunya ("أبو" + element) or
     * a name plus a compound. Everything else at the corpus noise floor
     * whose first token does not independently resolve is a corrupted row.
     *
     * @param array{a: string, tp: float} $entry
     */
    private static function isMalformedCompound(array $entry): bool
    {
        $ar = trim($entry['a']);
        if (!str_contains($ar, ' ')) {
            return false;
        }
        $epsilon = self::config()['quality']['low_confidence_share_epsilon'];
        if (($entry['tp'] ?? 0.0) > $epsilon) {
            return false;
        }

        $parts = preg_split('/\s+/u', $ar) ?: [];
        $first = $parts[0] ?? '';

        if (in_array($first, self::config()['quality']['kunya_exempt_prefixes'], true)) {
            return false;
        }

        return !isset(self::arLookup()[$first]);
    }

    /**
     * @return array<string, true>
     */
    private static function arLookup(): array
    {
        if (self::$arLookup === null) {
            self::$arLookup = [];
            foreach (Catalog::names() as $entry) {
                self::$arLookup[trim($entry['a'])] = true;
            }
        }
        return self::$arLookup;
    }

    /**
     * @return array<string, mixed>
     */
    private static function config(): array
    {
        if (self::$config !== null) {
            return self::$config;
        }

        $fallback = [
            'quality' => [
                'non_personal_ar' => [
                    'الله', 'الرجل', 'الرجال', 'شربه', 'لافندي', 'لفندي', 'ماء', 'البيت',
                ],
                'uncertain_meaning_markers' => [
                    'غير واضح', 'لا يوجد معنى', 'غير معروف',
                    'قد يكون تحريف', 'تحريفاً', 'تحريفًا',
                ],
                'low_confidence_share_epsilon' => 0.0001,
                'kunya_exempt_prefixes' => ['أبو', 'ابو', 'أم', 'ام'],
            ],
        ];

        $path = dirname(__DIR__) . '/data/logic_config.json';
        $raw = @file_get_contents($path);
        if ($raw === false) {
            self::$config = $fallback;
            return self::$config;
        }

        $decoded = json_decode($raw, true);
        if (!is_array($decoded) || !isset($decoded['quality']) || !is_array($decoded['quality'])) {
            self::$config = $fallback;
            return self::$config;
        }

        self::$config = $decoded;
        return self::$config;
    }
}
