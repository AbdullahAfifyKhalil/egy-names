<?php

declare(strict_types=1);

namespace Afify\FakerEgyNames;

/**
 * One grounded patronymic chain from generate().
 */
final class GeneratedName
{
    /**
     * @param list<string> $partsAr
     * @param list<string> $partsEn
     */
    public function __construct(
        public readonly string $ar,
        public readonly string $en,
        public readonly array $partsAr,
        public readonly array $partsEn,
    ) {
    }

    /** @return array{ar: string, en: string, parts_ar: list<string>, parts_en: list<string>} */
    public function toArray(): array
    {
        return [
            'ar' => $this->ar,
            'en' => $this->en,
            'parts_ar' => $this->partsAr,
            'parts_en' => $this->partsEn,
        ];
    }

    /** Python-shaped aliases: parts_ar / parts_en. */
    public function __get(string $name): mixed
    {
        return match ($name) {
            'parts_ar' => $this->partsAr,
            'parts_en' => $this->partsEn,
            default => throw new \Error('Undefined property: ' . self::class . '::$' . $name),
        };
    }
}
