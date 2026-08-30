<?php

declare(strict_types=1);

namespace Afify\EgyNames;

enum Gender: string
{
    case MALE = 'male';
    case FEMALE = 'female';
    case NEUTRAL = 'neutral';

    public static function fromCode(string $c): self
    {
        return match ($c) {
            'm' => self::MALE,
            'f' => self::FEMALE,
            default => self::NEUTRAL,
        };
    }

    public static function parse(?string $val): ?self
    {
        if ($val === null) {
            return null;
        }
        $raw = trim($val);
        $s = strtolower($raw);
        return match ($s) {
            'm', 'male' => self::MALE,
            'f', 'female' => self::FEMALE,
            'n', 'neutral' => self::NEUTRAL,
            default => match ($raw) {
                'ذكر' => self::MALE,
                'أنثى', 'انثى' => self::FEMALE,
                'مشترك', 'محايد' => self::NEUTRAL,
                default => null,
            },
        };
    }
}

enum Religion: string
{
    case MUSLIM = 'muslim';
    case CHRISTIAN = 'christian';
    case NEUTRAL = 'neutral';

    public static function fromCode(string $c): self
    {
        return match ($c) {
            'm' => self::MUSLIM,
            'c' => self::CHRISTIAN,
            default => self::NEUTRAL,
        };
    }

    public static function parse(?string $val): ?self
    {
        if ($val === null) {
            return null;
        }
        $raw = trim($val);
        $s = strtolower($raw);
        return match ($s) {
            'm', 'muslim', 'islam' => self::MUSLIM,
            'c', 'christian', 'coptic' => self::CHRISTIAN,
            'n', 'neutral' => self::NEUTRAL,
            default => match ($raw) {
                'مسلم' => self::MUSLIM,
                'مسيحي', 'قبطي' => self::CHRISTIAN,
                'مشترك', 'محايد' => self::NEUTRAL,
                default => null,
            },
        };
    }
}

enum NameRole: string
{
    case GIVEN = 'given';
    case FAMILY = 'family';
    case KUNYA = 'kunya';
    case TRIBAL = 'tribal';

    public static function fromCode(string $c): self
    {
        return match ($c) {
            'g' => self::GIVEN,
            'f' => self::FAMILY,
            'k' => self::KUNYA,
            't' => self::TRIBAL,
            default => self::GIVEN,
        };
    }

    public static function parse(?string $val): ?self
    {
        if ($val === null) {
            return null;
        }
        $raw = trim($val);
        $s = strtolower($raw);
        return match ($s) {
            'g', 'given', 'first' => self::GIVEN,
            'f', 'family', 'surname', 'last' => self::FAMILY,
            'k', 'kunya', 'patronymic' => self::KUNYA,
            't', 'tribal', 'clan' => self::TRIBAL,
            default => match ($raw) {
                'علم', 'اسم' => self::GIVEN,
                'عائلة', 'لقب' => self::FAMILY,
                'كنية' => self::KUNYA,
                'قبلي', 'قبيلة' => self::TRIBAL,
                default => null,
            },
        };
    }

    public function isFamilyLike(): bool
    {
        return $this === self::FAMILY || $this === self::TRIBAL;
    }
}

enum FrequencyClass: string
{
    case COMMON = 'common';
    case NORMAL = 'normal';
    case RARE = 'rare';

    public static function fromCode(string $c): self
    {
        return match ($c) {
            'c' => self::COMMON,
            'n' => self::NORMAL,
            default => self::RARE,
        };
    }

    public static function parse(?string $val): ?self
    {
        if ($val === null) {
            return null;
        }
        $raw = trim($val);
        $s = strtolower($raw);
        return match ($s) {
            'c', 'common' => self::COMMON,
            'n', 'normal' => self::NORMAL,
            'r', 'rare' => self::RARE,
            default => match ($raw) {
                'شائع' => self::COMMON,
                'متوسط', 'عادي' => self::NORMAL,
                'نادر' => self::RARE,
                default => null,
            },
        };
    }
}

/**
 * Shared camelCase / snake_case / ArrayAccess surface for public DTOs.
 */
trait FieldAliases
{
    public function __get(string $name): mixed
    {
        if (property_exists($this, $name)) {
            return $this->$name;
        }
        $snake = self::toSnake($name);
        if ($snake !== $name && property_exists($this, $snake)) {
            return $this->$snake;
        }
        throw new \Error('Undefined property: ' . static::class . '::$' . $name);
    }

    public function offsetExists(mixed $offset): bool
    {
        $key = (string) $offset;
        return property_exists($this, $key) || property_exists($this, self::toSnake($key));
    }

