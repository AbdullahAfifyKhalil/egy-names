"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.annotateSingle = annotateSingle;
exports.annotate = annotate;
const lookupIndices_1 = require("./lookupIndices");
const types_1 = require("./types");
function annotateSingle(name) {
    const entry = (0, lookupIndices_1.lookup)(name);
    if (!entry)
        return null;
    return (0, types_1.toNameInfo)(entry);
}
function annotate(name) {
    if (!name || !name.trim())
        return null;
    const tokens = name.trim().split(/\s+/);
    if (tokens.length === 1) {
        return annotateSingle(tokens[0]);
    }
    return tokens.map((t) => annotateSingle(t));
}
//# sourceMappingURL=annotator.js.map