import Foundation

public final class Translator: @unchecked Sendable {
    private static func isCompoundPrefix(_ prefix: String) -> Bool {
        let p = LookupIndices.normalizeAr(prefix)
        return ["عبد", "ابو", "ابن", "ام", "نور", "سيف", "شمس", "منه", "فاطمه", "علاء", "بهاء", "ضياء", "سراج", "محيي", "حسام", "تقي"].contains(p)
    }

    public static func translate(_ fullName: String, customPath: String? = nil) -> String {
        let trimmed = fullName.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return "" }

        let tokens = trimmed.components(separatedBy: .whitespacesAndNewlines).filter { !$0.isEmpty }
        let isAr = LookupIndices.isArabic(trimmed)
        var result: [String] = []
        var i = 0
        let n = tokens.count

        while i < n {
            let current = tokens[i]

            if isAr {
                if i < n - 1 && isCompoundPrefix(current) {
                    let next = tokens[i + 1]
                    let compound = "\(current) \(next)"
                    let compoundNoSpace = "\(current)\(next)"

                    var entry = LookupIndices.lookupAr(compound, customPath: customPath)
                    if entry == nil {
                        entry = LookupIndices.lookupAr(compoundNoSpace, customPath: customPath)
                    }

                    if let found = entry, !found.en.isEmpty {
                        result.append(found.en)
                        i += 2
                        continue
                    }
                }

                if let entry = LookupIndices.lookupAr(current, customPath: customPath), !entry.en.isEmpty {
                    result.append(entry.en)
                } else {
                    result.append(current)
                }
            } else {
                if let entry = LookupIndices.lookupEn(current, customPath: customPath), !entry.ar.isEmpty {
                    result.append(entry.ar)
                } else {
                    result.append(current)
                }
            }

            i += 1
        }

        return result.joined(separator: " ")
    }
}
