import Foundation

/// Loader for the shared, cross-SDK rule config (`data/logic_config.json`,
/// synced into `Resources/logic_config.json` by `scripts/sync-catalog.sh`).
///
/// Mirrors `python/src/egy_names/_rules_config.py`. If the config file is
/// missing or malformed, falls back to the values last known correct from
/// the audits that produced it, so the library never hard-fails on a
/// packaging mistake.
struct RulesInferRule: Codable, Sendable {
    let script: String?
    let match: String?
    let prefix: RulesStringOrList?
    let suffix: RulesStringOrList?
    let contains: RulesStringOrList?
    let value: String?
    let confidence: Double?
}

/// Decodes a JSON field that may be either a single string or an array of strings.
enum RulesStringOrList: Codable, Sendable {
    case single(String)
    case list([String])

    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        if let s = try? container.decode(String.self) {
            self = .single(s)
        } else {
            self = .list(try container.decode([String].self))
        }
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        switch self {
        case .single(let s): try container.encode(s)
        case .list(let l): try container.encode(l)
        }
    }

    var values: [String] {
        switch self {
        case .single(let s): return [s]
        case .list(let l): return l
        }
    }
}

private struct RulesQualityConfig: Codable, Sendable {
    let nonPersonalAr: [String]?
    let uncertainMeaningMarkers: [String]?
    let lowConfidenceShareEpsilon: Double?
    let kunyaExemptPrefixes: [String]?

    enum CodingKeys: String, CodingKey {
        case nonPersonalAr = "non_personal_ar"
        case uncertainMeaningMarkers = "uncertain_meaning_markers"
        case lowConfidenceShareEpsilon = "low_confidence_share_epsilon"
        case kunyaExemptPrefixes = "kunya_exempt_prefixes"
    }
}

private struct RulesInferThresholds: Codable, Sendable {
    let genderMinP: Double?
    let muslimMinP: Double?
    let christianMinP: Double?
    let roleMinP: Double?

    enum CodingKeys: String, CodingKey {
        case genderMinP = "gender_min_p"
        case muslimMinP = "muslim_min_p"
        case christianMinP = "christian_min_p"
        case roleMinP = "role_min_p"
    }
}

private struct RulesInferRules: Codable, Sendable {
    let gender: [RulesInferRule]?
    let religion: [RulesInferRule]?
    let role: [RulesInferRule]?
}

private struct RulesConfigFile: Codable, Sendable {
    let quality: RulesQualityConfig?
    let inferThresholds: RulesInferThresholds?
    let inferRules: RulesInferRules?

    enum CodingKeys: String, CodingKey {
        case quality
        case inferThresholds = "infer_thresholds"
        case inferRules = "infer_rules"
    }
}

public struct InferThresholds: Sendable {
    public let genderMinP: Double
    public let muslimMinP: Double
    public let christianMinP: Double
    public let roleMinP: Double
}

public final class RulesConfig: @unchecked Sendable {
    private static let lock = NSLock()
    private static var loaded = false

    private static var _nonPersonalAr: Set<String> = []
    private static var _uncertainMeaningMarkers: [String] = []
    private static var _lowConfidenceShareEpsilon: Double = 0.0001
    private static var _kunyaExemptPrefixes: [String] = []
    private static var _inferThresholds = InferThresholds(
        genderMinP: 0.70, muslimMinP: 0.85, christianMinP: 0.90, roleMinP: 0.88
    )
    private static var _inferRulesGender: [RulesInferRule] = []
    private static var _inferRulesReligion: [RulesInferRule] = []
    private static var _inferRulesRole: [RulesInferRule] = []

    private static let fallbackNonPersonalAr: [String] = [
        "الله", "الرجل", "الرجال", "شربه", "لافندي", "لفندي", "ماء", "البيت",
    ]

    private static let fallbackUncertainMeaningMarkers: [String] = [
        "غير واضح", "لا يوجد معنى", "غير معروف",
        "قد يكون تحريف", "تحريفاً", "تحريفًا",
    ]

    private static let fallbackKunyaExemptPrefixes: [String] = ["أبو", "ابو", "أم", "ام"]

    private static func ensureLoaded() {
        if loaded { return }
        lock.lock()
        defer { lock.unlock() }
        if loaded { return }
        load()
        loaded = true
    }

    private static func load() {
        var config: RulesConfigFile?

        #if SWIFT_PACKAGE
        if let url = Bundle.module.url(forResource: "logic_config", withExtension: "json"),
           let data = try? Data(contentsOf: url) {
            config = try? JSONDecoder().decode(RulesConfigFile.self, from: data)
        }
        #endif

        guard let cfg = config else {
            applyFallback()
            return
        }

        _nonPersonalAr = Set(cfg.quality?.nonPersonalAr ?? fallbackNonPersonalAr)
        _uncertainMeaningMarkers = cfg.quality?.uncertainMeaningMarkers ?? fallbackUncertainMeaningMarkers
        _lowConfidenceShareEpsilon = cfg.quality?.lowConfidenceShareEpsilon ?? 0.0001
        _kunyaExemptPrefixes = cfg.quality?.kunyaExemptPrefixes ?? fallbackKunyaExemptPrefixes

        _inferThresholds = InferThresholds(
            genderMinP: cfg.inferThresholds?.genderMinP ?? 0.70,
            muslimMinP: cfg.inferThresholds?.muslimMinP ?? 0.85,
            christianMinP: cfg.inferThresholds?.christianMinP ?? 0.90,
            roleMinP: cfg.inferThresholds?.roleMinP ?? 0.88
        )

        _inferRulesGender = cfg.inferRules?.gender ?? []
        _inferRulesReligion = cfg.inferRules?.religion ?? []
        _inferRulesRole = cfg.inferRules?.role ?? []
    }

    private static func applyFallback() {
        _nonPersonalAr = Set(fallbackNonPersonalAr)
        _uncertainMeaningMarkers = fallbackUncertainMeaningMarkers
        _lowConfidenceShareEpsilon = 0.0001
        _kunyaExemptPrefixes = fallbackKunyaExemptPrefixes
        _inferThresholds = InferThresholds(
            genderMinP: 0.70, muslimMinP: 0.85, christianMinP: 0.90, roleMinP: 0.88
        )
        _inferRulesGender = []
        _inferRulesReligion = []
        _inferRulesRole = []
    }

    public static var nonPersonalAr: Set<String> {
        ensureLoaded()
        return _nonPersonalAr
    }

    public static var uncertainMeaningMarkers: [String] {
        ensureLoaded()
        return _uncertainMeaningMarkers
    }

    public static var lowConfidenceShareEpsilon: Double {
        ensureLoaded()
        return _lowConfidenceShareEpsilon
    }

    public static var kunyaExemptPrefixes: [String] {
        ensureLoaded()
        return _kunyaExemptPrefixes
    }

    public static var inferThresholds: InferThresholds {
        ensureLoaded()
        return _inferThresholds
    }

    static func inferRules(_ kind: String) -> [RulesInferRule] {
        ensureLoaded()
        switch kind {
        case "gender": return _inferRulesGender
        case "religion": return _inferRulesReligion
        case "role": return _inferRulesRole
        default: return []
        }
    }
}
