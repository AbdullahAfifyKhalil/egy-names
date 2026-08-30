<?php

declare(strict_types=1);

namespace Afify\FakerEgyNames\Tests;

use Afify\FakerEgyNames\GeneratedName;
use Afify\FakerEgyNames\Provider;
use Faker\Factory;
use PHPUnit\Framework\TestCase;

final class ProviderTest extends TestCase
{
    public function testEgyptianFakerRegistersMethods(): void
    {
        $fake = egyptian_faker();
        $this->assertInstanceOf(GeneratedName::class, $fake->egyptian_name(seed: 1));
        $this->assertIsString($fake->egyptian_full_name(seed: 1));
        $this->assertIsString($fake->egyptian_person(seed: 1));
        $this->assertIsString($fake->egyptian_father(seed: 1));
        $this->assertIsString($fake->egyptian_grandfather(seed: 1));
        $this->assertIsString($fake->egyptian_family(seed: 1));
    }

    public function testEgyptianNameReturnsEngineObject(): void
    {
        $fake = egyptian_faker();
        $name = $fake->egyptian_name();
        $this->assertInstanceOf(GeneratedName::class, $name);
        $this->assertNotSame('', $name->ar);
        $this->assertNotSame('', $name->en);
        $this->assertGreaterThanOrEqual(2, count($name->partsAr));
        $this->assertCount(count($name->partsAr), $name->partsEn);
        $this->assertSame(implode(' ', $name->partsAr), $name->ar);
        $this->assertSame(implode(' ', $name->partsEn), $name->en);
        $this->assertSame($name->partsAr, $name->parts_ar);
    }

    public function testLangArEnBoth(): void
    {
        $fake = egyptian_faker();
        $en = $fake->egyptian_full_name();
        $ar = $fake->egyptian_full_name('ar');
        $both = $fake->egyptian_full_name(lang: 'both');
        $this->assertIsString($en);
        $this->assertDoesNotMatchRegularExpression('/[\x{0600}-\x{06FF}]/u', $en);
        $this->assertIsString($ar);
        $this->assertMatchesRegularExpression('/[\x{0600}-\x{06FF}]/u', $ar);
        $this->assertIsArray($both);
        $this->assertCount(2, $both);
        $this->assertMatchesRegularExpression('/[\x{0600}-\x{06FF}]/u', $both[0]);
        $this->assertDoesNotMatchRegularExpression('/[\x{0600}-\x{06FF}]/u', $both[1]);
    }

    public function testSameSeedYieldsSameChainSlots(): void
    {
        $fake = egyptian_faker();
        $name = $fake->egyptian_name(length: 4, seed: 11);
        $this->assertSame($name->en, $fake->egyptian_full_name(length: 4, seed: 11));
        $this->assertSame($name->ar, $fake->egyptian_full_name('ar', length: 4, seed: 11));
        $this->assertSame($name->partsEn[0], $fake->egyptian_person(length: 4, seed: 11));
        $this->assertSame($name->partsEn[1], $fake->egyptian_father(length: 4, seed: 11));
        $this->assertSame($name->partsEn[2], $fake->egyptian_grandfather(length: 4, seed: 11));
        $this->assertSame($name->partsEn[3], $fake->egyptian_family(length: 4, seed: 11));
        $this->assertSame([$name->partsAr[0], $name->partsEn[0]], $fake->egyptian_person(lang: 'both', length: 4, seed: 11));
    }

    public function testFamilyNameFalseHasEmptyFamily(): void
    {
        $fake = egyptian_faker();
        $name = $fake->egyptian_name(length: 3, family_name: false, seed: 3);
        $this->assertCount(3, $name->partsEn);
        $this->assertSame('', $fake->egyptian_family(length: 3, family_name: false, seed: 3));
        $this->assertSame($name->partsEn[2], $fake->egyptian_grandfather(length: 3, family_name: false, seed: 3));
    }

    public function testFakerSeedIsReproducible(): void
    {
        $a = Factory::create();
        $a->addProvider(new Provider($a));
        $b = Factory::create();
        $b->addProvider(new Provider($b));

        // FakerPHP's seed() is process-wide mt_srand — reseed immediately before each draw.
        $a->seed(42);
        $left = $a->egyptian_full_name();
        $b->seed(42);
        $right = $b->egyptian_full_name();
        $this->assertSame($left, $right);

        $c = Factory::create();
        $c->addProvider(new Provider($c));
        $a->seed(42);
        $fromA = $a->egyptian_full_name();
        $c->seed(99);
        $fromC = $c->egyptian_full_name();
        $this->assertNotSame($fromA, $fromC);
    }

    public function testExplicitSeedOverridesFakerRng(): void
    {
        $fake = egyptian_faker();
        $fake->seed(1);
        $left = $fake->egyptian_full_name(seed: 123);
        $fake->seed(999);
        $right = $fake->egyptian_full_name(seed: 123);
        $this->assertSame($left, $right);
    }

    public function testDefaultChainHasFatherAndFamily(): void
    {
        $fake = egyptian_faker();
        $name = $fake->egyptian_name();
        $this->assertGreaterThanOrEqual(4, count($name->partsEn));
        $this->assertNotSame('', $fake->egyptian_father(seed: 0));
        $this->assertNotSame('', $fake->egyptian_family(seed: 0));
    }

    public function testParseTemplate(): void
    {
        $fake = egyptian_faker();
        $text = $fake->parse('{{egyptian_full_name}}');
        $this->assertNotSame('', $text);
        $this->assertNotSame('{{egyptian_full_name}}', $text);
    }

    public function testCamelCaseAliases(): void
    {
        $fake = egyptian_faker();
        $name = $fake->egyptianName(length: 4, seed: 8);
        $this->assertSame($name->en, $fake->egyptianFullName(length: 4, seed: 8));
        $this->assertSame($name->partsEn[0], $fake->egyptianPerson(length: 4, seed: 8));
    }
}
