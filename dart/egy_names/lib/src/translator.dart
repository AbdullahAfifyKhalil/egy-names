import 'lookup_indices.dart';

class Translator {
  static String translateToken(
    String token, {
    String? to,
    String? dataPath,
  }) {
    final srcIsAr = LookupIndices.isArabic(token);
    final target = to ?? (srcIsAr ? 'en' : 'ar');

    if (target == 'en') {
      final entry = LookupIndices.lookupAr(token, dataPath: dataPath);
      return entry != null ? entry.en : token;
    } else {
      final entry = LookupIndices.lookupEn(token, dataPath: dataPath);
      return entry != null ? entry.ar : token;
    }
  }

  static String translate(
    String fullName, {
    String? to,
    String? dataPath,
  }) {
    if (fullName.trim().isEmpty) return fullName;
    final tokens = fullName.trim().split(RegExp(r'\s+'));
    final translated = tokens.map(
      (t) => translateToken(t, to: to, dataPath: dataPath),
    );
    return translated.join(' ');
  }
}
