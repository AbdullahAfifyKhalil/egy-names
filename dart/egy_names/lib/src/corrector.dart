import 'lookup_indices.dart';

class Corrector {
  static String correctToken(String token, {String? dataPath}) {
    if (token.trim().isEmpty) return token;
    final t = token.trim();

    // 1. Direct surface correction pair
    final canonical = LookupIndices.getCorrection(t, dataPath: dataPath);
    if (canonical != null) return canonical;

    // 2. Exact match in arabic index (including phonetic variants)
    final entry = LookupIndices.lookupAr(t, dataPath: dataPath);
    if (entry != null) return entry.ar;

    // 3. Normalized form lookup
    final norm = LookupIndices.normalizeAr(t);
    final arNorm = LookupIndices.getArNormForms(dataPath: dataPath);
    final normEntry = arNorm[norm];
    if (normEntry != null) return normEntry.ar;

    // 4. Trailing Alif / Alif Maqsura check
    if (norm.endsWith('\u0627')) {
      final alt = '${norm.substring(0, norm.length - 1)}\u064A';
      final altMatch = arNorm[alt];
      if (altMatch != null) return altMatch.ar;
    } else if (norm.endsWith('\u064A')) {
      final alt = '${norm.substring(0, norm.length - 1)}\u0627';
      final altMatch = arNorm[alt];
      if (altMatch != null) return altMatch.ar;
    }

    return t;
  }

  static String correct(String name, {String? dataPath}) {
    if (name.trim().isEmpty) return name;
    final rawTokens = name.trim().split(RegExp(r'\s+'));
    final result = <String>[];

    for (var i = 0; i < rawTokens.length; i++) {
      final current = rawTokens[i];

      // Check compound pair (e.g. "عبد" + "الرحيم" -> "عبدالرحيم")
      if (i < rawTokens.length - 1) {
        final next = rawTokens[i + 1];
        final compound = '$current $next';
        final compoundNoSpace = '$current$next';

        final compoundEntry = LookupIndices.lookupAr(compound, dataPath: dataPath) ??
            LookupIndices.lookupAr(compoundNoSpace, dataPath: dataPath);
        if (compoundEntry != null) {
          result.add(compoundEntry.ar);
          i++; // skip compound second part
          continue;
        }
      }

      result.add(correctToken(current, dataPath: dataPath));
    }

    return result.join(' ');
  }
}
