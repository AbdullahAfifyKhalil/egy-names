<?php

declare(strict_types=1);

namespace Afify\EgyNames;

final class BatchProcessor
{
    public function __construct(private EgyptianNames $parent)
    {
    }

    /**
     * @param list<string> $names
     * @return list<string>
     */
    public function translate(array $names, ?string $to = null): array
    {
        $out = [];
        foreach ($names as $n) {
            $out[] = $this->parent->translate($n, $to);
        }
        return $out;
    }

    /**
     * @param list<string> $names
     * @return list<NameInfo|list<NameInfo|null>|null>
     */
    public function annotate(array $names): array
    {
        $out = [];
        foreach ($names as $n) {
            $out[] = $this->parent->annotate($n);
        }
        return $out;
    }

    /**
     * @param list<string> $names
     * @return list<string>
     */
    public function correct(array $names): array
    {
        $out = [];
        foreach ($names as $n) {
            $out[] = $this->parent->correct($n);
        }
        return $out;
    }

    /**
     * @param list<string> $names
     * @return list<list<string>>
     */
    public function split(array $names): array
    {
        $out = [];
        foreach ($names as $n) {
            $out[] = $this->parent->split($n);
        }
        return $out;
    }

    /**
     * @param list<string> $names
     * @return list<GenderDetection>
     */
    public function detectGender(array $names): array
    {
        $out = [];
        foreach ($names as $n) {
            $out[] = $this->parent->detectGender($n);
        }
        return $out;
    }

    /**
     * @param list<string> $names
     * @return list<GenderDetection>
     */
    public function detect_gender(array $names): array
    {
        return $this->detectGender($names);
    }

    /**
     * @param list<string> $names
     * @return list<ReligionDetection>
     */
    public function detectReligion(array $names): array
    {
        $out = [];
        foreach ($names as $n) {
            $out[] = $this->parent->detectReligion($n);
        }
        return $out;
    }

    /**
     * @param list<string> $names
     * @return list<ReligionDetection>
     */
    public function detect_religion(array $names): array
    {
        return $this->detectReligion($names);
    }

    /**
     * @param list<string> $names
     * @return list<string>
     */
    public function tashkeel(array $names): array
    {
        $out = [];
        foreach ($names as $n) {
            $out[] = $this->parent->tashkeel($n);
        }
        return $out;
    }
}
