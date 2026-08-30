/// Loader for the shared, cross-SDK rule config.
///
/// `data/logic_config.json` (synced by scripts/sync-catalog.sh, same as
/// names.json.gz) is the single source of truth for every threshold and
/// rule list that used to be hardcoded per language: non-personal
/// surfaces, low-confidence detection, ML abstention thresholds, and the
/// gender/religion/role prefix-suffix rule tables. Only pure algorithms
/// (compound-token lookahead, first-personal-token-wins, corpus-share
/// tie-break) stay as code, because they cannot be expressed as data.
///
/// If the config file is missing or malformed, fall back to the values
/// last known correct from this session's audits, so the library never
/// hard-fails on a packaging mistake.
library;

import 'dart:convert';
import 'dart:io';

import 'data.dart';

class InferThresholds {
  final double genderMinP;
  final double muslimMinP;
  final double christianMinP;
  final double roleMinP;

  const InferThresholds({
    required this.genderMinP,
    required this.muslimMinP,
    required this.christianMinP,
    required this.roleMinP,
  });
}

class RulesConfig {
  final Set<String> nonPersonalAr;
  final List<String> uncertainMeaningMarkers;
  final double lowConfidenceShareEpsilon;
  final List<String> kunyaExemptPrefixes;
  final InferThresholds inferThresholds;
  final Map<String, List<Map<String, dynamic>>> inferRules;

  const RulesConfig({
    required this.nonPersonalAr,
    required this.uncertainMeaningMarkers,
    required this.lowConfidenceShareEpsilon,
    required this.kunyaExemptPrefixes,
    required this.inferThresholds,
    required this.inferRules,
  });

  static const RulesConfig fallback = RulesConfig(
    nonPersonalAr: {
      'الله',
      'الرجل',
      'الرجال',
      'شربه',
      'لافندي',
      'لفندي',
      'ماء',
      'البيت',
    },
    uncertainMeaningMarkers: [
      'غير واضح',
      'لا يوجد معنى',
      'غير معروف',
      'قد يكون تحريف',
      'تحريفاً',
      'تحريفًا',
    ],
    lowConfidenceShareEpsilon: 0.0001,
    kunyaExemptPrefixes: ['أبو', 'ابو', 'أم', 'ام'],
    inferThresholds: InferThresholds(
      genderMinP: 0.70,
      muslimMinP: 0.85,
      christianMinP: 0.90,
      roleMinP: 0.88,
    ),
    inferRules: {'gender': [], 'religion': [], 'role': []},
  );
}

class RulesConfigLoader {
  static RulesConfig? _cached;

  static const _configRel = 'lib/src/data/logic_config.json';

  static RulesConfig load({String? customPath}) {
    if (_cached != null && customPath == null) {
      return _cached!;
    }

    final config = _tryLoad(customPath) ?? RulesConfig.fallback;

    if (customPath == null) {
      _cached = config;
    }
    return config;
  }

  static void clearCache() {
    _cached = null;
  }

  static RulesConfig? _tryLoad(String? customPath) {
    try {
      final path = _resolveConfigPath(customPath);
      final file = File(path);
      if (!file.existsSync()) return null;

      final jsonMap =
          jsonDecode(file.readAsStringSync()) as Map<String, dynamic>;
      final quality = jsonMap['quality'] as Map<String, dynamic>? ?? {};
      final inferThresholdsMap =
          jsonMap['infer_thresholds'] as Map<String, dynamic>? ?? {};
      final inferRulesMap = jsonMap['infer_rules'] as Map<String, dynamic>? ?? {};

      final nonPersonalAr = ((quality['non_personal_ar'] as List<dynamic>?) ?? [])
          .map((e) => e.toString())
          .toSet();
      final uncertainMarkers =
          ((quality['uncertain_meaning_markers'] as List<dynamic>?) ?? [])
              .map((e) => e.toString())
              .toList();
      final epsilon = (quality['low_confidence_share_epsilon'] as num?)
              ?.toDouble() ??
          RulesConfig.fallback.lowConfidenceShareEpsilon;
      final kunyaPrefixes =
          ((quality['kunya_exempt_prefixes'] as List<dynamic>?) ?? [])
              .map((e) => e.toString())
              .toList();

      final thresholds = InferThresholds(
        genderMinP: (inferThresholdsMap['gender_min_p'] as num?)?.toDouble() ??
            RulesConfig.fallback.inferThresholds.genderMinP,
        muslimMinP: (inferThresholdsMap['muslim_min_p'] as num?)?.toDouble() ??
            RulesConfig.fallback.inferThresholds.muslimMinP,
        christianMinP:
            (inferThresholdsMap['christian_min_p'] as num?)?.toDouble() ??
                RulesConfig.fallback.inferThresholds.christianMinP,
        roleMinP: (inferThresholdsMap['role_min_p'] as num?)?.toDouble() ??
            RulesConfig.fallback.inferThresholds.roleMinP,
      );

      final inferRules = <String, List<Map<String, dynamic>>>{};
      for (final kind in ['gender', 'religion', 'role']) {
        final rawList = inferRulesMap[kind] as List<dynamic>? ?? [];
        inferRules[kind] = rawList
            .whereType<Map<String, dynamic>>()
            .toList();
      }

      return RulesConfig(
        nonPersonalAr: nonPersonalAr.isNotEmpty
            ? nonPersonalAr
            : RulesConfig.fallback.nonPersonalAr,
        uncertainMeaningMarkers: uncertainMarkers,
        lowConfidenceShareEpsilon: epsilon,
        kunyaExemptPrefixes: kunyaPrefixes,
        inferThresholds: thresholds,
        inferRules: inferRules,
      );
    } catch (_) {
      return null;
    }
  }

  static String _resolveConfigPath(String? customPath) {
    if (customPath != null && File(customPath).existsSync()) {
      return customPath;
    }

    final fromConfig = DataLoader.resolveSiblingDataPath(_configRel);
    if (fromConfig != null) return fromConfig;

    final possiblePaths = [
      _configRel,
      'packages/egy_names/src/data/logic_config.json',
      '${Directory.current.path}/$_configRel',
      '${Directory.current.path}/dart/egy_names/$_configRel',
      Platform.script.resolve('src/data/logic_config.json').toFilePath(),
      Platform.script.resolve('../lib/src/data/logic_config.json').toFilePath(),
    ];

    for (final p in possiblePaths) {
      try {
        if (File(p).existsSync()) return p;
      } catch (_) {}
    }

    return _configRel;
  }
}
