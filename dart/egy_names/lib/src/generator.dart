import 'dart:math';
import 'lookup_indices.dart';
import 'types.dart';

class Generator {
  static const int defaultMinLen = 4;
  static const int defaultMaxLen = 5;

  static List<NameEntry> _filterEntries(
    List<NameEntry> entries, {
    Gender? gender,
    Religion? religion,
    NameRole? role,
    FrequencyClass? frequency,
  }) {
    return entries.where((e) {
      if (gender != null && e.gender != gender && e.gender != Gender.neutral) {
        return false;
      }
      if (religion != null &&
          e.religion != religion &&
          e.religion != Religion.neutral) {
        return false;
      }
      if (role != null && e.role != role) {
        return false;
      }
      if (frequency != null && e.frequency != frequency) {
        return false;
      }
      return true;
    }).toList();
  }

  static NameEntry _weightedPick(
    List<NameEntry> entries,
    int slotIdx,
    Random rng,
  ) {
    final candidates = <NameEntry>[];
    final weights = <double>[];
    double totalWeight = 0.0;

    for (final e in entries) {
      final w = (slotIdx < e.slotPcts.length ? e.slotPcts[slotIdx] : 0.0) *
          e.corpusShare;
      if (w > 0) {
        candidates.add(e);
        weights.add(w);
        totalWeight += w;
      }
    }

    if (candidates.isEmpty) {
      for (final e in entries) {
        final w = max(e.corpusShare, 1e-9);
        candidates.add(e);
        weights.add(w);
        totalWeight += w;
      }
    }

    double r = rng.nextDouble() * totalWeight;
    for (int i = 0; i < candidates.length; i++) {
      r -= weights[i];
      if (r <= 0) {
        return candidates[i];
      }
    }

    return candidates.last;
  }

  static List<GeneratedName> generate({
    int count = 1,
    String? gender,
    String? religion,
    int? length,
    bool familyName = true,
    String? frequency,
    int? seed,
    String? dataPath,
  }) {
    final rng = seed != null ? Random(seed) : Random();
    final allEntries = LookupIndices.getAll(dataPath: dataPath);

    final g = Gender.fromString(gender);
    final r = Religion.fromString(religion);
    final f = FrequencyClass.fromString(frequency);

    var firstPool = _filterEntries(
      allEntries,
      gender: g,
      religion: r,
      role: NameRole.given,
      frequency: f,
    );
    var patronPool = _filterEntries(
      allEntries,
      gender: Gender.male,
      religion: r,
      role: NameRole.given,
      frequency: f,
    );
    var familyPool = _filterEntries(
      allEntries,
      religion: r,
      role: NameRole.family,
      frequency: f,
    );

    if (firstPool.isEmpty) {
      firstPool = _filterEntries(allEntries, gender: g, role: NameRole.given);
    }
    if (patronPool.isEmpty) {
      patronPool = _filterEntries(
        allEntries,
        gender: Gender.male,
        role: NameRole.given,
      );
    }
    if (familyPool.isEmpty) {
      familyPool = _filterEntries(allEntries, role: NameRole.family);
    }

    final results = <GeneratedName>[];

    for (int c = 0; c < count; c++) {
      final chainLen = length ??
          (defaultMinLen + rng.nextInt(defaultMaxLen - defaultMinLen + 1));

      final partsAr = <String>[];
      final partsEn = <String>[];
      final seen = <String>{};

      // Slot 1
      var entry = _weightedPick(firstPool, 0, rng);
      int attempts = 0;
      while (seen.contains(entry.ar) && attempts < 20) {
        entry = _weightedPick(firstPool, 0, rng);
        attempts++;
      }
      partsAr.add(entry.ar);
      partsEn.add(entry.en);
      seen.add(entry.ar);

      // Patronymic slots 2 .. (N-1 or N)
      final patronEnd = familyName ? chainLen - 1 : chainLen;
      for (int slot = 1; slot < patronEnd; slot++) {
        final slotIdx = min(slot, 7);
        entry = _weightedPick(patronPool, slotIdx, rng);
        attempts = 0;
        while (seen.contains(entry.ar) && attempts < 20) {
          entry = _weightedPick(patronPool, slotIdx, rng);
          attempts++;
        }
        partsAr.add(entry.ar);
        partsEn.add(entry.en);
        seen.add(entry.ar);
      }

      // Family name slot
      if (familyName && chainLen > 1) {
        final slotIdx = min(chainLen - 1, 7);
        entry = _weightedPick(familyPool, slotIdx, rng);
        attempts = 0;
        while (seen.contains(entry.ar) && attempts < 20) {
          entry = _weightedPick(familyPool, slotIdx, rng);
          attempts++;
        }
        partsAr.add(entry.ar);
        partsEn.add(entry.en);
      }

      results.add(
        GeneratedName(
          ar: partsAr.join(' '),
          en: partsEn.join(' '),
          partsAr: partsAr,
          partsEn: partsEn,
        ),
      );
    }

    return results;
  }
}
