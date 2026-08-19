import { entryToInfo } from "./annotator";
import { getAll, isArabic, normalizeAr, normalizeEn } from "./lookupIndices";
import {
  FrequencyClass,
  Gender,
  NameEntry,
  NameInfo,
  NameRole,
  Religion,
} from "./types";

export function search(filters?: {
  gender?: Gender | string;
  religion?: Religion | string;
  role?: NameRole | string;
  frequency?: FrequencyClass | string;
  startsWith?: string;
  endsWith?: string;
  contains?: string;
  minCorpusShare?: number;
  maxResults?: number;
  sortBy?: "corpus_share" | "alphabetical";
}): NameInfo[] {
  const entries = getAll();
  const maxResults = filters?.maxResults || 50;
  const sortBy = filters?.sortBy || "corpus_share";

  const prefixAr = filters?.startsWith ? isArabic(filters.startsWith) : false;
  const suffixAr = filters?.endsWith ? isArabic(filters.endsWith) : false;
  const containsAr = filters?.contains ? isArabic(filters.contains) : false;

  let results: NameEntry[] = entries.filter((e) => {
    if (filters?.gender && e.gender !== filters.gender && e.gender !== "neutral")
      return false;
    if (
      filters?.religion &&
      e.religion !== filters.religion &&
      e.religion !== "neutral"
    )
      return false;
    if (filters?.role && e.role !== filters.role) return false;
    if (filters?.frequency && e.frequency !== filters.frequency) return false;
    if (
      filters?.minCorpusShare !== undefined &&
      e.corpusShare < filters.minCorpusShare
    )
      return false;

    if (filters?.startsWith) {
      if (prefixAr) {
        if (!normalizeAr(e.ar).startsWith(normalizeAr(filters.startsWith)))
          return false;
      } else {
        if (!normalizeEn(e.en).startsWith(normalizeEn(filters.startsWith)))
          return false;
      }
    }

    if (filters?.endsWith) {
      if (suffixAr) {
        if (!normalizeAr(e.ar).endsWith(normalizeAr(filters.endsWith)))
          return false;
      } else {
        if (!normalizeEn(e.en).endsWith(normalizeEn(filters.endsWith)))
          return false;
      }
    }

    if (filters?.contains) {
      if (containsAr) {
        if (!normalizeAr(e.ar).includes(normalizeAr(filters.contains)))
          return false;
      } else {
        if (!normalizeEn(e.en).includes(normalizeEn(filters.contains)))
          return false;
      }
    }

    return true;
  });

  if (sortBy === "alphabetical") {
    results.sort((a, b) => a.ar.localeCompare(b.ar, "ar"));
  } else {
    results.sort((a, b) => b.corpusShare - a.corpusShare);
  }

  return results.slice(0, maxResults).map(entryToInfo);
}
