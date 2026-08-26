# faker-egy-names

Faker provider for Egyptian names. It does not sample names itself — every call goes to [`egy-names`](https://pypi.org/project/egy-names/) `0.3.2` `generate()`.

This is a companion package. `egy-names` stays offline, zero-dependency, and unchanged.

## Install

```bash
pip install faker-egy-names
```

## Use

```python
from faker import Faker
from faker_egy_names import Provider

fake = Faker()
fake.add_provider(Provider)

# Coherent 6-slot chain (use this for one person)
name = fake.egyptian_name(gender="female", religion="muslim")
print(name.ar)   # يارا عادل فاروق الشناوي
print(name.en)   # Yara Adel Farouk Elshenawy
print(name.parts_ar)

# Slot helpers — each call generates a new chain
fake.egyptian_full_name()                    # English full name
fake.egyptian_full_name("ar")                # Arabic full name
fake.egyptian_full_name(lang="both")         # (ar, en)
fake.egyptian_person(gender="male")
fake.egyptian_father()
fake.egyptian_grandfather()
fake.egyptian_family()
```

Or:

```python
from faker_egy_names import egyptian_faker

fake = egyptian_faker()
fake.egyptian_full_name(religion="christian", length=4, seed=1)
```

`Faker.seed_instance(n)` is honored unless you pass `seed=` yourself.

## Methods

| Method | Returns |
| :--- | :--- |
| `egyptian_name(...)` | `GeneratedName` (`ar`, `en`, `parts_ar`, `parts_en`) |
| `egyptian_full_name(lang="en", ...)` | Full patronymic string |
| `egyptian_person(lang="en", ...)` | Slot 1 — the person |
| `egyptian_father(lang="en", ...)` | Slot 2 — father |
| `egyptian_grandfather(lang="en", ...)` | Slot 3 — grandfather |
| `egyptian_family(lang="en", ...)` | Final clan / toponymic surname |

Shared keyword arguments (passed through to `egy-names.generate()`):

`gender`, `religion`, `length`, `family_name`, `frequency`, `seed`

`lang` is `"en"`, `"ar"`, or `"both"`. There is no `first_name` / `last_name` mapping — that flattening is what this library exists to avoid.

Slot helpers on separate calls are **not** the same person. For one fixture, call `egyptian_name()` once and read `parts_ar` / `parts_en`.
