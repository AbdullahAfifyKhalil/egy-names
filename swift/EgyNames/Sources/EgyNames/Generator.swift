import Foundation

public final class Generator: @unchecked Sendable {
    public static func generate(
        count: Int = 5,
        length: Int = 3,
        gender: String? = nil,
        religion: String? = nil,
        seed: Int? = nil,
        customPath: String? = nil
    ) -> [GeneratedName] {
        LookupIndices.ensureBuilt(customPath: customPath)
        let allEntries = LookupIndices.getAll(customPath: customPath)

        let targetGender = gender.map { Gender.from(string: $0) }
        let targetReligion = religion.map { Religion.from(string: $0) }

        var slotCandidates: [[NameEntry]] = Array(repeating: [], count: 5)
        var slotWeights: [[Double]] = Array(repeating: [], count: 5)

        for slot in 0..<5 {
            for entry in allEntries {
                if slot == 0 {
                    if let tg = targetGender, entry.gender != tg && entry.gender != .neutral {
                        continue
                    }
                } else {
                    if entry.gender != .male && entry.gender != .neutral && entry.role != .family {
                        continue
                    }
                }

                if let tr = targetReligion, entry.religion != tr && entry.religion != .neutral {
                    continue
                }

                var weight = entry.corpusShare
                if slot < entry.slotPcts.count {
                    weight *= (entry.slotPcts[slot] / 100.0)
                }

                if weight > 0.0 {
                    slotCandidates[slot].append(entry)
                    slotWeights[slot].append(weight)
                }
            }
        }

        // Fallback for empty slots
        for slot in 0..<5 {
            if slotCandidates[slot].isEmpty {
                for entry in allEntries {
                    if slot == 0, let tg = targetGender, entry.gender != tg { continue }
                    slotCandidates[slot].append(entry)
                    slotWeights[slot].append(entry.corpusShare)
                }
            }
        }

        var results: [GeneratedName] = []
        for _ in 0..<count {
            var partsAr: [String] = []
            var partsEn: [String] = []
            var seen: Set<String> = []

            for s in 0..<length {
                let slotIdx = min(s, 4)
                let candidates = slotCandidates[slotIdx]
                let weights = slotWeights[slotIdx]
                guard !candidates.isEmpty else { continue }

                let totalWeight = weights.reduce(0, +)
                var selected = candidates[0]
                var attempts = 0

                repeat {
                    let randomVal = Double.random(in: 0..<totalWeight)
                    var runningSum = 0.0
                    for (idx, w) in weights.enumerated() {
                        runningSum += w
                        if randomVal <= runningSum {
                            selected = candidates[idx]
                            break
                        }
                    }
                    attempts += 1
                } while seen.contains(selected.ar) && attempts < 10

                seen.insert(selected.ar)
                partsAr.append(selected.ar)
                partsEn.append(selected.en)
            }

            results.append(GeneratedName(
                ar: partsAr.joined(separator: " "),
                en: partsEn.joined(separator: " "),
                partsAr: partsAr,
                partsEn: partsEn
            ))
        }

        return results
    }
}
