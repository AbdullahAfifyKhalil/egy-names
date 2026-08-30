<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * In-memory indices + Arabic / English normalization.
 * Port of typescript/src/lookupIndices.ts.
 */
final class Lookup
{
    private static bool $built = false;

    /** @var array<string, NameEntry> */
    private static array $arIndex = [];

    /** @var array<string, NameEntry> */
    private static array $enIndex = [];

    /** @var array<string, NameEntry> */
    private static array $arNormIndex = [];

    /** @var array<string, string> */
    private static array $correctionIndex = [];

    /** @var list<NameEntry> */
    private static array $ranked = [];

    /** @var list<NameEntry> */
    private static array $allEntries = [];

    public static function normalizeAr(string $text): string
    {
        $s = preg_replace('/[\x{0610}-\x{061A}\x{064B}-\x{065F}\x{0670}\x{06D6}-\x{06ED}]/u', '', $text) ?? $text;
        $s = preg_replace('/\x{0640}/u', '', $s) ?? $s;
        $s = preg_replace('/[\x{0622}\x{0623}\x{0625}\x{0671}]/u', "\u{0627}", $s) ?? $s;
        $s = str_replace("\u{0649}", "\u{064A}", $s);
        $s = str_replace("\u{0629}", "\u{0647}", $s);
        return $s;
    }

    public static function normalizeEn(string $text): string
    {
        return strtolower(str_replace(['-', "'"], '', trim($text)));
    }

    private static function claimEn(string $key, NameEntry $entry): void
    {
        $existing = self::$enIndex[$key] ?? null;
        if ($existing === null || $entry->corpusShare > $existing->corpusShare) {
            self::$enIndex[$key] = $entry;
        }
    }

    /**
     * Bind an Arabic variant spelling to the lemma with the larger
     * corpus share, same rule as English keys.
     *
     * A canonical key (some entry's own ar / normalized-ar) always wins
     * over any OTHER entry's variant claiming the same string — a rare
     * misspelling must never shadow a real lemma's own canonical
     * spelling. Among two variants with no canonical claim, the higher
     * corpus share wins, exactly like claimEn.
     *
     * @param array<string, NameEntry> $index
     * @param array<string, true> $canonicalKeys
     */
    private static function claimArVariant(array &$index, array $canonicalKeys, string $key, NameEntry $entry): void
    {
        if (isset($canonicalKeys[$key])) {
            return;
        }
        $existing = $index[$key] ?? null;
        if ($existing === null || $entry->corpusShare > $existing->corpusShare) {
            $index[$key] = $entry;
        }
    }

    public static function isArabic(string $text): bool
    {
        return (bool) preg_match('/[\x{0600}-\x{06FF}\x{FE70}-\x{FEFF}]/u', $text);
    }

    /**
     * Unicode code-point characters (BMP-safe; matches JS string indexing for Arabic).
     *
     * @return list<string>
     */
    public static function chars(string $text): array
    {
        if ($text === '') {
            return [];
        }
        $parts = preg_split('//u', $text, -1, PREG_SPLIT_NO_EMPTY);
        return $parts === false ? [] : $parts;
    }

    public static function charLen(string $text): int
    {
        return count(self::chars($text));
    }

    public static function charSubstr(string $text, int $start, ?int $length = null): string
    {
        $chars = self::chars($text);
        $slice = $length === null ? array_slice($chars, $start) : array_slice($chars, $start, $length);
        return implode('', $slice);
    }

    public static function lookupAr(string $name): ?NameEntry
    {
        self::ensureBuilt();
        if (trim($name) === '') {
            return null;
        }
        $trimmed = trim($name);

        if (isset(self::$arIndex[$trimmed])) {
            return self::$arIndex[$trimmed];
        }

        $norm = self::normalizeAr($trimmed);
        if (isset(self::$arNormIndex[$norm])) {
            return self::$arNormIndex[$norm];
        }

        if (str_ends_with($norm, "\u{0627}")) {
            $alt = self::charSubstr($norm, 0, -1) . "\u{064A}";
            if (isset(self::$arNormIndex[$alt])) {
                return self::$arNormIndex[$alt];
            }
        } elseif (str_ends_with($norm, "\u{064A}")) {
            $alt = self::charSubstr($norm, 0, -1) . "\u{0627}";
            if (isset(self::$arNormIndex[$alt])) {
                return self::$arNormIndex[$alt];
            }
        }

        $noSpace = preg_replace('/\s+/u', '', $trimmed) ?? $trimmed;
        if ($noSpace !== $trimmed) {
            $match = self::$arIndex[$noSpace] ?? self::$arNormIndex[self::normalizeAr($noSpace)] ?? null;
            if ($match !== null) {
                return $match;
            }
        }

        return null;
    }

