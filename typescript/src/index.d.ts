import { NameInfo, GeneratedName, ChainPart, GenderDetection, ReligionDetection, RankInfo, UniquenessScore } from "./types";
import { search } from "./search";
export declare class EgyptianNames {
    private seed?;
    constructor(options?: {
        seed?: number;
    });
    generate(options?: {
        count?: number;
        gender?: string;
        religion?: string;
        length?: number;
        familyName?: boolean;
        frequency?: string;
        lang?: string;
        seed?: number;
    }): GeneratedName[];
    translate(name: string, to?: "ar" | "en"): string;
    annotate(name: string): NameInfo | null | (NameInfo | null)[];
    split(fullName: string): string[];
    tashkeel(name: string): string;
    correct(name: string): string;
    meaning(name: string): {
        ar: string;
        en: string;
    } | null;
    families(options?: {
        count?: number;
        frequency?: string;
        religion?: string;
        startsWith?: string;
    }): NameInfo[];
    search(options: Parameters<typeof search>[0]): NameInfo[];
    isValid(name: string): boolean;
    detectGender(fullName: string): GenderDetection;
    detectReligion(fullName: string): ReligionDetection;
    fingerprint(name: string): any;
    rank(name: string): RankInfo | null;
    private levenshtein;
    similar(name: string, options?: {
        maxResults?: number;
        maxDistance?: number;
    }): string[];
    analyzeChain(fullName: string): ChainPart[];
    uniqueness(fullName: string): UniquenessScore;
    format(fullName: string, options?: {
        style?: string;
    }): any;
    suggest(options?: {
        gender?: string;
        religion?: string;
        role?: string;
        frequency?: string;
        startsWith?: string;
        count?: number;
    }): string[];
    stats(): any;
    get batch(): BatchProcessor;
}
declare class BatchProcessor {
    private parent;
    constructor(parent: EgyptianNames);
    translate(names: string[], to?: "ar" | "en"): string[];
    annotate(names: string[]): (NameInfo | null | (NameInfo | null)[])[];
    correct(names: string[]): string[];
    split(names: string[]): string[][];
    detectGender(names: string[]): GenderDetection[];
    detectReligion(names: string[]): ReligionDetection[];
    tashkeel(names: string[]): string[];
}
export {};
//# sourceMappingURL=index.d.ts.map