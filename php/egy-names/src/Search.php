<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * Port of typescript/src/search.ts.
 */
final class Search
{
    /**
     * @return list<NameInfo>
     */
    public static function search(
        ?string $gender = null,
        ?string $religion = null,
        ?string $role = null,
        ?string $frequency = null,
        ?string $starts_with = null,
        ?string $ends_with = null,
        ?string $prefix = null,
        ?string $suffix = null,
        ?string $contains = null,
        ?float $min_corpus_share = null,
        ?int $max_results = null,
        ?string $sort_by = null,
    ): array {
        $entries = Lookup::getAll();

        $g = Gender::parse($gender);
        if ($g === Gender::NEUTRAL) {
            $g = null;
        }
        $r = Religion::parse($religion);
        if ($r === Religion::NEUTRAL) {
            $r = null;
        }
        $rl = NameRole::parse($role);
        $f = FrequencyClass::parse($frequency);

        $effectiveStarts = $prefix ?? $starts_with;
        $effectiveEnds = $suffix ?? $ends_with;
        $prefixAr = $effectiveStarts !== null && $effectiveStarts !== '' && Lookup::isArabic($effectiveStarts);
        $suffixAr = $effectiveEnds !== null && $effectiveEnds !== '' && Lookup::isArabic($effectiveEnds);
        $containsAr = $contains !== null && $contains !== '' && Lookup::isArabic($contains);

        $filtered = [];
        foreach ($entries as $e) {
            if ($g !== null && $e->gender !== $g && $e->gender !== Gender::NEUTRAL) {
                continue;
            }
            if ($r !== null && $e->religion !== $r && $e->religion !== Religion::NEUTRAL) {
                continue;
            }
            if ($rl !== null && $e->role !== $rl) {
                continue;
            }
            if ($f !== null && $e->frequency !== $f) {
                continue;
            }
            if ($min_corpus_share !== null && $e->corpusShare < $min_corpus_share) {
                continue;
            }

            if ($effectiveStarts) {
                if ($prefixAr) {
                    if (!str_starts_with(Lookup::normalizeAr($e->ar), Lookup::normalizeAr($effectiveStarts))) {
                        continue;
                    }
                } elseif (!str_starts_with(Lookup::normalizeEn($e->en), Lookup::normalizeEn($effectiveStarts))) {
                    continue;
                }
            }

            if ($effectiveEnds) {
                if ($suffixAr) {
                    if (!str_ends_with(Lookup::normalizeAr($e->ar), Lookup::normalizeAr($effectiveEnds))) {
                        continue;
                    }
                } elseif (!str_ends_with(Lookup::normalizeEn($e->en), Lookup::normalizeEn($effectiveEnds))) {
                    continue;
                }
            }

            if ($contains) {
                if ($containsAr) {
                    if (!str_contains(Lookup::normalizeAr($e->ar), Lookup::normalizeAr($contains))) {
                        continue;
                    }
                } elseif (!str_contains(Lookup::normalizeEn($e->en), Lookup::normalizeEn($contains))) {
                    continue;
                }
            }

            $filtered[] = $e;
        }

        $sortBy = $sort_by ?? 'corpus_share';
        if ($sortBy === 'alphabetical') {
            usort($filtered, static fn (NameEntry $a, NameEntry $b): int => $a->ar <=> $b->ar);
        } else {
            usort($filtered, static fn (NameEntry $a, NameEntry $b): int => $b->corpusShare <=> $a->corpusShare);
        }

        $maxResults = $max_results ?? 50;
        $sliced = array_slice($filtered, 0, $maxResults);
        $out = [];
        foreach ($sliced as $e) {
            $out[] = NameInfo::fromEntry($e);
        }
        return $out;
    }
}
