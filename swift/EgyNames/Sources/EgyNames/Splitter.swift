import Foundation

public final class Splitter: @unchecked Sendable {
    private static let BASE_SEGMENT_COST = 1.0
    private static let UNKNOWN_PENALTY = 8.0
    private static let LENGTH_BONUS_PER_CHAR = -0.05

    private static func getFreqBonus(_ fc: FrequencyClass) -> Double {
        switch fc {
        case .common: return -0.6
        case .normal: return -0.2
        case .rare: return 0.0
        }
    }

    public static func dpSegment(_ text: String, customPath: String? = nil) -> [String] {
        LookupIndices.ensureBuilt(customPath: customPath)
        let chars = Array(text)
        let n = chars.count
        guard n > 0 else { return [text] }

        let arNorm = LookupIndices.getArNormForms(customPath: customPath)

        var dpCost = Array(repeating: Double.infinity, count: n + 1)
        var dpPrev = Array(repeating: -1, count: n + 1)

        dpCost[0] = 0.0
        dpPrev[0] = 0

        for i in 1...n {
            let startJ = (i > 45) ? (i - 45) : 0
            for j in startJ..<i {
                if dpCost[j] == Double.infinity { continue }

                let substr = String(chars[j..<i])
                if substr.count < 2 && j > 0 { continue }

                let norm = LookupIndices.normalizeAr(substr)
                if let entry = arNorm[norm] {
                    let cost = dpCost[j] + BASE_SEGMENT_COST + getFreqBonus(entry.frequency) + LENGTH_BONUS_PER_CHAR * Double(substr.count)
                    if cost < dpCost[i] {
                        dpCost[i] = cost
                        dpPrev[i] = j
                    }
                } else {
                    let cost = dpCost[j] + UNKNOWN_PENALTY + Double(substr.count)
                    if cost < dpCost[i] {
                        dpCost[i] = cost
                        dpPrev[i] = j
                    }
                }
            }
        }

        if dpCost[n] == Double.infinity {
            return [text]
        }

        var segments: [String] = []
        var pos = n
        while pos > 0 {
            let prev = dpPrev[pos]
            if prev < 0 { break }
            segments.append(String(chars[prev..<pos]))
            pos = prev
        }

        return segments.reversed()
    }

    public static func split(_ fullName: String, customPath: String? = nil) -> [String] {
        let trimmed = fullName.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return [] }

        let tokens = trimmed.components(separatedBy: .whitespacesAndNewlines).filter { !$0.isEmpty }
        if tokens.count > 1 {
            return tokens
        }

        if LookupIndices.isArabic(trimmed) {
            if LookupIndices.lookup(trimmed, customPath: customPath) != nil {
                return [trimmed]
            }
            return dpSegment(trimmed, customPath: customPath)
        }

        return [trimmed]
    }
}
