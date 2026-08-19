import { FrequencyClass, Gender, NameEntry, NameRole, Religion } from "./types";

export interface DataBundle {
  version: string;
  corpusTokens: number;
  corpusStudents: number;
  cohortYears: number[];
  names: NameEntry[];
  corrections: Record<string, string>;
}

let cachedBundle: DataBundle | null = null;
let loadPromise: Promise<DataBundle> | null = null;

const GENDER_MAP: Record<string, Gender> = {
  m: "male",
  f: "female",
  n: "neutral",
};

const RELIGION_MAP: Record<string, Religion> = {
  m: "muslim",
  c: "christian",
  n: "neutral",
};

const ROLE_MAP: Record<string, NameRole> = {
  g: "given",
  f: "family",
};

const FREQ_MAP: Record<string, FrequencyClass> = {
  c: "common",
  n: "normal",
  r: "rare",
};

export async function loadDataBundle(url: string = "/names.json.gz"): Promise<DataBundle> {
  if (cachedBundle) {
    return cachedBundle;
  }

  if (loadPromise) {
    return loadPromise;
  }

  loadPromise = (async () => {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch dataset from ${url}: ${response.statusText}`);
    }

    const arrayBuffer = await response.arrayBuffer();
    let rawData: any;

    // 1. Try DecompressionStream
    try {
      const blob = new Blob([arrayBuffer]);
      const stream = blob.stream().pipeThrough(new DecompressionStream("gzip"));
      const decompressed = await new Response(stream).json();
      rawData = decompressed;
    } catch (decompError) {
      // 2. If it was already decoded by browser or proxy
      try {
        const text = new TextDecoder().decode(arrayBuffer);
        rawData = JSON.parse(text);
      } catch (jsonError) {
        throw new Error(`Failed to decompress and parse ${url}: ${decompError}`);
      }
    }

    const names: NameEntry[] = (rawData.names || []).map((raw: any) => ({
      ar: raw.a || "",
      en: raw.e || "",
      gender: GENDER_MAP[raw.g] || "neutral",
      religion: RELIGION_MAP[raw.r] || "neutral",
      role: ROLE_MAP[raw.l] || "given",
      arVariants: raw.av ? raw.av.split("|") : [raw.a || ""],
      enVariants: raw.ev ? raw.ev.split("|") : [raw.e || ""],
      slotPcts: raw.p || [],
      corpusShare: raw.tp || 0.0,
      frequency: FREQ_MAP[raw.fc] || "rare",
      tashkeel: raw.t || "",
      meaningAr: raw.ma || "",
      meaningEn: raw.me || "",
    }));

    cachedBundle = {
      version: rawData.version || "0.1.0",
      corpusTokens: rawData.corpus_tokens || 0,
      corpusStudents: rawData.corpus_students || 0,
      cohortYears: rawData.cohort_years || [],
      names,
      corrections: rawData.corrections || {},
    };

    return cachedBundle;
  })();

  return loadPromise;
}

export function isDataLoaded(): boolean {
  return cachedBundle !== null;
}

export function getDataBundleSync(): DataBundle {
  if (!cachedBundle) {
    throw new Error("Dataset is not loaded yet. Call await loadDataBundle() first.");
  }
  return cachedBundle;
}
