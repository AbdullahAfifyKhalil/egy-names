/// Compound-aware tokenization for Arabic full names.
library;

import 'lookup_indices.dart';
import 'types.dart';

/// One resolved token of a full name: its surface text plus its book
/// entry, if any.
class CompoundToken {
  final String text;
  final NameEntry? entry;

  const CompoundToken(this.text, this.entry);
}

/// Split on whitespace, but merge an adjacent pair into one lemma
/// when the book has it as a two-word compound (e.g. kunya "Abu X").
///
/// A handful of book entries are legitimately two words (roughly 800
/// "Abu X" kunya/family lemmas plus a few compound given names). A
/// blind whitespace split treats them as two meaningless fragments,
/// breaking gender/religion detection and split() on names that
/// contain one. Greedy pairwise lookahead, same approach tashkeel()
/// already uses for "عبد الرحمن"-style pairs.
List<CompoundToken> compoundTokens(String fullName, {String? dataPath}) {
  final raw = fullName.trim().split(RegExp(r'\s+'));
  final out = <CompoundToken>[];
  var i = 0;
  final n = raw.length;
  while (i < n) {
    if (i < n - 1) {
      final pair = '${raw[i]} ${raw[i + 1]}';
      final pairEntry = LookupIndices.lookupAr(pair, dataPath: dataPath) ??
          LookupIndices.lookupAr('${raw[i]}${raw[i + 1]}', dataPath: dataPath);
      if (pairEntry != null) {
        out.add(CompoundToken(pair, pairEntry));
        i += 2;
        continue;
      }
    }
    out.add(CompoundToken(raw[i], LookupIndices.lookup(raw[i], dataPath: dataPath)));
    i += 1;
  }
  return out;
}
