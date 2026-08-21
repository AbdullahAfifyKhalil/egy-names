export enum Gender {
  MALE = "male",
  FEMALE = "female",
  NEUTRAL = "neutral",
}

export enum Religion {
  MUSLIM = "muslim",
  CHRISTIAN = "christian",
  NEUTRAL = "neutral",
}

export enum NameRole {
  GIVEN = "given",
  FAMILY = "family",
}

export enum FrequencyClass {
  COMMON = "common", // ≥ 500 occurrences
  NORMAL = "normal", // 10–499 occurrences
  RARE = "rare", // < 10 occurrences
}

export interface PetName {
  ar: string;
  tashkeel: string;
  en: string;
  ipa: string;
}

export interface RawNameEntry {
  a: string;
  e: string;
  g: "m" | "f" | "n";
  r: "m" | "c" | "n";
  l: "g" | "f";
  av?: string;
  ev?: string;
  p: number[];
  tp: number;
  fc: "c" | "n" | "r";
  t: string;
  te?: string;
  is?: string;
  ie?: string;
  ma: string;
  me: string;
  dl?: string;
  dla?: string;
  dlt?: string;
  dle?: string;
  dli?: string;
  rt?: string;
  ot?: string;
  ff?: string;
  ffa?: string;
  ffe?: string;
  tc?: string;
}

export class NameEntry {
  ar: string;
  en: string;
  gender: Gender;
  religion: Religion;
  role: NameRole;
  arVariants: string[];
  enVariants: string[];
  slotPcts: number[];
  corpusShare: number;
  frequency: FrequencyClass;
  tashkeel: string;
  tashkeelStandard: string;
  tashkeelEg: string;
  ipaStandard: string;
  ipaEg: string;
  meaningAr: string;
  meaningEn: string;
  dallaa: string[];
  dallaaAr: string[];
  dallaaTashkeel: string[];
  dallaaEn: string[];
  dallaaIpa: string[];
  root: string;
  originType: string;
  famousFigures: string[];
  famousFiguresAr: string[];
  famousFiguresEn: string[];
  trendCategory: string;

  constructor(raw: RawNameEntry) {
    this.ar = raw.a;
    this.en = raw.e;
    this.gender = raw.g === "m" ? Gender.MALE : raw.g === "f" ? Gender.FEMALE : Gender.NEUTRAL;
    this.religion = raw.r === "m" ? Religion.MUSLIM : raw.r === "c" ? Religion.CHRISTIAN : Religion.NEUTRAL;
    this.role = raw.l === "g" ? NameRole.GIVEN : NameRole.FAMILY;
    this.arVariants = raw.av ? raw.av.split("|") : [raw.a];
    this.enVariants = raw.ev ? raw.ev.split("|") : [raw.e];
    this.slotPcts = raw.p || [0, 0, 0, 0, 0, 0, 0, 0];
    this.corpusShare = raw.tp || 0;
    this.frequency = raw.fc === "c" ? FrequencyClass.COMMON : raw.fc === "n" ? FrequencyClass.NORMAL : FrequencyClass.RARE;
    this.tashkeel = raw.t || raw.a;
    this.tashkeelStandard = raw.t || raw.a;
    this.tashkeelEg = raw.te || raw.t || raw.a;
    this.ipaStandard = raw.is || "";
    this.ipaEg = raw.ie || "";
    this.meaningAr = raw.ma || "";
    this.meaningEn = raw.me || "";

    const dlaRaw = raw.dla || raw.dl || "";
    this.dallaaAr = dlaRaw ? dlaRaw.split("|") : [];
    this.dallaa = this.dallaaAr;
    this.dallaaTashkeel = raw.dlt ? raw.dlt.split("|") : [];
    this.dallaaEn = raw.dle ? raw.dle.split("|") : [];
    this.dallaaIpa = raw.dli ? raw.dli.split("|") : [];

    this.root = raw.rt || "N/A";
    this.originType = raw.ot || "arabic_classical";

    const ffaRaw = raw.ffa || raw.ff || "";
    this.famousFiguresAr = ffaRaw ? ffaRaw.split("|") : [];
    this.famousFigures = this.famousFiguresAr;
    this.famousFiguresEn = raw.ffe ? raw.ffe.split("|") : [];

    this.trendCategory = raw.tc || "classic_timeless";
  }
}

export interface NameInfo {
  ar: string;
  en: string;
  gender: string;
  religion: string;
  role: string;
  frequency_class: string;
  corpus_share: number;
  tashkeel: string;
  tashkeel_standard: string;
  tashkeel_eg: string;
  ipa_standard: string;
  ipa_eg: string;
  meaning_ar: string | null;
  meaning_en: string | null;
  dallaa: string[];
  dallaa_ar: string[];
  dallaa_tashkeel: string[];
  dallaa_en: string[];
  dallaa_ipa: string[];
  root: string;
  origin_type: string;
  famous_figures: string[];
  famous_figures_ar: string[];
  famous_figures_en: string[];
  trend_category: string;
  ar_variants: string[];
  en_variants: string[];
  slot_distribution: number[];
}

export function toNameInfo(entry: NameEntry): NameInfo {
  return {
    ar: entry.ar,
    en: entry.en,
    gender: entry.gender,
    religion: entry.religion,
    role: entry.role,
    frequency_class: entry.frequency,
    corpus_share: entry.corpusShare,
    tashkeel: entry.tashkeel,
    tashkeel_standard: entry.tashkeelStandard,
    tashkeel_eg: entry.tashkeelEg,
    ipa_standard: entry.ipaStandard,
    ipa_eg: entry.ipaEg,
    meaning_ar: entry.meaningAr || null,
    meaning_en: entry.meaningEn || null,
    dallaa: [...entry.dallaaAr],
    dallaa_ar: [...entry.dallaaAr],
    dallaa_tashkeel: [...entry.dallaaTashkeel],
    dallaa_en: [...entry.dallaaEn],
    dallaa_ipa: [...entry.dallaaIpa],
    root: entry.root,
    origin_type: entry.originType,
    famous_figures: [...entry.famousFiguresAr],
    famous_figures_ar: [...entry.famousFiguresAr],
    famous_figures_en: [...entry.famousFiguresEn],
    trend_category: entry.trendCategory,
    ar_variants: [...entry.arVariants],
    en_variants: [...entry.enVariants],
    slot_distribution: [...entry.slotPcts],
  };
}

export interface GeneratedName {
  ar: string;
  en: string;
  parts_ar: string[];
  parts_en: string[];
}

export interface ChainPart {
  name: string;
  slot: number;
  role: string;
  detail: string;
}

export interface GenderDetection {
  gender: string;
  confidence: number;
}

export interface ReligionDetection {
  religion: string;
  confidence: number;
}

export interface RankInfo {
  rank: number;
  percentile: number;
  corpus_share: string;
  description: string;
}

export interface UniquenessScore {
  score: number;
  label: string;
  note: string;
}

export interface Fingerprint {
  name_ar: string;
  name_en: string;
  type: string;
  slots: Record<string, number>;
  corpus_share: number;
  description: string;
}

export interface FormatResult {
  first?: string;
  last?: string;
}

export interface CorpusStats {
  total_names: number;
  given_names: number;
  family_names: number;
  male_names: number;
  female_names: number;
  [key: string]: unknown;
}
