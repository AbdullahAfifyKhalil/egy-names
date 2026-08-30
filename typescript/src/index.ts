import { getMetadata, clearCache } from "./data";
import {
  lookup,
  lookupAr,
  lookupEn,
  normalizeAr,
  normalizeEn,
  isArabic,
  getAll,
  getRanked,
} from "./lookupIndices";
import { isGeneratableEntry, isLineageRole, isLowConfidenceEntry, isPersonalEntry } from "./quality";
import { compoundTokens } from "./compoundTokens";
import {
  Gender,
  Religion,
  NameRole,
  FrequencyClass,
  NameInfo,
  toNameInfo,
  PetName,
  GeneratedName,
  ChainPart,
  GenderDetection,
  ReligionDetection,
  RankInfo,
  UniquenessScore,
  Fingerprint,
  FormatResult,
  CorpusStats,
} from "./types";

import { generateNames } from "./generator";
import { translate, translateToken } from "./translator";
import { annotate, annotateSingle } from "./annotator";
import { split } from "./splitter";
import { correct, correctToken } from "./corrector";
import { search } from "./search";

export class EgyptianNames {
  private seed?: number;

  constructor(options?: { seed?: number }) {
    this.seed = options?.seed;
  }

  // Core Features
  public generate(options?: {
    count?: number;
    gender?: string;
    religion?: string;
    length?: number;
    familyName?: boolean;
    frequency?: string;
    lang?: string;
    seed?: number;
  }): GeneratedName[] {
    return generateNames({
      ...options,
      seed: options?.seed !== undefined ? options.seed : this.seed,
    });
  }

  public translate(name: string, to?: "ar" | "en"): string {
    return translate(name, to);
  }

  public annotate(name: string): NameInfo | null | (NameInfo | null)[] {
    return annotate(name);
  }

  public split(fullName: string): string[] {
    return split(fullName);
  }

  public tashkeel(name: string, dialect: "standard" | "egyptian" = "standard"): string {
    if (!name || !name.trim()) return "";
    const rawTokens = name.trim().split(/\s+/);
    const result: string[] = [];
    const isEg = dialect === "egyptian";

    for (let i = 0; i < rawTokens.length; i++) {
      const current = rawTokens[i];

      if (i < rawTokens.length - 1) {
        const next = rawTokens[i + 1];
        const compound = `${current} ${next}`;
        const compoundNoSpace = `${current}${next}`;
        const compoundEntry = lookupAr(compound) || lookupAr(compoundNoSpace);
        if (compoundEntry) {
          const val = isEg ? compoundEntry.tashkeelEg : compoundEntry.tashkeelStandard;
          if (val) {
            result.push(val);
            i++;
            continue;
          }
        }
      }

      const entry = lookupAr(current);
      if (entry) {
        const val = isEg ? entry.tashkeelEg : entry.tashkeelStandard;
        result.push(val || current);
      } else {
        result.push(current);
      }
    }

    return result.join(" ");
  }

  public tashkeelEg(name: string): string {
    return this.tashkeel(name, "egyptian");
  }

  public tashkeelStandard(name: string): string {
    return this.tashkeel(name, "standard");
  }

  public ipa(name: string, dialect: "standard" | "egyptian" = "standard"): string {
    if (!name || !name.trim()) return "";
    const tokens = name.includes(" ") ? name.trim().split(/\s+/) : this.split(name);
    const isEg = dialect === "egyptian";
    const ipaParts: string[] = [];

    for (const tok of tokens) {
      const entry = lookup(tok);
      if (entry) {
        const ipaVal = isEg ? entry.ipaEg : entry.ipaStandard;
        if (ipaVal) {
          ipaParts.push(ipaVal.replace(/^[/[\]]+|[/[\]]+$/g, ""));
        } else {
          ipaParts.push(tok);
        }
      } else {
        ipaParts.push(tok);
      }
    }

    const joined = ipaParts.join(" ");
    return isEg ? `[${joined}]` : `/${joined}/`;
  }

  public ipaEg(name: string): string {
    return this.ipa(name, "egyptian");
  }

  public ipaStandard(name: string): string {
    return this.ipa(name, "standard");
  }

  public lookup(name: string): NameInfo | null {
    const entry = lookup(name);
    return entry ? toNameInfo(entry) : null;
  }

