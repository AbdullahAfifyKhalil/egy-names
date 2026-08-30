# faker-egy-names (PHP)

Faker provider for Egyptian names. Same idea as the [Python companion](https://pypi.org/project/faker-egy-names/): it does not invent a first name and a last name. Every call runs the egy-names `generate()` rules — grounded patronymic chains from the 44,626-lemma book.

The engine is [`afify/egy-names`](https://packagist.org/packages/afify/egy-names). This companion ships a generate-only catalog so Faker tests do not load the full book. Offline. MIT. Product page: [afify.co/egy-names](https://afify.co/egy-names).

## Install

```bash
composer require afify/faker-egy-names
```

Packagist: [`afify/faker-egy-names`](https://packagist.org/packages/afify/faker-egy-names) `0.1.0`.

From this monorepo:

```json
{
  "repositories": [
    {
      "type": "path",
      "url": "faker-egy-names-php"
    }
  ],
  "require": {
    "afify/faker-egy-names": "@dev"
  }
}
```

Requires PHP 8.1+ and [FakerPHP](https://fakerphp.github.io/).

## Use

```php
require 'vendor/autoload.php';

$fake = egyptian_faker();

// Coherent chain (use this for one person)
$name = $fake->egyptian_name(gender: 'female', religion: 'muslim');
echo $name->ar;       // يارا عادل فاروق الشناوي
echo $name->en;       // Yara Adel Farouk Elshenawy
print_r($name->parts_ar);

// Slot helpers — each call generates a new chain
$fake->egyptian_full_name();              // English full name
$fake->egyptian_full_name('ar');          // Arabic full name
$fake->egyptian_full_name(lang: 'both');  // [ar, en]
$fake->egyptian_person(gender: 'male');
$fake->egyptian_father();
$fake->egyptian_grandfather();
$fake->egyptian_family();
```

Or:

```php
use Afify\FakerEgyNames\Provider;
use Faker\Factory;

$fake = Factory::create();
$fake->addProvider(new Provider($fake));
$fake->seed(1);
$fake->egyptian_full_name(religion: 'christian', length: 4, seed: 1);
```

`$fake->seed(n)` is honored unless you pass `seed:` yourself. FakerPHP seeds process-wide `mt_srand` (not an instance RNG). Reseed immediately before a call if two generators must match. An explicit `seed:` argument is independent of that. CamelCase aliases (`egyptianName`, `egyptianFullName`, …) do the same work. Seeds are not aligned with the Python companion.

## Methods

| Method | Returns |
| :--- | :--- |
| `egyptian_name(...)` | `GeneratedName` (`ar`, `en`, `parts_ar` / `partsAr`, `parts_en` / `partsEn`) |
| `egyptian_full_name($lang = 'en', ...)` | Full patronymic string, or `[ar, en]` when `$lang === 'both'` |
| `egyptian_person($lang = 'en', ...)` | Slot 1 — the person |
| `egyptian_father($lang = 'en', ...)` | Slot 2 — father |
| `egyptian_grandfather($lang = 'en', ...)` | Slot 3 — grandfather |
| `egyptian_family($lang = 'en', ...)` | Final clan / toponymic surname |

Shared arguments (passed through to `generate()`):

`gender`, `religion`, `length`, `family_name`, `frequency`, `seed`

`$lang` is `"en"`, `"ar"`, or `"both"`. There is no `firstName` / `lastName` mapping. That flattening is what this library exists to avoid.

Slot helpers on separate calls are **not** the same person. For one fixture, call `egyptian_name()` once and read `parts_ar` / `parts_en`.

## License

MIT. Copyright (c) 2026 Afify by Abdullah Afify. An Afify open-source project. [afify.co/egy-names](https://afify.co/egy-names)
