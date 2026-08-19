import 'lookup_indices.dart';
import 'types.dart';

class SearchEngine {
  static List<NameInfo> search({
    String? gender,
    String? religion,
    String? role,
    String? frequency,
    String? startsWith,
    String? endsWith,
    String? contains,
    double? minCorpusShare,
    int maxResults = 50,
    String sortBy = 'corpus_share',
    String? dataPath,
  }) {
    final entries = LookupIndices.getAll(dataPath: dataPath);

    final g = Gender.fromString(gender);
    final r = Religion.fromString(religion);
    final rl = NameRole.fromString(role);
    final f = FrequencyClass.fromString(frequency);

    final prefixAr =
        startsWith != null && LookupIndices.isArabic(startsWith);
    final suffixAr =
        endsWith != null && LookupIndices.isArabic(endsWith);
    final containsAr =
        contains != null && LookupIndices.isArabic(contains);

    final filtered = entries.where((e) {
      if (g != null && e.gender != g && e.gender != Gender.neutral) {
        return false;
      }
      if (r != null && e.religion != r && e.religion != Religion.neutral) {
        return false;
      }
      if (rl != null && e.role != rl) {
        return false;
      }
      if (f != null && e.frequency != f) {
        return false;
      }
      if (minCorpusShare != null && e.corpusShare < minCorpusShare) {
        return false;
      }

      if (startsWith != null) {
        if (prefixAr) {
          if (!LookupIndices.normalizeAr(e.ar)
              .startsWith(LookupIndices.normalizeAr(startsWith))) {
            return false;
          }
        } else {
          if (!LookupIndices.normalizeEn(e.en)
              .startsWith(LookupIndices.normalizeEn(startsWith))) {
            return false;
          }
        }
      }

      if (endsWith != null) {
        if (suffixAr) {
          if (!LookupIndices.normalizeAr(e.ar)
              .endsWith(LookupIndices.normalizeAr(endsWith))) {
            return false;
          }
        } else {
          if (!LookupIndices.normalizeEn(e.en)
              .endsWith(LookupIndices.normalizeEn(endsWith))) {
            return false;
          }
        }
      }

      if (contains != null) {
        if (containsAr) {
          if (!LookupIndices.normalizeAr(e.ar)
              .contains(LookupIndices.normalizeAr(contains))) {
            return false;
          }
        } else {
          if (!LookupIndices.normalizeEn(e.en)
              .contains(LookupIndices.normalizeEn(contains))) {
            return false;
          }
        }
      }

      return true;
    }).toList();

    if (sortBy == 'alphabetical') {
      filtered.sort((a, b) => a.ar.compareTo(b.ar));
    } else {
      filtered.sort((a, b) => b.corpusShare.compareTo(a.corpusShare));
    }

    final capped = filtered.take(maxResults).toList();
    return capped.map((e) => NameInfo.fromEntry(e)).toList();
  }
}