  public info(name: string): NameInfo | null {
    return this.lookup(name);
  }

  public dallaa(name: string, format: "plain" | "tashkeel" | "en" | "ipa" = "plain"): string[] {
    const entry = lookup(name);
    if (!entry) return [];
    const fmt = format.toLowerCase();
    if (fmt === "tashkeel" || fmt === "tashkeel_eg" || fmt === "tk") {
      return entry.dallaaTashkeel.length > 0 ? [...entry.dallaaTashkeel] : [...entry.dallaaAr];
    } else if (fmt === "en" || fmt === "english") {
      return [...entry.dallaaEn];
    } else if (fmt === "ipa" || fmt === "phonetic") {
      return [...entry.dallaaIpa];
    }
    return [...entry.dallaaAr];
  }

  public dallaaInfo(name: string): PetName[] {
    const entry = lookup(name);
    if (!entry || entry.dallaaAr.length === 0) return [];
    const result: PetName[] = [];
    for (let i = 0; i < entry.dallaaAr.length; i++) {
      result.push({
        ar: entry.dallaaAr[i],
        tashkeel: entry.dallaaTashkeel[i] || entry.dallaaAr[i],
        en: entry.dallaaEn[i] || "",
        ipa: entry.dallaaIpa[i] || "",
      });
    }
    return result;
  }

  public petNames(name: string, format: "plain" | "tashkeel" | "en" | "ipa" = "plain"): string[] {
    return this.dallaa(name, format);
  }

  public root(name: string): string | null {
    const entry = lookup(name);
    return entry && entry.root !== "N/A" ? entry.root : null;
  }

  public origin(name: string): string | null {
    const entry = lookup(name);
    return entry ? entry.originType : null;
  }

  public famousFigures(name: string, lang: "ar" | "en" = "ar"): string[] {
    const entry = lookup(name);
    if (!entry) return [];
    if (lang.toLowerCase().startsWith("en")) {
      return entry.famousFiguresEn.length > 0 ? [...entry.famousFiguresEn] : [...entry.famousFiguresAr];
    }
    return [...entry.famousFiguresAr];
  }

  public trend(name: string): string | null {
    const entry = lookup(name);
    return entry ? entry.trendCategory : null;
  }

  public correct(name: string): string {
    return correct(name);
  }

  public meaning(name: string): { ar: string; en: string } | null {
    const entry = lookup(name);
    if (!entry) return null;
    if (!entry.meaningAr && !entry.meaningEn) return null;
    return {
      ar: entry.meaningAr,
      en: entry.meaningEn,
    };
  }

  public families(options?: {
    count?: number;
    frequency?: string;
    religion?: string;
    startsWith?: string;
  }): NameInfo[] {
    return search({
      role: "family",
      maxResults: options?.count || 50,
      frequency: options?.frequency,
      religion: options?.religion,
      startsWith: options?.startsWith,
    });
  }

  public search(options: Parameters<typeof search>[0]): NameInfo[] {
    return search(options);
  }

  // Creative Features
  public isValid(name: string): boolean {
    const entry = lookup(name);
    return entry !== undefined && isPersonalEntry(entry) && !isLowConfidenceEntry(entry);
  }

  /**
   * Gender of the person: the first personal, non-lineage token wins.
   *
   * Later tokens are father, grandfather, family. They do not vote. A
   * tie must not become male. Two-word compound lemmas (e.g. kunya
   * "Abu X") are recognized as one token, not two fragments.
   */
  public detectGender(fullName: string): GenderDetection {
    const tokens = compoundTokens(fullName);
    if (tokens.length === 0) return { gender: "neutral", confidence: 0 };

    let skippedLineage = 0;
    for (let i = 0; i < tokens.length; i++) {
      const entry = tokens[i][1];
      if (!entry || !isPersonalEntry(entry) || isLowConfidenceEntry(entry)) continue;
      if (isLineageRole(entry)) {
        skippedLineage++;
        continue;
      }
      if (entry.gender === Gender.NEUTRAL) {
        return { gender: "neutral", confidence: 0.6 };
      }
      const confidence = skippedLineage === 0 && i === 0 ? 1.0 : 0.85;
      return { gender: entry.gender, confidence };
    }
    return { gender: "neutral", confidence: 0 };
  }

