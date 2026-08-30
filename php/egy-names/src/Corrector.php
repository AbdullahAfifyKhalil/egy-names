<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * Port of typescript/src/corrector.ts.
 */
final class Corrector
{
    public static function correctToken(string $token): string
    {
        if (trim($token) === '') {
            return '';
        }
        $t = trim($token);

        $entry = Lookup::lookupAr($t);
        if ($entry !== null) {
            return $entry->ar;
        }

        $canonical = Lookup::getCorrect($t);
        if ($canonical !== null) {
            return $canonical;
        }

        $norm = Lookup::normalizeAr($t);
        $arNorm = Lookup::getArNormForms();
        if (isset($arNorm[$norm])) {
            return $arNorm[$norm]->ar;
        }

        if (str_ends_with($norm, "\u{0627}")) {
            $alt = Lookup::charSubstr($norm, 0, -1) . "\u{064A}";
            if (isset($arNorm[$alt])) {
                return $arNorm[$alt]->ar;
            }
        } elseif (str_ends_with($norm, "\u{064A}")) {
            $alt = Lookup::charSubstr($norm, 0, -1) . "\u{0627}";
            if (isset($arNorm[$alt])) {
                return $arNorm[$alt]->ar;
            }
        }

        return $t;
    }

    public static function correct(string $name): string
    {
        if (trim($name) === '') {
            return '';
        }
        $rawTokens = preg_split('/\s+/u', trim($name)) ?: [];
        $result = [];
        $n = count($rawTokens);

        for ($i = 0; $i < $n; $i++) {
            $current = $rawTokens[$i];

            if ($i < $n - 1) {
                $next = $rawTokens[$i + 1];
                $compound = $current . ' ' . $next;
                $compoundNoSpace = $current . $next;
                $compoundEntry = Lookup::lookupAr($compound) ?? Lookup::lookupAr($compoundNoSpace);
                if ($compoundEntry !== null) {
                    $result[] = $compoundEntry->ar;
                    $i++;
                    continue;
                }
            }

            $result[] = self::correctToken($current);
        }

        return implode(' ', $result);
    }
}
