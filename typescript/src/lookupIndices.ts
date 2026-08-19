import { getEntries, getCorrections } from "./data";
import { NameEntry } from "./types";

let built = false;

const arIndex: Map<string, NameEntry> = new Map();
const enIndex: Map<string, NameEntry> = new Map();
const arNormIndex: Map<string, NameEntry> = new Map();
const correctionIndex: Map<string, string> = new Map();
let ranked: NameEntry[] = [];
let allEntries: NameEntry[] = [];

// Regex for Arabic normalization
const ALEF_VARIANTS = /[\u0622\u0623\u0625\u0671]/g;
const TASHKEEL = /[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]/g;
const TATWEEL = /\u0640/g;
const ALEF_MAQSURA = "\u0649";
const YA = "\u064A";
const TA_MARBUTA = "\u0629";
const HA = "\u0647";

export function normalizeAr(text: string): string {
  let s = text.replace(TASHKEEL, "");
  s = s.replace(TATWEEL, "");
  s = s.replace(ALEF_VARIANTS, "\u0627");
  s = s.replace(new RegExp(ALEF_MAQSURA, "g"), YA);
  s = s.replace(new RegExp(TA_MARBUTA, "g"), HA);
  return s;
}

export function normalizeEn(text: string): string {
  return text.toLowerCase().replace(/-/g, "").replace(/'/g, "").trim();
}

function build(): void {
  if (built) return;

  const entries = getEntries();
  const corrections = getCorrections();

  for (const entry of entries) {
    // AR index
    if (!arIndex.has(entry.ar)) arIndex.set(entry.ar, entry);
    const normAr = normalizeAr(entry.ar);
    if (!arNormIndex.has(normAr)) arNormIndex.set(normAr, entry);

    for (const v of entry.arVariants) {
      const vStripped = v.trim();
      if (vStripped) {
        if (!arIndex.has(vStripped)) arIndex.set(vStripped, entry);
        const normV = normalizeAr(vStripped);
        if (!arNormIndex.has(normV)) arNormIndex.set(normV, entry);
      }
    }

    // EN index
    const normEn = normalizeEn(entry.en);
    if (!enIndex.has(normEn)) enIndex.set(normEn, entry);
    
    for (const v of entry.enVariants) {
      const vStripped = v.trim();
      if (vStripped) {
        const normV = normalizeEn(vStripped);
        if (!enIndex.has(normV)) enIndex.set(normV, entry);
      }
    }
  }

  // Correction index
  for (const [k, v] of Object.entries(corrections)) {
    correctionIndex.set(k, v);
  }

  allEntries = [...entries];
  ranked = [...entries].sort((a, b) => b.corpusShare - a.corpusShare);
  built = true;
}

function ensureBuilt(): void {
  if (!built) {
    build();
  }
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

export function isArabic(text: string): boolean {
  return /[\u0600-\u06FF\uFE70-\uFEFF]/.test(text);
}

export function lookup(name: string): NameEntry | undefined {
  ensureBuilt();
  if (isArabic(name)) {
    return lookupAr(name);
  }
  return lookupEn(name);
}

export function getCorrect(surface: string): string | undefined {
  ensureBuilt();
  return correctionIndex.get(surface);
}

export function getRanked(): NameEntry[] {
  ensureBuilt();
  return ranked;
}

export function getAll(): NameEntry[] {
  ensureBuilt();
  return allEntries;
}

export function getArForms(): Map<string, NameEntry> {
  ensureBuilt();
  return arIndex;
}

export function getArNormForms(): Map<string, NameEntry> {
  ensureBuilt();
  return arNormIndex;
}
