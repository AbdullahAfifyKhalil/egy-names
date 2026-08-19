export type Lang = "en" | "ar";

export interface Translations {
  brandSubtitle: string;
  engineLive: string;
  copyInstall: string;
  installCopied: string;
  heroTag: string;
  heroTitle: string;
  heroDesc: string;
  statLemmas: string;
  statTokens: string;
  statStudents: string;
  statKeys: string;

  // Tabs
  tabGenerator: string;
  tabTranslator: string;
  tabSplitter: string;
  tabInspector: string;
  tabCorrector: string;
  tabChain: string;
  tabSearch: string;
  tabPlayground: string;

  // Generator
  genTitle: string;
  genDesc: string;
  genderLabel: string;
  genderAll: string;
  genderMale: string;
  genderFemale: string;
  religionLabel: string;
  religionAll: string;
  religionMuslim: string;
  religionChristian: string;
  freqLabel: string;
  freqAll: string;
  freqCommon: string;
  freqNormal: string;
  freqRare: string;
  lengthLabel: string;
  countLabel: string;
  familySurnameToggle: string;
  btnGenerate: string;
  genOutputHeader: string;

  // Translator
  transTitle: string;
  transDesc: string;
  tryPresets: string;
  arToEnHeader: string;
  enToArHeader: string;
  arInputPlaceholder: string;
  enInputPlaceholder: string;
  transTokensHeader: string;
  btnCopy: string;
  enOutputLabel: string;
  arOutputLabel: string;

  // Splitter
  splitTitle: string;
  splitDesc: string;
  splitInputLabel: string;
  splitPlaceholder: string;
  splitTokensHeader: string;
  btnCopySplit: string;

  // Inspector
  inspectTitle: string;
  inspectDesc: string;
  popularLookups: string;
  inspectInputLabel: string;
  inspectPlaceholder: string;
  inspectEmptyPrompt: string;
  etymologyHeader: string;
  nationalRankHeader: string;
  percentileRankLabel: string;
  corpusShareLabel: string;
  slotProbHeader: string;
  variantsHeader: string;

  // Corrector
  correctTitle: string;
  correctDesc: string;
  correctInputLabel: string;
  correctPlaceholder: string;
  standardizedHeader: string;
  tashkeelHeader: string;

  // Chain AI
  chainTitle: string;
  chainDesc: string;
  chainInputLabel: string;
  chainPlaceholder: string;
  structureHeader: string;
  genderDetectionHeader: string;
  religionDetectionHeader: string;
  uniquenessHeader: string;

  // Search
  searchTitle: string;
  searchDesc: string;
  searchQueryLabel: string;
  searchPrefixLabel: string;
  roleLabel: string;
  roleAll: string;
  roleGiven: string;
  roleFamily: string;
  thNum: string;
  thArabic: string;
  thEnglish: string;
  thGender: string;
  thReligion: string;
  thRole: string;

  // Playground
  playgroundTitle: string;
  playgroundDesc: string;
  btnCopyCode: string;

  // Footer
  footerLine1: string;
  footerLine2: string;

  // Terms & Labels
  terms: {
    male: string;
    female: string;
    unisex: string;
    muslim: string;
    christian: string;
    neutral: string;
    given: string;
    family: string;
    father: string;
    grandfather: string;
    great_grandfather: string;
    common: string;
    normal: string;
    rare: string;
    slot: string;
    slot1: string;
    slot2: string;
    slot3: string;
    slot4: string;
    slot5: string;
    slot6: string;
    slot7: string;
    slot8: string;
    copied: string;
    resultsCount: (n: number) => string;
  };
}

