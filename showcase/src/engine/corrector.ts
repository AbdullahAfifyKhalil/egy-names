import {
  getArNormForms,
  getCorrection,
  lookupAr,
  normalizeAr,
} from "./lookupIndices";

export function correctToken(token: string): string {
  if (!token || !token.trim()) return token;
  const t = token.trim();

  // 1. Direct surface correction pair
  const canonical = getCorrection(t);
  if (canonical) return canonical;

  // 2. Exact match in arabic index (including phonetic variants)
  const exact = lookupAr(t);
  if (exact) return exact.ar;

  // 3. Normalized form lookup
  const norm = normalizeAr(t);
  const arNorm = getArNormForms();
  const normMatch = arNorm.get(norm);
  if (normMatch) return normMatch.ar;

  // 4. Trailing Alif / Alif Maqsura check
  if (norm.endsWith("\u0627")) {
    const alt = norm.slice(0, -1) + "\u064A";
    const altMatch = arNorm.get(alt);
    if (altMatch) return altMatch.ar;
  } else if (norm.endsWith("\u064A")) {
    const alt = norm.slice(0, -1) + "\u0627";
    const altMatch = arNorm.get(alt);
    if (altMatch) return altMatch.ar;
  }

  return t;
}

export function correct(name: string): string {
  if (!name || !name.trim()) return name;
  const rawTokens = name.trim().split(/\s+/);
  const result: string[] = [];

  for (let i = 0; i < rawTokens.length; i++) {
    const current = rawTokens[i];

    // Check if current token forms a compound name with next token (e.g. "عبد" + "الرحيم" -> "عبدالرحيم" or "أبو" + "بكر")
    if (i < rawTokens.length - 1) {
      const next = rawTokens[i + 1];
      const compound = `${current} ${next}`;
      const compoundNoSpace = `${current}${next}`;

      const compoundEntry = lookupAr(compound) || lookupAr(compoundNoSpace);
      if (compoundEntry) {
        result.push(compoundEntry.ar);
        i++; // skip compound second part
        continue;
      }
    }

    result.push(correctToken(current));
  }

  return result.join(" ");
}
