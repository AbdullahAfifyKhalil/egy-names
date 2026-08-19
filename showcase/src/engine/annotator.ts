import { lookup } from "./lookupIndices";
import { NameEntry, NameInfo } from "./types";

export function entryToInfo(entry: NameEntry): NameInfo {
  return {
    ar: entry.ar,
    en: entry.en,
    gender: entry.gender,
    religion: entry.religion,
    role: entry.role,
    frequencyClass: entry.frequency,
    corpusShare: entry.corpusShare,
    tashkeel: entry.tashkeel,
    meaningAr: entry.meaningAr || null,
    meaningEn: entry.meaningEn || null,
    arVariants: [...entry.arVariants],
    enVariants: [...entry.enVariants],
    slotDistribution: [...entry.slotPcts],
  };
}

export function annotateSingle(name: string): NameInfo | null {
  const entry = lookup(name);
  if (!entry) return null;
  return entryToInfo(entry);
}

export function annotate(name: string): NameInfo | null | (NameInfo | null)[] {
  if (!name || !name.trim()) return null;
  const tokens = name.trim().split(/\s+/);
  if (tokens.length === 1) {
    return annotateSingle(tokens[0]);
  }
  return tokens.map((t) => annotateSingle(t));
}
