import { annotate, annotateSingle } from "./annotator";
import { correct } from "./corrector";
import { getDataBundleSync, isDataLoaded, loadDataBundle } from "./data";
import { generateNames } from "./generator";
import {
  ensureBuilt,
  getAll,
  getRanked,
  lookup,
  lookupAr,
} from "./lookupIndices";
import { search } from "./search";
import { split } from "./splitter";
import { translate, translateToken } from "./translator";
import {
  ChainPart,
  FrequencyClass,
  Gender,
  GenderDetection,
  GeneratedName,
  NameInfo,
  NameRole,
  RankInfo,
  Religion,
  ReligionDetection,
  UniquenessScore,
} from "./types";

export class EgyptianNames {
  private seed?: number;

  constructor(options?: { seed?: number }) {
    this.seed = options?.seed;
  }

  public async init(url: string = "/names.json.gz"): Promise<void> {
    await loadDataBundle(url);
    ensureBuilt();
  }

  public generate(options?: {
    count?: number;
    gender?: Gender;
    religion?: Religion;
    length?: number;
    familyName?: boolean;
    frequency?: FrequencyClass;
    seed?: number;
  }): GeneratedName[] {
    return generateNames({
      count: options?.count,
      gender: options?.gender,
      religion: options?.religion,
      length: options?.length,
      familyName: options?.familyName,
      frequency: options?.frequency,
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

  public tashkeel(name: string): string {
    if (!name || !name.trim()) return name;
    const rawTokens = name.trim().split(/\s+/);
    const result: string[] = [];

    for (let i = 0; i < rawTokens.length; i++) {
      const current = rawTokens[i];

      if (i < rawTokens.length - 1) {
        const next = rawTokens[i + 1];
        const compound = `${current} ${next}`;
        const compoundNoSpace = `${current}${next}`;
        const compoundEntry = lookupAr(compound) || lookupAr(compoundNoSpace);
        if (compoundEntry && compoundEntry.tashkeel) {
          result.push(compoundEntry.tashkeel);
          i++;
          continue;
        }
      }

      const entry = lookupAr(current);
      result.push(entry?.tashkeel || current);
    }

    return result.join(" ");
  }

  public correct(name: string): string {
    return correct(name);
  }

  public meaning(name: string): { ar: string; en: string } | null {
    const entry = lookup(name);
    if (!entry || (!entry.meaningAr && !entry.meaningEn)) return null;
    return {
      ar: entry.meaningAr || "",
      en: entry.meaningEn || "",
    };
  }

  public families(options?: {
    count?: number;
    frequency?: FrequencyClass;
    religion?: Religion;
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

  public search(filters?: {
    gender?: Gender | string;
    religion?: Religion | string;
    role?: NameRole | string;
    frequency?: FrequencyClass | string;
    startsWith?: string;
    endsWith?: string;
    contains?: string;
    minCorpusShare?: number;
    maxResults?: number;
    sortBy?: "corpus_share" | "alphabetical";
  }): NameInfo[] {
    return search(filters);
  }

  public isValid(name: string): boolean {
    return lookup(name) !== undefined;
  }

  public detectGender(fullName: string): GenderDetection {
    const tokens = fullName.trim().split(/\s+/);
    if (tokens.length === 0) return { gender: "neutral", confidence: 0 };

    let maleScore = 0;
    let femaleScore = 0;
    let neutralScore = 0;
    let totalWeight = 0;

    for (let i = 0; i < tokens.length; i++) {
      const entry = lookup(tokens[i]);
      if (!entry) continue;

      const w = i === 0 ? 4.0 : i === 1 ? 2.0 : 1.0;
      totalWeight += w;

      if (entry.gender === "male") maleScore += w;
      else if (entry.gender === "female") femaleScore += w;
      else neutralScore += w;
    }

    if (totalWeight === 0) return { gender: "neutral", confidence: 0 };

    const scores = { male: maleScore, female: femaleScore, neutral: neutralScore };
    const best = (Object.keys(scores) as Gender[]).reduce((a, b) =>
      scores[a] > scores[b] ? a : b
    );

    return {
      gender: best,
      confidence: scores[best] / totalWeight,
    };
  }

  public detectReligion(fullName: string): ReligionDetection {
    const tokens = fullName.trim().split(/\s+/);
    if (tokens.length === 0) return { religion: "neutral", confidence: 0 };

    let muslimScore = 0;
    let christianScore = 0;
    let neutralScore = 0;
    let totalWeight = 0;

    for (const t of tokens) {
      const entry = lookup(t);
      if (!entry) continue;

      const w = 1.0;
      totalWeight += w;

      if (entry.religion === "muslim") muslimScore += w;
      else if (entry.religion === "christian") christianScore += w;
      else neutralScore += w;
    }

    if (totalWeight === 0) return { religion: "neutral", confidence: 0 };

    const scores = {
      muslim: muslimScore,
      christian: christianScore,
      neutral: neutralScore,
    };
    const best = (Object.keys(scores) as Religion[]).reduce((a, b) =>
      scores[a] > scores[b] ? a : b
    );

    return {
      religion: best,
      confidence: scores[best] / totalWeight,
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
          corpusShare: `${entry.corpusShare.toFixed(4)}%`,
          description: desc,
        };
      }
    }
    return null;
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

      let role = "ancestor";
      let detail = `Ancestor (generation ${i})`;

      if (i === 0) {
        role = "person";
        detail = "The individual's given name";
      } else if (i === n - 1 && entry?.role === "family") {
        role = "family_name";
        detail = "Family/tribal surname";
      } else if (i === 1) {
        role = "father";
        detail = "Father's name";
      } else if (i === 2) {
        role = "grandfather";
        detail = "Paternal grandfather";
      } else if (i === 3) {
        role = "great_grandfather";
        detail = "Great-grandfather";
      }

      parts.push({
        name: t,
        slot,
        role,
        detail,
      });
    }

    return parts;
  }

  public uniqueness(fullName: string): UniquenessScore {
    const tokens = fullName.trim().split(/\s+/);
    if (tokens.length === 0) {
      return { score: 0.5, label: "unknown", note: "Empty input" };
    }

    const shares: number[] = [];
    let unknownCount = 0;

    for (const t of tokens) {
      const entry = lookup(t);
      if (entry) shares.push(entry.corpusShare);
      else unknownCount++;
    }

    if (shares.length === 0) {
      return {
        score: 1.0,
        label: "unknown",
        note: "None of the name parts are in the Egyptian corpus",
      };
    }

    const logSum = shares.reduce((acc, s) => acc + Math.log(Math.max(s, 1e-9)), 0);
    const logMean = logSum / shares.length;

    const maxLog = 2.6;
    const minLog = -9.2;
    let score = 1.0 - (logMean - minLog) / (maxLog - minLog);
    score = Math.max(0.0, Math.min(1.0, score));
    score = Math.min(1.0, score + unknownCount * 0.15);

    let label: UniquenessScore["label"];
    let note: string;

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

  public stats(): Record<string, any> {
    const bundle = getDataBundleSync();
    const entries = getAll();
    return {
      version: bundle.version,
      corpus_tokens: bundle.corpusTokens,
      corpus_students: bundle.corpusStudents,
      cohort_years: bundle.cohortYears,
      total_names: entries.length,
      given_names: entries.filter((e) => e.role === "given").length,
      family_names: entries.filter((e) => e.role === "family").length,
      male_names: entries.filter((e) => e.gender === "male").length,
      female_names: entries.filter((e) => e.gender === "female").length,
    };
  }
}

export const EgyNames = EgyptianNames;
export type {
  Gender,
  Religion,
  NameRole,
  FrequencyClass,
  NameInfo,
  GeneratedName,
  ChainPart,
  GenderDetection,
  ReligionDetection,
  RankInfo,
  UniquenessScore,
};