export const DICTIONARY: Record<Lang, Translations> = {
  en: {
    brandSubtitle: "By Afify • Abdullah Afify",
    engineLive: "Online",
    copyInstall: "pip / npm install egy-names",
    installCopied: "Install command copied to clipboard.",
    heroTag: "Egyptian Onomastic Dataset & NLP Suite",
    heroTitle: "Egyptian Name Intelligence Engine",
    heroDesc:
      "A high-performance algorithmic suite for patronymic name generation, transliteration, space-less dynamic programming segmentation, etymology, and demographic classification.",
    statLemmas: "Verified Lemmas",
    statTokens: "Corpus Tokens",
    statStudents: "Student Records (2024–2026)",
    statKeys: "Index Lookup Keys",

    tabGenerator: "Generator",
    tabTranslator: "Translator",
    tabSplitter: "Segmentation",
    tabInspector: "Etymology & Stats",
    tabCorrector: "Orthography & Tashkeel",
    tabChain: "Chain Analysis",
    tabSearch: "Corpus Explorer",
    tabPlayground: "API & SDKs",

    genTitle: "Full Name Generation",
    genDesc:
      "Generates authentic full names by sampling from positional probability distributions derived from national corpus records.",
    genderLabel: "Gender",
    genderAll: "All",
    genderMale: "Male",
    genderFemale: "Female",
    religionLabel: "Cultural Context",
    religionAll: "All",
    religionMuslim: "Muslim",
    religionChristian: "Christian",
    freqLabel: "Frequency Tier",
    freqAll: "All",
    freqCommon: "Common",
    freqNormal: "Normal",
    freqRare: "Rare",
    lengthLabel: "Chain Length",
    countLabel: "Quantity",
    familySurnameToggle: "Include family surname at chain termination",
    btnGenerate: "Generate Names",
    genOutputHeader: "Generated Output",

    transTitle: "Bi-Directional Transliteration",
    transDesc:
      "Deterministic and phonetic mapping between Arabic orthography and standardized English transliterations.",
    tryPresets: "Examples:",
    arToEnHeader: "Arabic to English",
    enToArHeader: "English to Arabic",
    arInputPlaceholder: "Enter Arabic full name...",
    enInputPlaceholder: "Enter English transliterated name...",
    transTokensHeader: "Token Decomposition",
    btnCopy: "Copy",
    enOutputLabel: "English Transliteration",
    arOutputLabel: "Arabic Representation",

    splitTitle: "Dynamic Programming Segmentation",
    splitDesc:
      "Splits unspaced or concatenated Arabic names into canonical constituent tokens using cost-minimizing dynamic programming.",
    splitInputLabel: "Input Name String",
    splitPlaceholder: "Enter concatenated or spaced name...",
    splitTokensHeader: "Extracted Name Components",
    btnCopySplit: "Copy Tokenized",

    inspectTitle: "Linguistic & Statistical Analysis",
    inspectDesc:
      "Inspect etymological roots, national popularity ranking, and positional distribution across patronymic slots.",
    popularLookups: "Examples:",
    inspectInputLabel: "Name Lookup",
    inspectPlaceholder: "Search lemma name...",
    inspectEmptyPrompt: "Enter any name above to view corpus distribution and meaning.",
    etymologyHeader: "Etymology & Meaning",
    nationalRankHeader: "Corpus Rank & Popularity",
    percentileRankLabel: "Percentile",
    corpusShareLabel: "Corpus Frequency",
    slotProbHeader: "Positional Distribution by Slot",
    variantsHeader: "Orthographic Variants & Transliterations",

    correctTitle: "Orthographic Normalization & Tashkeel",
    correctDesc:
      "Resolves common typos, dialectal spelling variations, and generates fully diacritized Arabic forms.",
    correctInputLabel: "Input Name",
    correctPlaceholder: "Enter name with spelling variations or typos...",
    standardizedHeader: "Canonical Normalized Form",
    tashkeelHeader: "Diacritized Form (Tashkeel)",

    chainTitle: "Patronymic Structure & Demographic Inference",
    chainDesc:
      "Analyzes generational hierarchy and computes probabilistic gender, cultural context, and uniqueness metrics.",
    chainInputLabel: "Patronymic Chain",
    chainPlaceholder: "Enter complete 3 to 5 part name...",
    structureHeader: "Generational Structure",
    genderDetectionHeader: "Gender Classification",
    religionDetectionHeader: "Cultural Background Inference",
    uniquenessHeader: "Name Uniqueness Index",

    searchTitle: "Corpus Database Query",
    searchDesc:
      "Direct filtered queries across all 33,117 lemmas in the indexed national database.",
    searchQueryLabel: "Contains",
    searchPrefixLabel: "Prefix",
    roleLabel: "Role",
    roleAll: "All",
    roleGiven: "Given Name",
    roleFamily: "Family Name",
    thNum: "Index",
    thArabic: "Arabic (Diacritized)",
    thEnglish: "English",
    thGender: "Gender",
    thReligion: "Context",
    thRole: "Role",

    playgroundTitle: "Developer SDK Reference",
    playgroundDesc:
      "Production-ready integration snippets for all supported runtime environments.",
    btnCopyCode: "Copy Code",

    footerLine1: "egy-names — Open-source Egyptian onomastic intelligence library.",
    footerLine2: "MIT License • Developed by Abdullah Afify (Afify).",

    terms: {
      male: "Male",
      female: "Female",
      unisex: "Unisex",
      muslim: "Muslim",
      christian: "Christian",
      neutral: "General",
      given: "Given Name",
      family: "Family Name",
      father: "Father",
      grandfather: "Grandfather",
      great_grandfather: "Great-Grandfather",
      common: "Common",
      normal: "Normal",
      rare: "Rare",
      slot: "Slot",
      slot1: "1st (Given)",
      slot2: "2nd (Father)",
      slot3: "3rd (Grandfather)",
      slot4: "4th",
      slot5: "5th",
      slot6: "6th",
      slot7: "7th",
      slot8: "8th+",
      copied: "Copied: ",
      resultsCount: (n: number) => `${n} results displayed`,
    },
  },

  ar: {
    brandSubtitle: "بواسطة عفيفي • عبد الله عفيفي",
    engineLive: "متصل",
    copyInstall: "pip / npm install egy-names",
    installCopied: "تم نسخ أمر التثبيت.",
    heroTag: "المنظومة الوطنية لذكاء وتصنيف الأسماء المصرية",
    heroTitle: "محرك معالجة وفحص الأسماء المصرية",
    heroDesc:
      "مكتبة خوارزمية عالية الكفاءة لتوليد سلاسل النسب، الترجمة الصوتية، تقسيم النصوص المتصلة بالبرمجة الديناميكية، والتأصيل اللغوي والديموغرافي.",
    statLemmas: "اسم موثق ومعياري",
    statTokens: "اسم في المدونة الوطنية",
    statStudents: "سجل طالب (2024–2026)",
    statKeys: "مفتاح بحث وترجمة",

    tabGenerator: "توليد الأسماء",
    tabTranslator: "الترجمة والتعريب",
    tabSplitter: "التقسيم الآلي",
    tabInspector: "المعاني والإحصاء",
    tabCorrector: "التصحيح والتشكيل",
    tabChain: "تحليل سلاسل النسب",
    tabSearch: "مستكشف المدونة",
    tabPlayground: "حزم التطوير (SDK)",

    genTitle: "توليد سلاسل الأسماء الأصيلة",
    genDesc:
      "توليد سلاسل أسماء مركبة وفق التوزيعات الاحتمالية الحقيقية المستخرجة من السجلات الوطنية.",
    genderLabel: "النوع",
    genderAll: "الكل",
    genderMale: "ذكور",
    genderFemale: "إناث",
    religionLabel: "السياق الثقافي",
    religionAll: "الكل",
    religionMuslim: "إسلامي",
    religionChristian: "مسيحي",
    freqLabel: "درجة الشيوع",
    freqAll: "الكل",
    freqCommon: "شائع",
    freqNormal: "متوسط",
    freqRare: "نادر",
    lengthLabel: "طول السلسلة",
    countLabel: "العدد",
    familySurnameToggle: "إلحاق اسم عائلة / لقب في نهاية السلسلة",
    btnGenerate: "توليد الأسماء",
    genOutputHeader: "النتائج المولدة",

    transTitle: "الترجمة الصوتية ثنائية الاتجاه",
    transDesc:
      "مطابقة صوتية ومعيارية دقيقة بين الرسم العربي والترجمة الصوتية بالإنجليزية.",
    tryPresets: "أمثلة:",
    arToEnHeader: "من العربية إلى الإنجليزية",
    enToArHeader: "من الإنجليزية إلى العربية",
    arInputPlaceholder: "أدخل الاسم بالعربية...",
    enInputPlaceholder: "أدخل الاسم بالإنجليزية...",
    transTokensHeader: "تفكيك الأجزاء",
    btnCopy: "نسخ",
    enOutputLabel: "الصيغة الإنجليزية",
    arOutputLabel: "الصيغة العربية",

    splitTitle: "تقسيم الأسماء المتصلة بالبرمجة الديناميكية",
    splitDesc:
      "فصل وتفكيك الأسماء المكتوبة بدون مسافات إلى مفرداتها الأصلية بدقة خوارزمية عالية.",
    splitInputLabel: "النص المدخل",
    splitPlaceholder: "أدخل اسماً متصلاً أو مركباً...",
    splitTokensHeader: "المفردات المستخرجة",
    btnCopySplit: "نسخ بعد الفصل",

    inspectTitle: "التحليل المعجمي والإحصائي",
    inspectDesc:
      "استعراض المعنى اللغوي والجذر، الترتيب الوطني للشيوع، وتوزيع مواضع الاسم في سلاسل النسب.",
    popularLookups: "أمثلة:",
    inspectInputLabel: "البحث عن اسم",
    inspectPlaceholder: "ابحث عن أي اسم...",
    inspectEmptyPrompt: "أدخل اسماً أعلاه لعرض بياناته وإحصائياته الوطنية.",
    etymologyHeader: "المعنى والتأصيل اللغوي",
    nationalRankHeader: "الترتيب والشيوع الوطني",
    percentileRankLabel: "الشريحة المئوية",
    corpusShareLabel: "نسبة الحضور",
    slotProbHeader: "توزيع موضع الاسم في السلاسل",
    variantsHeader: "الصيغ والبدائل الصوتية",

    correctTitle: "التصحيح الإملائي وضبط التشكيل",
    correctDesc:
      "معالجة الأخطاء الشائعة والكتابة غير المعيارية وضبط التشكيل الدقيق للأسماء.",
    correctInputLabel: "الاسم المراد تصحيحه",
    correctPlaceholder: "أدخل اسماً به أخطاء أو كتابة عامية...",
    standardizedHeader: "الصيغة المعيارية المصححة",
    tashkeelHeader: "الصيغة المشكولة بالكامل",

    chainTitle: "بنية النسب والاستنتاج الديموغرافي",
    chainDesc:
      "تحليل طبقات الأجيال واستنتاج النوع والسياق الديني ومؤشر تفرد السلسلة.",
    chainInputLabel: "سلسلة النسب",
    chainPlaceholder: "أدخل اسماً ثلاثياً أو رباعياً أو خماسياً...",
    structureHeader: "طبقات الأجيال",
    genderDetectionHeader: "تصنيف النوع الاحتمالي",
    religionDetectionHeader: "استنتاج السياق الثقافي",
    uniquenessHeader: "مؤشر تفرد وندرة الاسم",

    searchTitle: "استعلام قاعدة البيانات الوطنية",
    searchDesc:
      "بحث وفلترة فورية متعددة المعايير في كامل الـ 33,117 اسماً مصرياً معتمداً.",
    searchQueryLabel: "يحتوي على",
    searchPrefixLabel: "يبدأ بـ",
    roleLabel: "النوع",
    roleAll: "الكل",
    roleGiven: "اسم شخصي",
    roleFamily: "اسم عائلة / لقب",
    thNum: "الرقم",
    thArabic: "الاسم (مشكولاً)",
    thEnglish: "الإنجليزية",
    thGender: "النوع",
    thReligion: "السياق",
    thRole: "التصنيف",

    playgroundTitle: "حزم وأدوات الربط البرمجي",
    playgroundDesc:
      "نماذج وأكواد جاهزة للاستخدام عبر بيئات التشغيل الخمس المدعومة.",
    btnCopyCode: "نسخ الكود",

    footerLine1: "egy-names — مكتبة مفتوحة المصدر لمعالجة وتصنيف الأسماء المصرية.",
    footerLine2: "ترخيص MIT • تطوير عبد الله عفيفي (Afify).",

    terms: {
      male: "ذكر",
      female: "أنثى",
      unisex: "مشترك",
      muslim: "إسلامي",
      christian: "مسيحي",
      neutral: "عام",
      given: "اسم شخصي",
      family: "اسم عائلة",
      father: "اسم الأب",
      grandfather: "اسم الجد",
      great_grandfather: "اسم والد الجد",
      common: "شائع",
      normal: "متوسط",
      rare: "نادر",
      slot: "الموضع",
      slot1: "الأول (الشخصي)",
      slot2: "الثاني (الأب)",
      slot3: "الثالث (الجد)",
      slot4: "الرابع",
      slot5: "الخامس",
      slot6: "السادس",
      slot7: "السابع",
      slot8: "الثامن وأكثر",
      copied: "تم النسخ: ",
      resultsCount: (n: number) => `تم عرض ${n} نتيجة`,
    },
  },
};
