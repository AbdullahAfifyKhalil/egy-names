<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * Generational age engine. Port of python egy_names/_index.py age functions.
 */
final class Age
{
    private const CORPUS_ANCHOR_YEAR = 2020;
    private const STUDENT_GRAD_AGE = 18;
    private const CORPUS_STUDENT_BIRTH = 2002;
    private const GENERATION_GAP = 30;
    private const GAUSSIAN_SIGMA = 12;

    /** @var array<int, string> */
    private const GEN_LABELS = [
        0 => 'youth',
        1 => 'parent',
        2 => 'grandparent',
        3 => 'great-grandparent',
    ];

    /**
     * Slot birth-year centres: student / father / grandfather / great-grandfather / timeless / timeless.
     *
     * @return list<int|null>
     */
    private static function slotBirthCenters(): array
    {
        return [
            self::CORPUS_STUDENT_BIRTH,
            self::CORPUS_STUDENT_BIRTH - self::GENERATION_GAP,
            self::CORPUS_STUDENT_BIRTH - 2 * self::GENERATION_GAP,
            self::CORPUS_STUDENT_BIRTH - 3 * self::GENERATION_GAP,
            null,
            null,
        ];
    }

    public static function gaussian(float $x, float $center, float $sigma): float
    {
        return exp(-0.5 * (($x - $center) / $sigma) ** 2);
    }

    public static function scoreForAge(NameEntry $entry, int $birthYear): float
    {
        $p = $entry->slotPcts;
        while (count($p) < 6) {
            $p[] = 0.0;
        }
        $p = array_slice($p, 0, 6);
        if (array_sum($p) == 0.0) {
            return 0.0;
        }

        $centers = self::slotBirthCenters();
        $total = 0.0;
        foreach ($centers as $i => $centre) {
            if ($centre === null) {
                $total += $p[$i] * 0.05;
            } else {
                $total += $p[$i] * self::gaussian((float) $birthYear, (float) $centre, (float) self::GAUSSIAN_SIGMA);
            }
        }

        $maxW = 0.0;
        for ($i = 0; $i < 4; $i++) {
            $c = $centers[$i];
            if ($c !== null) {
                $maxW = max($maxW, self::gaussian((float) $birthYear, (float) $c, (float) self::GAUSSIAN_SIGMA));
            }
        }
        $normalizer = $maxW > 0 ? $maxW * 100 : 100;
        return min($total / $normalizer, 1.0);
    }

    /**
     * @return list<NameEntry>
     */
    public static function namesForAge(
        int $age,
        ?string $gender = null,
        ?int $as_of_year = null,
        int $top = 20,
        bool $include_family = false,
    ): array {
        Lookup::getAll();
        $year = $as_of_year ?? (int) date('Y');
        $birthYear = $year - max(0, $age);
        $genderFilter = Gender::parse($gender);

        $results = [];
        foreach (Lookup::getAll() as $entry) {
            if (!$include_family && $entry->role !== NameRole::GIVEN && $entry->role !== NameRole::KUNYA) {
                continue;
            }
            if ($genderFilter !== null && $entry->gender !== $genderFilter && $entry->gender !== Gender::NEUTRAL) {
                continue;
            }

            $score = self::scoreForAge($entry, $birthYear);
            if ($score <= 0.0) {
                continue;
            }

            $freqBoost = 1.0 + log(1 + $entry->corpusShare * 1000);
            $results[] = [$score * $freqBoost, $entry];
        }

        usort($results, static fn (array $a, array $b): int => $b[0] <=> $a[0]);
        $out = [];
        foreach (array_slice($results, 0, $top) as $row) {
            $out[] = $row[1];
        }
        return $out;
    }

    public static function ageProfile(NameEntry $entry, ?int $as_of_year = null): AgeProfile
    {
        $year = $as_of_year ?? (int) date('Y');
        $p = $entry->slotPcts;
        while (count($p) < 6) {
            $p[] = 0.0;
        }
        $p = array_slice($p, 0, 6);

        $ageScores = [];
        for ($age = 0; $age <= 100; $age += 5) {
            $birthYear = $year - $age;
            $ageScores[$age] = round(self::scoreForAge($entry, $birthYear), 3);
        }

        $maxScore = $ageScores !== [] ? max($ageScores) : 0;
        $threshold = $maxScore * 0.5;
        $inPeak = [];
        foreach ($ageScores as $a => $s) {
            if ($s >= $threshold) {
                $inPeak[] = $a;
            }
        }
        $peakRange = $inPeak !== [] ? [min($inPeak), max($inPeak)] : [0, 100];

        $centers = self::slotBirthCenters();
        $slotScores = [];
        foreach ($centers as $i => $centre) {
            if ($centre === null) {
                $slotScores[] = $p[$i] * 0.05;
            } else {
                $peakBirth = $year - intdiv($peakRange[0] + $peakRange[1], 2);
                $slotScores[] = $p[$i] * self::gaussian((float) $peakBirth, (float) $centre, (float) self::GAUSSIAN_SIGMA);
            }
        }

        if ($entry->role === NameRole::FAMILY || $entry->role === NameRole::TRIBAL) {
            $dominantSlot = 5;
            $genLabel = 'timeless';
        } elseif (array_sum($slotScores) == 0.0) {
            $dominantSlot = 1;
            $genLabel = 'unknown';
        } else {
            $dominantSlot = (int) array_search(max($slotScores), $slotScores, true) + 1;
            $genLabel = self::GEN_LABELS[$dominantSlot - 1] ?? 'timeless';
        }

        return new AgeProfile($peakRange, $genLabel, $dominantSlot, $ageScores);
    }

