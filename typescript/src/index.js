"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.EgyptianNames = void 0;
const data_1 = require("./data");
const lookupIndices_1 = require("./lookupIndices");
const types_1 = require("./types");
const generator_1 = require("./generator");
const translator_1 = require("./translator");
const annotator_1 = require("./annotator");
const splitter_1 = require("./splitter");
const corrector_1 = require("./corrector");
const search_1 = require("./search");
class EgyptianNames {
    seed;
    constructor(options) {
        this.seed = options?.seed;
    }
    // Core Features
    generate(options) {
        return (0, generator_1.generateNames)({
            ...options,
            seed: options?.seed !== undefined ? options.seed : this.seed,
        });
    }
    translate(name, to) {
        return (0, translator_1.translate)(name, to);
    }
    annotate(name) {
        return (0, annotator_1.annotate)(name);
    }
    split(fullName) {
        return (0, splitter_1.split)(fullName);
    }
    tashkeel(name) {
        const tokens = name.trim().split(/\s+/);
        const result = tokens.map((t) => {
            const entry = (0, lookupIndices_1.lookupAr)(t);
            return entry && entry.tashkeel ? entry.tashkeel : t;
        });
        return result.join(" ");
    }
    correct(name) {
        return (0, corrector_1.correct)(name);
    }
    meaning(name) {
        const entry = (0, lookupIndices_1.lookup)(name);
        if (!entry)
            return null;
        if (!entry.meaningAr && !entry.meaningEn)
            return null;
        return {
            ar: entry.meaningAr,
            en: entry.meaningEn,
        };
    }
    families(options) {
        return (0, search_1.search)({
            role: "family",
            maxResults: options?.count || 50,
            frequency: options?.frequency,
            religion: options?.religion,
            startsWith: options?.startsWith,
        });
    }
    search(options) {
        return (0, search_1.search)(options);
    }
    // Creative Features
    isValid(name) {
        return (0, lookupIndices_1.lookup)(name) !== undefined;
    }
    detectGender(fullName) {
        const tokens = fullName.trim().split(/\s+/);
        if (tokens.length === 0)
            return { gender: "neutral", confidence: 0 };
        let maleScore = 0;
        let femaleScore = 0;
        let neutralScore = 0;
        let totalWeight = 0;
        for (let i = 0; i < tokens.length; i++) {
            const entry = (0, lookupIndices_1.lookup)(tokens[i]);
            if (!entry)
                continue;
            const w = i === 0 ? 4.0 : i === 1 ? 2.0 : 1.0;
            totalWeight += w;
            if (entry.gender === types_1.Gender.MALE)
                maleScore += w;
            else if (entry.gender === types_1.Gender.FEMALE)
                femaleScore += w;
            else
                neutralScore += w;
        }
        if (totalWeight === 0)
            return { gender: "neutral", confidence: 0 };
        const maxScore = Math.max(maleScore, femaleScore, neutralScore);
        const confidence = maxScore / totalWeight;
        if (maxScore === maleScore)
            return { gender: "male", confidence };
        if (maxScore === femaleScore)
            return { gender: "female", confidence };
        return { gender: "neutral", confidence };
    }
    detectReligion(fullName) {
        const tokens = fullName.trim().split(/\s+/);
        if (tokens.length === 0)
            return { religion: "neutral", confidence: 0 };
        let muslimScore = 0;
        let christianScore = 0;
        let neutralScore = 0;
        let totalWeight = 0;
        for (let i = 0; i < tokens.length; i++) {
            const entry = (0, lookupIndices_1.lookup)(tokens[i]);
            if (!entry)
                continue;
            const w = 1.0;
            totalWeight += w;
            if (entry.religion === types_1.Religion.MUSLIM)
                muslimScore += w;
            else if (entry.religion === types_1.Religion.CHRISTIAN)
                christianScore += w;
            else
                neutralScore += w;
        }
        if (totalWeight === 0)
            return { religion: "neutral", confidence: 0 };
        const maxScore = Math.max(muslimScore, christianScore, neutralScore);
        const confidence = maxScore / totalWeight;
        if (maxScore === muslimScore)
            return { religion: "muslim", confidence };
        if (maxScore === christianScore)
            return { religion: "christian", confidence };
        return { religion: "neutral", confidence };
    }
    fingerprint(name) {
        const entry = (0, lookupIndices_1.lookup)(name);
        if (!entry)
            return null;
        const slots = entry.slotPcts;
        const slotLabels = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th+"];
        let peakSlot = 0;
        let maxPct = -1;
        for (let i = 0; i < slots.length; i++) {
            if (slots[i] > maxPct) {
                maxPct = slots[i];
                peakSlot = i;
            }
        }
        let nameType = "";
        if (entry.role === types_1.NameRole.FAMILY) {
            nameType = slots[0] < 1.0 ? "pure_surname" : "surname_given";
        }
        else if (peakSlot === 0 && slots[0] > 40) {
            nameType = "primary_given";
        }
        else if (peakSlot === 0) {
            nameType = "given_name";
        }
        else {
            nameType = "patronymic";
        }
        const descParts = [];
        if (nameType === "primary_given")
            descParts.push(`Dominant first name (${slots[0].toFixed(1)}% in slot 1)`);
        else if (nameType === "pure_surname")
            descParts.push("Almost exclusively a family/surname");
        else if (nameType === "given_name")
            descParts.push("Given name appearing across multiple positions");
        else
            descParts.push(`Peaks in slot ${peakSlot + 1}`);
        if (entry.frequency === types_1.FrequencyClass.COMMON)
            descParts.push("very common");
        else if (entry.frequency === types_1.FrequencyClass.RARE)
            descParts.push("rare");
        const slotMap = {};
        for (let i = 0; i < slotLabels.length; i++) {
            slotMap[slotLabels[i]] = Math.round(slots[i] * 100) / 100;
        }
        return {
            name_ar: entry.ar,
            name_en: entry.en,
            type: nameType,
            slots: slotMap,
            corpus_share: entry.corpusShare,
            description: descParts.join("; "),
        };
    }
    rank(name) {
        const entry = (0, lookupIndices_1.lookup)(name);
        if (!entry)
            return null;
        const ranked = (0, lookupIndices_1.getRanked)();
        const total = ranked.length;
        for (let i = 0; i < total; i++) {
            if (ranked[i].ar === entry.ar) {
                const rankPos = i + 1;
                const percentile = (1 - (rankPos - 1) / total) * 100;
                let desc = `The #${rankPos} most common name in the Egyptian corpus`;
                if (rankPos <= 10)
                    desc = `Top 10 — ${desc}`;
                else if (rankPos <= 100)
                    desc = `Top 100 — ${desc}`;
                else if (rankPos <= 1000)
                    desc = `Top 1000 — ${desc}`;
                return {
                    rank: rankPos,
                    percentile: Math.round(percentile * 100) / 100,
                    corpus_share: `${entry.corpusShare.toFixed(4)}%`,
                    description: desc,
                };
            }
        }
        return null;
    }
    levenshtein(s1, s2) {
        if (s1.length < s2.length)
            return this.levenshtein(s2, s1);
        if (s2.length === 0)
            return s1.length;
        let prevRow = Array.from({ length: s2.length + 1 }, (_, i) => i);
        for (let i = 0; i < s1.length; i++) {
            const currRow = [i + 1];
            for (let j = 0; j < s2.length; j++) {
                const insertions = prevRow[j + 1] + 1;
                const deletions = currRow[j] + 1;
                const substitutions = prevRow[j] + (s1[i] !== s2[j] ? 1 : 0);
                currRow.push(Math.min(insertions, deletions, substitutions));
            }
            prevRow = currRow;
        }
        return prevRow[prevRow.length - 1];
    }
    similar(name, options) {
        const maxResults = options?.maxResults || 10;
        const maxDistance = options?.maxDistance || 3;
        const useAr = (0, lookupIndices_1.isArabic)(name);
        const entries = (0, lookupIndices_1.getAll)();
        const nameNorm = useAr ? (0, lookupIndices_1.normalizeAr)(name) : (0, lookupIndices_1.normalizeEn)(name);
        const scored = [];
        for (const e of entries) {
            const candidate = useAr ? e.ar : e.en;
            const candNorm = useAr ? (0, lookupIndices_1.normalizeAr)(candidate) : (0, lookupIndices_1.normalizeEn)(candidate);
            if (candNorm === nameNorm)
                continue;
            const dist = this.levenshtein(nameNorm, candNorm);
            if (dist <= maxDistance) {
                scored.push({ dist, share: e.corpusShare, candidate });
            }
        }
        scored.sort((a, b) => {
            if (a.dist !== b.dist)
                return a.dist - b.dist;
            return b.share - a.share;
        });
        return scored.slice(0, maxResults).map((s) => s.candidate);
    }
    analyzeChain(fullName) {
        const tokens = fullName.trim().split(/\s+/);
        if (tokens.length === 0)
            return [];
        const parts = [];
        const n = tokens.length;
        for (let i = 0; i < n; i++) {
            const t = tokens[i];
            const entry = (0, lookupIndices_1.lookup)(t);
            const slot = i + 1;
            let roleLabel = "";
            let detail = "";
            if (i === 0) {
                roleLabel = "person";
                detail = "The individual's given name";
            }
            else if (i === n - 1 && entry && entry.role === types_1.NameRole.FAMILY) {
                roleLabel = "family_name";
                detail = "Family/tribal surname";
            }
            else if (i === 1) {
                roleLabel = "father";
                detail = "Father's name";
            }
            else if (i === 2) {
                roleLabel = "grandfather";
                detail = "Paternal grandfather";
            }
            else if (i === 3) {
                roleLabel = "great_grandfather";
                detail = "Great-grandfather";
            }
            else {
                roleLabel = "ancestor";
                detail = `Ancestor (generation ${i})`;
            }
            parts.push({
                name: t,
                slot,
                role: roleLabel,
                detail,
            });
        }
        return parts;
    }
    uniqueness(fullName) {
        const tokens = fullName.trim().split(/\s+/);
        if (tokens.length === 0)
            return { score: 0.5, label: "unknown", note: "Empty input" };
        const shares = [];
        let unknownCount = 0;
        for (const t of tokens) {
            const entry = (0, lookupIndices_1.lookup)(t);
            if (entry)
                shares.push(entry.corpusShare);
            else
                unknownCount++;
        }
        if (shares.length === 0) {
            return { score: 1.0, label: "unknown", note: "None of the name parts are in the Egyptian corpus" };
        }
        let logSum = 0;
        for (const s of shares) {
            logSum += Math.log(Math.max(s, 1e-9));
        }
        const logMean = logSum / shares.length;
        const maxLog = 2.6;
        const minLog = -9.2;
        let score = 1.0 - (logMean - minLog) / (maxLog - minLog);
        score = Math.max(0.0, Math.min(1.0, score));
        score = Math.min(1.0, score + unknownCount * 0.15);
        let label = "";
        let note = "";
        if (score < 0.2) {
            label = "extremely_common";
            note = "Each part is among the most common names nationally";
        }
        else if (score < 0.4) {
            label = "common";
            note = "Well-known name parts with high national frequency";
        }
        else if (score < 0.6) {
            label = "moderate";
            note = "A mix of common and less common name parts";
        }
        else if (score < 0.8) {
            label = "distinctive";
            note = "Contains uncommon or regionally specific names";
        }
        else {
            label = "highly_unique";
            note = "Rare name combination — distinctive family heritage";
        }
        return {
            score: Math.round(score * 1000) / 1000,
            label,
            note,
        };
    }
    format(fullName, options) {
        const style = options?.style || "full";
        const tokens = fullName.trim().split(/\s+/);
        if (tokens.length === 0)
            return fullName;
        if (style === "full")
            return tokens.join(" ");
        if (style === "first_last") {
            const first = tokens[0];
            const last = tokens.length > 1 ? tokens[tokens.length - 1] : "";
            return { first, last };
        }
        if (style === "western") {
            const firstEn = (0, translator_1.translateToken)(tokens[0], "en");
            const lastEn = tokens.length > 1 ? (0, translator_1.translateToken)(tokens[tokens.length - 1], "en") : "";
            return `${firstEn} ${lastEn}`.trim();
        }
        if (style === "initials") {
            const initials = tokens.slice(0, -1).map((t) => `${t[0]}.`);
            initials.push(tokens[tokens.length - 1]);
            return initials.join(" ");
        }
        return tokens.join(" ");
    }
    suggest(options) {
        const results = (0, search_1.search)({
            gender: options?.gender,
            religion: options?.religion,
            role: options?.role,
            frequency: options?.frequency,
            startsWith: options?.startsWith,
            maxResults: options?.count || 10,
        });
        return results.map((r) => r.ar);
    }
    stats() {
        const meta = (0, data_1.getMetadata)();
        const entries = (0, lookupIndices_1.getAll)();
        let given = 0;
        let family = 0;
        let male = 0;
        let female = 0;
        for (const e of entries) {
            if (e.role === types_1.NameRole.GIVEN)
                given++;
            if (e.role === types_1.NameRole.FAMILY)
                family++;
            if (e.gender === types_1.Gender.MALE)
                male++;
            if (e.gender === types_1.Gender.FEMALE)
                female++;
        }
        return {
            ...meta,
            total_names: entries.length,
            given_names: given,
            family_names: family,
            male_names: male,
            female_names: female,
        };
    }
    get batch() {
        return new BatchProcessor(this);
    }
}
exports.EgyptianNames = EgyptianNames;
class BatchProcessor {
    parent;
    constructor(parent) {
        this.parent = parent;
    }
    translate(names, to) {
        return names.map((n) => this.parent.translate(n, to));
    }
    annotate(names) {
        return names.map((n) => this.parent.annotate(n));
    }
    correct(names) {
        return names.map((n) => this.parent.correct(n));
    }
    split(names) {
        return names.map((n) => this.parent.split(n));
    }
    detectGender(names) {
        return names.map((n) => this.parent.detectGender(n));
    }
    detectReligion(names) {
        return names.map((n) => this.parent.detectReligion(n));
    }
    tashkeel(names) {
        return names.map((n) => this.parent.tashkeel(n));
    }
}
//# sourceMappingURL=index.js.map