<?php

declare(strict_types=1);

namespace Afify\EgyNames\Tests;

use Afify\EgyNames\AgeDetection;
use Afify\EgyNames\EgyptianNames;
use Afify\EgyNames\EgyNames;
use Afify\EgyNames\GeneratedName;
use PHPUnit\Framework\TestCase;

final class SmokeTest extends TestCase
{
    private EgyptianNames $en;

    protected function setUp(): void
    {
        $this->en = new EgyNames();
    }

    public function testStatsTotalNames(): void
    {
        $stats = $this->en->stats();
        $this->assertArrayHasKey('total_names', $stats);
        $this->assertGreaterThanOrEqual(40000, $stats['total_names']);
    }

    public function testTranslateArabicToEnglish(): void
    {
        $out = $this->en->translate('محمد أحمد علي');
        $this->assertStringContainsString('Mohamed', $out);
        $this->assertStringContainsString('Ahmed', $out);
    }

    public function testTranslateEnglishToArabic(): void
    {
        $out = $this->en->translate('Mohamed Ahmed Ali');
        $this->assertStringContainsString('محمد', $out);
    }

    public function testSplitConcatenated(): void
    {
        $parts = $this->en->split('محمدأحمدعليحسنالشناوي');
        $this->assertGreaterThanOrEqual(4, count($parts));
        $this->assertContains('محمد', $parts);
    }

    public function testCorrectAhmed(): void
    {
        $out = $this->en->correct('احمد');
        $this->assertTrue($out === 'أحمد' || str_contains($out, 'أحمد'));
    }

    public function testCorrectMustafa(): void
    {
        $this->assertSame('مصطفى', $this->en->correct('مصطفا'));
    }

    public function testTashkeelMohamed(): void
    {
        $tk = $this->en->tashkeel('محمد');
        $this->assertNotSame('', $tk);
        $info = $this->en->info('محمد');
        $this->assertNotNull($info);
        if ($info->tashkeel !== $info->ar) {
            $this->assertNotSame('محمد', $tk);
        }
    }

    public function testAnnotateAndInfoHaveMeaning(): void
    {
        $info = $this->en->info('محمد');
        $this->assertNotNull($info);
        $this->assertNotNull($info->meaning_ar);
        $this->assertNotSame('', $info->meaning_ar);
        $annotated = $this->en->annotate('محمد');
        $this->assertNotNull($annotated);
        $this->assertNotNull($annotated->meaningAr);
    }

    public function testGenerateFemaleSeeded(): void
    {
        $names = $this->en->generate(count: 2, gender: 'female', length: 4, seed: 1);
        $this->assertCount(2, $names);
        foreach ($names as $name) {
            $this->assertInstanceOf(GeneratedName::class, $name);
            $this->assertNotSame('', $name->ar);
            $this->assertNotSame('', $name->en);
            $this->assertNotEmpty($name->parts_ar);
            $this->assertNotEmpty($name->partsEn);
            $this->assertCount(count($name->parts_ar), $name->parts_en);
        }
    }

    public function testDetectGenderFemale(): void
    {
        $det = $this->en->detect_gender('مريم إبراهيم حسن');
        $this->assertSame('female', $det->gender);
    }

    public function testDetectReligionChristian(): void
    {
        $det = $this->en->detectReligion('مينا جرجس بطرس');
        $this->assertNotSame('', $det->religion);
        $this->assertContains($det->religion, ['christian', 'neutral', 'muslim']);
        $this->assertNotSame('muslim', $det->religion);
    }

    public function testDallaaMohamed(): void
    {
        $this->assertNotEmpty($this->en->dallaa('محمد'));
    }

    public function testIsValid(): void
    {
        $this->assertTrue($this->en->is_valid('محمد'));
        $this->assertFalse($this->en->isValid('zzzznotaname'));
    }

    public function testDetectAge(): void
    {
        $det = $this->en->detect_age('محمد');
        $this->assertInstanceOf(AgeDetection::class, $det);
        $this->assertIsInt($det->estimated_age);
        $this->assertIsInt($det->estimatedAge);
    }

    public function testBatchTranslate(): void
    {
        $out = $this->en->batch()->translate(['محمد أحمد', 'فاطمة']);
        $this->assertCount(2, $out);
        $this->assertStringContainsString('Mohamed', $out[0]);
    }
}
