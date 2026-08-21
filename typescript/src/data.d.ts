import { NameEntry, RawNameEntry } from "./types";
export interface DataBundle {
    version: string;
    corpus_tokens: number;
    corpus_students: number;
    cohort_years: number[];
    names: RawNameEntry[];
    corrections: Record<string, string>;
}
export declare function loadRaw(filePath?: string): DataBundle;
export declare function getBundle(filePath?: string): DataBundle;
export declare function getEntries(filePath?: string): NameEntry[];
export declare function getCorrections(filePath?: string): Record<string, string>;
export declare function getMetadata(filePath?: string): {
    version: string;
    corpus_tokens: number;
    corpus_students: number;
    cohort_years: number[];
};
export declare function clearCache(): void;
//# sourceMappingURL=data.d.ts.map