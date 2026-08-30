"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.NON_PERSONAL_AR = void 0;
exports.isPersonalEntry = isPersonalEntry;
exports.isGeneratableEntry = isGeneratableEntry;
exports.isLineageRole = isLineageRole;
const types_1 = require("./types");
exports.NON_PERSONAL_AR = new Set([
    "الله",
    "الرجل",
    "الرجال",
    "شربه",
    "لافندي",
    "لفندي",
    "ماء",
    "البيت",
]);
function isPersonalEntry(entry) {
    return !exports.NON_PERSONAL_AR.has(entry.ar);
}
function isGeneratableEntry(entry) {
    return isPersonalEntry(entry) && !entry.ar.trim().includes(" ");
}
function isLineageRole(entry) {
    return entry.role === types_1.NameRole.FAMILY;
}