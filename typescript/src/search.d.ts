import { NameInfo } from "./types";
export declare function search(options: {
    gender?: string;
    religion?: string;
    role?: string;
    frequency?: string;
    startsWith?: string;
    endsWith?: string;
    contains?: string;
    minCorpusShare?: number;
    maxResults?: number;
    sortBy?: "corpus_share" | "alphabetical" | "rank";
}): NameInfo[];
//# sourceMappingURL=search.d.ts.map