    public function offsetGet(mixed $offset): mixed
    {
        return $this->__get((string) $offset);
    }

    public function offsetSet(mixed $offset, mixed $value): void
    {
        throw new \Error(static::class . ' is read-only');
    }

    public function offsetUnset(mixed $offset): void
    {
        throw new \Error(static::class . ' is read-only');
    }

    private static function toSnake(string $name): string
    {
        return strtolower((string) preg_replace('/(?<!^)[A-Z]/', '_$0', $name));
    }
}

final class PetName implements \ArrayAccess
{
    use FieldAliases;

    public function __construct(
        public readonly string $ar,
        public readonly string $tashkeel,
        public readonly string $en,
        public readonly string $ipa,
    ) {
    }

    /** @return array{ar: string, tashkeel: string, en: string, ipa: string} */
    public function toArray(): array
    {
        return [
            'ar' => $this->ar,
            'tashkeel' => $this->tashkeel,
            'en' => $this->en,
            'ipa' => $this->ipa,
        ];
    }
}

final class NameEntry
{
    /** @var list<string> */
    public array $arVariants;
    /** @var list<string> */
    public array $enVariants;
    /** @var list<float> */
    public array $slotPcts;
    public float $corpusShare;
    public FrequencyClass $frequency;
    public string $tashkeel;
    public string $tashkeelStandard;
    public string $tashkeelEg;
    public string $ipaStandard;
    public string $ipaEg;
    public string $meaningAr;
    public string $meaningEn;
    /** @var list<string> */
    public array $dallaa;
    /** @var list<string> */
    public array $dallaaAr;
    /** @var list<string> */
    public array $dallaaTashkeel;
    /** @var list<string> */
    public array $dallaaEn;
    /** @var list<string> */
    public array $dallaaIpa;
    public string $root;
    public string $originType;
    /** @var list<string> */
    public array $famousFigures;
    /** @var list<string> */
    public array $famousFiguresAr;
    /** @var list<string> */
    public array $famousFiguresEn;
    public string $trendCategory;

    /**
     * @param array<string, mixed> $raw
     */
    public function __construct(
        public string $ar,
        public string $en,
        public Gender $gender,
        public Religion $religion,
        public NameRole $role,
        array $raw,
    ) {
        $this->arVariants = isset($raw['av']) && $raw['av'] !== '' ? explode('|', (string) $raw['av']) : [$raw['a']];
        $this->enVariants = isset($raw['ev']) && $raw['ev'] !== '' ? explode('|', (string) $raw['ev']) : [$raw['e']];
        $slots = $raw['p'] ?? [0, 0, 0, 0, 0, 0, 0, 0];
        $this->slotPcts = array_map('floatval', is_array($slots) ? $slots : [0, 0, 0, 0, 0, 0, 0, 0]);
        $this->corpusShare = (float) ($raw['tp'] ?? 0);
        $this->frequency = FrequencyClass::fromCode((string) ($raw['fc'] ?? 'r'));
        $this->tashkeel = (string) ($raw['t'] ?? $raw['a']);
        $this->tashkeelStandard = (string) ($raw['t'] ?? $raw['a']);
        $this->tashkeelEg = (string) ($raw['te'] ?? $raw['t'] ?? $raw['a']);
        $this->ipaStandard = (string) ($raw['is'] ?? '');
        $this->ipaEg = (string) ($raw['ie'] ?? '');
        $this->meaningAr = (string) ($raw['ma'] ?? '');
        $this->meaningEn = (string) ($raw['me'] ?? '');

        $dlaRaw = (string) ($raw['dla'] ?? $raw['dl'] ?? '');
        $this->dallaaAr = $dlaRaw !== '' ? explode('|', $dlaRaw) : [];
        $this->dallaa = $this->dallaaAr;
        $this->dallaaTashkeel = isset($raw['dlt']) && $raw['dlt'] !== '' ? explode('|', (string) $raw['dlt']) : [];
        $this->dallaaEn = isset($raw['dle']) && $raw['dle'] !== '' ? explode('|', (string) $raw['dle']) : [];
        $this->dallaaIpa = isset($raw['dli']) && $raw['dli'] !== '' ? explode('|', (string) $raw['dli']) : [];

        $this->root = (string) ($raw['rt'] ?? 'N/A');
        $this->originType = (string) ($raw['ot'] ?? 'arabic_classical');

        $ffaRaw = (string) ($raw['ffa'] ?? $raw['ff'] ?? '');
        $this->famousFiguresAr = $ffaRaw !== '' ? explode('|', $ffaRaw) : [];
        $this->famousFigures = $this->famousFiguresAr;
        $this->famousFiguresEn = isset($raw['ffe']) && $raw['ffe'] !== '' ? explode('|', (string) $raw['ffe']) : [];

        $this->trendCategory = (string) ($raw['tc'] ?? 'classic_timeless');
    }

