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

function claimEn(key: string, entry: NameEntry): void {
  const existing = enIndex.get(key);
  if (!existing || entry.corpusShare > existing.corpusShare) {
    enIndex.set(key, entry);
  }
}

/**
 * Bind an Arabic variant spelling to the lemma with the larger corpus
 * share, same rule as `claimEn`.
 *
 * A canonical key (some entry's own `ar`/normalized `ar`) always wins
 * over any OTHER entry's variant claiming the same string — a rare
 * misspelling must never shadow a real lemma's own canonical spelling.
 * Among two variants with no canonical claim, the higher corpus share
 * wins, exactly like `claimEn`.
 */
function claimArVariant(
  index: Map<string, NameEntry>,
  canonicalKeys: Set<string>,
  key: string,
  entry: NameEntry
): void {
  if (canonicalKeys.has(key)) {
    // Already bound to its own entry in the canonical pass; a variant
    // from a different lemma must never override it.
    return;
  }
  const existing = index.get(key);
  if (!existing || entry.corpusShare > existing.corpusShare) {
    index.set(key, entry);
  }
}

function build(): void {
  if (built) return;

  const entries = getEntries();
  const corrections = getCorrections();

  // AR index, pass 1: canonical spellings are unconditional and take
  // priority over any other lemma's variant claiming the same string
  // (book has zero duplicate canonical ar values).
  const canonicalArKeys = new Set(entries.map((e) => e.ar));
  const canonicalArNormKeys = new Set(entries.map((e) => normalizeAr(e.ar)));
  for (const entry of entries) {
    arIndex.set(entry.ar, entry);
    arNormIndex.set(normalizeAr(entry.ar), entry);
  }

  for (const entry of entries) {
    // AR index, pass 2: variants. Keep the higher-share lemma when two
    // rows' variants claim the same spelling — same rule as English
    // keys, so a rare misspelling cannot steal a common name's lookup.
    for (const v of entry.arVariants) {
      const vStripped = v.trim();
      if (vStripped) {
        claimArVariant(arIndex, canonicalArKeys, vStripped, entry);
        claimArVariant(arNormIndex, canonicalArNormKeys, normalizeAr(vStripped), entry);
      }
    }

    // EN index — keep the higher-share lemma on a colliding key
    claimEn(normalizeEn(entry.en), entry);
    for (const v of entry.enVariants) {
      const vStripped = v.trim();
      if (vStripped) {
        claimEn(normalizeEn(vStripped), entry);
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
