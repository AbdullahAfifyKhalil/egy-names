<?php

declare(strict_types=1);

namespace Afify\FakerEgyNames;

/**
 * Lazy loader for the generate-only lemma catalog (egy-names 0.3.6).
 */
final class Catalog
{
    /** @var list<array{a: string, e: string, g: string, r: string, l: string, fc: string, p: list<float>, tp: float}>|null */
    private static ?array $names = null;

    /**
     * @return list<array{a: string, e: string, g: string, r: string, l: string, fc: string, p: list<float>, tp: float}>
     */
    public static function names(): array
    {
        if (self::$names !== null) {
            return self::$names;
        }

        $limit = (string) ini_get('memory_limit');
        if ($limit !== '-1') {
            $n = (int) $limit;
            if (preg_match('/^(\d+)\s*([KMG])?$/i', $limit, $m)) {
                $n = (int) $m[1];
                $n *= match (strtoupper($m[2] ?? '')) {
                    'G' => 1024 * 1024 * 1024,
                    'M' => 1024 * 1024,
                    'K' => 1024,
                    default => 1,
                };
            }
            if ($n > 0 && $n < 1024 * 1024 * 1024) {
                ini_set('memory_limit', '1024M');
            }
        }

        $path = dirname(__DIR__) . '/data/names.json.gz';
        $raw = @file_get_contents($path);
        if ($raw === false) {
            throw new \RuntimeException('egy-names generate catalog is missing: ' . $path);
        }
        $json = gzdecode($raw);
        if ($json === false) {
            throw new \RuntimeException('egy-names generate catalog is not valid gzip');
        }
        unset($raw);
        $bundle = json_decode($json, true, 512, JSON_THROW_ON_ERROR);
        unset($json);
        if (!isset($bundle['names']) || !is_array($bundle['names'])) {
            throw new \RuntimeException('egy-names generate catalog has no names');
        }

        self::$names = $bundle['names'];
        return self::$names;
    }
}