  /**
   * Religion of the person: the first given name, like gender.
   *
   * A father, grandfather, or family surname from one community does
   * not override the person's own first name. Lineage tokens only vote
   * if the person's own name gives no distinctive signal — an
   * intermarried or mixed-heritage family's surname should not outvote
   * what the person is actually named. Two-word compound lemmas (e.g.
   * kunya "Abu X") are recognized as one token.
   */
  public detectReligion(fullName: string): ReligionDetection {
    const tokens = compoundTokens(fullName);
    if (tokens.length === 0) return { religion: "neutral", confidence: 0 };

    let skippedLineage = 0;
    for (let i = 0; i < tokens.length; i++) {
      const entry = tokens[i][1];
      if (!entry || !isPersonalEntry(entry) || isLowConfidenceEntry(entry)) continue;
      if (isLineageRole(entry)) {
        skippedLineage++;
        continue;
      }
      if (entry.religion === Religion.NEUTRAL) continue;
      const confidence = skippedLineage === 0 && i === 0 ? 1.0 : 0.9;
      return { religion: entry.religion, confidence };
    }

    // The person's own given names carried no distinctive signal
    // (neutral or not found). Fall back to an aggregate vote across
    // every token, lineage included, rather than declaring neutral.
    let muslim = 0;
    let christian = 0;
    let first: "muslim" | "christian" | null = null;

    for (const [, entry] of tokens) {
      if (!entry || !isPersonalEntry(entry) || isLowConfidenceEntry(entry)) continue;
      if (entry.religion === Religion.MUSLIM) {
        muslim++;
        if (first === null) first = "muslim";
      } else if (entry.religion === Religion.CHRISTIAN) {
        christian++;
        if (first === null) first = "christian";
      }
    }

    if (muslim === 0 && christian === 0) return { religion: "neutral", confidence: 0 };
    const distinctive = muslim + christian;
    if (muslim > christian) return { religion: "muslim", confidence: 0.5 * (muslim / distinctive) };
    if (christian > muslim) {
      return { religion: "christian", confidence: 0.5 * (christian / distinctive) };
    }
    return { religion: first ?? "neutral", confidence: 0.5 };
  }

  public fingerprint(name: string): Fingerprint | null {
    const entry = lookup(name);
    if (!entry) return null;

    const slots = entry.slotPcts;
    const slotLabels = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th+"];

    let peakSlot = 0;
    let maxPct = -1;
    for (let i = 0; i < slots.length; i++) {
      if (slots[i] > maxPct) {
        maxPct = slots[i];
        peakSlot = i;
      }
    }

    let nameType = "";
    if (entry.role === NameRole.FAMILY) {
      nameType = slots[0] < 1.0 ? "pure_surname" : "surname_given";
    } else if (peakSlot === 0 && slots[0] > 40) {
      nameType = "primary_given";
    } else if (peakSlot === 0) {
      nameType = "given_name";
    } else {
      nameType = "patronymic";
    }

    const descParts = [];
    if (nameType === "primary_given") descParts.push(`Dominant first name (${slots[0].toFixed(1)}% in slot 1)`);
    else if (nameType === "pure_surname") descParts.push("Almost exclusively a family/surname");
    else if (nameType === "given_name") descParts.push("Given name appearing across multiple positions");
    else descParts.push(`Peaks in slot ${peakSlot + 1}`);

    if (entry.frequency === FrequencyClass.COMMON) descParts.push("very common");
    else if (entry.frequency === FrequencyClass.RARE) descParts.push("rare");

    const slotMap: Record<string, number> = {};
    for (let i = 0; i < slotLabels.length; i++) {
      slotMap[slotLabels[i]] = Math.round(slots[i] * 100) / 100;
    }

    return {
      name_ar: entry.ar,
      name_en: entry.en,
      type: nameType,
      slots: slotMap,
      corpus_share: entry.corpusShare,
      description: descParts.join("; "),
    };
  }

