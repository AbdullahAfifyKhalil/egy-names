import * as fs from "fs";
import * as path from "path";
import * as zlib from "zlib";
import { NameEntry, RawNameEntry } from "./types";

const DATA_FILE = path.join(__dirname, "data", "names.json.gz");

export interface DataBundle {
  version: string;
  corpus_tokens: number;
  corpus_students: number;
  cohort_years: number[];
  names: RawNameEntry[];
  corrections: Record<string, string>;
}

let cache: DataBundle | null = null;
let entriesCache: NameEntry[] | null = null;

export function loadRaw(filePath: string = DATA_FILE): DataBundle {
  const compressed = fs.readFileSync(filePath);
  const jsonStr = zlib.gunzipSync(compressed).toString("utf-8");
  return JSON.parse(jsonStr) as DataBundle;
}

export function getBundle(filePath?: string): DataBundle {
  if (cache !== null && !filePath) {
    return cache;
  }
  const bundle = loadRaw(filePath);
  if (!filePath) {
    cache = bundle;
  }
  return bundle;
}

export function getEntries(filePath?: string): NameEntry[] {
  if (entriesCache !== null && !filePath) {
    return entriesCache;
  }
  const bundle = getBundle(filePath);
  const entries = bundle.names.map((r) => new NameEntry(r));
  if (!filePath) {
    entriesCache = entries;
  }
  return entries;
}

export function getCorrections(filePath?: string): Record<string, string> {
  const bundle = getBundle(filePath);
  return bundle.corrections || {};
}

export function getMetadata(filePath?: string) {
  const bundle = getBundle(filePath);
  return {
    version: bundle.version || "0.0.0",
    corpus_tokens: bundle.corpus_tokens || 0,
    corpus_students: bundle.corpus_students || 0,
    cohort_years: bundle.cohort_years || [],
  };
}

export function clearCache(): void {
  cache = null;
  entriesCache = null;
}