    /**
     * @param array<string, mixed> $raw
     */
    public static function fromRaw(array $raw): self
    {
        return new self(
            (string) $raw['a'],
            (string) $raw['e'],
            Gender::fromCode((string) $raw['g']),
            Religion::fromCode((string) $raw['r']),
            NameRole::fromCode((string) $raw['l']),
            $raw,
        );
    }
}

final class NameInfo implements \ArrayAccess
{
    use FieldAliases;

    /**
     * @param list<string> $dallaa
     * @param list<string> $dallaa_ar
     * @param list<string> $dallaa_tashkeel
     * @param list<string> $dallaa_en
     * @param list<string> $dallaa_ipa
     * @param list<string> $famous_figures
     * @param list<string> $famous_figures_ar
     * @param list<string> $famous_figures_en
     * @param list<string> $ar_variants
     * @param list<string> $en_variants
     * @param list<float> $slot_distribution
     */
    public function __construct(
        public readonly string $ar,
        public readonly string $en,
        public readonly string $gender,
        public readonly string $religion,
        public readonly string $role,
        public readonly string $frequency_class,
        public readonly float $corpus_share,
        public readonly string $tashkeel,
        public readonly string $tashkeel_standard,
        public readonly string $tashkeel_eg,
        public readonly string $ipa_standard,
        public readonly string $ipa_eg,
        public readonly ?string $meaning_ar,
        public readonly ?string $meaning_en,
        public readonly array $dallaa,
        public readonly array $dallaa_ar,
        public readonly array $dallaa_tashkeel,
        public readonly array $dallaa_en,
        public readonly array $dallaa_ipa,
        public readonly string $root,
        public readonly string $origin_type,
        public readonly array $famous_figures,
        public readonly array $famous_figures_ar,
        public readonly array $famous_figures_en,
        public readonly string $trend_category,
        public readonly array $ar_variants,
        public readonly array $en_variants,
        public readonly array $slot_distribution,
    ) {
    }

    public static function fromEntry(NameEntry $entry): self
    {
        return new self(
            $entry->ar,
            $entry->en,
            $entry->gender->value,
            $entry->religion->value,
            $entry->role->value,
            $entry->frequency->value,
            $entry->corpusShare,
            $entry->tashkeel,
            $entry->tashkeelStandard,
            $entry->tashkeelEg,
            $entry->ipaStandard,
            $entry->ipaEg,
            $entry->meaningAr !== '' ? $entry->meaningAr : null,
            $entry->meaningEn !== '' ? $entry->meaningEn : null,
            $entry->dallaaAr,
            $entry->dallaaAr,
            $entry->dallaaTashkeel,
            $entry->dallaaEn,
            $entry->dallaaIpa,
            $entry->root,
            $entry->originType,
            $entry->famousFiguresAr,
            $entry->famousFiguresAr,
            $entry->famousFiguresEn,
            $entry->trendCategory,
            $entry->arVariants,
            $entry->enVariants,
            $entry->slotPcts,
        );
    }

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return [
            'ar' => $this->ar,
            'en' => $this->en,
            'gender' => $this->gender,
            'religion' => $this->religion,
            'role' => $this->role,
            'frequency_class' => $this->frequency_class,
            'corpus_share' => $this->corpus_share,
            'tashkeel' => $this->tashkeel,
            'tashkeel_standard' => $this->tashkeel_standard,
            'tashkeel_eg' => $this->tashkeel_eg,
            'ipa_standard' => $this->ipa_standard,
            'ipa_eg' => $this->ipa_eg,
            'meaning_ar' => $this->meaning_ar,
            'meaning_en' => $this->meaning_en,
            'dallaa' => $this->dallaa,
            'dallaa_ar' => $this->dallaa_ar,
            'dallaa_tashkeel' => $this->dallaa_tashkeel,
            'dallaa_en' => $this->dallaa_en,
            'dallaa_ipa' => $this->dallaa_ipa,
            'root' => $this->root,
            'origin_type' => $this->origin_type,
            'famous_figures' => $this->famous_figures,
            'famous_figures_ar' => $this->famous_figures_ar,
            'famous_figures_en' => $this->famous_figures_en,
            'trend_category' => $this->trend_category,
            'ar_variants' => $this->ar_variants,
            'en_variants' => $this->en_variants,
            'slot_distribution' => $this->slot_distribution,
        ];
    }
}

final class GeneratedName implements \ArrayAccess
{
    use FieldAliases;

