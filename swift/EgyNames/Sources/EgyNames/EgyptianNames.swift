import Foundation

public final class EgyptianNames: @unchecked Sendable {
    public let customDataPath: String?
    public let defaultSeed: Int?

    private static func isCompoundPrefix(_ prefix: String) -> Bool {
        let p = LookupIndices.normalizeAr(prefix)
        return ["عبد", "ابو", "ابن", "ام", "نور", "سيف", "شمس", "منه", "فاطمه", "علاء", "بهاء", "ضياء", "سراج", "محيي", "حسام", "تقي"].contains(p)
    }

    public init(seed: Int? = nil, dataPath: String? = nil) {
        self.defaultSeed = seed
        self.customDataPath = dataPath
        LookupIndices.ensureBuilt(customPath: dataPath)
    }

    public func generate(
        count: Int = 5,
        length: Int = 3,
        gender: String? = nil,
        religion: String? = nil,
        seed: Int? = nil
    ) -> [GeneratedName] {
        let s = seed ?? defaultSeed
        return Generator.generate(
            count: count,
            length: length,
            gender: gender,
            religion: religion,
            seed: s,
            customPath: customDataPath
        )
    }

    public func translate(_ fullName: String) -> String {
        return Translator.translate(fullName, customPath: customDataPath)
    }

    public func correct(_ fullName: String) -> String {
        return Corrector.correct(fullName, customPath: customDataPath)
    }

    public func tashkeel(_ fullName: String) -> String {
        let trimmed = fullName.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return fullName }

        let rawTokens = trimmed.components(separatedBy: .whitespacesAndNewlines).filter { !$0.isEmpty }
        var result: [String] = []
        var i = 0
        let n = rawTokens.count

        while i < n {
            let current = rawTokens[i]

            if i < n - 1 && EgyptianNames.isCompoundPrefix(current) {
                let next = rawTokens[i + 1]
                let compound = "\(current) \(next)"
                let compoundNoSpace = "\(current)\(next)"

                var compoundEntry = LookupIndices.lookupAr(compound, customPath: customDataPath)
                if compoundEntry == nil {
                    compoundEntry = LookupIndices.lookupAr(compoundNoSpace, customPath: customDataPath)
                }

                if let found = compoundEntry, !found.tashkeel.isEmpty {
                    result.append(found.tashkeel)
                    i += 2
                    continue
                }
            }

            if let entry = LookupIndices.lookupAr(current, customPath: customDataPath), !entry.tashkeel.isEmpty {
                result.append(entry.tashkeel)
            } else {
                result.append(current)
            }
            i += 1
        }