    /**
     * @param list<array{0: NameEntry, 1: int}> $tokenEntries
     */
    public static function detectAgeFromChain(array $tokenEntries, ?int $as_of_year = null): AgeDetection
    {
        $year = $as_of_year ?? (int) date('Y');
        $slotWeights = [0 => 1.0, 1 => 0.6, 2 => 0.3, 3 => 0.15];

        $tokenEstimates = [];
        foreach ($tokenEntries as [$entry, $slotIdx]) {
            if ($entry->role === NameRole::FAMILY || $entry->role === NameRole::TRIBAL) {
                continue;
            }
            [$peakAge, $sharpness] = self::peakAgeForEntry($entry, $year);
            $implied = max(0, min(100, $peakAge - $slotIdx * self::GENERATION_GAP));
            $weight = $slotWeights[$slotIdx] ?? 0.1;
            $tokenEstimates[] = [$implied, $sharpness, $weight];
        }

        if ($tokenEstimates === []) {
            return new AgeDetection(
                35,
                [0, 100],
                0.0,
                'timeless',
                'Only family/clan names were given — no age signal available.',
            );
        }

        $totalWeight = 0.0;
        $weightedAgeSum = 0.0;
        foreach ($tokenEstimates as [$age, , $w]) {
            $totalWeight += $w;
            $weightedAgeSum += $age * $w;
        }
        $estimatedAge = (int) round($weightedAgeSum / $totalWeight);

        $slot0Sharpness = $tokenEstimates[0][1] ?? 0.0;
        $baseConfidence = $slot0Sharpness;

        if (count($tokenEstimates) >= 2) {
            $impliedAges = [];
            foreach ($tokenEstimates as [$age]) {
                $impliedAges[] = (float) $age;
            }
            $spread = self::sampleStdev($impliedAges);
            $agreementBonus = max(0.0, 0.2 * (1.0 - $spread / 30.0));
            $confidence = min(1.0, $baseConfidence + $agreementBonus);
        } else {
            $confidence = $baseConfidence;
        }
        $confidence = round($confidence, 3);

        $sigma = self::GAUSSIAN_SIGMA;
        $ageRange = [max(0, $estimatedAge - $sigma), min(100, $estimatedAge + $sigma)];

        $slot0Entries = [];
        foreach ($tokenEntries as [$e, $si]) {
            if ($si === 0 && $e->role !== NameRole::FAMILY && $e->role !== NameRole::TRIBAL) {
                $slot0Entries[] = $e;
            }
        }
        if ($slot0Entries !== []) {
            $estBirth = $year - $estimatedAge;
            $closest = 0;
            $best = PHP_FLOAT_MAX;
            for ($i = 0; $i < 4; $i++) {
                $diff = abs($estBirth - (self::CORPUS_STUDENT_BIRTH - $i * self::GENERATION_GAP));
                if ($diff < $best) {
                    $best = $diff;
                    $closest = $i;
                }
            }
            $genLabel = self::GEN_LABELS[$closest] ?? 'timeless';
        } else {
            $genLabel = 'unknown';
        }

        $nTokens = count($tokenEstimates);
        $tokenWord = $nTokens === 1 ? 'name' : $nTokens . '-token chain';
        $rangeStr = $ageRange[0] . '–' . $ageRange[1] . ' years old';
        if ($confidence >= 0.6) {
            $confStr = 'high confidence';
        } elseif ($confidence >= 0.3) {
            $confStr = 'moderate confidence';
        } else {
            $confStr = 'low confidence (common across generations)';
        }
        $note = 'Based on ' . $tokenWord . ': estimated age ~' . $estimatedAge
            . ' (' . $rangeStr . '), ' . $genLabel . ' generation, ' . $confStr . '.';

        return new AgeDetection($estimatedAge, $ageRange, $confidence, $genLabel, $note);
    }

    public static function detectAgeForEntry(NameEntry $entry, ?int $as_of_year = null): AgeDetection
    {
        return self::detectAgeFromChain([[$entry, 0]], $as_of_year);
    }

    /**
     * @return array{0: int, 1: float}
     */
    private static function peakAgeForEntry(NameEntry $entry, int $year): array
    {
        $scores = [];
        for ($age = 0; $age <= 100; $age++) {
            $scores[$age] = self::scoreForAge($entry, $year - $age);
        }
        if ($scores === [] || max($scores) == 0.0) {
            return [35, 0.0];
        }
        $peak = (int) array_search(max($scores), $scores, true);
        $peakS = $scores[$peak];
        $meanS = array_sum($scores) / count($scores);
        $sharpness = ($peakS - $meanS) / ($peakS + 1e-9);
        return [$peak, max(0.0, min(1.0, $sharpness))];
    }

    /**
     * @param list<float> $values
     */
    private static function sampleStdev(array $values): float
    {
        $n = count($values);
        if ($n < 2) {
            return 0.0;
        }
        $mean = array_sum($values) / $n;
        $var = 0.0;
        foreach ($values as $v) {
            $var += ($v - $mean) ** 2;
        }
        return sqrt($var / ($n - 1));
    }
}
