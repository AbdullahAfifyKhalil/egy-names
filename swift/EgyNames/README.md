# EgyNames (Swift)

Egyptian names engine for Swift (iOS / macOS). Same book as the other SDKs — 44,626 lemmas, offline.

A legal Egyptian name is a patronymic chain, not a first name and a last name. This package generates, translates, splits, and corrects those chains.

**[afify.co/egy-names](https://afify.co/egy-names)** — origin, process, insights, lab, examples, and demo.

**[The Secret Code of Egyptian Names](https://medium.com/@abdullah.afify/the-secret-code-of-egyptian-names-how-we-engineered-a-14-dimensional-nlp-engine-5205db7f04f4)** — how the engine was built.

## Accuracy

The book comes from real records. Some names will still come back wrong — a rare spelling, a name the catalog has never seen. If you find one, [open an issue](https://github.com/AbdullahAfifyKhalil/egy-names/issues).

## Install

Add in Xcode or `Package.swift`:

```swift
.package(url: "https://github.com/AbdullahAfifyKhalil/egy-names.git", from: "0.3.5")
```

The root `Package.swift` points at `swift/EgyNames/`.

## Use

```swift
import EgyNames

let e = EgyptianNames()

print(e.split("محمدأحمدعليحسنالشناوي"))
print(e.translate("محمد أحمد علي الشناوي"))
print(e.correct("احمد مصطفا عبد الرحيم"))

let name = e.generate(count: 1, length: 4, gender: "female", religion: "muslim")[0]
print("\(name.ar)  \(name.en)")

print(e.isValid("محمد"))   // true
print(e.isValid("الله"))   // false — in the index, not a person's name

print(e.detectGender("فاطمة محمد علي"))     // first personal token wins
print(e.detectReligion("مينا جرجس بطرس"))
```

Full API: [DOCUMENTATION.md](https://github.com/AbdullahAfifyKhalil/egy-names/blob/main/DOCUMENTATION.md). Runnable script: [`examples/swift/`](https://github.com/AbdullahAfifyKhalil/egy-names/tree/main/examples/swift).

## Other languages

Same book, other SDKs — no samples here. See the [repo](https://github.com/AbdullahAfifyKhalil/egy-names) and [afify.co/egy-names](https://afify.co/egy-names).

## License

MIT. Copyright (c) 2026 Afify by Abdullah Afify. An Afify open-source project.
