<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * Lazy gzip JSON catalog loader (full 0.3.6 book).
 */
final class Catalog
{
    /** @var array<string, mixed>|null */
    private static ?array $bundle = null;

    /** @var list<NameEntry>|null */
    private static ?array $entries = null;

    /**
     * @return array<string, mixed>
     */
    public static function bundle(): array
    {
        if (self::$bundle !== null) {
            return self::$bundle;
        }

        $path = dirname(__DIR__) . '/data/names.json.gz';
        $raw = @file_get_contents($path);
        if ($raw === false) {
            throw new \RuntimeException('egy-names catalog is missing: ' . $path);
        }
        $json = gzdecode($raw);
        if ($json === false) {
            throw new \RuntimeException('egy-names catalog is not valid gzip');
        }
        unset($raw);
        $bundle = json_decode($json, true, 512, JSON_THROW_ON_ERROR);
        unset($json);
        if (!is_array($bundle) || !isset($bundle['names']) || !is_array($bundle['names'])) {
            throw new \RuntimeException('egy-names catalog has no names');
        }

        $nested = is_array($bundle['metadata'] ?? null) ? $bundle['metadata'] : [];
        self::$bundle = [
            'version' => $nested['version'] ?? $bundle['version'] ?? '0.0.0',
            'corpus_tokens' => $nested['corpus_tokens'] ?? $bundle['corpus_tokens'] ?? 0,
            'corpus_students' => $nested['corpus_students'] ?? $bundle['corpus_students'] ?? 0,
            'cohort_years' => $nested['cohort_years'] ?? $bundle['cohort_years'] ?? [],
            'metadata' => $nested,
            'names' => $bundle['names'],
            'corrections' => is_array($bundle['corrections'] ?? null) ? $bundle['corrections'] : [],
        ];
        unset($bundle);
        return self::$bundle;
    }

    /**
     * @return list<NameEntry>
     */
    public static function entries(): array
    {
        if (self::$entries !== null) {
            return self::$entries;
        }
        $bundle = self::bundle();
        $entries = [];
        foreach ($bundle['names'] as $raw) {
            if (is_array($raw)) {
                $entries[] = NameEntry::fromRaw($raw);
            }
        }
        unset(self::$bundle['names']);
        self::$entries = $entries;
        return self::$entries;
    }

    /**
     * @return array<string, string>
     */
    public static function corrections(): array
    {
        $bundle = self::bundle();
        $corrections = $bundle['corrections'] ?? [];
        if (!is_array($corrections)) {
            return [];
        }
        $out = [];
        foreach ($corrections as $k => $v) {
            $out[(string) $k] = (string) $v;
        }
        return $out;
    }

    /**
     * @return array{version: string, corpus_tokens: int|float, corpus_students: int|float, cohort_years: list<mixed>}
     */
    public static function metadata(): array
    {
        $bundle = self::bundle();
        return [
            'version' => (string) ($bundle['version'] ?? '0.0.0'),
            'corpus_tokens' => $bundle['corpus_tokens'] ?? 0,
            'corpus_students' => $bundle['corpus_students'] ?? 0,
            'cohort_years' => is_array($bundle['cohort_years'] ?? null) ? $bundle['cohort_years'] : [],
        ];
    }

    public static function clearCache(): void
    {
        self::$bundle = null;
        self::$entries = null;
        Lookup::reset();
    }
}
