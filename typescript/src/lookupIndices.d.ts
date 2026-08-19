import { NameEntry } from "./types";
export declare function normalizeAr(text: string): string;
export declare function normalizeEn(text: string): string;
export declare function lookupAr(name: string): NameEntry | undefined;
export declare function lookupEn(name: string): NameEntry | undefined;
export declare function isArabic(text: string): boolean;
export declare function lookup(name: string): NameEntry | undefined;
export declare function getCorrect(surface: string): string | undefined;
export declare function getRanked(): NameEntry[];
export declare function getAll(): NameEntry[];
export declare function getArForms(): Map<string, NameEntry>;
export declare function getArNormForms(): Map<string, NameEntry>;
//# sourceMappingURL=lookupIndices.d.ts.map