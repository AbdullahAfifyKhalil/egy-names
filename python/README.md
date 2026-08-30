# egy-names (Python)

Egyptian names engine for Python 3.9+. Same book as the other SDKs — 44,626 lemmas, offline.

A legal Egyptian name is a patronymic chain, not a first name and a last name. This package generates, translates, splits, and corrects those chains.

**[afify.co/egy-names](https://afify.co/egy-names)** — origin, process, insights, lab, examples, and demo.

**[The Secret Code of Egyptian Names](https://medium.com/@abdullah.afify/the-secret-code-of-egyptian-names-how-we-engineered-a-14-dimensional-nlp-engine-5205db7f04f4)** — how the engine was built.

## Accuracy

The book comes from real records. Names outside the book go through the [fallback model](https://huggingface.co/Abdullah-afify/egy-names-fallback-classifier). Every guess is marked `inferred`. If it is not sure, it abstains. If you find a miss, [open an issue](https://github.com/AbdullahAfifyKhalil/egy-names/issues).

## Install

```bash
pip install egy-names==0.3.6
```

## Use

```python
from egy_names import EgyNames

e = EgyNames()

print(e.split("محمدأحمدعليحسنالشناوي"))
# ['محمد', 'أحمد', 'علي', 'حسن', 'الشناوي']

print(e.translate("محمد أحمد علي الشناوي"))
# Mohamed Ahmed Ali El Shenawy

print(e.correct("احمد مصطفا عبد الرحيم"))
# أحمد مصطفى عبدالرحيم

name = e.generate(gender="female", religion="muslim", length=4)[0]
print(name.ar, name.en)

print(e.is_valid("محمد"))   # True
print(e.is_valid("الله"))   # False — in the index, not a person's name

print(e.detect_gender("فاطمة محمد علي"))     # first personal token wins
print(e.detect_religion("مينا جرجس بطرس"))

book = e.identify("محمد")
print(book.ar, book.inferred, book.source)   # book path

for tok in e.identify_all("محمد زوكرمانوفيتش"):
    print(tok.surface, tok.gender, tok.inferred, tok.source)
```

`identify` / `identify_all` are Python only. Book first. Then the fallback model. Check `inferred`.

Need the same names inside existing Faker tests? [`pip install faker-egy-names`](https://pypi.org/project/faker-egy-names/).

Full API: [DOCUMENTATION.md](https://github.com/AbdullahAfifyKhalil/egy-names/blob/main/DOCUMENTATION.md). Runnable script: [`examples/python/`](https://github.com/AbdullahAfifyKhalil/egy-names/tree/main/examples/python).

## Other languages

Same book, other SDKs — no samples here. See the [repo](https://github.com/AbdullahAfifyKhalil/egy-names) and [afify.co/egy-names](https://afify.co/egy-names).

## License

MIT. Copyright (c) 2026 Afify by Abdullah Afify. An Afify open-source project.
