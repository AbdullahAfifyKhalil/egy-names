import Foundation

public final class LookupIndices: @unchecked Sendable {
    private static var arIndex: [String: NameEntry] = [:]
    private static var enIndex: [String: NameEntry] = [:]
    private static var arNormIndex: [String: NameEntry] = [:]
    private static var correctionIndex: [String: String] = [:]
    private static var allEntries: [NameEntry] = []
    private static var rankedEntries: [NameEntry] = []
    private static var metadata: [String: AnyCodable] = [:]
    private static var isBuilt = false
    private static let lock = NSLock()

    public static func normalizeAr(_ text: String) -> String {
        guard !text.isEmpty else { return "" }
        var result = ""
        result.reserveCapacity(text.utf8.count)

        for scalar in text.unicodeScalars {
            let v = scalar.value

            // Strip Tashkeel & Diacritics
            if (v >= 0x064B && v <= 0x065F) || v == 0x0670 || (v >= 0x0610 && v <= 0x061A) || (v >= 0x06D6 && v <= 0x06ED) {
                continue
            }

            // Strip Tatweel (0x0640)
            if v == 0x0640 {
                continue
            }

            // Normalize Alef variants (آ 0x0622, أ 0x0623, إ 0x0625, ٱ 0x0671 -> ا 0x0627)
            if v == 0x0622 || v == 0x0623 || v == 0x0625 || v == 0x0671 {
                result.append("\u{0627}")
                continue
            }

            // Alef Maqsura (ى 0x0649 -> ي 0x064A)
            if v == 0x0649 {
                result.append("\u{064A}")
                continue
            }

            // Ta Marbuta (ة 0x0629 -> ه 0x0647)
            if v == 0x0629 {
                result.append("\u{0647}")
                continue
            }

            result.append(String(scalar))
        }

        return result
    }

    public static func normalizeEn(_ text: String) -> String {
        return text.lowercased().trimmingCharacters(in: .whitespacesAndNewlines)
    }

    public static func isArabic(_ text: String) -> Bool {
        for scalar in text.unicodeScalars {
            if scalar.value >= 0x0600 && scalar.value <= 0x06FF {
                return true
            }
        }
        return false
    }

    public static func ensureBuilt(customPath: String? = nil) {
        if isBuilt { return }
        lock.lock()
        defer { lock.unlock() }
        if isBuilt { return }

        let bundle = DataLoader.loadBundle(customPath: customPath)
        allEntries = bundle.names
        metadata = bundle.metadata
        correctionIndex = bundle.corrections

        for entry in allEntries {
            arIndex[entry.ar] = entry
            let norm = normalizeAr(entry.ar)
            if arNormIndex[norm] == nil {
                arNormIndex[norm] = entry
            }

            for v in entry.arVariants {
                if !v.isEmpty {
                    arIndex[v] = entry
                    let normV = normalizeAr(v)
                    if arNormIndex[normV] == nil {
                        arNormIndex[normV] = entry
                    }
                }
            }

            let normEn = normalizeEn(entry.en)
            if enIndex[normEn] == nil {
                enIndex[normEn] = entry
            }
            for v in entry.enVariants {
                if !v.isEmpty {
                    let normEv = normalizeEn(v)
                    if enIndex[normEv] == nil {
                        enIndex[normEv] = entry
                    }
                }
            }
        }

        rankedEntries = allEntries.sorted(by: { $0.corpusShare > $1.corpusShare })
        isBuilt = true
    }

    public static func lookupAr(_ name: String, customPath: String? = nil) -> NameEntry? {
        ensureBuilt(customPath: customPath)
        let trimmed = name.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return nil }

        // 1. Direct match
        if let direct = arIndex[trimmed] {
            return direct
        }

        // 2. Normalized match
        let norm = normalizeAr(trimmed)
        if let normMatch = arNormIndex[norm] {
            return normMatch
        }

        // 3. Alif / Alif Maqsura phonetic equivalence
        if norm.hasSuffix("\u{0627}") {
            let alt = String(norm.dropLast()) + "\u{064A}"
            if let altMatch = arNormIndex[alt] {
                return altMatch
            }
        } else if norm.hasSuffix("\u{064A}") {
            let alt = String(norm.dropLast()) + "\u{0627}"
            if let altMatch = arNormIndex[alt] {
                return altMatch
            }
        }

        // 4. Space-less compound match
        let noSpace = trimmed.replacingOccurrences(of: " ", with: "")
        if noSpace != trimmed {
            if let nsMatch = arIndex[noSpace] {
                return nsMatch
            }
            if let nsNormMatch = arNormIndex[normalizeAr(noSpace)] {
                return nsNormMatch
            }
        }

        return nil
    }

    public static func lookupEn(_ name: String, customPath: String? = nil) -> NameEntry? {
        ensureBuilt(customPath: customPath)
        return enIndex[normalizeEn(name)]
    }

    public static func lookup(_ name: String, customPath: String? = nil) -> NameEntry? {
        ensureBuilt(customPath: customPath)
        if isArabic(name) {
            return lookupAr(name, customPath: customPath)
        }
        return lookupEn(name, customPath: customPath)
    }

    public static func getCorrection(surface: String, customPath: String? = nil) -> String? {
        ensureBuilt(customPath: customPath)
        return correctionIndex[surface]
    }

    public static func getAll(customPath: String? = nil) -> [NameEntry] {
        ensureBuilt(customPath: customPath)
        return allEntries
    }

    public static func getRanked(customPath: String? = nil) -> [NameEntry] {
        ensureBuilt(customPath: customPath)
        return rankedEntries
    }

    public static func getArNormForms(customPath: String? = nil) -> [String: NameEntry] {
        ensureBuilt(customPath: customPath)
        return arNormIndex
    }

    public static func getMetadata(customPath: String? = nil) -> [String: AnyCodable] {
        ensureBuilt(customPath: customPath)
        return metadata
    }
}
