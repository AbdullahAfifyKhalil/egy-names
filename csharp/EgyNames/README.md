# Egyptian Names (`egy-names`)

A production-grade Egyptian onomastic intelligence library for .NET (C#, F#, VB.NET).

Powered by **33,117 verified Egyptian name lemmas** and **134,000+ lookup keys**, derived from an engineered dataset of 2.46 million Egyptian student records (11 million+ name tokens) from the Thanawiya Amma cohorts (2024–2026).

Developed by **Abdullah Afify** / **Afify**.

---

## Installation (NuGet)

```bash
dotnet add package egy-names
```

---

## Quick Start (C#)

```csharp
using EgyNames;

var engine = new EgyNamesEngine();

// 1. Generate Authentic Egyptian Full Names
var names = engine.Generate(count: 3, gender: Gender.Male, religion: Religion.Muslim);
foreach (var n in names)
{
    Console.WriteLine($"{n.Ar}  --  {n.En}");
}

// 2. Translation
Console.WriteLine(engine.Translate("محمد أحمد علي")); // Mohamed Ahmed Ali
Console.WriteLine(engine.Translate("Mohamed Ahmed Ali")); // محمد أحمد علي

// 3. Split Concatenated Space-less Names (DP Algorithm)
var splitResult = engine.Split("محمدأحمدعليحسنالشاذلي");
Console.WriteLine(string.Join(", ", splitResult)); // محمد, أحمد, علي, حسن, الشاذلي

// 4. Tashkeel & Correction
Console.WriteLine(engine.Correct("احمد")); // أحمد
Console.WriteLine(engine.Tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن

// 5. Annotate & Meaning
var meaning = engine.Meaning("محمد");
Console.WriteLine(meaning?.Ar);

// 6. Chain Analysis & Inferences
Console.WriteLine(engine.DetectGender("مريم إبراهيم حسن"));
Console.WriteLine(engine.DetectReligion("جورج بطرس سمير ميخائيل"));
```

---

## License & Copyright

**MIT License**

Copyright (c) 2026 **Afify by Abdullah Afify**
