import Foundation

public final class SearchEngine: @unchecked Sendable {
    public static func search(
        gender: Gender? = nil,
        religion: Religion? = nil,
        role: NameRole? = nil,
        frequency: FrequencyClass? = nil,
        startsWith: String? = nil,
        endsWith: String? = nil,
        contains: String? = nil,
        minCorpusShare: Double = 0.0,
        maxResults: Int = 50,
        sortBy: String = "corpus_share",
        customPath: String? = nil
    ) -> [NameInfo] {
        LookupIndices.ensureBuilt(customPath: customPath)
        let all = LookupIndices.getAll(customPath: customPath)

        var matched: [NameEntry] = []
        for e in all {
            if let g = gender, e.gender != g { continue }
            if let r = religion, e.religion != r { continue }
            if let ro = role, e.role != ro { continue }
            if let f = frequency, e.frequency != f { continue }
            if e.corpusShare < minCorpusShare { continue }

            if let prefix = startsWith, !prefix.isEmpty {
                if !e.ar.hasPrefix(prefix) && !e.en.hasPrefix(prefix) { continue }
            }

            if let suffix = endsWith, !suffix.isEmpty {
                if !e.ar.hasSuffix(suffix) && !e.en.hasSuffix(suffix) { continue }
            }

            if let sub = contains, !sub.isEmpty {
                if !e.ar.contains(sub) && !e.en.contains(sub) { continue }
            }

            matched.append(e)
        }

        if sortBy == "corpus_share" {
            matched.sort(by: { $0.corpusShare > $1.corpusShare })
        }

        let limit = (maxResults > 0) ? min(maxResults, matched.count) : matched.count
        return matched.prefix(limit).map { $0.toNameInfo() }
    }
}
