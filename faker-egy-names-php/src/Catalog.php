<?php

declare(strict_types=1);

namespace Afify\FakerEgyNames;

/**
 * Lazy loader for the generate-only lemma catalog (egy-names 0.3.2).
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

        $path = dirname(__DIR__) . '/data/names.json.gz';
        $raw = @file_get_contents($path);
        if ($raw === false) {
            throw new \RuntimeException('egy-names generate catalog is missing: ' . $path);
        }
        $json = gzdecode($raw);
        if ($json === false) {
            throw new \RuntimeException('egy-names generate catalog is not valid gzip');
        }
        $bundle = json_decode($json, true, 512, JSON_THROW_ON_ERROR);
        if (!isset($bundle['names']) || !is_array($bundle['names'])) {
            throw new \RuntimeException('egy-names generate catalog has no names');
        }

        self::$names = $bundle['names'];
        return self::$names;
    }
}
