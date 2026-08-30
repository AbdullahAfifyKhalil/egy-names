<?php

/**
 * afify/faker-egy-names 0.1.1 — PHP Faker showcase.
 */

declare(strict_types=1);

$autoload = [
    __DIR__ . '/vendor/autoload.php',
    __DIR__ . '/../../faker-egy-names-php/vendor/autoload.php',
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
    fwrite(STDERR, "Run `composer require afify/faker-egy-names` first.\n");
    exit(1);
}

$fake = egyptian_faker();

echo str_repeat('=', 60) . PHP_EOL;
echo " afify/faker-egy-names 0.1.1 — PHP" . PHP_EOL;
echo str_repeat('=', 60) . PHP_EOL;

$name = $fake->egyptian_name(gender: 'female', religion: 'muslim', length: 4, seed: 1);
echo "\n1. One coherent person — call egyptian_name() once:\n";
echo "   {$name->ar}\n";
echo "   {$name->en}\n";
echo '   parts_ar: ' . json_encode($name->parts_ar, JSON_UNESCAPED_UNICODE) . PHP_EOL;

echo "\n2. Slot helpers (each call is a new chain):\n";
echo '   full en: ' . $fake->egyptian_full_name(seed: 1) . PHP_EOL;
echo '   full ar: ' . $fake->egyptian_full_name(lang: 'ar', seed: 1) . PHP_EOL;
echo '   person:  ' . $fake->egyptian_person(gender: 'male', seed: 2) . PHP_EOL;
echo '   father:  ' . $fake->egyptian_father(seed: 2) . PHP_EOL;
echo '   family:  ' . $fake->egyptian_family(seed: 2) . PHP_EOL;

echo "\nThere is no first_name / last_name mapping.\n";
