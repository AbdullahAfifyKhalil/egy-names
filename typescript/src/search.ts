import { getAll, isArabic, normalizeAr, normalizeEn } from "./lookupIndices";
import { Gender, Religion, NameRole, FrequencyClass, NameInfo, toNameInfo } from "./types";

export function search(options: {
  gender?: string;
  religion?: string;
  role?: string;
  frequency?: string;
  startsWith?: string;
  endsWith?: string;
  contains?: string;
  minCorpusShare?: number;
  maxResults?: number;
  sortBy?: "corpus_share" | "alphabetical" | "rank";
}): NameInfo[] {
  const entries = getAll();

  let g: Gender | undefined;
  if (options.gender === "male") g = Gender.MALE;
  if (options.gender === "female") g = Gender.FEMALE;

  let r: Religion | undefined;
  if (options.religion === "muslim") r = Religion.MUSLIM;
  if (options.religion === "christian") r = Religion.CHRISTIAN;

  let rl: NameRole | undefined;
  if (options.role === "given") rl = NameRole.GIVEN;
  if (options.role === "family") rl = NameRole.FAMILY;

  let f: FrequencyClass | undefined;
  if (options.frequency === "common") f = FrequencyClass.COMMON;
  if (options.frequency === "normal") f = FrequencyClass.NORMAL;
  if (options.frequency === "rare") f = FrequencyClass.RARE;

  const prefixAr = options.startsWith && isArabic(options.startsWith);
  const suffixAr = options.endsWith && isArabic(options.endsWith);
  const containsAr = options.contains && isArabic(options.contains);

  let filtered = entries.filter((e) => {
    if (g !== undefined && e.gender !== g && e.gender !== Gender.NEUTRAL) return false;
    if (r !== undefined && e.religion !== r && e.religion !== Religion.NEUTRAL) return false;
    if (rl !== undefined && e.role !== rl) return false;
    if (f !== undefined && e.frequency !== f) return false;
    if (options.minCorpusShare !== undefined && e.corpusShare < options.minCorpusShare) return false;

    if (options.startsWith) {
      if (prefixAr) {
        if (!normalizeAr(e.ar).startsWith(normalizeAr(options.startsWith))) return false;
      } else {
        if (!normalizeEn(e.en).startsWith(normalizeEn(options.startsWith))) return false;
      }
    }

    if (options.endsWith) {
      if (suffixAr) {
        if (!normalizeAr(e.ar).endsWith(normalizeAr(options.endsWith))) return false;
      } else {
        if (!normalizeEn(e.en).endsWith(normalizeEn(options.endsWith))) return false;
      }
    }

    if (options.contains) {
      if (containsAr) {
        if (!normalizeAr(e.ar).includes(normalizeAr(options.contains))) return false;
      } else {
        if (!normalizeEn(e.en).includes(normalizeEn(options.contains))) return false;
      }
    }

    return true;
  });

  const sortBy = options.sortBy || "corpus_share";
  if (sortBy === "alphabetical") {
    filtered.sort((a, b) => a.ar.localeCompare(b.ar));
  } else {
    filtered.sort((a, b) => b.corpusShare - a.corpusShare);
  }

  const maxResults = options.maxResults ?? 50;
  return filtered.slice(0, maxResults).map(toNameInfo);
}
