# Egyptian Names (`egy-names`)

A production-grade Egyptian onomastic intelligence library for Java, Kotlin, Scala, and Android.

Powered by **33,117 verified Egyptian name lemmas** and **134,000+ lookup keys**, derived from an engineered dataset of 2.46 million Egyptian student records (11 million+ name tokens) from the Thanawiya Amma cohorts (2024–2026).

Developed by **Abdullah Afify** / **Afify**.

---

## Installation (Maven / Gradle)

### Maven (`pom.xml`)

```xml
<dependency>
    <groupId>com.afify</groupId>
    <artifactId>egy-names</artifactId>
    <version>0.1.0</version>
</dependency>
```

### Gradle (`build.gradle`)

```groovy
implementation 'com.afify:egy-names:0.1.0'
```

---

## Quick Start (Java)

```java
import com.afify.egynames.EgyNames;
import com.afify.egynames.model.Models;

public class App {
    public static void main(String[] args) {
        EgyNames en = new EgyNames();

        // 1. Generate Authentic Egyptian Full Names
        var names = en.generate(3, "male", "muslim");
        for (var n : names) {
            System.out.println(n.ar + "  --  " + n.en);
        }

        // 2. Translation
        System.out.println(en.translate("محمد أحمد علي")); // Mohamed Ahmed Ali
        System.out.println(en.translate("Mohamed Ahmed Ali")); // محمد أحمد علي

        // 3. Split Space-less Concatenated Names
        System.out.println(en.split("محمدأحمدعليحسنالشاذلي")); // [محمد, أحمد, علي, حسن, الشاذلي]

        // 4. Tashkeel & Correction
        System.out.println(en.correct("احمد")); // أحمد
        System.out.println(en.tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن

        // 5. Annotate & Meaning
        var meaning = en.meaning("محمد");
        System.out.println(meaning.get("ar"));

        // 6. Chain Analysis & Inferences
        System.out.println(en.detectGender("مريم إبراهيم حسن"));
        System.out.println(en.detectReligion("جورج بطرس سمير ميخائيل"));
    }
}
```

---

## License & Copyright

**MIT License**

Copyright (c) 2026 **Afify by Abdullah Afify**
