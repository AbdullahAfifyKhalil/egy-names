import 'compound_tokens.dart';
import 'lookup_indices.dart';

class Splitter {
  static const double baseSegmentCost = 1.0;
  static const double unknownPenalty = 8.0;
  static const double lengthBonusPerChar = -0.05;

  static const Map<String, double> freqBonus = {
    'c': -0.6,
    'n': -0.2,
    'r': 0.0,
  };

  static List<String> _dpSegment(String text, {String? dataPath}) {
    final arIndex = LookupIndices.getArForms(dataPath: dataPath);
    final arNorm = LookupIndices.getArNormForms(dataPath: dataPath);

    final n = text.length;
    // dp[i] = (cost, backpointer, isKnown)
    final dpCost = List<double>.filled(n + 1, double.infinity);
    final dpPrev = List<int>.filled(n + 1, -1);
    final dpKnown = List<bool>.filled(n + 1, false);

    dpCost[0] = 0.0;
    dpPrev[0] = 0;
    dpKnown[0] = true;

    for (int i = 1; i <= n; i++) {
      final startJ = i > 30 ? i - 30 : 0;
      for (int j = startJ; j < i; j++) {
        if (dpCost[j] == double.infinity) continue;

        final substr = text.substring(j, i);
        if (substr.length < 2 && j > 0) continue;

        var entry = arIndex[substr];
        entry ??= arNorm[LookupIndices.normalizeAr(substr)];

        if (entry != null) {
          final fChar = entry.frequency.value.isNotEmpty
              ? entry.frequency.value.substring(0, 1)
              : 'r';
          final cost = dpCost[j] +
              baseSegmentCost +
              (freqBonus[fChar] ?? 0.0) +
              lengthBonusPerChar * substr.length;
          if (cost < dpCost[i]) {
            dpCost[i] = cost;
            dpPrev[i] = j;
            dpKnown[i] = true;
          }
        } else {
          final cost = dpCost[j] + unknownPenalty + substr.length;
          if (cost < dpCost[i]) {
            dpCost[i] = cost;
            dpPrev[i] = j;
            dpKnown[i] = false;
          }
        }
      }
    }

    if (dpCost[n] == double.infinity) {
      return [text];
    }

    final segments = <String>[];
    int pos = n;
    while (pos > 0) {
      final prev = dpPrev[pos];
      segments.add(text.substring(prev, pos));
      pos = prev;
    }

    return segments.reversed.toList();
  }

  static List<String> split(String fullName, {String? dataPath}) {
    if (fullName.trim().isEmpty) return [];

    final text = fullName.trim();
    if (text.contains(' ')) {
      return compoundTokens(text, dataPath: dataPath)
          .map((t) => t.text)
          .toList();
    }

    if (LookupIndices.isArabic(text)) {
      final entry = LookupIndices.lookup(text, dataPath: dataPath);
      if (entry != null) {
        return [text];
      }
      return _dpSegment(text, dataPath: dataPath);
    }

    return [text];
  }
}