    /**
     * @param list<string> $parts_ar
     * @param list<string> $parts_en
     */
    public function __construct(
        public readonly string $ar,
        public readonly string $en,
        public readonly array $parts_ar,
        public readonly array $parts_en,
    ) {
    }

    /** @return array{ar: string, en: string, parts_ar: list<string>, parts_en: list<string>} */
    public function toArray(): array
    {
        return [
            'ar' => $this->ar,
            'en' => $this->en,
            'parts_ar' => $this->parts_ar,
            'parts_en' => $this->parts_en,
        ];
    }
}

final class ChainPart implements \ArrayAccess
{
    use FieldAliases;

    public function __construct(
        public readonly string $name,
        public readonly int $slot,
        public readonly string $role,
        public readonly string $detail,
    ) {
    }

    /** @return array{name: string, slot: int, role: string, detail: string} */
    public function toArray(): array
    {
        return [
            'name' => $this->name,
            'slot' => $this->slot,
            'role' => $this->role,
            'detail' => $this->detail,
        ];
    }
}

final class GenderDetection implements \ArrayAccess
{
    use FieldAliases;

    public function __construct(
        public readonly string $gender,
        public readonly float $confidence,
    ) {
    }

    /** @return array{gender: string, confidence: float} */
    public function toArray(): array
    {
        return ['gender' => $this->gender, 'confidence' => $this->confidence];
    }
}

final class ReligionDetection implements \ArrayAccess
{
    use FieldAliases;

    public function __construct(
        public readonly string $religion,
        public readonly float $confidence,
    ) {
    }

    /** @return array{religion: string, confidence: float} */
    public function toArray(): array
    {
        return ['religion' => $this->religion, 'confidence' => $this->confidence];
    }
}

final class RankInfo implements \ArrayAccess
{
    use FieldAliases;

    public function __construct(
        public readonly int $rank,
        public readonly float $percentile,
        public readonly string $corpus_share,
        public readonly string $description,
    ) {
    }

    /** @return array{rank: int, percentile: float, corpus_share: string, description: string} */
    public function toArray(): array
    {
        return [
            'rank' => $this->rank,
            'percentile' => $this->percentile,
            'corpus_share' => $this->corpus_share,
            'description' => $this->description,
        ];
    }
}

final class UniquenessScore implements \ArrayAccess
{
    use FieldAliases;

    public function __construct(
        public readonly float $score,
        public readonly string $label,
        public readonly string $note,
    ) {
    }

    /** @return array{score: float, label: string, note: string} */
    public function toArray(): array
    {
        return [
            'score' => $this->score,
            'label' => $this->label,
            'note' => $this->note,
        ];
    }
}

final class Fingerprint implements \ArrayAccess
{
    use FieldAliases;

    /**
     * @param array<string, float> $slots
     */
    public function __construct(
        public readonly string $name_ar,
        public readonly string $name_en,
        public readonly string $type,
        public readonly array $slots,
        public readonly float $corpus_share,
        public readonly string $description,
    ) {
    }

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return [
            'name_ar' => $this->name_ar,
            'name_en' => $this->name_en,
            'type' => $this->type,
            'slots' => $this->slots,
            'corpus_share' => $this->corpus_share,
            'description' => $this->description,
        ];
    }
}

final class FormatResult implements \ArrayAccess
{
    use FieldAliases;

    public function __construct(
        public readonly string $first,
        public readonly string $last,
    ) {
    }

    /** @return array{first: string, last: string} */
    public function toArray(): array
    {
        return ['first' => $this->first, 'last' => $this->last];
    }
}

final class AgeProfile implements \ArrayAccess
{
    use FieldAliases;

    /**
     * @param array{0: int, 1: int} $peak_age_range
     * @param array<int, float> $age_scores
     */
    public function __construct(
        public readonly array $peak_age_range,
        public readonly string $generation_label,
        public readonly int $dominant_slot,
        public readonly array $age_scores,
    ) {
    }

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return [
            'peak_age_range' => $this->peak_age_range,
            'generation_label' => $this->generation_label,
            'dominant_slot' => $this->dominant_slot,
            'age_scores' => $this->age_scores,
        ];
    }
}

final class AgeDetection implements \ArrayAccess
{
    use FieldAliases;

    /**
     * @param array{0: int, 1: int} $age_range
     */
    public function __construct(
        public readonly int $estimated_age,
        public readonly array $age_range,
        public readonly float $confidence,
        public readonly string $generation_label,
        public readonly string $note,
    ) {
    }

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return [
            'estimated_age' => $this->estimated_age,
            'age_range' => $this->age_range,
            'confidence' => $this->confidence,
            'generation_label' => $this->generation_label,
            'note' => $this->note,
        ];
    }
}
