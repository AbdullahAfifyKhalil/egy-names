"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.loadRaw = loadRaw;
exports.getBundle = getBundle;
exports.getEntries = getEntries;
exports.getCorrections = getCorrections;
exports.getMetadata = getMetadata;
exports.clearCache = clearCache;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const zlib = __importStar(require("zlib"));
const types_1 = require("./types");
const DATA_FILE = path.join(__dirname, "data", "names.json.gz");
let cache = null;
let entriesCache = null;
function loadRaw(filePath = DATA_FILE) {
    const compressed = fs.readFileSync(filePath);
    const jsonStr = zlib.gunzipSync(compressed).toString("utf-8");
    return JSON.parse(jsonStr);
}
function getBundle(filePath) {
    if (cache !== null && !filePath) {
        return cache;
    }
    const bundle = loadRaw(filePath);
    if (!filePath) {
        cache = bundle;
    }
    return bundle;
}
function getEntries(filePath) {
    if (entriesCache !== null && !filePath) {
        return entriesCache;
    }
    const bundle = getBundle(filePath);
    const entries = bundle.names.map((r) => new types_1.NameEntry(r));
    if (!filePath) {
        entriesCache = entries;
    }
    return entries;
}
function getCorrections(filePath) {
    const bundle = getBundle(filePath);
    return bundle.corrections || {};
}
function getMetadata(filePath) {
    const bundle = getBundle(filePath);
    return {
        version: bundle.version || "0.0.0",
        corpus_tokens: bundle.corpus_tokens || 0,
        corpus_students: bundle.corpus_students || 0,
        cohort_years: bundle.cohort_years || [],
    };
}
function clearCache() {
    cache = null;
    entriesCache = null;
}
//# sourceMappingURL=data.js.map