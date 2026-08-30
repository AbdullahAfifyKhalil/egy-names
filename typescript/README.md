# egy-names (TypeScript)

Egyptian names engine for Node and the browser. Same book as the other SDKs — 44,626 lemmas, offline.

A legal Egyptian name is a patronymic chain, not a first name and a last name. This package generates, translates, splits, and corrects those chains.

**[afify.co/egy-names](https://afify.co/egy-names)** — origin, process, insights, lab, examples, and demo.

**[The Secret Code of Egyptian Names](https://medium.com/@abdullah.afify/the-secret-code-of-egyptian-names-how-we-engineered-a-14-dimensional-nlp-engine-5205db7f04f4)** — how the engine was built.

## Accuracy

The book comes from real records. Some names will still come back wrong — a rare spelling, a name the catalog has never seen. If you find one, [open an issue](https://github.com/AbdullahAfifyKhalil/egy-names/issues).

## Install

```bash
npm install egy-names@0.3.5
```

## Use

```ts
import { EgyNames } from "egy-names";

const e = new EgyNames();

console.log(e.split("محمدأحمدعليحسنالشناوي"));
// ['محمد', 'أحمد', 'علي', 'حسن', 'الشناوي']

console.log(e.translate("محمد أحمد علي الشناوي"));
// Mohamed Ahmed Ali Elshenawy

console.log(e.correct("احمد مصطفا عبد الرحيم"));
// أحمد مصطفى عبدالرحيم

const name = e.generate({ gender: "female", religion: "muslim", length: 4 })[0];
console.log(name.ar, name.en);

console.log(e.isValid("محمد"));   // true
console.log(e.isValid("الله"));   // false — in the index, not a person's name

console.log(e.detectGender("فاطمة محمد علي"));     // first personal token wins
console.log(e.detectReligion("مينا جرجس بطرس"));
```

Full API: [DOCUMENTATION.md](https://github.com/AbdullahAfifyKhalil/egy-names/blob/main/DOCUMENTATION.md). Runnable script: [`examples/typescript/`](https://github.com/AbdullahAfifyKhalil/egy-names/tree/main/examples/typescript).

## Other languages

Same book, other SDKs — no samples here. See the [repo](https://github.com/AbdullahAfifyKhalil/egy-names) and [afify.co/egy-names](https://afify.co/egy-names).

## License

MIT. Copyright (c) 2026 Afify by Abdullah Afify. An Afify open-source project.
