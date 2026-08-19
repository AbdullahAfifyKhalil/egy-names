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

public struct NameEntry: Codable, Sendable {
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
    public let meaningAr: String
    public let meaningEn: String
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
    public let meaningAr: String
    public let meaningEn: String
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
            ar: self.ar,
            en: self.en,
            gender: self.gender.rawValue,
            religion: self.religion.rawValue,
            role: self.role.rawValue,
            frequencyClass: self.frequency.rawValue,
            corpusShare: self.corpusShare,
            tashkeel: self.tashkeel,
            meaningAr: self.meaningAr,
            meaningEn: self.meaningEn,
            arVariants: self.arVariants,
            enVariants: self.enVariants,
            slotDistribution: self.slotPcts
        )
    }
}
