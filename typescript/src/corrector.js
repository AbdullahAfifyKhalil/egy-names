"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.correctToken = correctToken;
exports.correct = correct;
const lookupIndices_1 = require("./lookupIndices");
function correctToken(token) {
    if (!token || !token.trim())
        return token;
    const t = token.trim();
    const canonical = (0, lookupIndices_1.getCorrect)(t);
    if (canonical)
        return canonical;
    const entry = (0, lookupIndices_1.lookupAr)(t);
    if (entry)
        return entry.ar;
    const norm = (0, lookupIndices_1.normalizeAr)(t);
    const arNorm = (0, lookupIndices_1.getArNormForms)();
    const normEntry = arNorm.get(norm);
    if (normEntry)
        return normEntry.ar;
    return t;
}
function correct(name) {
    if (!name || !name.trim())
        return name;
    const tokens = name.trim().split(/\s+/);
    return tokens.map(correctToken).join(" ");
}
//# sourceMappingURL=corrector.js.map