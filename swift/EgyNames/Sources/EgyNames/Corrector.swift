import Foundation

public final class Corrector: @unchecked Sendable {
    private static func isCompoundPrefix(_ prefix: String) -> Bool {
        let p = LookupIndices.normalizeAr(prefix)
        return ["عبد", "ابو", "ابن", "ام", "نور", "سيف", "شمس", "منه", "فاطمه", "علاء", "بهاء", "ضياء", "سراج", "محيي", "حسام", "تقي"].contains(p)
    }

    public static func correctToken(_ token: String, customPath: String? = nil) -> String {
        let t = token.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !t.isEmpty else { return token }

        // 1. Direct surface correction pair
        if let canonical = LookupIndices.getCorrection(surface: t, customPath: customPath) {
            return canonical
        }

        // 2. Exact match in index
        if let entry = LookupIndices.lookupAr(t, customPath: customPath) {
            return entry.ar
        }

        // 3. Normalized match
        let norm = LookupIndices.normalizeAr(t)
        let arNorm = LookupIndices.getArNormForms(customPath: customPath)
        if let normEntry = arNorm[norm] {
            return normEntry.ar
        }

        // 4. Trailing Alif / Alif Maqsura check
        if norm.hasSuffix("\u{0627}") {
            let alt = String(norm.dropLast()) + "\u{064A}"
            if let altEntry = arNorm[alt] {
                return altEntry.ar
            }
        } else if norm.hasSuffix("\u{064A}") {
            let alt = String(norm.dropLast()) + "\u{0627}"
            if let altEntry = arNorm[alt] {
                return altEntry.ar
            }
        }

        return t
    }

    public static func correct(_ name: String, customPath: String? = nil) -> String {
        let trimmed = name.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return name }

        let rawTokens = trimmed.components(separatedBy: .whitespacesAndNewlines).filter { !$0.isEmpty }
        var result: [String] = []
        var i = 0
        let n = rawTokens.count

        while i < n {
            let current = rawTokens[i]

            // Check compound
            if i < n - 1 && isCompoundPrefix(current) {
                let next = rawTokens[i + 1]
                let compound = "\(current) \(next)"
                let compoundNoSpace = "\(current)\(next)"

                if let direct = LookupIndices.getCorrection(surface: compound, customPath: customPath) {
                    result.append(direct)
                    i += 2
                    continue
                }

                if let directNoSpace = LookupIndices.getCorrection(surface: compoundNoSpace, customPath: customPath) {
                    result.append(directNoSpace)
                    i += 2
                    continue
                }

                var compoundEntry = LookupIndices.lookupAr(compound, customPath: customPath)
                if compoundEntry == nil {
                    compoundEntry = LookupIndices.lookupAr(compoundNoSpace, customPath: customPath)
                }

                if let found = compoundEntry {
                    result.append(found.ar)
                    i += 2
                    continue
                }
            }

            result.append(correctToken(current, customPath: customPath))
            i += 1
        }

        return result.joined(separator: " ")
    }
}
