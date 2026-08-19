import {
  getArForms,
  getArNormForms,
  isArabic,
  lookup,
  normalizeAr,
} from "./lookupIndices";
import { FrequencyClass } from "./types";

const BASE_SEGMENT_COST = 1.0;
const UNKNOWN_PENALTY = 8.0;
const LENGTH_BONUS_PER_CHAR = -0.05;

const FREQ_BONUS: Record<FrequencyClass, number> = {
  common: -0.6,
  normal: -0.2,
  rare: 0.0,
};

function dpSegment(text: string): string[] {
  const arIndex = getArForms();
  const arNorm = getArNormForms();
  const n = text.length;

  const dpCost: number[] = new Array(n + 1).fill(Infinity);
  const dpPrev: number[] = new Array(n + 1).fill(-1);

  dpCost[0] = 0.0;
  dpPrev[0] = 0;

  for (let i = 1; i <= n; i++) {
    const startJ = Math.max(0, i - 30);
    for (let j = startJ; j < i; j++) {
      if (dpCost[j] === Infinity) continue;

      const substr = text.slice(j, i);
      if (substr.length < 2 && j > 0) continue;

      let entry = arIndex.get(substr);
      if (!entry) {
        entry = arNorm.get(normalizeAr(substr));
      }

      if (entry) {
        const bonus = FREQ_BONUS[entry.frequency as FrequencyClass] || 0.0;
        const cost =
          dpCost[j] + BASE_SEGMENT_COST + bonus + LENGTH_BONUS_PER_CHAR * substr.length;
        if (cost < dpCost[i]) {
          dpCost[i] = cost;
          dpPrev[i] = j;
        }
      } else {
        const cost = dpCost[j] + UNKNOWN_PENALTY + substr.length;
        if (cost < dpCost[i]) {
          dpCost[i] = cost;
          dpPrev[i] = j;
        }
      }
    }
  }

  if (dpCost[n] === Infinity) {
    return [text];
  }

  const segments: string[] = [];
  let pos = n;
  while (pos > 0) {
    const prev = dpPrev[pos];
    segments.push(text.slice(prev, pos));
    pos = prev;
  }

  segments.reverse();
  return segments;
}

export function split(fullName: string): string[] {
  if (!fullName || !fullName.trim()) return [];

  const text = fullName.trim();
  if (text.includes(" ")) {
    return text.split(/\s+/);
  }

  if (isArabic(text)) {
    const directEntry = lookup(text);
    if (directEntry) {
      return [text];
    }
    return dpSegment(text);
  }

  return [text];
}
