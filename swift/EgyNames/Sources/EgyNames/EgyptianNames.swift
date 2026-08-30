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

    public func tashkeel(_ name: String, dialect: String = "standard") -> String {
        if name.isEmpty { return name }
        let rawTokens = name.split(separator: " ").map(String.init)
        var result: [String] = []
        let isEg = dialect.lowercased().hasPrefix("eg")

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

                if let found = compoundEntry {
                    let val = isEg ? found.tashkeelEg : found.tashkeelStandard
                    if !val.isEmpty {
                        result.append(val)
                        i += 2
                        continue
                    }
                }
            }

            if let entry = LookupIndices.lookupAr(current, customPath: customDataPath) {
                let val = isEg ? entry.tashkeelEg : entry.tashkeelStandard
                result.append(!val.isEmpty ? val : current)
            } else {
                result.append(current)
            }
            i += 1
        }

        return result.joined(separator: " ")
    }

    public func tashkeelEg(_ name: String) -> String {
        return tashkeel(name, dialect: "egyptian")
    }

    public func ipa(_ name: String, dialect: String = "standard") -> String {
        if name.isEmpty { return "" }
        let tokens = name.contains(" ") ? name.split(separator: " ").map(String.init) : split(name)
        let isEg = dialect.lowercased().hasPrefix("eg")
        var ipaParts: [String] = []

        for tok in tokens {
            if let entry = LookupIndices.lookup(tok, customPath: customDataPath) {
                let ipaVal = isEg ? entry.ipaEg : entry.ipaStandard
                if !ipaVal.isEmpty {
                    let clean = ipaVal.trimmingCharacters(in: CharacterSet(charactersIn: "/[]"))
                    ipaParts.append(clean)
                } else {
                    ipaParts.append(tok)
                }
            } else {
                ipaParts.append(tok)
            }
        }

        let joined = ipaParts.joined(separator: " ")
        return isEg ? "[\(joined)]" : "/\(joined)/"
    }

    public func ipaEg(_ name: String) -> String {
        return ipa(name, dialect: "egyptian")
    }

    public func dallaa(_ name: String, format: String = "plain") -> [String] {
        guard let entry = LookupIndices.lookup(name, customPath: customDataPath) else {
            return []
        }
        let fmt = format.lowercased()
        if fmt == "tashkeel" || fmt == "tashkeel_eg" || fmt == "tk" {
            return !entry.dallaaTashkeel.isEmpty ? entry.dallaaTashkeel : entry.dallaaAr
        } else if fmt == "en" || fmt == "english" {
            return entry.dallaaEn
        } else if fmt == "ipa" || fmt == "phonetic" {
            return entry.dallaaIpa
        }
        return entry.dallaaAr
    }

    public func dallaaInfo(_ name: String) -> [PetName] {
        guard let entry = LookupIndices.lookup(name, customPath: customDataPath), !entry.dallaaAr.isEmpty else {
            return []
        }
        var result: [PetName] = []
        for i in 0..<entry.dallaaAr.count {
            let ar = entry.dallaaAr[i]
            let tk = i < entry.dallaaTashkeel.count ? entry.dallaaTashkeel[i] : ar
            let en = i < entry.dallaaEn.count ? entry.dallaaEn[i] : ""
            let ipa = i < entry.dallaaIpa.count ? entry.dallaaIpa[i] : ""
            result.append(PetName(ar: ar, tashkeel: tk, en: en, ipa: ipa))
        }
        return result
    }

    public func petNames(_ name: String, format: String = "plain") -> [String] {
        return dallaa(name, format: format)
    }

    public func root(_ name: String) -> String? {
        guard let entry = LookupIndices.lookup(name, customPath: customDataPath), entry.root != "N/A" else {
            return nil
        }
        return entry.root
    }

    public func origin(_ name: String) -> String? {
        guard let entry = LookupIndices.lookup(name, customPath: customDataPath) else {
            return nil
        }
        return entry.originType
    }

    public func famousFigures(_ name: String, lang: String = "ar") -> [String] {
        guard let entry = LookupIndices.lookup(name, customPath: customDataPath) else {
            return []
        }
        if lang.lowercased().hasPrefix("en") {
            return !entry.famousFiguresEn.isEmpty ? entry.famousFiguresEn : entry.famousFiguresAr
        }
        return entry.famousFiguresAr
    }

    public func trend(_ name: String) -> String? {
        guard let entry = LookupIndices.lookup(name, customPath: customDataPath) else {
            return nil
        }
        return entry.trendCategory
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

    /// Gender of the person: the first given name.
    ///
    /// Later tokens are father, grandfather, family. They do not vote. A
    /// tie must not become male. Two-word compound lemmas (e.g. kunya
    /// "Abu X") are recognized as one token, not two fragments.
    public func detectGender(_ fullName: String) -> GenderDetection {
        let tokens = LookupIndices.compoundTokens(fullName, customPath: customDataPath)
        guard !tokens.isEmpty else {
            return GenderDetection(gender: "neutral", confidence: 0.0)
        }

        var skippedLineage = 0
        for (i, token) in tokens.enumerated() {
            guard let entry = token.1,
                  Quality.isPersonalEntry(entry),
                  !Quality.isLowConfidenceEntry(entry) else { continue }
            if Quality.isLineageRole(entry) {
                skippedLineage += 1
                continue
            }
            if entry.gender == .neutral {
                return GenderDetection(gender: "neutral", confidence: 0.6)
            }
            let confidence = (skippedLineage == 0 && i == 0) ? 1.0 : 0.85
            return GenderDetection(gender: entry.gender.rawValue, confidence: confidence)
        }
        return GenderDetection(gender: "neutral", confidence: 0.0)
    }

    /// Religion of the person: the first given name, like gender.
    ///
    /// A father, grandfather, or family surname from one community does
    /// not override the person's own first name. Lineage tokens only vote
    /// if the person's own name gives no distinctive signal.
    public func detectReligion(_ fullName: String) -> ReligionDetection {
        let tokens = LookupIndices.compoundTokens(fullName, customPath: customDataPath)
        guard !tokens.isEmpty else {
            return ReligionDetection(religion: "neutral", confidence: 0.0)
        }

        var skippedLineage = 0
        for (i, token) in tokens.enumerated() {
            guard let entry = token.1,
                  Quality.isPersonalEntry(entry),
                  !Quality.isLowConfidenceEntry(entry) else { continue }
            if Quality.isLineageRole(entry) {
                skippedLineage += 1
                continue
            }
            if entry.religion == .neutral {
                continue
            }
            let confidence = (skippedLineage == 0 && i == 0) ? 1.0 : 0.9
            return ReligionDetection(religion: entry.religion.rawValue, confidence: confidence)
        }

        // The person's own given names carried no distinctive signal
        // (neutral or not found). Fall back to an aggregate vote across
        // every token, lineage included, rather than declaring neutral.
        var muslim = 0.0
        var christian = 0.0
        var first: String?

        for token in tokens {
            guard let entry = token.1,
                  Quality.isPersonalEntry(entry),
                  !Quality.isLowConfidenceEntry(entry) else { continue }
            if entry.religion == .muslim {
                muslim += 1
                if first == nil { first = "muslim" }
            } else if entry.religion == .christian {
                christian += 1
                if first == nil { first = "christian" }
            }
        }

        if muslim == 0.0 && christian == 0.0 {
            return ReligionDetection(religion: "neutral", confidence: 0.0)
        }

        let distinctive = muslim + christian
        if muslim > christian {
            return ReligionDetection(religion: "muslim", confidence: 0.5 * muslim / distinctive)
        }
        if christian > muslim {
            return ReligionDetection(religion: "christian", confidence: 0.5 * christian / distinctive)
        }
        return ReligionDetection(religion: first ?? "neutral", confidence: 0.5)
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

    /// True if this is a usable personal name.
    ///
    /// Catalog surfaces that are not a person (God, titles, common nouns)
    /// stay in lookup for split. They are not valid names.
    public func isValid(_ name: String) -> Bool {
        guard let entry = LookupIndices.lookup(name, customPath: customDataPath) else {
            return false
        }
        return Quality.isPersonalEntry(entry) && !Quality.isLowConfidenceEntry(entry)
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
