<?php

declare(strict_types=1);

namespace Afify\EgyNames;

/**
 * Port of typescript/src/annotator.ts.
 */
final class Annotator
{
    public static function annotateSingle(string $name): ?NameInfo
    {
        $entry = Lookup::lookup($name);
        if ($entry === null) {
            return null;
        }
        return NameInfo::fromEntry($entry);
    }

    /**
     * @return NameInfo|list<NameInfo|null>|null
     */
    public static function annotate(string $name): NameInfo|array|null
    {
        if (trim($name) === '') {
            return null;
        }

        $tokens = preg_split('/\s+/u', trim($name)) ?: [];
        if (count($tokens) === 1) {
            return self::annotateSingle($tokens[0]);
        }

        $out = [];
        foreach ($tokens as $t) {
            $out[] = self::annotateSingle($t);
        }
        return $out;
    }
}