  public rank(name: string): RankInfo | null {
    const entry = lookup(name);
    if (!entry) return null;

    const ranked = getRanked();
    const total = ranked.length;

    for (let i = 0; i < total; i++) {
      if (ranked[i].ar === entry.ar) {
        const rankPos = i + 1;
        const percentile = (1 - (rankPos - 1) / total) * 100;
        let desc = `The #${rankPos} most common name in the Egyptian corpus`;
        if (rankPos <= 10) desc = `Top 10 — ${desc}`;
        else if (rankPos <= 100) desc = `Top 100 — ${desc}`;
        else if (rankPos <= 1000) desc = `Top 1000 — ${desc}`;

        return {
          rank: rankPos,
          percentile: Math.round(percentile * 100) / 100,
          corpus_share: `${entry.corpusShare.toFixed(4)}%`,
          description: desc,
        };
      }
    }
    return null;
  }

  private levenshtein(s1: string, s2: string): number {
    if (s1.length < s2.length) return this.levenshtein(s2, s1);
    if (s2.length === 0) return s1.length;

    let prevRow = Array.from({ length: s2.length + 1 }, (_, i) => i);
    for (let i = 0; i < s1.length; i++) {
      const currRow = [i + 1];
      for (let j = 0; j < s2.length; j++) {
        const insertions = prevRow[j + 1] + 1;
        const deletions = currRow[j] + 1;
        const substitutions = prevRow[j] + (s1[i] !== s2[j] ? 1 : 0);
        currRow.push(Math.min(insertions, deletions, substitutions));
      }
      prevRow = currRow;
    }
    return prevRow[prevRow.length - 1];
  }

  public similar(name: string, options?: { maxResults?: number; maxDistance?: number }): string[] {
    const maxResults = options?.maxResults || 10;
    const maxDistance = options?.maxDistance || 3;
    const useAr = isArabic(name);
    const entries = getAll();
    const nameNorm = useAr ? normalizeAr(name) : normalizeEn(name);

    const scored: { dist: number; share: number; candidate: string }[] = [];
    for (const e of entries) {
      const candidate = useAr ? e.ar : e.en;
      const candNorm = useAr ? normalizeAr(candidate) : normalizeEn(candidate);
      if (candNorm === nameNorm) continue;

      const dist = this.levenshtein(nameNorm, candNorm);
      if (dist <= maxDistance) {
        scored.push({ dist, share: e.corpusShare, candidate });
      }
    }

    scored.sort((a, b) => {
      if (a.dist !== b.dist) return a.dist - b.dist;
      return b.share - a.share;
    });

    return scored.slice(0, maxResults).map((s) => s.candidate);
  }

  public analyzeChain(fullName: string): ChainPart[] {
    const tokens = fullName.trim().split(/\s+/);
    if (tokens.length === 0) return [];

    const parts: ChainPart[] = [];
    const n = tokens.length;

    for (let i = 0; i < n; i++) {
      const t = tokens[i];
      const entry = lookup(t);
      const slot = i + 1;

      let roleLabel = "";
      let detail = "";

      if (i === 0) {
        roleLabel = "person";
        detail = "The individual's given name";
      } else if (i === n - 1 && entry && entry.role === NameRole.FAMILY) {
        roleLabel = "family_name";
        detail = "Family/tribal surname";
      } else if (i === 1) {
        roleLabel = "father";
        detail = "Father's name";
      } else if (i === 2) {
        roleLabel = "grandfather";
        detail = "Paternal grandfather";
      } else if (i === 3) {
        roleLabel = "great_grandfather";
        detail = "Great-grandfather";
      } else {
        roleLabel = "ancestor";
        detail = `Ancestor (generation ${i})`;
      }

      parts.push({
        name: t,
        slot,
        role: roleLabel,
        detail,
      });
    }

    return parts;
  }

