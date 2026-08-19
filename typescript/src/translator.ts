import { lookupAr, lookupEn, isArabic } from "./lookupIndices";

export function translateToken(token: string, to?: "ar" | "en"): string {
  const srcIsArabic = isArabic(token);
  const target = to || (srcIsArabic ? "en" : "ar");

  if (target === "en") {
    const entry = lookupAr(token);
    return entry ? entry.en : token;
  } else {
    const entry = lookupEn(token);
    return entry ? entry.ar : token;
  }
}

export function translate(fullName: string, to?: "ar" | "en"): string {
  if (!fullName || !fullName.trim()) return fullName;
  const tokens = fullName.trim().split(/\s+/);
  const translated = tokens.map((t) => translateToken(t, to));
  return translated.join(" ");
}
