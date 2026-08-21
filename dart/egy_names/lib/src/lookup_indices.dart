import 'data.dart';
import 'types.dart';

class LookupIndices {
  static bool _built = false;

  static final Map<String, NameEntry> _arIndex = {};
  static final Map<String, NameEntry> _enIndex = {};
  static final Map<String, NameEntry> _arNormIndex = {};
  static final Map<String, String> _correctionIndex = {};
  static List<NameEntry> _allEntries = [];
  static List<NameEntry> _rankedEntries = [];

  static final RegExp _tashkeelRegex =
      RegExp(r'[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]');
  static final RegExp _tatweelRegex = RegExp(r'\u0640');
  static final RegExp _alefVariantsRegex = RegExp(r'[\u0622\u0623\u0625\u0671]');
  static final RegExp _isArabicRegex =
      RegExp(r'[\u0600-\u06FF\uFE70-\uFEFF]');

  static String normalizeAr(String text) {
    var s = text.replaceAll(_tashkeelRegex, '');
    s = s.replaceAll(_tatweelRegex, '');
    s = s.replaceAll(_alefVariantsRegex, '\u0627');
    s = s.replaceAll('\u0649', '\u064A'); // ى -> ي
    s = s.replaceAll('\u0629', '\u0647'); // ة -> ه
    return s;
  }

  static String normalizeEn(String text) {
    return text.toLowerCase().replaceAll('-', '').replaceAll("'", '').trim();
  }

  static bool isArabic(String text) {
    return _isArabicRegex.hasMatch(text);
  }

  static void ensureBuilt({String? dataPath}) {
    if (_built) return;

    final bundle = DataLoader.loadBundle(customPath: dataPath);
    _allEntries = List.unmodifiable(bundle.names);

    for (final entry in _allEntries) {
      // AR Index
      _arIndex.putIfAbsent(entry.ar, () => entry);
      final normAr = normalizeAr(entry.ar);
      _arNormIndex.putIfAbsent(normAr, () => entry);

      for (final v in entry.arVariants) {
        final stripped = v.trim();
        if (stripped.isNotEmpty) {
          _arIndex.putIfAbsent(stripped, () => entry);
          _arNormIndex.putIfAbsent(normalizeAr(stripped), () => entry);
        }
      }

      // EN Index
      final normEn = normalizeEn(entry.en);
      _enIndex.putIfAbsent(normEn, () => entry);

      for (final v in entry.enVariants) {
        final stripped = v.trim();
        if (stripped.isNotEmpty) {
          _enIndex.putIfAbsent(normalizeEn(stripped), () => entry);
        }
      }
    }

    // Corrections
    _correctionIndex.addAll(bundle.corrections);

    // Ranked
    final sorted = List<NameEntry>.from(_allEntries);
    sorted.sort((a, b) => b.corpusShare.compareTo(a.corpusShare));
    _rankedEntries = List.unmodifiable(sorted);

    _built = true;
  }

  static NameEntry? lookupAr(String name, {String? dataPath}) {
    ensureBuilt(dataPath: dataPath);
    if (name.trim().isEmpty) return null;
    final trimmed = name.trim();

    // 1. Direct match
    final direct = _arIndex[trimmed];
    if (direct != null) return direct;

    // 2. Normalized match
    final norm = normalizeAr(trimmed);
    final normMatch = _arNormIndex[norm];
    if (normMatch != null) return normMatch;

    // 3. Alif / Alif Maqsura terminal phonetic equivalence (e.g. مصطفا <-> مصطفى)
    if (norm.endsWith('\u0627')) {
      final alt = '${norm.substring(0, norm.length - 1)}\u064A';
      final altMatch = _arNormIndex[alt];
      if (altMatch != null) return altMatch;
    } else if (norm.endsWith('\u064A')) {
      final alt = '${norm.substring(0, norm.length - 1)}\u0627';
      final altMatch = _arNormIndex[alt];
      if (altMatch != null) return altMatch;
    }

    // 4. Space-less compound match (e.g. عبد الرحيم <-> عبدالرحيم)
    final noSpace = trimmed.replaceAll(RegExp(r'\s+'), '');
    if (noSpace != trimmed) {
      final noSpaceMatch = _arIndex[noSpace] ?? _arNormIndex[normalizeAr(noSpace)];
      if (noSpaceMatch != null) return noSpaceMatch;
    }

    return null;
  }

  static NameEntry? lookupEn(String name, {String? dataPath}) {
    ensureBuilt(dataPath: dataPath);
    return _enIndex[normalizeEn(name)];
  }

  static NameEntry? lookup(String name, {String? dataPath}) {
    ensureBuilt(dataPath: dataPath);
    if (isArabic(name)) {
      return lookupAr(name, dataPath: dataPath);
    }
    return lookupEn(name, dataPath: dataPath);
  }

  static String? getCorrection(String surface, {String? dataPath}) {
    ensureBuilt(dataPath: dataPath);
    return _correctionIndex[surface];
  }

  static List<NameEntry> getAll({String? dataPath}) {
    ensureBuilt(dataPath: dataPath);
    return _allEntries;
  }

  static List<NameEntry> getRanked({String? dataPath}) {
    ensureBuilt(dataPath: dataPath);
    return _rankedEntries;
  }

  static Map<String, NameEntry> getArForms({String? dataPath}) {
    ensureBuilt(dataPath: dataPath);
    return _arIndex;
  }

  static Map<String, NameEntry> getArNormForms({String? dataPath}) {
    ensureBuilt(dataPath: dataPath);
    return _arNormIndex;
  }
}
