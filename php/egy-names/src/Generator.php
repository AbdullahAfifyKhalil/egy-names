<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * Slot-weighted grounded generation. Rules from typescript/src/generator.ts.
 * RNG is PHP Randomizer/Mt19937 (same as faker-egy-names-php). Not seed-aligned with Python.
 */
final class Generator
{
    private const DEFAULT_MIN_LEN = 4;
    private const DEFAULT_MAX_LEN = 5;

    /**
     * @return list<GeneratedName>
     */
    public static function generate(
        int $count = 1,
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $family_name = true,
        ?string $frequency = null,
        string $lang = 'both',
        ?int $seed = null,
    ): array {
        unset($lang);
        if ($count <= 0) {
            return [];
        }

        $rng = new \Random\Randomizer(new \Random\Engine\Mt19937($seed ?? random_int(0, 0x7fffffff)));

        $g = Gender::parse($gender);
        if ($g === Gender::NEUTRAL) {
            $g = null;
        }
        $r = Religion::parse($religion);
        if ($r === Religion::NEUTRAL) {
            $r = null;
        }
        $f = FrequencyClass::parse($frequency);

        $all = Lookup::getAll();
        $firstPool = self::filter($all, $g, $r, NameRole::GIVEN, $f);
        $patronPool = self::filter($all, Gender::MALE, $r, NameRole::GIVEN, $f);
        $familyPool = self::filter($all, null, $r, NameRole::FAMILY, $f);

        if ($firstPool === []) {
            $firstPool = self::filter($all, $g, null, NameRole::GIVEN, null);
        }
        if ($patronPool === []) {
            $patronPool = self::filter($all, Gender::MALE, null, NameRole::GIVEN, null);
        }
        if ($familyPool === []) {
            $familyPool = self::filter($all, null, null, NameRole::FAMILY, null);
        }

        $results = [];
        for ($c = 0; $c < $count; $c++) {
            $chainLen = $length ?? $rng->getInt(self::DEFAULT_MIN_LEN, self::DEFAULT_MAX_LEN);
            $partsAr = [];
            $partsEn = [];
            $seen = [];

            $entry = self::pick($firstPool, 0, $rng, $seen);
            $partsAr[] = $entry->ar;
            $partsEn[] = $entry->en;
            $seen[$entry->ar] = true;

            $patronEnd = $family_name ? $chainLen - 1 : $chainLen;
            for ($slot = 1; $slot < $patronEnd; $slot++) {
                $slotIdx = min($slot, 7);
                $entry = self::pick($patronPool, $slotIdx, $rng, $seen);
                $partsAr[] = $entry->ar;
                $partsEn[] = $entry->en;
                $seen[$entry->ar] = true;
            }

            if ($family_name && $chainLen > 1) {
                $slotIdx = min($chainLen - 1, 7);
                $entry = self::pick($familyPool, $slotIdx, $rng, $seen);
                $partsAr[] = $entry->ar;
                $partsEn[] = $entry->en;
            }

            $results[] = new GeneratedName(
                implode(' ', $partsAr),
                implode(' ', $partsEn),
                $partsAr,
                $partsEn,
            );
        }

        return $results;
    }

    /**
     * @param list<NameEntry> $entries
     * @return list<NameEntry>
     */
    private static function filter(
        array $entries,
        ?Gender $gender,
        ?Religion $religion,
        ?NameRole $role,
        ?FrequencyClass $frequency,
    ): array {
        $out = [];
        foreach ($entries as $e) {
            if ($gender !== null && $e->gender !== $gender && $e->gender !== Gender::NEUTRAL) {
                continue;
            }
            if ($religion !== null && $e->religion !== $religion && $e->religion !== Religion::NEUTRAL) {
                continue;
            }
            if ($role !== null && $e->role !== $role) {
                continue;
            }
            if ($frequency !== null && $e->frequency !== $frequency) {
                continue;
            }
            if (!Quality::isGeneratable($e)) {
                continue;
            }
            $out[] = $e;
        }
        return $out;
    }

    /**
     * @param list<NameEntry> $entries
     * @param array<string, true> $seen
     */
    private static function pick(array $entries, int $slotIdx, \Random\Randomizer $rng, array $seen): NameEntry
    {
        $entry = self::weightedPick($entries, $slotIdx, $rng);
        $attempts = 0;
        while (isset($seen[$entry->ar]) && $attempts < 20) {
            $entry = self::weightedPick($entries, $slotIdx, $rng);
            $attempts++;
        }
        return $entry;
    }

    /**
     * @param list<NameEntry> $entries
     */
    private static function weightedPick(array $entries, int $slotIdx, \Random\Randomizer $rng): NameEntry
    {
        $candidates = [];
        $weights = [];
        foreach ($entries as $e) {
            $slotVal = $e->slotPcts[$slotIdx] ?? 0.0;
            $w = $slotVal * $e->corpusShare;
            if ($w > 0) {
                $candidates[] = $e;
                $weights[] = $w;
            }
        }
        if ($candidates === []) {
            $candidates = $entries;
            $weights = [];
            foreach ($entries as $e) {
                $weights[] = max($e->corpusShare, 1e-9);
            }
        }

        $sum = array_sum($weights);
        $r = ($rng->getInt(0, 1_000_000_000) / 1_000_000_000) * $sum;
        $acc = 0.0;
        $last = $candidates[0];
        foreach ($candidates as $i => $e) {
            $acc += $weights[$i];
            $last = $e;
            if ($r <= $acc) {
                return $e;
            }
        }
        return $last;
    }
}
