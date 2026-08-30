<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * Loader for the shared, cross-SDK rule config.
 *
 * data/logic_config.json (synced by scripts/sync-catalog.sh, same as
 * names.json.gz) is the single source of truth for every threshold and
 * rule list that used to be hardcoded per language. Only pure algorithms
 * (compound-token lookahead, first-personal-token-wins, corpus-share
 * tie-break) stay as code, because they cannot be expressed as data.
 *
 * If the config file is missing or malformed, fall back to the values
 * last known correct from this session's audits, so the library never
 * hard-fails on a packaging mistake.
 */
final class RulesConfig
{
    /** @var array<string, mixed>|null */
    private static ?array $config = null;

    /** @var array<string, mixed> */
    private const FALLBACK = [
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
        'infer_thresholds' => [
            'gender_min_p' => 0.70,
            'muslim_min_p' => 0.85,
            'christian_min_p' => 0.90,
            'role_min_p' => 0.88,
        ],
        'infer_rules' => ['gender' => [], 'religion' => [], 'role' => []],
    ];

    /**
     * @return array<string, mixed>
     */
    private static function load(): array
    {
        if (self::$config !== null) {
            return self::$config;
        }

        $path = dirname(__DIR__) . '/data/logic_config.json';
        $raw = @file_get_contents($path);
        if ($raw === false) {
            self::$config = self::FALLBACK;
            return self::$config;
        }

        $decoded = json_decode($raw, true);
        if (!is_array($decoded)) {
            self::$config = self::FALLBACK;
            return self::$config;
        }

        self::$config = $decoded;
        return self::$config;
    }

    /**
     * @return list<string>
     */
    public static function nonPersonalAr(): array
    {
        $v = self::load()['quality']['non_personal_ar'] ?? self::FALLBACK['quality']['non_personal_ar'];
        return is_array($v) ? array_values($v) : self::FALLBACK['quality']['non_personal_ar'];
    }

    /**
     * @return list<string>
     */
    public static function uncertainMeaningMarkers(): array
    {
        $v = self::load()['quality']['uncertain_meaning_markers']
            ?? self::FALLBACK['quality']['uncertain_meaning_markers'];
        return is_array($v) ? array_values($v) : self::FALLBACK['quality']['uncertain_meaning_markers'];
    }

    public static function lowConfidenceShareEpsilon(): float
    {
        $v = self::load()['quality']['low_confidence_share_epsilon']
            ?? self::FALLBACK['quality']['low_confidence_share_epsilon'];
        return is_numeric($v) ? (float) $v : self::FALLBACK['quality']['low_confidence_share_epsilon'];
    }

    /**
     * @return list<string>
     */
    public static function kunyaExemptPrefixes(): array
    {
        $v = self::load()['quality']['kunya_exempt_prefixes'] ?? self::FALLBACK['quality']['kunya_exempt_prefixes'];
        return is_array($v) ? array_values($v) : self::FALLBACK['quality']['kunya_exempt_prefixes'];
    }

    /**
     * @return array<string, float>
     */
    public static function inferThresholds(): array
    {
        $v = self::load()['infer_thresholds'] ?? self::FALLBACK['infer_thresholds'];
        return is_array($v) ? $v : self::FALLBACK['infer_thresholds'];
    }

    /**
     * Rule table for 'gender' | 'religion' | 'role'.
     *
     * @return list<array<string, mixed>>
     */
    public static function inferRules(string $kind): array
    {
        $v = self::load()['infer_rules'][$kind] ?? [];
        return is_array($v) ? array_values($v) : [];
    }
}
