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

export interface RawNameEntry {
  a: string;
  e: string;
  g: "m" | "f" | "n";
  r: "m" | "c" | "n";
  l: "g" | "f";
  av: string;
  ev: string;
  p: number[];
  tp: number;
  fc: "c" | "n" | "r";
  t: string;
  ma: string;
  me: string;
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
  meaningAr: string;
  meaningEn: string;

  constructor(raw: RawNameEntry) {
    this.ar = raw.a;
    this.en = raw.e;
    this.gender = raw.g === "m" ? Gender.MALE : raw.g === "f" ? Gender.FEMALE : Gender.NEUTRAL;
    this.religion = raw.r === "m" ? Religion.MUSLIM : raw.r === "c" ? Religion.CHRISTIAN : Religion.NEUTRAL;
    this.role = raw.l === "g" ? NameRole.GIVEN : NameRole.FAMILY;
    this.arVariants = raw.av ? raw.av.split("|") : [raw.a];
    this.enVariants = raw.ev ? raw.ev.split("|") : [raw.e];
    this.slotPcts = raw.p;
    this.corpusShare = raw.tp;
    this.frequency = raw.fc === "c" ? FrequencyClass.COMMON : raw.fc === "n" ? FrequencyClass.NORMAL : FrequencyClass.RARE;
    this.tashkeel = raw.t;
    this.meaningAr = raw.ma;
    this.meaningEn = raw.me;
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
  meaning_ar: string | null;
  meaning_en: string | null;
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
    meaning_ar: entry.meaningAr || null,
    meaning_en: entry.meaningEn || null,
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