    public static function lookupEn(string $name): ?NameEntry
    {
        self::ensureBuilt();
        return self::$enIndex[self::normalizeEn($name)] ?? null;
    }

    public static function lookup(string $name): ?NameEntry
    {
        self::ensureBuilt();
        if (self::isArabic($name)) {
            return self::lookupAr($name);
        }
        return self::lookupEn($name);
    }

    public static function getCorrect(string $surface): ?string
    {
        self::ensureBuilt();
        return self::$correctionIndex[$surface] ?? null;
    }

    /**
     * @return list<NameEntry>
     */
    public static function getRanked(): array
    {
        self::ensureBuilt();
        return self::$ranked;
    }

    /**
     * @return list<NameEntry>
     */
    public static function getAll(): array
    {
        self::ensureBuilt();
        return self::$allEntries;
    }

    /**
     * @return array<string, NameEntry>
     */
    public static function getArForms(): array
    {
        self::ensureBuilt();
        return self::$arIndex;
    }

    /**
     * @return array<string, NameEntry>
     */
    public static function getArNormForms(): array
    {
        self::ensureBuilt();
        return self::$arNormIndex;
    }

    public static function reset(): void
    {
        self::$built = false;
        self::$arIndex = [];
        self::$enIndex = [];
        self::$arNormIndex = [];
        self::$correctionIndex = [];
        self::$ranked = [];
        self::$allEntries = [];
    }

    private static function ensureBuilt(): void
    {
        if (!self::$built) {
            self::build();
        }
    }

    private static function build(): void
    {
        if (self::$built) {
            return;
        }

        $entries = Catalog::entries();
        $corrections = Catalog::corrections();

        // Pass 1: canonical spellings are unconditional and take priority
        // over any other lemma's variant claiming the same string (book
        // has zero duplicate canonical ar values).
        $canonicalArKeys = [];
        $canonicalArNormKeys = [];
        foreach ($entries as $entry) {
            $canonicalArKeys[$entry->ar] = true;
            $canonicalArNormKeys[self::normalizeAr($entry->ar)] = true;
            self::$arIndex[$entry->ar] = $entry;
            self::$arNormIndex[self::normalizeAr($entry->ar)] = $entry;
        }

        foreach ($entries as $entry) {
            // Pass 2: variants. Keep the higher-share lemma when two
            // rows' variants claim the same spelling — same rule as
            // English keys, so a rare misspelling cannot steal a common
            // name's lookup.
            foreach ($entry->arVariants as $v) {
                $vStripped = trim($v);
                if ($vStripped === '') {
                    continue;
                }
                self::claimArVariant(self::$arIndex, $canonicalArKeys, $vStripped, $entry);
                self::claimArVariant(
                    self::$arNormIndex,
                    $canonicalArNormKeys,
                    self::normalizeAr($vStripped),
                    $entry,
                );
            }

            self::claimEn(self::normalizeEn($entry->en), $entry);

            foreach ($entry->enVariants as $v) {
                $vStripped = trim($v);
                if ($vStripped === '') {
                    continue;
                }
                self::claimEn(self::normalizeEn($vStripped), $entry);
            }
        }

        foreach ($corrections as $k => $v) {
            self::$correctionIndex[$k] = $v;
        }

        self::$allEntries = $entries;
        $ranked = $entries;
        usort($ranked, static fn (NameEntry $a, NameEntry $b): int => $b->corpusShare <=> $a->corpusShare);
        self::$ranked = $ranked;
        self::$built = true;
    }
}
