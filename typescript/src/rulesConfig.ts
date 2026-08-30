import * as fs from "fs";
import * as path from "path";

/**
 * Loader for the shared, cross-SDK rule config.
 *
 * `data/logic_config.json` (synced by scripts/sync-catalog.sh, same as
 * names.json.gz) is the single source of truth for every threshold and
 * rule list that used to be hardcoded per language. If the config file
 * is missing or malformed, fall back to the values last known correct
 * from this session's audits, so the library never hard-fails on a
 * packaging mistake.
 */

const CONFIG_PATH = path.join(__dirname, "data", "logic_config.json");

export interface InferThresholds {
  gender_min_p: number;
  muslim_min_p: number;
  christian_min_p: number;
  role_min_p: number;
}

export interface InferRule {
  script?: string;
  prefix?: string | string[];
  suffix?: string | string[];
  contains?: string | string[];
  match?: string;
  value?: string;
  confidence?: number;
}

interface QualityConfig {
  non_personal_ar: string[];
  uncertain_meaning_markers: string[];
  low_confidence_share_epsilon: number;
  kunya_exempt_prefixes: string[];
}

interface LogicConfig {
  quality: QualityConfig;
  infer_thresholds: InferThresholds;
  infer_rules: {
    gender: InferRule[];
    religion: InferRule[];
    role: InferRule[];
  };
}

const FALLBACK: LogicConfig = {
  quality: {
    non_personal_ar: ["الله", "الرجل", "الرجال", "شربه", "لافندي", "لفندي", "ماء", "البيت"],
    uncertain_meaning_markers: [
      "غير واضح",
      "لا يوجد معنى",
      "غير معروف",
      "قد يكون تحريف",
      "تحريفاً",
      "تحريفًا",
    ],
    low_confidence_share_epsilon: 0.0001,
    kunya_exempt_prefixes: ["أبو", "ابو", "أم", "ام"],
  },
  infer_thresholds: {
    gender_min_p: 0.7,
    muslim_min_p: 0.85,
    christian_min_p: 0.9,
    role_min_p: 0.88,
  },
  infer_rules: { gender: [], religion: [], role: [] },
};

let config: LogicConfig | null = null;

function load(): LogicConfig {
  if (config) return config;
  try {
    const raw = fs.readFileSync(CONFIG_PATH, "utf-8");
    config = JSON.parse(raw) as LogicConfig;
  } catch {
    config = FALLBACK;
  }
  return config;
}

export function nonPersonalAr(): Set<string> {
  return new Set(load().quality?.non_personal_ar || FALLBACK.quality.non_personal_ar);
}

export function uncertainMeaningMarkers(): string[] {
  return load().quality?.uncertain_meaning_markers || FALLBACK.quality.uncertain_meaning_markers;
}

export function lowConfidenceShareEpsilon(): number {
  const v = load().quality?.low_confidence_share_epsilon;
  return typeof v === "number" ? v : FALLBACK.quality.low_confidence_share_epsilon;
}

export function kunyaExemptPrefixes(): string[] {
  return load().quality?.kunya_exempt_prefixes || FALLBACK.quality.kunya_exempt_prefixes;
}

export function inferThresholds(): InferThresholds {
  return load().infer_thresholds || FALLBACK.infer_thresholds;
}

export function inferRules(kind: "gender" | "religion" | "role"): InferRule[] {
  return load().infer_rules?.[kind] || [];
}

/** Test-only: force the next `load()` to re-read the config file. */
export function clearConfigCache(): void {
  config = null;
}