  public uniqueness(fullName: string): UniquenessScore {
    const tokens = fullName.trim().split(/\s+/);
    if (tokens.length === 0) return { score: 0.5, label: "unknown", note: "Empty input" };

    const shares: number[] = [];
    let unknownCount = 0;
    for (const t of tokens) {
      const entry = lookup(t);
      if (entry) shares.push(entry.corpusShare);
      else unknownCount++;
    }

    if (shares.length === 0) {
      return { score: 1.0, label: "unknown", note: "None of the name parts are in the Egyptian corpus" };
    }

    let logSum = 0;
    for (const s of shares) {
      logSum += Math.log(Math.max(s, 1e-9));
    }
    const logMean = logSum / shares.length;

    const maxLog = 2.6;
    const minLog = -9.2;
    let score = 1.0 - (logMean - minLog) / (maxLog - minLog);
    score = Math.max(0.0, Math.min(1.0, score));
    score = Math.min(1.0, score + unknownCount * 0.15);

    let label = "";
    let note = "";
    if (score < 0.2) {
      label = "extremely_common";
      note = "Each part is among the most common names nationally";
    } else if (score < 0.4) {
      label = "common";
      note = "Well-known name parts with high national frequency";
    } else if (score < 0.6) {
      label = "moderate";
      note = "A mix of common and less common name parts";
    } else if (score < 0.8) {
      label = "distinctive";
      note = "Contains uncommon or regionally specific names";
    } else {
      label = "highly_unique";
      note = "Rare name combination — distinctive family heritage";
    }

    return {
      score: Math.round(score * 1000) / 1000,
      label,
      note,
    };
  }

  public format(fullName: string, options?: { style?: string }): string | FormatResult {
    const style = options?.style || "full";
    const tokens = fullName.trim().split(/\s+/);
    if (tokens.length === 0) return fullName;

    if (style === "full") return tokens.join(" ");

    if (style === "first_last") {
      const first = tokens[0];
      const last = tokens.length > 1 ? tokens[tokens.length - 1] : "";
      return { first, last };
    }

    if (style === "western") {
      const firstEn = translateToken(tokens[0], "en");
      const lastEn = tokens.length > 1 ? translateToken(tokens[tokens.length - 1], "en") : "";
      return `${firstEn} ${lastEn}`.trim();
    }

    if (style === "initials") {
      const initials = tokens.slice(0, -1).map((t) => `${t[0]}.`);
      initials.push(tokens[tokens.length - 1]);
      return initials.join(" ");
    }

    return tokens.join(" ");
  }

  public suggest(options?: {
    gender?: string;
    religion?: string;
    role?: string;
    frequency?: string;
    startsWith?: string;
    count?: number;
  }): string[] {
    const results = search({
      gender: options?.gender,
      religion: options?.religion,
      role: options?.role,
      frequency: options?.frequency,
      startsWith: options?.startsWith,
      maxResults: options?.count || 10,
    });
    return results.map((r) => r.ar);
  }

  public stats(): CorpusStats {
    const meta = getMetadata();
    const entries = getAll();
    let given = 0;
    let family = 0;
    let male = 0;
    let female = 0;

    for (const e of entries) {
      if (e.role === NameRole.GIVEN) given++;
      if (e.role === NameRole.FAMILY) family++;
      if (e.gender === Gender.MALE) male++;
      if (e.gender === Gender.FEMALE) female++;
    }

    return {
      ...meta,
      total_names: entries.length,
      given_names: given,
      family_names: family,
      male_names: male,
      female_names: female,
    };
  }

  public get batch() {
    return new BatchProcessor(this);
  }
}

class BatchProcessor {
  constructor(private parent: EgyptianNames) {}

  public translate(names: string[], to?: "ar" | "en"): string[] {
    return names.map((n) => this.parent.translate(n, to));
  }

  public annotate(names: string[]): (NameInfo | null | (NameInfo | null)[])[] {
    return names.map((n) => this.parent.annotate(n));
  }

  public correct(names: string[]): string[] {
    return names.map((n) => this.parent.correct(n));
  }

  public split(names: string[]): string[][] {
    return names.map((n) => this.parent.split(n));
  }

  public detectGender(names: string[]): GenderDetection[] {
    return names.map((n) => this.parent.detectGender(n));
  }

  public detectReligion(names: string[]): ReligionDetection[] {
    return names.map((n) => this.parent.detectReligion(n));
  }

  public tashkeel(names: string[]): string[] {
    return names.map((n) => this.parent.tashkeel(n));
  }
}

export {
  EgyptianNames as EgyNames,
  Gender,
  Religion,
  NameRole,
  FrequencyClass,
  NameInfo,
  PetName,
  GeneratedName,
  ChainPart,
  GenderDetection,
  ReligionDetection,
  RankInfo,
  UniquenessScore,
  Fingerprint,
  FormatResult,
  CorpusStats,
};
