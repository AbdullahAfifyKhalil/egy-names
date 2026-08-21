"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateNames = generateNames;
const lookupIndices_1 = require("./lookupIndices");
const types_1 = require("./types");
const DEFAULT_MIN_LEN = 4;
const DEFAULT_MAX_LEN = 5;
// Simple random generator for reproducible seeds if needed (placeholder, usually Math.random is fine)
// We'll use a basic LCG if a seed is provided
function LCG(seed) {
    let z = seed;
    return function () {
        z = (z * 16807) % 2147483647;
        return (z - 1) / 2147483646;
    };
}
function filterEntries(entries, options) {
    let result = entries;
    if (options.gender !== undefined) {
        result = result.filter((e) => e.gender === options.gender || e.gender === types_1.Gender.NEUTRAL);
    }
    if (options.religion !== undefined) {
        result = result.filter((e) => e.religion === options.religion || e.religion === types_1.Religion.NEUTRAL);
    }
    if (options.role !== undefined) {
        result = result.filter((e) => e.role === options.role);
    }
    if (options.frequency !== undefined) {
        result = result.filter((e) => e.frequency === options.frequency);
    }
    return result;
}
function weightedPick(entries, slotIdx, randFunc) {
    const candidates = [];
    const weights = [];
    let totalWeight = 0;
    for (const e of entries) {
        const w = e.slotPcts[slotIdx] * e.corpusShare;
        if (w > 0) {
            candidates.push(e);
            weights.push(w);
            totalWeight += w;
        }
    }
    if (candidates.length === 0) {
        for (const e of entries) {
            const w = Math.max(e.corpusShare, 1e-9);
            candidates.push(e);
            weights.push(w);
            totalWeight += w;
        }
    }
    let randomVal = randFunc() * totalWeight;
    for (let i = 0; i < candidates.length; i++) {
        randomVal -= weights[i];
        if (randomVal <= 0) {
            return candidates[i];
        }
    }
    return candidates[candidates.length - 1];
}
function generateNames(options) {
    const count = options.count || 1;
    const familyName = options.familyName !== false; // default true
    const lang = options.lang || "both";
    const randFunc = options.seed !== undefined ? LCG(options.seed) : Math.random;
    const allEntries = (0, lookupIndices_1.getAll)();
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
    let f;
    if (options.frequency === "common")
        f = types_1.FrequencyClass.COMMON;
    if (options.frequency === "normal")
        f = types_1.FrequencyClass.NORMAL;
    if (options.frequency === "rare")
        f = types_1.FrequencyClass.RARE;
    const patronGender = types_1.Gender.MALE;
    let firstPool = filterEntries(allEntries, { gender: g, religion: r, role: types_1.NameRole.GIVEN, frequency: f });
    let patronPool = filterEntries(allEntries, { gender: patronGender, religion: r, role: types_1.NameRole.GIVEN, frequency: f });
    let familyPool = filterEntries(allEntries, { religion: r, role: types_1.NameRole.FAMILY, frequency: f });
    if (firstPool.length === 0)
        firstPool = filterEntries(allEntries, { gender: g, role: types_1.NameRole.GIVEN });
    if (patronPool.length === 0)
        patronPool = filterEntries(allEntries, { gender: patronGender, role: types_1.NameRole.GIVEN });
    if (familyPool.length === 0)
        familyPool = filterEntries(allEntries, { role: types_1.NameRole.FAMILY });
    const results = [];
    for (let c = 0; c < count; c++) {
        const chainLen = options.length ? options.length : Math.floor(randFunc() * (DEFAULT_MAX_LEN - DEFAULT_MIN_LEN + 1)) + DEFAULT_MIN_LEN;
        const partsAr = [];
        const partsEn = [];
        const seen = new Set();
        // Slot 1
        let entry = weightedPick(firstPool, 0, randFunc);
        let attempts = 0;
        while (seen.has(entry.ar) && attempts < 20) {
            entry = weightedPick(firstPool, 0, randFunc);
            attempts++;
        }
        partsAr.push(entry.ar);
        partsEn.push(entry.en);
        seen.add(entry.ar);
        // Slots 2 .. (N-1 or N)
        const patronEnd = familyName ? chainLen - 1 : chainLen;
        for (let slot = 1; slot < patronEnd; slot++) {
            const slotIdx = Math.min(slot, 7);
            entry = weightedPick(patronPool, slotIdx, randFunc);
            attempts = 0;
            while (seen.has(entry.ar) && attempts < 20) {
                entry = weightedPick(patronPool, slotIdx, randFunc);
                attempts++;
            }
            partsAr.push(entry.ar);
            partsEn.push(entry.en);
            seen.add(entry.ar);
        }
        // Last slot
        if (familyName && chainLen > 1) {
            const slotIdx = Math.min(chainLen - 1, 7);
            entry = weightedPick(familyPool, slotIdx, randFunc);
            attempts = 0;
            while (seen.has(entry.ar) && attempts < 20) {
                entry = weightedPick(familyPool, slotIdx, randFunc);
                attempts++;
            }
            partsAr.push(entry.ar);
            partsEn.push(entry.en);
        }
        results.push({
            ar: partsAr.join(" "),
            en: partsEn.join(" "),
            parts_ar: partsAr,
            parts_en: partsEn,
        });
    }
    return results;
}
//# sourceMappingURL=generator.js.map