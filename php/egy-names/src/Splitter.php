<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * Port of typescript/src/splitter.ts — DP shortest-path segmentation.
 */
final class Splitter
{
    private const BASE_SEGMENT_COST = 1.0;
    private const UNKNOWN_PENALTY = 8.0;
    private const LENGTH_BONUS_PER_CHAR = -0.05;

    /** @var array<string, float> */
    private const FREQ_BONUS = [
        'c' => -0.6,
        'n' => -0.2,
        'r' => 0.0,
    ];

    /**
     * @return list<string>
     */
    public static function split(string $fullName): array
    {
        if (trim($fullName) === '') {
            return [];
        }

        $text = trim($fullName);
        if (str_contains($text, ' ')) {
            return preg_split('/\s+/u', $text) ?: [];
        }

        if (Lookup::isArabic($text)) {
            $entry = Lookup::lookup($text);
            if ($entry !== null) {
                return [$text];
            }
            return self::dpSegment($text);
        }

        return [$text];
    }

    /**
     * @return list<string>
     */
    private static function dpSegment(string $text): array
    {
        $arIndex = Lookup::getArForms();
        $arNorm = Lookup::getArNormForms();
        $chars = Lookup::chars($text);
        $n = count($chars);

        $inf = INF;
        $dp = array_fill(0, $n + 1, [$inf, -1, false]);
        $dp[0] = [0.0, 0, true];

        for ($i = 1; $i <= $n; $i++) {
            $jStart = max(0, $i - 30);
            for ($j = $jStart; $j < $i; $j++) {
                if ($dp[$j][0] === $inf) {
                    continue;
                }

                $substr = implode('', array_slice($chars, $j, $i - $j));
                if (Lookup::charLen($substr) < 2 && $j > 0) {
                    continue;
                }

                $entry = $arIndex[$substr] ?? null;
                if ($entry === null) {
                    $entry = $arNorm[Lookup::normalizeAr($substr)] ?? null;
                }

                if ($entry !== null) {
                    $freqKey = $entry->frequency->value[0] ?? '';
                    $cost = $dp[$j][0]
                        + self::BASE_SEGMENT_COST
                        + (self::FREQ_BONUS[$freqKey] ?? 0.0)
                        + self::LENGTH_BONUS_PER_CHAR * Lookup::charLen($substr);
                    if ($cost < $dp[$i][0]) {
                        $dp[$i] = [$cost, $j, true];
                    }
                } else {
                    $cost = $dp[$j][0] + self::UNKNOWN_PENALTY + Lookup::charLen($substr);
                    if ($cost < $dp[$i][0]) {
                        $dp[$i] = [$cost, $j, false];
                    }
                }
            }
        }

        if ($dp[$n][0] === $inf) {
            return [$text];
        }

        $segments = [];
        $pos = $n;
        while ($pos > 0) {
            $prev = $dp[$pos][1];
            $segments[] = implode('', array_slice($chars, $prev, $pos - $prev));
            $pos = $prev;
        }

        return array_reverse($segments);
    }
}
