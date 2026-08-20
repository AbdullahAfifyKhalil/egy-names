import Foundation

public final class Annotator: @unchecked Sendable {
    public static func annotateSingle(_ name: String, customPath: String? = nil) -> NameInfo? {
        guard let entry = LookupIndices.lookup(name, customPath: customPath) else {
            return nil
        }
        return entry.toNameInfo()
    }

    public static func annotate(_ fullName: String, customPath: String? = nil) -> [NameInfo] {
        let tokens = fullName.trimmingCharacters(in: .whitespacesAndNewlines)
            .components(separatedBy: .whitespacesAndNewlines)
            .filter { !$0.isEmpty }

        var results: [NameInfo] = []
        for t in tokens {
            if let info = annotateSingle(t, customPath: customPath) {
                results.append(info)
            }
        }
        return results
    }
}