        return result.joined(separator: " ")
    }

    public func split(_ fullName: String) -> [String] {
        return Splitter.split(fullName, customPath: customDataPath)
    }

    public func annotate(_ fullName: String) -> [NameInfo] {
        return Annotator.annotate(fullName, customPath: customDataPath)
    }

    public func annotateSingle(_ name: String) -> NameInfo? {
        return Annotator.annotateSingle(name, customPath: customDataPath)
    }

    public func meaning(_ name: String) -> [String: String]? {
        guard let entry = LookupIndices.lookup(name, customPath: customDataPath) else {
            return nil
        }
        if entry.meaningAr.isEmpty && entry.meaningEn.isEmpty {
            return nil
        }
        return [
            "ar": entry.meaningAr,
            "en": entry.meaningEn
        ]
    }

    public func families(
        count: Int = 50,
        frequency: FrequencyClass? = nil,
        religion: Religion? = nil,
        startsWith: String? = nil
    ) -> [NameInfo] {
        return SearchEngine.search(
            gender: nil,
            religion: religion,
            role: .family,
            frequency: frequency,
            startsWith: startsWith,
            minCorpusShare: 0.0,
            maxResults: count,
            sortBy: "corpus_share",
            customPath: customDataPath
        )
    }

    public func search(
        gender: Gender? = nil,
        religion: Religion? = nil,
        role: NameRole? = nil,
        frequency: FrequencyClass? = nil,
        startsWith: String? = nil,
        endsWith: String? = nil,
        contains: String? = nil,
        minCorpusShare: Double = 0.0,
        maxResults: Int = 50,
        sortBy: String = "corpus_share"
    ) -> [NameInfo] {
        return SearchEngine.search(
            gender: gender,
            religion: religion,
            role: role,
            frequency: frequency,
            startsWith: startsWith,
            endsWith: endsWith,
            contains: contains,
            minCorpusShare: minCorpusShare,
            maxResults: maxResults,
            sortBy: sortBy,
            customPath: customDataPath
        )
    }

    public func detectGender(_ fullName: String) -> GenderDetection {
        let parts = split(fullName)
        guard let first = parts.first,
              let entry = LookupIndices.lookup(first, customPath: customDataPath),
              entry.gender != .neutral else {
            return GenderDetection(gender: "neutral", confidence: 0.5)
        }

        let confidence = (entry.gender == .female) ? 0.95 : 0.90
        return GenderDetection(gender: entry.gender.rawValue, confidence: confidence)
    }

    public func detectReligion(_ fullName: String) -> ReligionDetection {
        let parts = split(fullName)
        guard !parts.isEmpty else {
            return ReligionDetection(religion: "unknown", confidence: 0.0)
        }

        var cCount = 0
        var mCount = 0
        for p in parts {
            if let entry = LookupIndices.lookup(p, customPath: customDataPath) {
                if entry.religion == .christian { cCount += 1 }
                else if entry.religion == .muslim { mCount += 1 }
            }
        }

        if cCount > 0 && cCount >= mCount {
            return ReligionDetection(religion: "christian", confidence: min(0.99, 0.60 + Double(cCount) * 0.20))
        }
        if mCount > 0 {
            return ReligionDetection(religion: "muslim", confidence: min(0.99, 0.60 + Double(mCount) * 0.15))
        }
        return ReligionDetection(religion: "neutral", confidence: 0.5)
    }

    public func analyzeChain(_ fullName: String) -> [ChainPart] {
        let parts = split(fullName)
        let n = parts.count
        var chain: [ChainPart] = []

        for (i, p) in parts.enumerated() {
            let role: String
            let detail: String

            if i == 0 {
                role = "person"
                detail = "Given Name (اسم الشخص)"
            } else if i == 1 {
                role = "father"
                detail = "Father's Name (اسم الأب)"
            } else if i == 2 {
                role = "grandfather"
                detail = "Grandfather's Name (اسم الجد)"
            } else if i == n - 1 && n >= 4 {
                role = "family_name"
                detail = "Family / Surname (اللقب / اسم العائلة)"
            } else {
                role = "ancestor"
                detail = "Ancestor Name (السلف)"
            }

            chain.append(ChainPart(name: p, slot: i + 1, role: role, detail: detail))
        }

        return chain
    }

    public func rank(_ name: String) -> RankInfo? {
        guard let entry = LookupIndices.lookup(name, customPath: customDataPath) else {
            return nil
        }

        let ranked = LookupIndices.getRanked(customPath: customDataPath)
        var pos = 1
        for r in ranked {
            if r.ar == entry.ar { break }
            pos += 1
        }

        let percentile = 100.0 * (1.0 - Double(pos) / Double(ranked.count))
        let shareStr = String(format: "%.4f%%", entry.corpusShare)
        return RankInfo(
            rank: pos,
            percentile: percentile,
            corpusShare: shareStr,
            description: "Rank #\(pos) of \(ranked.count)"
        )
    }

    public func uniqueness(_ fullName: String) -> UniquenessScore {
        let parts = split(fullName)
        guard !parts.isEmpty else {
            return UniquenessScore(score: 0.0, label: "unknown", note: "Empty name")
        }

        var prod = 1.0
        var found = 0
        for p in parts {
            if let entry = LookupIndices.lookup(p, customPath: customDataPath), entry.corpusShare > 0.0 {
                prod *= (entry.corpusShare / 100.0)
                found += 1
            }
        }

        if found == 0 {
            return UniquenessScore(score: 0.5, label: "moderate", note: "Unranked name elements")
        }

        let score = 1.0 - min(1.0, prod * 10000.0)
        let label: String
        if score > 0.85 { label = "rare" }
        else if score > 0.60 { label = "distinctive" }
        else if score > 0.35 { label = "moderate" }
        else { label = "common" }

        return UniquenessScore(score: score, label: label, note: "Estimated uniqueness score")
    }

    public func isValid(_ name: String) -> Bool {
        return LookupIndices.lookup(name, customPath: customDataPath) != nil
    }

    public func stats() -> [String: Any] {
        LookupIndices.ensureBuilt(customPath: customDataPath)
        let all = LookupIndices.getAll(customPath: customDataPath)
        var given = 0, family = 0, male = 0, female = 0

        for e in all {
            if e.role == .given { given += 1 } else { family += 1 }
            if e.gender == .male { male += 1 } else if e.gender == .female { female += 1 }
        }

        return [
            "total_names": all.count,
            "given_names": given,
            "family_names": family,
            "male_names": male,
            "female_names": female,
            "metadata": LookupIndices.getMetadata(customPath: customDataPath)
        ]
    }
}

public typealias EgyNames = EgyptianNames
