"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.normalizeAr = normalizeAr;
exports.normalizeEn = normalizeEn;
exports.lookupAr = lookupAr;
exports.lookupEn = lookupEn;
exports.isArabic = isArabic;
exports.lookup = lookup;
exports.getCorrect = getCorrect;
exports.getRanked = getRanked;
exports.getAll = getAll;
exports.getArForms = getArForms;
exports.getArNormForms = getArNormForms;
const data_1 = require("./data");
const types_1 = require("./types");
let built = false;
const arIndex = new Map();
const enIndex = new Map();
const arNormIndex = new Map();
const correctionIndex = new Map();
let ranked = [];
let allEntries = [];
// Regex for Arabic normalization
const ALEF_VARIANTS = /[\u0622\u0623\u0625\u0671]/g;
const TASHKEEL = /[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]/g;
const TATWEEL = /\u0640/g;
const ALEF_MAQSURA = "\u0649";
const YA = "\u064A";
const TA_MARBUTA = "\u0629";
const HA = "\u0647";
function normalizeAr(text) {
    let s = text.replace(TASHKEEL, "");
    s = s.replace(TATWEEL, "");
    s = s.replace(ALEF_VARIANTS, "\u0627");
    s = s.replace(new RegExp(ALEF_MAQSURA, "g"), YA);
    s = s.replace(new RegExp(TA_MARBUTA, "g"), HA);
    return s;
}
function normalizeEn(text) {
    return text.toLowerCase().replace(/-/g, "").replace(/'/g, "").trim();
}
function claimEn(key, entry) {
    const existing = enIndex.get(key);
    if (!existing || entry.corpusShare > existing.corpusShare) {
        enIndex.set(key, entry);
    }
}
function build() {
    if (built)
        return;
    const entries = (0, data_1.getEntries)();
    const corrections = (0, data_1.getCorrections)();
    for (const entry of entries) {
        // AR index
        if (!arIndex.has(entry.ar))
            arIndex.set(entry.ar, entry);
        const normAr = normalizeAr(entry.ar);
        if (!arNormIndex.has(normAr))
            arNormIndex.set(normAr, entry);
        for (const v of entry.arVariants) {
            const vStripped = v.trim();
            if (vStripped) {
                if (!arIndex.has(vStripped))
                    arIndex.set(vStripped, entry);
                const normV = normalizeAr(vStripped);
                if (!arNormIndex.has(normV))
                    arNormIndex.set(normV, entry);
            }
        }
        // EN index — keep the higher-share lemma on a colliding key
        claimEn(normalizeEn(entry.en), entry);
        for (const v of entry.enVariants) {
            const vStripped = v.trim();
            if (vStripped) {
                claimEn(normalizeEn(vStripped), entry);
            }
        }
    }
    // Correction index
    for (const [k, v] of Object.entries(corrections)) {
        correctionIndex.set(k, v);
    }
    allEntries = [...entries];
    ranked = [...entries].sort((a, b) => b.corpusShare - a.corpusShare);
    built = true;
}
function ensureBuilt() {
    if (!built) {
        build();
    }
}
function lookupAr(name) {
    ensureBuilt();
    let entry = arIndex.get(name);
    if (entry)
        return entry;
    return arNormIndex.get(normalizeAr(name));
}
function lookupEn(name) {
    ensureBuilt();
    return enIndex.get(normalizeEn(name));
}
function isArabic(text) {
    return /[\u0600-\u06FF\uFE70-\uFEFF]/.test(text);
}
function lookup(name) {
    ensureBuilt();
    if (isArabic(name)) {
        return lookupAr(name);
    }
    return lookupEn(name);
}
function getCorrect(surface) {
    ensureBuilt();
    return correctionIndex.get(surface);
}
function getRanked() {
    ensureBuilt();
    return ranked;
}
function getAll() {
    ensureBuilt();
    return allEntries;
}
function getArForms() {
    ensureBuilt();
    return arIndex;
}
function getArNormForms() {
    ensureBuilt();
    return arNormIndex;
}
//# sourceMappingURL=lookupIndices.js.map