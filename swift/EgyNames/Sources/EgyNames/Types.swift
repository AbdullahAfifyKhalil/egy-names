import Foundation

public enum Gender: String, Codable, Sendable {
    case male = "male"
    case female = "female"
    case neutral = "neutral"

    public static func from(string: String) -> Gender {
        let s = string.lowercased()
        if s == "m" || s == "male" { return .male }
        if s == "f" || s == "female" { return .female }
        return .neutral
    }
}

public enum Religion: String, Codable, Sendable {
    case muslim = "muslim"
    case christian = "christian"
    case neutral = "neutral"

    public static func from(string: String) -> Religion {
        let s = string.lowercased()
        if s == "m" || s == "muslim" { return .muslim }
        if s == "c" || s == "christian" { return .christian }
        return .neutral
    }
}

public enum NameRole: String, Codable, Sendable {
    case given = "given"
    case family = "family"

    public static func from(string: String) -> NameRole {
        let s = string.lowercased()
        if s == "f" || s == "family" { return .family }
        return .given
    }
}

public enum FrequencyClass: String, Codable, Sendable {
    case common = "common"
    case normal = "normal"
    case rare = "rare"

    public static func from(string: String) -> FrequencyClass {
        let s = string.lowercased()
        if s == "c" || s == "common" { return .common }
        if s == "n" || s == "normal" { return .normal }
        return .rare
    }
}

public struct PetName: Codable, Sendable {
    public let ar: String
    public let tashkeel: String
    public let en: String
    public let ipa: String

    public init(ar: String, tashkeel: String, en: String, ipa: String) {
        self.ar = ar
        self.tashkeel = tashkeel
        self.en = en
        self.ipa = ipa
    }
}

public struct NameEntry: Sendable {
    public let ar: String
    public let en: String
    public let gender: Gender
    public let religion: Religion
    public let role: NameRole
    public let arVariants: [String]
    public let enVariants: [String]
    public let slotPcts: [Double]
    public let corpusShare: Double
    public let frequency: FrequencyClass
    public let tashkeel: String
    public let tashkeelStandard: String
    public let tashkeelEg: String
    public let ipaStandard: String
    public let ipaEg: String
    public let meaningAr: String
    public let meaningEn: String
    public let dallaa: [String]
    public let dallaaAr: [String]
    public let dallaaTashkeel: [String]
    public let dallaaEn: [String]
    public let dallaaIpa: [String]
    public let root: String
    public let originType: String
    public let famousFigures: [String]
    public let famousFiguresAr: [String]
    public let famousFiguresEn: [String]
    public let trendCategory: String
}

public struct NameInfo: Codable, Sendable {
    public let ar: String
    public let en: String
    public let gender: String
    public let religion: String
    public let role: String
    public let frequencyClass: String
    public let corpusShare: Double
    public let tashkeel: String
    public let tashkeelStandard: String
    public let tashkeelEg: String
    public let ipaStandard: String
    public let ipaEg: String
    public let meaningAr: String
    public let meaningEn: String
    public let dallaa: [String]
    public let dallaaAr: [String]
    public let dallaaTashkeel: [String]
    public let dallaaEn: [String]
    public let dallaaIpa: [String]
    public let root: String
    public let originType: String
    public let famousFigures: [String]
    public let famousFiguresAr: [String]
    public let famousFiguresEn: [String]
    public let trendCategory: String
    public let arVariants: [String]
    public let enVariants: [String]
    public let slotDistribution: [Double]
}

public struct GeneratedName: Codable, Sendable {
    public let ar: String
    public let en: String
    public let partsAr: [String]
    public let partsEn: [String]
}

public struct ChainPart: Codable, Sendable {
    public let name: String
    public let slot: Int
    public let role: String
    public let detail: String
}

public struct GenderDetection: Codable, Sendable {
    public let gender: String
    public let confidence: Double
}

public struct ReligionDetection: Codable, Sendable {
    public let religion: String
    public let confidence: Double
}

public struct RankInfo: Codable, Sendable {
    public let rank: Int
    public let percentile: Double
    public let corpusShare: String
    public let description: String
}

public struct UniquenessScore: Codable, Sendable {
    public let score: Double
    public let label: String
    public let note: String
}

extension NameEntry {
    public func toNameInfo() -> NameInfo {
        return NameInfo(
            ar: ar,
            en: en,
            gender: gender.rawValue,
            religion: religion.rawValue,
            role: role.rawValue,
            frequencyClass: frequency.rawValue,
            corpusShare: corpusShare,
            tashkeel: tashkeel,
            tashkeelStandard: tashkeelStandard,
            tashkeelEg: tashkeelEg,
            ipaStandard: ipaStandard,
            ipaEg: ipaEg,
            meaningAr: meaningAr,
            meaningEn: meaningEn,
            dallaa: dallaaAr,
            dallaaAr: dallaaAr,
            dallaaTashkeel: dallaaTashkeel,
            dallaaEn: dallaaEn,
            dallaaIpa: dallaaIpa,
            root: root,
            originType: originType,
            famousFigures: famousFiguresAr,
            famousFiguresAr: famousFiguresAr,
            famousFiguresEn: famousFiguresEn,
            trendCategory: trendCategory,
            arVariants: arVariants,
            enVariants: enVariants,
            slotDistribution: slotPcts
        )
    }
}
