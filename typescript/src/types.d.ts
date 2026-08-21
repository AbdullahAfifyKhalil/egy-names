export declare enum Gender {
    MALE = "male",
    FEMALE = "female",
    NEUTRAL = "neutral"
}
export declare enum Religion {
    MUSLIM = "muslim",
    CHRISTIAN = "christian",
    NEUTRAL = "neutral"
}
export declare enum NameRole {
    GIVEN = "given",
    FAMILY = "family"
}
export declare enum FrequencyClass {
    COMMON = "common",// ≥ 500 occurrences
    NORMAL = "normal",// 10–499 occurrences
    RARE = "rare"
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
export declare class NameEntry {
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
    constructor(raw: RawNameEntry);
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
export declare function toNameInfo(entry: NameEntry): NameInfo;
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
//# sourceMappingURL=types.d.ts.map