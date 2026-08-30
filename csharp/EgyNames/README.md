# egy-names (.NET)

Egyptian names engine for C# / .NET. Same book as the other SDKs — 44,626 lemmas, offline.

A legal Egyptian name is a patronymic chain, not a first name and a last name. This package generates, translates, splits, and corrects those chains.

**[afify.co/egy-names](https://afify.co/egy-names)** — origin, process, insights, lab, examples, and demo.

**[The Secret Code of Egyptian Names](https://medium.com/@abdullah.afify/the-secret-code-of-egyptian-names-how-we-engineered-a-14-dimensional-nlp-engine-5205db7f04f4)** — how the engine was built.

## Accuracy

The book comes from real records. Some names will still come back wrong — a rare spelling, a name the catalog has never seen. If you find one, [open an issue](https://github.com/AbdullahAfifyKhalil/egy-names/issues).

## Install

```bash
dotnet add package egy-names --version 0.3.6
```

## Use

```csharp
using EgyptianNames;

var e = new EgyptianNamesEngine();

Console.WriteLine(string.Join(", ", e.Split("محمدأحمدعليحسنالشناوي")));
Console.WriteLine(e.Translate("محمد أحمد علي الشناوي"));
Console.WriteLine(e.Correct("احمد مصطفا عبد الرحيم"));

var name = e.Generate(count: 1, length: 4, gender: Gender.Female, religion: Religion.Muslim)[0];
Console.WriteLine($"{name.Ar}  {name.En}");

Console.WriteLine(e.IsValid("محمد"));   // true
Console.WriteLine(e.IsValid("الله"));   // false — in the index, not a person's name

Console.WriteLine(e.DetectGender("فاطمة محمد علي"));     // first personal token wins
Console.WriteLine(e.DetectReligion("مينا جرجس بطرس"));
```

Full API: [DOCUMENTATION.md](https://github.com/AbdullahAfifyKhalil/egy-names/blob/main/DOCUMENTATION.md). Runnable script: [`examples/csharp/`](https://github.com/AbdullahAfifyKhalil/egy-names/tree/main/examples/csharp).

## Other languages

Same book, other SDKs — no samples here. See the [repo](https://github.com/AbdullahAfifyKhalil/egy-names) and [afify.co/egy-names](https://afify.co/egy-names).

## License

MIT. Copyright (c) 2026 Afify by Abdullah Afify. An Afify open-source project.
