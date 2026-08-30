<?php

declare(strict_types=1);

namespace Afify\FakerEgyNames;

/**
 * Slot-weighted generate() — same rules as egy-names 0.3.2 / the Python faker.
 */
final class Engine
{
    private const DEFAULT_MIN_LEN = 4;
    private const DEFAULT_MAX_LEN = 5;

    public function generate(
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $familyName = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): GeneratedName {
        $rng = new \Random\Randomizer(new \Random\Engine\Mt19937($seed ?? random_int(0, 0x7fffffff)));

        $g = self::parseGender($gender);
        $r = self::parseReligion($religion);
        $f = self::parseFrequency($frequency);

        $all = Catalog::names();
        $firstPool = self::filter($all, $g, $r, 'g', $f);
        $patronPool = self::filter($all, 'm', $r, 'g', $f);
        $familyPool = self::filter($all, null, $r, 'f', $f);

        if ($firstPool === []) {
            $firstPool = self::filter($all, $g, null, 'g', null);
        }
        if ($patronPool === []) {
            $patronPool = self::filter($all, 'm', null, 'g', null);
        }
        if ($familyPool === []) {
            $familyPool = self::filter($all, null, null, 'f', null);
        }

        $chainLen = $length ?? $rng->getInt(self::DEFAULT_MIN_LEN, self::DEFAULT_MAX_LEN);
        $partsAr = [];
        $partsEn = [];
        $seen = [];

        $entry = $this->pick($firstPool, 0, $rng, $seen);
        $partsAr[] = $entry['a'];
        $partsEn[] = $entry['e'];
        $seen[$entry['a']] = true;

        $patronEnd = $familyName ? $chainLen - 1 : $chainLen;
        for ($slot = 1; $slot < $patronEnd; $slot++) {
            $slotIdx = min($slot, 7);
            $entry = $this->pick($patronPool, $slotIdx, $rng, $seen);
            $partsAr[] = $entry['a'];
            $partsEn[] = $entry['e'];
            $seen[$entry['a']] = true;
        }

        if ($familyName && $chainLen > 1) {
            $slotIdx = min($chainLen - 1, 7);
            $entry = $this->pick($familyPool, $slotIdx, $rng, $seen);
            $partsAr[] = $entry['a'];
            $partsEn[] = $entry['e'];
        }

        return new GeneratedName(
            implode(' ', $partsAr),
            implode(' ', $partsEn),
            $partsAr,
            $partsEn,
        );
    }

    /**
     * @param list<array{a: string, e: string, g: string, r: string, l: string, fc: string, p: list<float>, tp: float}> $entries
     * @return list<array{a: string, e: string, g: string, r: string, l: string, fc: string, p: list<float>, tp: float}>
     */
    private static function filter(
        array $entries,
        ?string $gender,
        ?string $religion,
        ?string $role,
        ?string $frequency,
    ): array {
        $out = [];
        foreach ($entries as $e) {
            if ($gender !== null && $e['g'] !== $gender && $e['g'] !== 'n') {
                continue;
            }
            if ($religion !== null && $e['r'] !== $religion && $e['r'] !== 'n') {
                continue;
            }
            if ($role !== null && $e['l'] !== $role) {
                continue;
            }
            if ($frequency !== null && ($e['fc'] ?? 'n') !== $frequency) {
                continue;
            }
            if (!Quality::isGeneratableEntry($e)) {
                continue;
            }
            $out[] = $e;
        }
        return $out;
    }

    /**
     * @param list<array{a: string, e: string, g: string, r: string, l: string, fc: string, p: list<float>, tp: float}> $entries
     * @param array<string, true> $seen
     * @return array{a: string, e: string, g: string, r: string, l: string, fc: string, p: list<float>, tp: float}
     */
    private function pick(array $entries, int $slotIdx, \Random\Randomizer $rng, array $seen): array
    {
        $entry = $this->weightedPick($entries, $slotIdx, $rng);
        $attempts = 0;
        while (isset($seen[$entry['a']]) && $attempts < 20) {
            $entry = $this->weightedPick($entries, $slotIdx, $rng);
            $attempts++;
        }
        return $entry;
    }

    /**
     * @param list<array{a: string, e: string, g: string, r: string, l: string, fc: string, p: list<float>, tp: float}> $entries
     * @return array{a: string, e: string, g: string, r: string, l: string, fc: string, p: list<float>, tp: float}
     */
    private function weightedPick(array $entries, int $slotIdx, \Random\Randomizer $rng): array
    {
        $candidates = [];
        $weights = [];
        foreach ($entries as $e) {
            $slots = $e['p'];
            $slotVal = $slots[$slotIdx] ?? ($slots[array_key_last($slots)] ?? 0.0);
            $w = $slotVal * $e['tp'];
            if ($w > 0) {
                $candidates[] = $e;
                $weights[] = $w;
            }
        }
        if ($candidates === []) {
            $candidates = $entries;
            $weights = [];
            foreach ($entries as $e) {
                $weights[] = max($e['tp'], 1e-9);
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

    private static function parseGender(?string $val): ?string
    {
        if ($val === null) {
            return null;
        }
        $s = strtolower(trim($val));
        return match ($s) {
            'm', 'male', 'ذكر' => 'm',
            'f', 'female', 'أنثى', 'انثى' => 'f',
            default => null,
        };
    }

    private static function parseReligion(?string $val): ?string
    {
        if ($val === null) {
            return null;
        }
        $s = strtolower(trim($val));
        return match ($s) {
            'm', 'muslim', 'islam', 'مسلم' => 'm',
            'c', 'christian', 'coptic', 'مسيحي', 'قبطي' => 'c',
            default => null,
        };
    }

    private static function parseFrequency(?string $val): ?string
    {
        if ($val === null) {
            return null;
        }
        $s = strtolower(trim($val));
        return match ($s) {
            'c', 'common', 'شائع' => 'c',
            'n', 'normal', 'متوسط', 'عادي' => 'n',
            'r', 'rare', 'نادر' => 'r',
            default => null,
        };
    }
}
