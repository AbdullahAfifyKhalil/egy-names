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

  static void _claimEn(String key, NameEntry entry) {
    final existing = _enIndex[key];
    if (existing == null || entry.corpusShare > existing.corpusShare) {
      _enIndex[key] = entry;
    }
  }

  /// Bind an Arabic variant spelling to the lemma with the larger
  /// corpus share, same rule as English keys.
  ///
  /// A canonical key (some entry's own `ar`/normalized `ar`) always
  /// wins over any OTHER entry's variant claiming the same string — a
  /// rare misspelling must never shadow a real lemma's own canonical
  /// spelling. Among two variants with no canonical claim, the higher
  /// corpus share wins, exactly like [_claimEn].
  static void _claimArVariant(
    Map<String, NameEntry> index,
    Set<String> canonicalKeys,
    String key,
    NameEntry entry,
  ) {
    if (canonicalKeys.contains(key)) {
      // Already bound to its own entry in the canonical pass; a
      // variant from a different lemma must never override it.
      return;
    }
    final existing = index[key];
    if (existing == null || entry.corpusShare > existing.corpusShare) {
      index[key] = entry;
    }
  }

  static bool isArabic(String text) {
    return _isArabicRegex.hasMatch(text);
  }

  static void ensureBuilt({String? dataPath}) {
    if (_built) return;

    final bundle = DataLoader.loadBundle(customPath: dataPath);
    _allEntries = List.unmodifiable(bundle.names);

    // AR index, pass 1: canonical spellings are unconditional and take
    // priority over any other lemma's variant claiming the same string
    // (the book has zero duplicate canonical ar values).
    final canonicalArKeys = _allEntries.map((e) => e.ar).toSet();
    final canonicalArNormKeys =
        _allEntries.map((e) => normalizeAr(e.ar)).toSet();
    for (final entry in _allEntries) {
      _arIndex[entry.ar] = entry;
      _arNormIndex[normalizeAr(entry.ar)] = entry;
    }

    for (final entry in _allEntries) {
      // AR index, pass 2: variants. Keep the higher-share lemma when
      // two rows' variants claim the same spelling — same rule as
      // English keys, so a rare misspelling cannot steal a common
      // name's lookup.
      for (final v in entry.arVariants) {
        final stripped = v.trim();
        if (stripped.isNotEmpty) {
          _claimArVariant(_arIndex, canonicalArKeys, stripped, entry);
          _claimArVariant(
            _arNormIndex,
            canonicalArNormKeys,
            normalizeAr(stripped),
            entry,
          );
        }
      }

      // EN Index — keep the higher-share lemma on a colliding key
      _claimEn(normalizeEn(entry.en), entry);

      for (final v in entry.enVariants) {
        final stripped = v.trim();
        if (stripped.isNotEmpty) {
          _claimEn(normalizeEn(stripped), entry);
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
