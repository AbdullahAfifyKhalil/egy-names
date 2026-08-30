# egy-names (Java)

Egyptian names engine for Java and Kotlin. Same book as the other SDKs — 44,626 lemmas, offline.

A legal Egyptian name is a patronymic chain, not a first name and a last name. This package generates, translates, splits, and corrects those chains.

**[afify.co/egy-names](https://afify.co/egy-names)** — origin, process, insights, lab, examples, and demo.

**[The Secret Code of Egyptian Names](https://medium.com/@abdullah.afify/the-secret-code-of-egyptian-names-how-we-engineered-a-14-dimensional-nlp-engine-5205db7f04f4)** — how the engine was built.

## Accuracy

The book comes from real records. Some names will still come back wrong — a rare spelling, a name the catalog has never seen. If you find one, [open an issue](https://github.com/AbdullahAfifyKhalil/egy-names/issues).

## Install

[JitPack](https://jitpack.io/#AbdullahAfifyKhalil/egy-names/v0.3.5):

```kotlin
implementation("com.github.AbdullahAfifyKhalil:egy-names:v0.3.5")
```

## Use

```java
import com.afify.egynames.EgyptianNames;

EgyptianNames e = new EgyptianNames();

System.out.println(e.split("محمدأحمدعليحسنالشناوي"));
System.out.println(e.translate("محمد أحمد علي الشناوي"));
System.out.println(e.correct("احمد مصطفا عبد الرحيم"));

var name = e.generate(1, "female", "muslim").get(0);
System.out.println(name.ar + "  " + name.en);

System.out.println(e.isValid("محمد"));   // true
System.out.println(e.isValid("الله"));   // false — in the index, not a person's name

System.out.println(e.detectGender("فاطمة محمد علي"));     // first personal token wins
System.out.println(e.detectReligion("مينا جرجس بطرس"));
```

Full API: [DOCUMENTATION.md](https://github.com/AbdullahAfifyKhalil/egy-names/blob/main/DOCUMENTATION.md). Runnable script: [`examples/java/`](https://github.com/AbdullahAfifyKhalil/egy-names/tree/main/examples/java).

## Other languages

Same book, other SDKs — no samples here. See the [repo](https://github.com/AbdullahAfifyKhalil/egy-names) and [afify.co/egy-names](https://afify.co/egy-names).

## License

MIT. Copyright (c) 2026 Afify by Abdullah Afify. An Afify open-source project.
