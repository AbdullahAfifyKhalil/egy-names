# egy-names (PHP)

Egyptian names engine for PHP 8.1+. Same book as the other SDKs — 44,626 lemmas, offline.

A legal Egyptian name is a patronymic chain, not a first name and a last name. This package generates, translates, splits, and corrects those chains. Product page: [afify.co/egy-names](https://afify.co/egy-names).

This is the engine. Packagist: [`afify/egy-names`](https://packagist.org/packages/afify/egy-names). For Faker fixtures, use [`afify/faker-egy-names`](https://packagist.org/packages/afify/faker-egy-names).

## Install

```bash
composer require afify/egy-names
```

Requires PHP 8.1+, `ext-json`, and `ext-zlib`. No Faker dependency.

## Use

```php
require 'vendor/autoload.php';

use Afify\EgyNames\EgyNames;

$en = new EgyNames();

$names = $en->generate(count: 2, gender: 'female', length: 4, family_name: true);
echo $names[0]->ar;
echo $names[0]->en;
print_r($names[0]->parts_ar);

echo $en->translate('محمد أحمد علي');          // Mohamed Ahmed Ali
echo $en->translate('Mohamed Ahmed Ali');     // محمد أحمد علي
print_r($en->split('محمدأحمدعليحسنالشناوي'));
echo $en->correct('احمد مصطفا');              // أحمد مصطفى
echo $en->tashkeel('محمد');
```

CamelCase aliases (`tashkeelEg`, `detectGender`, `isValid`, …) do the same work. Named arguments use snake_case so Python-shaped calls work.

`$en->batch()` (or `$en->batch`) maps `translate`, `annotate`, `correct`, `split`, `detectGender`, `detectReligion`, and `tashkeel` over arrays.

`generate(seed: n)` uses PHP `Randomizer` / `Mt19937`. Seeds are not aligned with Python.

## License

MIT. Copyright (c) 2026 Afify by Abdullah Afify. An Afify open-source project. [afify.co/egy-names](https://afify.co/egy-names)
