import { isArabic, lookupAr, lookupEn } from "./lookupIndices";

export function translateToken(token: string, to?: "ar" | "en"): string {
  const srcIsAr = isArabic(token);
  const target = to || (srcIsAr ? "en" : "ar");

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
  return tokens.map((t) => translateToken(t, to)).join(" ");
}
