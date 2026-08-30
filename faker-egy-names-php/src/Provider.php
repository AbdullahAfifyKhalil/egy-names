<?php

declare(strict_types=1);

namespace Afify\FakerEgyNames;

use Faker\Provider\Base;

/**
 * Egyptian patronymic names via the same generate() rules as faker-egy-names for Python.
 *
 * Snake_case methods match the Python API. CamelCase aliases are for FakerPHP style.
 */
class Provider extends Base
{
    private Engine $engine;

    public function __construct(\Faker\Generator $generator, ?Engine $engine = null)
    {
        parent::__construct($generator);
        $this->engine = $engine ?? new Engine();
    }

    public function egyptian_name(
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $family_name = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): GeneratedName {
        return $this->generateName($gender, $religion, $length, $family_name, $frequency, $seed);
    }

    public function egyptianName(
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $familyName = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): GeneratedName {
        return $this->egyptian_name($gender, $religion, $length, $familyName, $frequency, $seed);
    }

    /** @return string|array{0: string, 1: string} */
    public function egyptian_full_name(
        string $lang = 'en',
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $family_name = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): string|array {
        $name = $this->generateName($gender, $religion, $length, $family_name, $frequency, $seed);

        return self::localized($name->ar, $name->en, $lang);
    }

    /** @return string|array{0: string, 1: string} */
    public function egyptianFullName(
        string $lang = 'en',
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $familyName = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): string|array {
        return $this->egyptian_full_name($lang, $gender, $religion, $length, $familyName, $frequency, $seed);
    }

    /** @return string|array{0: string, 1: string} */
    public function egyptian_person(
        string $lang = 'en',
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $family_name = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): string|array {
        return $this->slot(0, $lang, $gender, $religion, $length, $family_name, $frequency, $seed);
    }

    /** @return string|array{0: string, 1: string} */
    public function egyptianPerson(
        string $lang = 'en',
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $familyName = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): string|array {
        return $this->egyptian_person($lang, $gender, $religion, $length, $familyName, $frequency, $seed);
    }

    /** @return string|array{0: string, 1: string} */
    public function egyptian_father(
        string $lang = 'en',
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $family_name = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): string|array {
        return $this->slot(1, $lang, $gender, $religion, $length, $family_name, $frequency, $seed);
    }

    /** @return string|array{0: string, 1: string} */
    public function egyptianFather(
        string $lang = 'en',
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $familyName = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): string|array {
        return $this->egyptian_father($lang, $gender, $religion, $length, $familyName, $frequency, $seed);
    }

    /** @return string|array{0: string, 1: string} */
    public function egyptian_grandfather(
        string $lang = 'en',
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $family_name = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): string|array {
        return $this->slot(2, $lang, $gender, $religion, $length, $family_name, $frequency, $seed);
    }

    /** @return string|array{0: string, 1: string} */
    public function egyptianGrandfather(
        string $lang = 'en',
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $familyName = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): string|array {
        return $this->egyptian_grandfather($lang, $gender, $religion, $length, $familyName, $frequency, $seed);
    }

    /** @return string|array{0: string, 1: string} */
    public function egyptian_family(
        string $lang = 'en',
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $family_name = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): string|array {
        $name = $this->generateName($gender, $religion, $length, $family_name, $frequency, $seed);
        [, , , $family] = self::roles($name, $family_name);

        return self::localized($family[0], $family[1], $lang);
    }

    /** @return string|array{0: string, 1: string} */
    public function egyptianFamily(
        string $lang = 'en',
        ?string $gender = null,
        ?string $religion = null,
        ?int $length = null,
        bool $familyName = true,
        ?string $frequency = null,
        ?int $seed = null,
    ): string|array {
        return $this->egyptian_family($lang, $gender, $religion, $length, $familyName, $frequency, $seed);
    }

    /** @return string|array{0: string, 1: string} */
    private function slot(
        int $index,
        string $lang,
        ?string $gender,
        ?string $religion,
        ?int $length,
        bool $familyName,
        ?string $frequency,
        ?int $seed,
    ): string|array {
        $name = $this->generateName($gender, $religion, $length, $familyName, $frequency, $seed);
        $roles = self::roles($name, $familyName);

        return self::localized($roles[$index][0], $roles[$index][1], $lang);
    }

    private function generateName(
        ?string $gender,
        ?string $religion,
        ?int $length,
        bool $familyName,
        ?string $frequency,
        ?int $seed,
    ): GeneratedName {
        $seed ??= $this->generator->numberBetween(0, 0x7fffffff);

        return $this->engine->generate(
            $gender,
            $religion,
            $length,
            $familyName,
            $frequency,
            $seed,
        );
    }

    /** @return string|array{0: string, 1: string} */
    private static function localized(string $ar, string $en, string $lang): string|array
    {
        return match (strtolower($lang ?: 'en')) {
            'ar' => $ar,
            'both' => [$ar, $en],
            default => $en,
        };
    }

    /**
     * @return array{0: array{0: string, 1: string}, 1: array{0: string, 1: string}, 2: array{0: string, 1: string}, 3: array{0: string, 1: string}}
     */
    private static function roles(GeneratedName $name, bool $familyName): array
    {
        $partsAr = $name->partsAr;
        $partsEn = $name->partsEn;
        $family = ['', ''];
        if ($familyName && count($partsAr) > 1) {
            $family = [array_pop($partsAr), array_pop($partsEn)];
        }

        $slot = static function (int $index) use ($partsAr, $partsEn): array {
            if ($index < count($partsAr)) {
                return [$partsAr[$index], $partsEn[$index]];
            }

            return ['', ''];
        };

        return [$slot(0), $slot(1), $slot(2), $family];
    }
}

class_alias(Provider::class, __NAMESPACE__ . '\\EgyptianNamesProvider');
