import { getAll } from "./lookupIndices";
import {
  FrequencyClass,
  Gender,
  GeneratedName,
  NameEntry,
  NameRole,
  Religion,
} from "./types";

const DEFAULT_MIN_LEN = 4;
const DEFAULT_MAX_LEN = 5;

function createRng(seed?: number) {
  if (seed === undefined) {
    return () => Math.random();
  }
  let s = seed;
  return () => {
    s = (s * 9301 + 49297) % 233280;
    return s / 233280;
  };
}

function filterEntries(
  entries: NameEntry[],
  filters: {
    gender?: Gender;
    religion?: Religion;
    role?: NameRole;
    frequency?: FrequencyClass;
  }
): NameEntry[] {
  return entries.filter((e) => {
    if (filters.gender && e.gender !== filters.gender && e.gender !== "neutral") return false;
    if (filters.religion && e.religion !== filters.religion && e.religion !== "neutral") return false;
    if (filters.role && e.role !== filters.role) return false;
    if (filters.frequency && e.frequency !== filters.frequency) return false;
    return true;
  });
}

function weightedPick(entries: NameEntry[], slotIdx: number, randomFn: () => number): NameEntry {
  const candidates: NameEntry[] = [];
  const weights: number[] = [];
  let totalWeight = 0;

  for (const e of entries) {
    const w = (e.slotPcts[slotIdx] || 0) * e.corpusShare;
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

  let r = randomFn() * totalWeight;
  for (let i = 0; i < candidates.length; i++) {
    r -= weights[i];
    if (r <= 0) return candidates[i];
  }

  return candidates[candidates.length - 1];
}

export function generateNames(options?: {
  count?: number;
  gender?: Gender;
  religion?: Religion;
  length?: number;
  familyName?: boolean;
  frequency?: FrequencyClass;
  seed?: number;
}): GeneratedName[] {
  const count = options?.count || 1;
  const familyName = options?.familyName !== undefined ? options.familyName : true;
  const rng = createRng(options?.seed);
  const allEntries = getAll();

  let firstPool = filterEntries(allEntries, {
    gender: options?.gender,
    religion: options?.religion,
    role: "given",
    frequency: options?.frequency,
  });

  let patronPool = filterEntries(allEntries, {
    gender: "male",
    religion: options?.religion,
    role: "given",
    frequency: options?.frequency,
  });

  let familyPool = filterEntries(allEntries, {
    religion: options?.religion,
    role: "family",
    frequency: options?.frequency,
  });

  if (firstPool.length === 0) firstPool = filterEntries(allEntries, { gender: options?.gender, role: "given" });
  if (patronPool.length === 0) patronPool = filterEntries(allEntries, { gender: "male", role: "given" });
  if (familyPool.length === 0) familyPool = filterEntries(allEntries, { role: "family" });

  const results: GeneratedName[] = [];

  for (let c = 0; c < count; c++) {
    const chainLen =
      options?.length ||
      Math.floor(rng() * (DEFAULT_MAX_LEN - DEFAULT_MIN_LEN + 1)) + DEFAULT_MIN_LEN;

    const partsAr: string[] = [];
    const partsEn: string[] = [];
    const seen = new Set<string>();

    // Slot 1: Person given name
    let entry = weightedPick(firstPool, 0, rng);
    let attempts = 0;
    while (seen.has(entry.ar) && attempts < 20) {
      entry = weightedPick(firstPool, 0, rng);
      attempts++;
    }
    partsAr.push(entry.ar);
    partsEn.push(entry.en);
    seen.add(entry.ar);

    // Patronymic chain (Slots 2 .. N-1 or N)
    const patronEnd = familyName ? chainLen - 1 : chainLen;
    for (let slot = 1; slot < patronEnd; slot++) {
      const slotIdx = Math.min(slot, 7);
      entry = weightedPick(patronPool, slotIdx, rng);
      attempts = 0;
      while (seen.has(entry.ar) && attempts < 20) {
        entry = weightedPick(patronPool, slotIdx, rng);
        attempts++;
      }
      partsAr.push(entry.ar);
      partsEn.push(entry.en);
      seen.add(entry.ar);
    }

    // Family surname slot
    if (familyName && chainLen > 1) {
      const slotIdx = Math.min(chainLen - 1, 7);
      entry = weightedPick(familyPool, slotIdx, rng);
      attempts = 0;
      while (seen.has(entry.ar) && attempts < 20) {
        entry = weightedPick(familyPool, slotIdx, rng);
        attempts++;
      }
      partsAr.push(entry.ar);
      partsEn.push(entry.en);
    }

    results.push({
      ar: partsAr.join(" "),
      en: partsEn.join(" "),
      partsAr,
      partsEn,
    });
  }

  return results;
}
