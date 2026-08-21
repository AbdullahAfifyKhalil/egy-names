import { getAll } from "./lookupIndices";
import { NameEntry, Gender, Religion, NameRole, FrequencyClass, GeneratedName } from "./types";

const DEFAULT_MIN_LEN = 4;
const DEFAULT_MAX_LEN = 5;

// Simple random generator for reproducible seeds if needed (placeholder, usually Math.random is fine)
// We'll use a basic LCG if a seed is provided
function LCG(seed: number) {
  let z = seed;
  return function () {
    z = (z * 16807) % 2147483647;
    return (z - 1) / 2147483646;
  };
}

function filterEntries(
  entries: NameEntry[],
  options: {
    gender?: Gender;
    religion?: Religion;
    role?: NameRole;
    frequency?: FrequencyClass;
  }
): NameEntry[] {
  let result = entries;

  if (options.gender !== undefined) {
    result = result.filter((e) => e.gender === options.gender || e.gender === Gender.NEUTRAL);
  }
  if (options.religion !== undefined) {
    result = result.filter((e) => e.religion === options.religion || e.religion === Religion.NEUTRAL);
  }
  if (options.role !== undefined) {
    result = result.filter((e) => e.role === options.role);
  }
  if (options.frequency !== undefined) {
    result = result.filter((e) => e.frequency === options.frequency);
  }

  return result;
}

function weightedPick(
  entries: NameEntry[],
  slotIdx: number,
  randFunc: () => number
): NameEntry {
  const candidates: NameEntry[] = [];
  const weights: number[] = [];
  let totalWeight = 0;

  for (const e of entries) {
    const w = e.slotPcts[slotIdx] * e.corpusShare;
    if (w > 0) {
      candidates.push(e);
      weights.push(w);
      totalWeight += w;
    }
  }

  if (candidates.length === 0) {
    for (const e of entries) {
      const w = Math.max(e.corpusShare, 1e-9);
      candidates.push(e);
      weights.push(w);
      totalWeight += w;
    }
  }

  let randomVal = randFunc() * totalWeight;
  for (let i = 0; i < candidates.length; i++) {
    randomVal -= weights[i];
    if (randomVal <= 0) {
      return candidates[i];
    }
  }

  return candidates[candidates.length - 1];
}

export function generateNames(options: {
  count?: number;
  gender?: string;
  religion?: string;
  length?: number;
  familyName?: boolean;
  frequency?: string;
  lang?: string;
  seed?: number;
}): GeneratedName[] {
  const count = options.count !== undefined ? options.count : 1;
  if (count <= 0) return [];
  const familyName = options.familyName !== false; // default true
  const lang = options.lang || "both";
  const randFunc = options.seed !== undefined ? LCG(options.seed) : Math.random;

  const allEntries = getAll();

  let g: Gender | undefined;
  if (options.gender === "male") g = Gender.MALE;
  if (options.gender === "female") g = Gender.FEMALE;

  let r: Religion | undefined;
  if (options.religion === "muslim") r = Religion.MUSLIM;
  if (options.religion === "christian") r = Religion.CHRISTIAN;

  let f: FrequencyClass | undefined;
  if (options.frequency === "common") f = FrequencyClass.COMMON;
  if (options.frequency === "normal") f = FrequencyClass.NORMAL;
  if (options.frequency === "rare") f = FrequencyClass.RARE;

  const patronGender = Gender.MALE;

  let firstPool = filterEntries(allEntries, { gender: g, religion: r, role: NameRole.GIVEN, frequency: f });
  let patronPool = filterEntries(allEntries, { gender: patronGender, religion: r, role: NameRole.GIVEN, frequency: f });
  let familyPool = filterEntries(allEntries, { religion: r, role: NameRole.FAMILY, frequency: f });

  if (firstPool.length === 0) firstPool = filterEntries(allEntries, { gender: g, role: NameRole.GIVEN });
  if (patronPool.length === 0) patronPool = filterEntries(allEntries, { gender: patronGender, role: NameRole.GIVEN });
  if (familyPool.length === 0) familyPool = filterEntries(allEntries, { role: NameRole.FAMILY });

  const results: GeneratedName[] = [];

  for (let c = 0; c < count; c++) {
    const chainLen = options.length ? options.length : Math.floor(randFunc() * (DEFAULT_MAX_LEN - DEFAULT_MIN_LEN + 1)) + DEFAULT_MIN_LEN;

    const partsAr: string[] = [];
    const partsEn: string[] = [];
    const seen: Set<string> = new Set();

    // Slot 1
    let entry = weightedPick(firstPool, 0, randFunc);
    let attempts = 0;
    while (seen.has(entry.ar) && attempts < 20) {
      entry = weightedPick(firstPool, 0, randFunc);
      attempts++;
    }
    partsAr.push(entry.ar);
    partsEn.push(entry.en);
    seen.add(entry.ar);

    // Slots 2 .. (N-1 or N)
    const patronEnd = familyName ? chainLen - 1 : chainLen;
    for (let slot = 1; slot < patronEnd; slot++) {
      const slotIdx = Math.min(slot, 7);
      entry = weightedPick(patronPool, slotIdx, randFunc);
      attempts = 0;
      while (seen.has(entry.ar) && attempts < 20) {
        entry = weightedPick(patronPool, slotIdx, randFunc);
        attempts++;
      }
      partsAr.push(entry.ar);
      partsEn.push(entry.en);
      seen.add(entry.ar);
    }

    // Last slot
    if (familyName && chainLen > 1) {
      const slotIdx = Math.min(chainLen - 1, 7);
      entry = weightedPick(familyPool, slotIdx, randFunc);
      attempts = 0;
      while (seen.has(entry.ar) && attempts < 20) {
        entry = weightedPick(familyPool, slotIdx, randFunc);
        attempts++;
      }
      partsAr.push(entry.ar);
      partsEn.push(entry.en);
    }

    results.push({
      ar: partsAr.join(" "),
      en: partsEn.join(" "),
      parts_ar: partsAr,
      parts_en: partsEn,
    });
  }

  return results;
}
