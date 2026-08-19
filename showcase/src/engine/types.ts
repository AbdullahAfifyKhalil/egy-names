export type Gender = "male" | "female" | "neutral";
export type Religion = "muslim" | "christian" | "neutral";
export type NameRole = "given" | "family";
export type FrequencyClass = "common" | "normal" | "rare";

export interface NameEntry {
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
}

export interface NameInfo {
  ar: string;
  en: string;
  gender: Gender;
  religion: Religion;
  role: NameRole;
  frequencyClass: FrequencyClass;
  corpusShare: number;
  tashkeel: string;
  meaningAr: string | null;
  meaningEn: string | null;
  arVariants: string[];
  enVariants: string[];
  slotDistribution: number[];
}

export interface GeneratedName {
  ar: string;
  en: string;
  partsAr: string[];
  partsEn: string[];
}

export interface ChainPart {
  name: string;
  slot: number;
  role: string;
  detail: string;
}

export interface GenderDetection {
  gender: "male" | "female" | "neutral";
  confidence: number;
}

export interface ReligionDetection {
  religion: "muslim" | "christian" | "neutral";
  confidence: number;
}

export interface RankInfo {
  rank: number;
  percentile: number;
  corpusShare: string;
  description: string;
}

export interface UniquenessScore {
  score: number;
  label:
    | "extremely_common"
    | "common"
    | "moderate"
    | "distinctive"
    | "highly_unique"
    | "unknown";
  note: string;
}
