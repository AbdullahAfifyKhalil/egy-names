"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.translateToken = translateToken;
exports.translate = translate;
const lookupIndices_1 = require("./lookupIndices");
function translateToken(token, to) {
    const srcIsArabic = (0, lookupIndices_1.isArabic)(token);
    const target = to || (srcIsArabic ? "en" : "ar");
    if (target === "en") {
        const entry = (0, lookupIndices_1.lookupAr)(token);
        return entry ? entry.en : token;
    }
    else {
        const entry = (0, lookupIndices_1.lookupEn)(token);
        return entry ? entry.ar : token;
    }
}
function translate(fullName, to) {
    if (!fullName || !fullName.trim())
        return fullName;
    const tokens = fullName.trim().split(/\s+/);
    const translated = tokens.map((t) => translateToken(t, to));
    return translated.join(" ");
}
//# sourceMappingURL=translator.js.map