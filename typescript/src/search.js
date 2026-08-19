"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.search = search;
const lookupIndices_1 = require("./lookupIndices");
const types_1 = require("./types");
function search(options) {
    const entries = (0, lookupIndices_1.getAll)();
    let g;
    if (options.gender === "male")
        g = types_1.Gender.MALE;
    if (options.gender === "female")
        g = types_1.Gender.FEMALE;
    let r;
    if (options.religion === "muslim")
        r = types_1.Religion.MUSLIM;
    if (options.religion === "christian")
        r = types_1.Religion.CHRISTIAN;
    let rl;
    if (options.role === "given")
        rl = types_1.NameRole.GIVEN;
    if (options.role === "family")
        rl = types_1.NameRole.FAMILY;
    let f;
    if (options.frequency === "common")
        f = types_1.FrequencyClass.COMMON;
    if (options.frequency === "normal")
        f = types_1.FrequencyClass.NORMAL;
    if (options.frequency === "rare")
        f = types_1.FrequencyClass.RARE;
    const prefixAr = options.startsWith && (0, lookupIndices_1.isArabic)(options.startsWith);
    const suffixAr = options.endsWith && (0, lookupIndices_1.isArabic)(options.endsWith);
    const containsAr = options.contains && (0, lookupIndices_1.isArabic)(options.contains);
    let filtered = entries.filter((e) => {
        if (g !== undefined && e.gender !== g && e.gender !== types_1.Gender.NEUTRAL)
            return false;
        if (r !== undefined && e.religion !== r && e.religion !== types_1.Religion.NEUTRAL)
            return false;
        if (rl !== undefined && e.role !== rl)
            return false;
        if (f !== undefined && e.frequency !== f)
            return false;
        if (options.minCorpusShare !== undefined && e.corpusShare < options.minCorpusShare)
            return false;
        if (options.startsWith) {
            if (prefixAr) {
                if (!(0, lookupIndices_1.normalizeAr)(e.ar).startsWith((0, lookupIndices_1.normalizeAr)(options.startsWith)))
                    return false;
            }
            else {
                if (!(0, lookupIndices_1.normalizeEn)(e.en).startsWith((0, lookupIndices_1.normalizeEn)(options.startsWith)))
                    return false;
            }
        }
        if (options.endsWith) {
            if (suffixAr) {
                if (!(0, lookupIndices_1.normalizeAr)(e.ar).endsWith((0, lookupIndices_1.normalizeAr)(options.endsWith)))
                    return false;
            }
            else {
                if (!(0, lookupIndices_1.normalizeEn)(e.en).endsWith((0, lookupIndices_1.normalizeEn)(options.endsWith)))
                    return false;
            }
        }
        if (options.contains) {
            if (containsAr) {
                if (!(0, lookupIndices_1.normalizeAr)(e.ar).includes((0, lookupIndices_1.normalizeAr)(options.contains)))
                    return false;
            }
            else {
                if (!(0, lookupIndices_1.normalizeEn)(e.en).includes((0, lookupIndices_1.normalizeEn)(options.contains)))
                    return false;
            }
        }
        return true;
    });
    const sortBy = options.sortBy || "corpus_share";
    if (sortBy === "alphabetical") {
        filtered.sort((a, b) => a.ar.localeCompare(b.ar));
    }
    else {
        filtered.sort((a, b) => b.corpusShare - a.corpusShare);
    }
    const maxResults = options.maxResults ?? 50;
    return filtered.slice(0, maxResults).map(types_1.toNameInfo);
}
//# sourceMappingURL=search.js.map