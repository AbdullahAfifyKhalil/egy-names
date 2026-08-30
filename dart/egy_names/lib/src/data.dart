import 'dart:convert';
import 'dart:io';
import 'types.dart';

class DataBundle {
  final String version;
  final int corpusTokens;
  final int corpusStudents;
  final List<int> cohortYears;
  final List<NameEntry> names;
  final Map<String, String> corrections;

  DataBundle({
    required this.version,
    required this.corpusTokens,
    required this.corpusStudents,
    required this.cohortYears,
    required this.names,
    required this.corrections,
  });
}

class DataLoader {
  static DataBundle? _cachedBundle;

  static const _catalogRel = 'lib/src/data/names.json.gz';

  static String? _fromPackageConfig() {
    var dir = Directory.current;
    for (var i = 0; i < 12; i++) {
      final configFile = File(
        '${dir.path}${Platform.pathSeparator}.dart_tool${Platform.pathSeparator}package_config.json',
      );
      if (configFile.existsSync()) {
        try {
          final json = jsonDecode(configFile.readAsStringSync()) as Map<String, dynamic>;
          for (final raw in (json['packages'] as List<dynamic>? ?? [])) {
            final pkg = raw as Map<String, dynamic>;
            if (pkg['name'] != 'egy_names') continue;
            final rootUri = pkg['rootUri'] as String? ?? '';
            final rootPath = rootUri.startsWith('file:')
                ? Uri.parse(rootUri).toFilePath()
                : dir.uri.resolve('.dart_tool/$rootUri').toFilePath();
            final trimmed = rootPath.replaceAll(RegExp(r'[/\\]+$'), '');
            final candidate = File(
              '$trimmed${Platform.pathSeparator}${_catalogRel.replaceAll('/', Platform.pathSeparator)}',
            );
            if (candidate.existsSync()) return candidate.path;
          }
        } catch (_) {}
      }
      final parent = dir.parent;
      if (parent.path == dir.path) break;
      dir = parent;
    }
    return null;
  }

  static String _resolveDataPath(String? customPath) {
    if (customPath != null && File(customPath).existsSync()) {
      return customPath;
    }

    final fromConfig = _fromPackageConfig();
    if (fromConfig != null) return fromConfig;

    // Try several standard relative locations
    final possiblePaths = [
      _catalogRel,
      'packages/egy_names/src/data/names.json.gz',
      '${Directory.current.path}/$_catalogRel',
      '${Directory.current.path}/dart/egy_names/$_catalogRel',
      Platform.script.resolve('src/data/names.json.gz').toFilePath(),
      Platform.script.resolve('../lib/src/data/names.json.gz').toFilePath(),
    ];

    for (final p in possiblePaths) {
      try {
        if (File(p).existsSync()) {
          return p;
        }
      } catch (_) {}
    }

    // Fallback to default
    return _catalogRel;
  }

  static DataBundle loadBundle({String? customPath}) {
    if (_cachedBundle != null && customPath == null) {
      return _cachedBundle!;
    }

    final filePath = _resolveDataPath(customPath);
    final file = File(filePath);
    if (!file.existsSync()) {
      throw FileSystemException(
        'Could not locate names.json.gz data file. Searched at: $filePath',
        filePath,
      );
    }

    final compressedBytes = file.readAsBytesSync();
    final decompressedBytes = gzip.decode(compressedBytes);
    final jsonString = utf8.decode(decompressedBytes);
    final jsonMap = jsonDecode(jsonString) as Map<String, dynamic>;

    final rawNames = jsonMap['names'] as List<dynamic>? ?? [];
    final names = rawNames
        .map((n) => NameEntry.fromJson(n as Map<String, dynamic>))
        .toList();

    final rawCorrections =
        jsonMap['corrections'] as Map<String, dynamic>? ?? {};
    final corrections = rawCorrections.map(
      (k, v) => MapEntry(k, v.toString()),
    );

    final meta = jsonMap['metadata'] as Map<String, dynamic>? ?? jsonMap;

    final rawYears = (jsonMap['cohort_years'] ?? meta['cohort_years']) as List<dynamic>? ?? [];
    final cohortYears = rawYears.map((y) => (y as num).toInt()).toList();

    final bundle = DataBundle(
      version: (jsonMap['version'] ?? meta['version']) as String? ?? '0.2.1',
      corpusTokens: ((jsonMap['corpus_tokens'] ?? meta['corpus_tokens'] ?? 0) as num).toInt(),
      corpusStudents: ((jsonMap['corpus_students'] ?? meta['corpus_students'] ?? meta['total_corpus_records'] ?? 0) as num).toInt(),
      cohortYears: cohortYears,
      names: names,
      corrections: corrections,
    );

    if (customPath == null) {
      _cachedBundle = bundle;
    }

    return bundle;
  }

  static void clearCache() {
    _cachedBundle = null;
  }
}
