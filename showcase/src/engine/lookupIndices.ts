import { getDataBundleSync } from "./data";
import { NameEntry } from "./types";

let arIndex: Map<string, NameEntry> = new Map();
let enIndex: Map<string, NameEntry> = new Map();
let arNormIndex: Map<string, NameEntry> = new Map();
let correctionIndex: Map<string, string> = new Map();
let allEntries: NameEntry[] = [];
let rankedEntries: NameEntry[] = [];
let built = false;

const TASHKEEL_RE = /[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]/g;
const TATWEEL_RE = /\u0640/g;
const ALEF_VARIANTS_RE = /[\u0622\u0623\u0625\u0671]/g;
const ARABIC_RE = /[\u0600-\u06FF\uFE70-\uFEFF]/;

export function normalizeAr(text: string): string {
  if (!text) return "";
  let s = text.replace(TASHKEEL_RE, "");
  s = s.replace(TATWEEL_RE, "");
  s = s.replace(ALEF_VARIANTS_RE, "\u0627");
  s = s.replace(/\u0649/g, "\u064A"); // ى -> ي
  s = s.replace(/\u0629/g, "\u0647"); // ة -> ه
  return s;
}

export function normalizeEn(text: string): string {
  if (!text) return "";
  return text.toLowerCase().replace(/[-']/g, "").trim();
}

export function isArabic(text: string): boolean {
  return ARABIC_RE.test(text);
}

export function ensureBuilt(): void {
  if (built) return;

  const bundle = getDataBundleSync();
  allEntries = bundle.names;

  for (const entry of allEntries) {
    arIndex.set(entry.ar, entry);
    const normAr = normalizeAr(entry.ar);
    if (!arNormIndex.has(normAr)) {
      arNormIndex.set(normAr, entry);
    }

    for (const v of entry.arVariants) {
      const stripped = v.trim();
      if (stripped) {
        if (!arIndex.has(stripped)) arIndex.set(stripped, entry);
        const normV = normalizeAr(stripped);
        if (!arNormIndex.has(normV)) arNormIndex.set(normV, entry);
      }
    }

    const normEn = normalizeEn(entry.en);
    if (!enIndex.has(normEn)) enIndex.set(normEn, entry);

    for (const v of entry.enVariants) {
      const stripped = v.trim();
      if (stripped) {
        const normV = normalizeEn(stripped);
        if (!enIndex.has(normV)) enIndex.set(normV, entry);
      }
    }
  }

  for (const [k, v] of Object.entries(bundle.corrections)) {
    correctionIndex.set(k, v);
  }

  rankedEntries = [...allEntries].sort((a, b) => b.corpusShare - a.corpusShare);
  built = true;
}

export function lookupAr(name: string): NameEntry | undefined {
  ensureBuilt();
  if (!name || !name.trim()) return undefined;
  const trimmed = name.trim();

  // 1. Direct match
  const direct = arIndex.get(trimmed);
  if (direct) return direct;

  // 2. Normalized match
  const norm = normalizeAr(trimmed);
  const normMatch = arNormIndex.get(norm);
  if (normMatch) return normMatch;

  // 3. Alif / Alif Maqsura terminal phonetic equivalence (e.g. مصطفا <-> مصطفى, موسا <-> موسى)
  if (norm.endsWith("\u0627")) {
    const alt = norm.slice(0, -1) + "\u064A";
    const altMatch = arNormIndex.get(alt);
    if (altMatch) return altMatch;
  } else if (norm.endsWith("\u064A")) {
    const alt = norm.slice(0, -1) + "\u0627";
    const altMatch = arNormIndex.get(alt);
    if (altMatch) return altMatch;
  }

  // 4. Space-less compound match (e.g. عبد الرحيم <-> عبدالرحيم)
  const noSpace = trimmed.replace(/\s+/g, "");
  if (noSpace !== trimmed) {
    const noSpaceMatch = arIndex.get(noSpace) || arNormIndex.get(normalizeAr(noSpace));
    if (noSpaceMatch) return noSpaceMatch;
  }

  return undefined;
}

export function lookupEn(name: string): NameEntry | undefined {
  ensureBuilt();
  return enIndex.get(normalizeEn(name));
}

export function lookup(name: string): NameEntry | undefined {
  if (isArabic(name)) return lookupAr(name);
  return lookupEn(name);
}

export function getCorrection(surface: string): string | undefined {
  ensureBuilt();
  return correctionIndex.get(surface);
}

export function getAll(): NameEntry[] {
  ensureBuilt();
  return allEntries;
}

export function getRanked(): NameEntry[] {
  ensureBuilt();
  return rankedEntries;
}

export function getArForms(): Map<string, NameEntry> {
  ensureBuilt();
  return arIndex;
}

export function getArNormForms(): Map<string, NameEntry> {
  ensureBuilt();
  return arNormIndex;
}
