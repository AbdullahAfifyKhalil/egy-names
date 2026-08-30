<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * The book is a 44k-lemma JSON tree. Default PHP memory_limit (128M)
 * cannot hold the decode. Raise the process limit to 1G when it is lower.
 * Leave unlimited (-1) and already-higher limits alone.
 */
final class Memory
{
    private const CATALOG_BYTES = 1024 * 1024 * 1024;

    public static function ensureCatalogBudget(): void
    {
        $raw = (string) ini_get('memory_limit');
        if ($raw === '-1') {
            return;
        }
        $bytes = self::toBytes($raw);
        if ($bytes >= 0 && $bytes < self::CATALOG_BYTES) {
            ini_set('memory_limit', '1024M');
        }
    }

    private static function toBytes(string $value): int
    {
        $value = trim($value);
        if ($value === '' || $value === '-1') {
            return -1;
        }
        if (!preg_match('/^(\d+)\s*([KMG])?$/i', $value, $m)) {
            return -1;
        }
        $n = (int) $m[1];
        return match (strtoupper($m[2] ?? '')) {
            'G' => $n * 1024 * 1024 * 1024,
            'M' => $n * 1024 * 1024,
            'K' => $n * 1024,
            default => $n,
        };
    }
}
