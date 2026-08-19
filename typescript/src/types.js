"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.NameEntry = exports.FrequencyClass = exports.NameRole = exports.Religion = exports.Gender = void 0;
exports.toNameInfo = toNameInfo;
var Gender;
(function (Gender) {
    Gender["MALE"] = "male";
    Gender["FEMALE"] = "female";
    Gender["NEUTRAL"] = "neutral";
})(Gender || (exports.Gender = Gender = {}));
var Religion;
(function (Religion) {
    Religion["MUSLIM"] = "muslim";
    Religion["CHRISTIAN"] = "christian";
    Religion["NEUTRAL"] = "neutral";
})(Religion || (exports.Religion = Religion = {}));
var NameRole;
(function (NameRole) {
    NameRole["GIVEN"] = "given";
    NameRole["FAMILY"] = "family";
})(NameRole || (exports.NameRole = NameRole = {}));
var FrequencyClass;
(function (FrequencyClass) {
    FrequencyClass["COMMON"] = "common";
    FrequencyClass["NORMAL"] = "normal";
    FrequencyClass["RARE"] = "rare";
})(FrequencyClass || (exports.FrequencyClass = FrequencyClass = {}));
class NameEntry {
    ar;
    en;
    gender;
    religion;
    role;
    arVariants;
    enVariants;
    slotPcts;
    corpusShare;
    frequency;
    tashkeel;
    meaningAr;
    meaningEn;
    constructor(raw) {
        this.ar = raw.a;
        this.en = raw.e;
        this.gender = raw.g === "m" ? Gender.MALE : raw.g === "f" ? Gender.FEMALE : Gender.NEUTRAL;
        this.religion = raw.r === "m" ? Religion.MUSLIM : raw.r === "c" ? Religion.CHRISTIAN : Religion.NEUTRAL;
        this.role = raw.l === "g" ? NameRole.GIVEN : NameRole.FAMILY;
        this.arVariants = raw.av ? raw.av.split("|") : [raw.a];
        this.enVariants = raw.ev ? raw.ev.split("|") : [raw.e];
        this.slotPcts = raw.p;
        this.corpusShare = raw.tp;
        this.frequency = raw.fc === "c" ? FrequencyClass.COMMON : raw.fc === "n" ? FrequencyClass.NORMAL : FrequencyClass.RARE;
        this.tashkeel = raw.t;
        this.meaningAr = raw.ma;
        this.meaningEn = raw.me;
    }
}
exports.NameEntry = NameEntry;
function toNameInfo(entry) {
    return {
        ar: entry.ar,
        en: entry.en,
        gender: entry.gender,
        religion: entry.religion,
        role: entry.role,
        frequency_class: entry.frequency,
        corpus_share: entry.corpusShare,
        tashkeel: entry.tashkeel,
        meaning_ar: entry.meaningAr || null,
        meaning_en: entry.meaningEn || null,
        ar_variants: [...entry.arVariants],
        en_variants: [...entry.enVariants],
        slot_distribution: [...entry.slotPcts],
    };
}
//# sourceMappingURL=types.js.map