"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.split = split;
const lookupIndices_1 = require("./lookupIndices");
const BASE_SEGMENT_COST = 1.0;
const UNKNOWN_PENALTY = 8.0;
const FREQ_BONUS = { c: -0.6, n: -0.2, r: 0.0 };
const LENGTH_BONUS_PER_CHAR = -0.05;
function dpSegment(text) {
    const arIndex = (0, lookupIndices_1.getArForms)();
    const arNorm = (0, lookupIndices_1.getArNormForms)();
    const n = text.length;
    // dp[i] = [cost, backpointer, isKnown]
    const INF = Infinity;
    const dp = Array(n + 1).fill([INF, -1, false]);
    dp[0] = [0.0, 0, true];
    for (let i = 1; i <= n; i++) {
        for (let j = Math.max(0, i - 30); j < i; j++) {
            if (dp[j][0] === INF)
                continue;
            const substr = text.substring(j, i);
            if (substr.length < 2 && j > 0)
                continue;
            let entry = arIndex.get(substr);
            if (!entry) {
                entry = arNorm.get((0, lookupIndices_1.normalizeAr)(substr));
            }
            if (entry) {
                const cost = dp[j][0] +
                    BASE_SEGMENT_COST +
                    (FREQ_BONUS[entry.frequency.charAt(0)] || 0.0) +
                    LENGTH_BONUS_PER_CHAR * substr.length;
                if (cost < dp[i][0]) {
                    dp[i] = [cost, j, true];
                }
            }
            else {
                const cost = dp[j][0] + UNKNOWN_PENALTY + substr.length;
                if (cost < dp[i][0]) {
                    dp[i] = [cost, j, false];
                }
            }
        }
    }
    if (dp[n][0] === INF) {
        return [text];
    }
    const segments = [];
    let pos = n;
    while (pos > 0) {
        const prev = dp[pos][1];
        segments.push(text.substring(prev, pos));
        pos = prev;
    }
    return segments.reverse();
}
function split(fullName) {
    if (!fullName || !fullName.trim())
        return [];
    const text = fullName.trim();
    if (text.includes(" ")) {
        return text.split(/\s+/);
    }
    if ((0, lookupIndices_1.isArabic)(text)) {
        const entry = (0, lookupIndices_1.lookup)(text);
        if (entry) {
            return [text];
        }
        return dpSegment(text);
    }
    return [text];
}
//# sourceMappingURL=splitter.js.map