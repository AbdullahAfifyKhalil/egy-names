import Foundation
import Compression

#if canImport(zlib)
import zlib
#endif

public struct DataBundle: Sendable {
    public let names: [NameEntry]
    public let corrections: [String: String]
    public let metadata: [String: AnyCodable]
}

public struct AnyCodable: Codable, @unchecked Sendable {
    public let value: Any

    public init(_ value: Any) {
        self.value = value
    }

    public init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        if let string = try? container.decode(String.self) {
            value = string
        } else if let int = try? container.decode(Int.self) {
            value = int
        } else if let double = try? container.decode(Double.self) {
            value = double
        } else if let bool = try? container.decode(Bool.self) {
            value = bool
        } else {
            value = ""
        }
    }

    public func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        if let string = value as? String {
            try container.encode(string)
        } else if let int = value as? Int {
            try container.encode(int)
        } else if let double = value as? Double {
            try container.encode(double)
        } else if let bool = value as? Bool {
            try container.encode(bool)
        }
    }
}

public final class DataLoader: @unchecked Sendable {
    private static var cachedBundle: DataBundle?
    private static let lock = NSLock()

    public static func decompressGzip(data: Data) -> Data? {
        guard data.count > 2 else { return nil }

        // Use zlib directly
        var stream = z_stream()
        stream.next_in = UnsafeMutablePointer<Bytef>(mutating: (data as NSData).bytes.bindMemory(to: Bytef.self, capacity: data.count))
        stream.avail_in = uInt(data.count)

        // 16 + MAX_WBITS to decode gzip format
        guard inflateInit2_(&stream, 16 + MAX_WBITS, ZLIB_VERSION, Int32(MemoryLayout<z_stream>.size)) == Z_OK else {
            return nil
        }
        defer { inflateEnd(&stream) }

        var decompressed = Data()
        let bufferSize = 65536
        let buffer = UnsafeMutablePointer<Bytef>.allocate(capacity: bufferSize)
        defer { buffer.deallocate() }

        while true {
            stream.next_out = buffer
            stream.avail_out = uInt(bufferSize)

            let status = inflate(&stream, Z_NO_FLUSH)
            if status == Z_OK || status == Z_STREAM_END {
                let bytesWritten = bufferSize - Int(stream.avail_out)
                if bytesWritten > 0 {
                    decompressed.append(buffer, count: bytesWritten)
                }
                if status == Z_STREAM_END {
                    break
                }
            } else {
                return nil
            }
        }

        return decompressed
    }

    public static func loadBundle(customPath: String? = nil) -> DataBundle {
        lock.lock()
        defer { lock.unlock() }

        if let cached = cachedBundle, customPath == nil {
            return cached
        }

        var fileData: Data?

        if let path = customPath, FileManager.default.fileExists(atPath: path) {
            fileData = try? Data(contentsOf: URL(fileURLWithPath: path))
        }

        if fileData == nil {
            #if SWIFT_PACKAGE
            if let url = Bundle.module.url(forResource: "names", withExtension: "json.gz") {
                fileData = try? Data(contentsOf: url)
            }
            #endif
        }

        if fileData == nil {
            let searchPaths = [
                "data/names.json.gz",
                "../data/names.json.gz",
                "../../data/names.json.gz",
                "/Volumes/MAC/Development/Personal/Egyptian Names/library building/data/names.json.gz",
                "/Volumes/MAC/Development/Afify.corp/Egyptian Names/library building/data/names.json.gz"
            ]
            for p in searchPaths {
                if FileManager.default.fileExists(atPath: p) {
                    fileData = try? Data(contentsOf: URL(fileURLWithPath: p))
                    if fileData != nil { break }
                }
            }
        }

        guard let rawGzData = fileData,
              let jsonData = decompressGzip(data: rawGzData) else {
            print("[EgyNames] Error: Could not locate or decompress names.json.gz")
            return DataBundle(names: [], corrections: [:], metadata: [:])
        }

        guard let jsonObject = try? JSONSerialization.jsonObject(with: jsonData) as? [String: Any] else {
            print("[EgyNames] Error: Invalid JSON structure")
            return DataBundle(names: [], corrections: [:], metadata: [:])
        }

        var names: [NameEntry] = []
        if let rawNames = jsonObject["names"] as? [[String: Any]] {
            names.reserveCapacity(rawNames.count)
            for item in rawNames {
                let ar = item["a"] as? String ?? ""
                let en = item["e"] as? String ?? ""
                let g = Gender.from(string: item["g"] as? String ?? "n")
                let r = Religion.from(string: item["r"] as? String ?? "n")
                let l = NameRole.from(string: item["l"] as? String ?? "g")

                let av = (item["av"] as? String)?.components(separatedBy: "|").filter { !$0.isEmpty } ?? [ar]
                let ev = (item["ev"] as? String)?.components(separatedBy: "|").filter { !$0.isEmpty } ?? [en]
                let p = item["p"] as? [Double] ?? []
                let tp = item["tp"] as? Double ?? 0.0
                let fc = FrequencyClass.from(string: item["fc"] as? String ?? "n")
                let t = item["t"] as? String ?? ""
                let ma = item["ma"] as? String ?? ""
                let me = item["me"] as? String ?? ""

                names.append(NameEntry(
                    ar: ar,
                    en: en,
                    gender: g,
                    religion: r,
                    role: l,
                    arVariants: av,
                    enVariants: ev,
                    slotPcts: p,
                    corpusShare: tp,
                    frequency: fc,
                    tashkeel: t,
                    meaningAr: ma,
                    meaningEn: me
                ))
            }
        }

        let corrections = jsonObject["corrections"] as? [String: String] ?? [:]
        var metadata: [String: AnyCodable] = [:]
        if let rawMeta = jsonObject["metadata"] as? [String: Any] {
            for (k, v) in rawMeta {
                metadata[k] = AnyCodable(v)
            }
        }

        let bundle = DataBundle(names: names, corrections: corrections, metadata: metadata)
        if customPath == nil {
            cachedBundle = bundle
        }
        return bundle
    }
}
