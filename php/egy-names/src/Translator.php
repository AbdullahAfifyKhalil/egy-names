<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * Port of typescript/src/translator.ts.
 */
final class Translator
{
    public static function translateToken(string $token, ?string $to = null): string
    {
        $srcIsArabic = Lookup::isArabic($token);
        $target = $to ?? ($srcIsArabic ? 'en' : 'ar');

        if ($target === 'en') {
            $entry = Lookup::lookupAr($token);
            return $entry !== null ? $entry->en : $token;
        }

        $entry = Lookup::lookupEn($token);
        return $entry !== null ? $entry->ar : $token;
    }

    public static function translate(string $fullName, ?string $to = null): string
    {
        if (trim($fullName) === '') {
            return '';
        }
        $tokens = preg_split('/\s+/u', trim($fullName)) ?: [];
        $translated = [];
        foreach ($tokens as $t) {
            $translated[] = self::translateToken($t, $to);
        }
        return implode(' ', $translated);
    }
}
