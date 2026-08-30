<?php

/**
 * afify/egy-names 0.3.6 — PHP showcase.
 */

declare(strict_types=1);

$autoload = [
    __DIR__ . '/vendor/autoload.php',
    __DIR__ . '/../../php/egy-names/vendor/autoload.php',
];
$loaded = false;
foreach ($autoload as $path) {
    if (is_file($path)) {
        require $path;
        $loaded = true;
        break;
    }
}
if (!$loaded) {
    fwrite(STDERR, "Run `composer require afify/egy-names` first.\n");
    exit(1);
}

use Afify\EgyNames\EgyNames;

$en = new EgyNames();

echo str_repeat('=', 60) . PHP_EOL;
echo " Egyptian Names (afify/egy-names) 0.3.6 — PHP" . PHP_EOL;
echo str_repeat('=', 60) . PHP_EOL;

echo "\n1. Generate a grounded chain:\n";
foreach ($en->generate(count: 3, length: 4, gender: 'female', religion: 'muslim') as $n) {
    echo "   {$n->ar}  ({$n->en})\n";
}

echo "\n2. Translate:\n";
echo '   ' . $en->translate('محمد أحمد علي الشناوي') . PHP_EOL;

echo "\n3. Correct:\n";
echo '   ' . $en->correct('احمد مصطفا عبد الرحيم') . PHP_EOL;

echo "\n4. Tashkeel and IPA:\n";
echo '   Standard: ' . $en->tashkeel('محمد عبدالرحمن') . PHP_EOL;
echo '   Egyptian: ' . $en->tashkeel_eg('محمد عبدالرحمن') . PHP_EOL;
echo '   IPA std:  ' . $en->ipa('جمال') . PHP_EOL;
echo '   IPA eg:   ' . $en->ipa_eg('جمال') . PHP_EOL;

echo "\n5. Split a concatenated dump:\n";
echo '   ' . json_encode($en->split('محمدأحمدعليحسنالشناوي'), JSON_UNESCAPED_UNICODE) . PHP_EOL;

echo "\n6. Pet names and figures:\n";
echo '   dallaa: ' . json_encode($en->dallaa('محمد', format: 'tashkeel'), JSON_UNESCAPED_UNICODE) . PHP_EOL;
$figures = $en->famous_figures('محمد', lang: 'en');
echo '   figures: ' . implode(' | ', array_slice($figures, 0, 2)) . PHP_EOL;

echo "\n7. Lookup:\n";
$info = $en->info('محمد');
echo "   {$info->ar} / {$info->en} | root=" . $en->root('محمد') . ' | origin=' . $en->origin('محمد') . PHP_EOL;
$meaning = $en->meaning('محمد');
echo '   meaning: ' . ($meaning['en'] ?? '') . PHP_EOL;

echo "\n8. Validity — personal names only:\n";
echo '   is_valid("محمد")  = ' . ($en->is_valid('محمد') ? 'true' : 'false') . PHP_EOL;
echo '   is_valid("Mahmoud") = ' . ($en->is_valid('Mahmoud') ? 'true' : 'false') . PHP_EOL;
echo '   is_valid("الله")   = ' . ($en->is_valid('الله') ? 'true' : 'false') . "  # in the index, not a person\n";

echo "\n9. First personal token wins:\n";
$gender = $en->detect_gender('فاطمة محمد علي');
$religion = $en->detect_religion('مينا جرجس بطرس');
echo "   {$gender->gender} ({$gender->confidence})\n";
echo "   {$religion->religion} ({$religion->confidence})\n";

echo "\n10. Chain, rank, uniqueness:\n";
foreach ($en->analyze_chain('محمد أحمد علي الشناوي') as $p) {
    echo "   Slot {$p->slot}: {$p->name} — {$p->role}\n";
}
$rank = $en->rank('محمد');
$uniq = $en->uniqueness('محمد أحمد علي الشناوي');
echo "   rank=#{$rank->rank}  uniqueness={$uniq->score} ({$uniq->label})\n";

echo "\n11. Age:\n";
$age = $en->detect_age('كريم أشرف فاروق');
if ($age !== null) {
    echo "   ~{$age->estimated_age} ({$age->generation_label})\n";
}
