import 'dart:math';

import 'src/annotator.dart';
import 'src/corrector.dart';
import 'src/data.dart';
import 'src/generator.dart';
import 'src/lookup_indices.dart';
import 'src/search.dart';
import 'src/splitter.dart';
import 'src/translator.dart';
import 'src/types.dart';

export 'src/types.dart';

typedef EgyNames = EgyptianNames;

class EgyptianNames {
  final int? seed;
  final String? customDataPath;

  EgyptianNames({this.seed, this.customDataPath});

  // ----------------------------------------------------------------------
  // Core Methods
  // ----------------------------------------------------------------------

  List<GeneratedName> generate({
    int count = 1,
    String? gender,
    String? religion,
    int? length,
    bool familyName = true,
    String? frequency,
    int? seed,
  }) {
    return Generator.generate(
      count: count,
      gender: gender,
      religion: religion,
      length: length,
      familyName: familyName,
      frequency: frequency,
      seed: seed ?? this.seed,
      dataPath: customDataPath,
    );
  }

  String translate(String name, {String? to}) {
    return Translator.translate(name, to: to, dataPath: customDataPath);
  }

  dynamic annotate(String name) {
    return Annotator.annotate(name, dataPath: customDataPath);
  }

  List<String> split(String fullName) {
    return Splitter.split(fullName, dataPath: customDataPath);
  }

  String tashkeel(String name) {
    if (name.trim().isEmpty) return name;
    final rawTokens = name.trim().split(RegExp(r'\s+'));
    final result = <String>[];

    for (var i = 0; i < rawTokens.length; i++) {
      final current = rawTokens[i];

      if (i < rawTokens.length - 1) {
        final next = rawTokens[i + 1];
        final compound = '$current $next';
        final compoundNoSpace = '$current$next';
        final compoundEntry = LookupIndices.lookupAr(compound, dataPath: customDataPath) ??
            LookupIndices.lookupAr(compoundNoSpace, dataPath: customDataPath);
        if (compoundEntry != null && compoundEntry.tashkeel.isNotEmpty) {
          result.add(compoundEntry.tashkeel);
          i++;
          continue;
        }
      }

      final entry = LookupIndices.lookupAr(current, dataPath: customDataPath);
      result.add(entry != null && entry.tashkeel.isNotEmpty ? entry.tashkeel : current);
    }

    return result.join(' ');
  }

  String correct(String name) {
    return Corrector.correct(name, dataPath: customDataPath);
  }

  Map<String, String>? meaning(String name) {
    final entry = LookupIndices.lookup(name, dataPath: customDataPath);
    if (entry == null) return null;
    if (entry.meaningAr.isEmpty && entry.meaningEn.isEmpty) return null;
    return {
      'ar': entry.meaningAr,
      'en': entry.meaningEn,
    };
  }

  List<NameInfo> families({
    int count = 50,
    String? frequency,
    String? religion,
    String? startsWith,
  }) {
    return SearchEngine.search(
      role: 'family',
      maxResults: count,
      frequency: frequency,
      religion: religion,
      startsWith: startsWith,
      dataPath: customDataPath,
    );
  }

  List<NameInfo> search({
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
  }) {
    return SearchEngine.search(
      gender: gender,
      religion: religion,
      role: role,
      frequency: frequency,
      startsWith: startsWith,
      endsWith: endsWith,
      contains: contains,
      minCorpusShare: minCorpusShare,
      maxResults: maxResults,
      sortBy: sortBy,
      dataPath: customDataPath,
    );
  }

  // ----------------------------------------------------------------------
  // Creative Methods
  // ----------------------------------------------------------------------

  bool isValid(String name) {
    return LookupIndices.lookup(name, dataPath: customDataPath) != null;
  }

  GenderDetection detectGender(String fullName) {
    final tokens = fullName.trim().split(RegExp(r'\s+'));
    if (tokens.isEmpty) {
      return GenderDetection(gender: 'neutral', confidence: 0.0);
    }

    double maleScore = 0;
    double femaleScore = 0;
    double neutralScore = 0;
    double totalWeight = 0;

    for (int i = 0; i < tokens.length; i++) {
      final entry =
          LookupIndices.lookup(tokens[i], dataPath: customDataPath);
      if (entry == null) continue;

      final w = i == 0 ? 4.0 : (i == 1 ? 2.0 : 1.0);
      totalWeight += w;

      if (entry.gender == Gender.male) {
        maleScore += w;
      } else if (entry.gender == Gender.female) {
        femaleScore += w;
      } else {
        neutralScore += w;
      }
    }

    if (totalWeight == 0) {
      return GenderDetection(gender: 'neutral', confidence: 0.0);
    }

    final maxScore = max(maleScore, max(femaleScore, neutralScore));
    final confidence = maxScore / totalWeight;

    if (maxScore == maleScore) {
      return GenderDetection(gender: 'male', confidence: confidence);
    }
    if (maxScore == femaleScore) {
      return GenderDetection(gender: 'female', confidence: confidence);
    }
    return GenderDetection(gender: 'neutral', confidence: confidence);
  }

  ReligionDetection detectReligion(String fullName) {
    final tokens = fullName.trim().split(RegExp(r'\s+'));
    if (tokens.isEmpty) {
      return ReligionDetection(religion: 'neutral', confidence: 0.0);
    }

    double muslimScore = 0;
    double christianScore = 0;
    double neutralScore = 0;
    double totalWeight = 0;

    for (int i = 0; i < tokens.length; i++) {
      final entry =
          LookupIndices.lookup(tokens[i], dataPath: customDataPath);
      if (entry == null) continue;

      const w = 1.0;
      totalWeight += w;

      if (entry.religion == Religion.muslim) {
        muslimScore += w;
      } else if (entry.religion == Religion.christian) {
        christianScore += w;
      } else {
        neutralScore += w;
      }
    }

    if (totalWeight == 0) {
      return ReligionDetection(religion: 'neutral', confidence: 0.0);
    }

    final maxScore = max(muslimScore, max(christianScore, neutralScore));
    final confidence = maxScore / totalWeight;

    if (maxScore == muslimScore) {
      return ReligionDetection(religion: 'muslim', confidence: confidence);
    }
    if (maxScore == christianScore) {
      return ReligionDetection(religion: 'christian', confidence: confidence);
    }
    return ReligionDetection(religion: 'neutral', confidence: confidence);
  }

  Map<String, dynamic>? fingerprint(String name) {
    final entry = LookupIndices.lookup(name, dataPath: customDataPath);
    if (entry == null) return null;

    final slots = entry.slotPcts;
    const slotLabels = [
      '1st',
      '2nd',
      '3rd',
      '4th',
      '5th',
      '6th',
      '7th',
      '8th+'
    ];

    int peakSlot = 0;
    double maxPct = -1;
    for (int i = 0; i < slots.length; i++) {
      if (slots[i] > maxPct) {
        maxPct = slots[i];
        peakSlot = i;
      }
    }

    String nameType = '';
    if (entry.role == NameRole.family) {
      nameType = (slots.isNotEmpty && slots[0] < 1.0)
          ? 'pure_surname'
          : 'surname_given';
    } else if (peakSlot == 0 && slots.isNotEmpty && slots[0] > 40) {
      nameType = 'primary_given';
    } else if (peakSlot == 0) {
      nameType = 'given_name';
    } else {
      nameType = 'patronymic';
    }

    final descParts = <String>[];
    if (nameType == 'primary_given') {
      descParts.add(
          'Dominant first name (${slots[0].toStringAsFixed(1)}% in slot 1)');
    } else if (nameType == 'pure_surname') {
      descParts.add('Almost exclusively a family/surname');
    } else if (nameType == 'given_name') {
      descParts.add('Given name appearing across multiple positions');
    } else {
      descParts.add('Peaks in slot ${peakSlot + 1}');
    }

    if (entry.frequency == FrequencyClass.common) {
      descParts.add('very common');
    } else if (entry.frequency == FrequencyClass.rare) {
      descParts.add('rare');
    }

    final slotMap = <String, double>{};
    for (int i = 0; i < slotLabels.length && i < slots.length; i++) {
      slotMap[slotLabels[i]] =
          double.parse(slots[i].toStringAsFixed(2));
    }

    return {
      'name_ar': entry.ar,
      'name_en': entry.en,
      'type': nameType,
      'slots': slotMap,
      'corpus_share': entry.corpusShare,
      'description': descParts.join('; '),
    };
  }

  RankInfo? rank(String name) {
    final entry = LookupIndices.lookup(name, dataPath: customDataPath);
    if (entry == null) return null;

    final ranked = LookupIndices.getRanked(dataPath: customDataPath);
    final total = ranked.length;

    for (int i = 0; i < total; i++) {
      if (ranked[i].ar == entry.ar) {
        final rankPos = i + 1;
        final percentile = (1 - (rankPos - 1) / total) * 100;
        String desc =
            'The #$rankPos most common name in the Egyptian corpus';
        if (rankPos <= 10) {
          desc = 'Top 10 — $desc';
        } else if (rankPos <= 100) {
          desc = 'Top 100 — $desc';
        } else if (rankPos <= 1000) {
          desc = 'Top 1000 — $desc';
        }

        return RankInfo(
          rank: rankPos,
          percentile: double.parse(percentile.toStringAsFixed(2)),
          corpusShare: '${entry.corpusShare.toStringAsFixed(4)}%',
          description: desc,
        );
      }
    }
    return null;
  }

  int _levenshtein(String s1, String s2) {
    if (s1.length < s2.length) return _levenshtein(s2, s1);
    if (s2.isEmpty) return s1.length;

    var prevRow = List<int>.generate(s2.length + 1, (i) => i);
    for (int i = 0; i < s1.length; i++) {
      final currRow = [i + 1];
      for (int j = 0; j < s2.length; j++) {
        final insertions = prevRow[j + 1] + 1;
        final deletions = currRow[j] + 1;
        final substitutions = prevRow[j] + (s1[i] != s2[j] ? 1 : 0);
        currRow.add(min(insertions, min(deletions, substitutions)));
      }
      prevRow = currRow;
    }
    return prevRow.last;
  }

  List<String> similar(
    String name, {
    int maxResults = 10,
    int maxDistance = 3,
  }) {
    final useAr = LookupIndices.isArabic(name);
    final entries = LookupIndices.getAll(dataPath: customDataPath);
    final nameNorm = useAr
        ? LookupIndices.normalizeAr(name)
        : LookupIndices.normalizeEn(name);

    final scored = <({int dist, double share, String candidate})>[];
    for (final e in entries) {
      final candidate = useAr ? e.ar : e.en;
      final candNorm = useAr
          ? LookupIndices.normalizeAr(candidate)
          : LookupIndices.normalizeEn(candidate);
      if (candNorm == nameNorm) continue;

      final dist = _levenshtein(nameNorm, candNorm);
      if (dist <= maxDistance) {
        scored.add((dist: dist, share: e.corpusShare, candidate: candidate));
      }
    }

    scored.sort((a, b) {
      if (a.dist != b.dist) return a.dist.compareTo(b.dist);
      return b.share.compareTo(a.share);
    });

    return scored.take(maxResults).map((s) => s.candidate).toList();
  }

  List<ChainPart> analyzeChain(String fullName) {
    final tokens = fullName.trim().split(RegExp(r'\s+'));
    if (tokens.isEmpty) return [];

    final parts = <ChainPart>[];
    final n = tokens.length;

    for (int i = 0; i < n; i++) {
      final t = tokens[i];
      final entry = LookupIndices.lookup(t, dataPath: customDataPath);
      final slot = i + 1;

      String roleLabel = '';
      String detail = '';

      if (i == 0) {
        roleLabel = 'person';
        detail = "The individual's given name";
      } else if (i == n - 1 && entry != null && entry.role == NameRole.family) {
        roleLabel = 'family_name';
        detail = 'Family/tribal surname';
      } else if (i == 1) {
        roleLabel = 'father';
        detail = "Father's name";
      } else if (i == 2) {
        roleLabel = 'grandfather';
        detail = 'Paternal grandfather';
      } else if (i == 3) {
        roleLabel = 'great_grandfather';
        detail = 'Great-grandfather';
      } else {
        roleLabel = 'ancestor';
        detail = 'Ancestor (generation $i)';
      }

      parts.add(
        ChainPart(
          name: t,
          slot: slot,
          role: roleLabel,
          detail: detail,
        ),
      );
    }

    return parts;
  }

  UniquenessScore uniqueness(String fullName) {
    final tokens = fullName.trim().split(RegExp(r'\s+'));
    if (tokens.isEmpty) {
      return UniquenessScore(
        score: 0.5,
        label: 'unknown',
        note: 'Empty input',
      );
    }

    final shares = <double>[];
    int unknownCount = 0;
    for (final t in tokens) {
      final entry = LookupIndices.lookup(t, dataPath: customDataPath);
      if (entry != null) {
        shares.add(entry.corpusShare);
      } else {
        unknownCount++;
      }
    }

    if (shares.isEmpty) {
      return UniquenessScore(
        score: 1.0,
        label: 'unknown',
        note: 'None of the name parts are in the Egyptian corpus',
      );
    }

    double logSum = 0;
    for (final s in shares) {
      logSum += log(max(s, 1e-9));
    }
    final logMean = logSum / shares.length;

    const maxLog = 2.6;
    const minLog = -9.2;
    double score = 1.0 - (logMean - minLog) / (maxLog - minLog);
    score = max(0.0, min(1.0, score));
    score = min(1.0, score + unknownCount * 0.15);

    String label = '';
    String note = '';
    if (score < 0.2) {
      label = 'extremely_common';
      note = 'Each part is among the most common names nationally';
    } else if (score < 0.4) {
      label = 'common';
      note = 'Well-known name parts with high national frequency';
    } else if (score < 0.6) {
      label = 'moderate';
      note = 'A mix of common and less common name parts';
    } else if (score < 0.8) {
      label = 'distinctive';
      note = 'Contains uncommon or regionally specific names';
    } else {
      label = 'highly_unique';
      note = 'Rare name combination — distinctive family heritage';
    }

    return UniquenessScore(
      score: double.parse(score.toStringAsFixed(3)),
      label: label,
      note: note,
    );
  }

  dynamic format(String fullName, {String style = 'full'}) {
    final tokens = fullName.trim().split(RegExp(r'\s+'));
    if (tokens.isEmpty) return fullName;

    if (style == 'full') return tokens.join(' ');

    if (style == 'first_last') {
      final first = tokens.first;
      final last = tokens.length > 1 ? tokens.last : '';
      return {'first': first, 'last': last};
    }

    if (style == 'western') {
      final firstEn = Translator.translateToken(tokens.first,
          to: 'en', dataPath: customDataPath);
      final lastEn = tokens.length > 1
          ? Translator.translateToken(tokens.last,
              to: 'en', dataPath: customDataPath)
          : '';
      return '$firstEn $lastEn'.trim();
    }

    if (style == 'initials') {
      final initials = tokens
          .sublist(0, tokens.length - 1)
          .map((t) => '${t.isNotEmpty ? t[0] : ""}.')
          .toList();
      initials.add(tokens.last);
      return initials.join(' ');
    }

    return tokens.join(' ');
  }

  List<String> suggest({
    String? gender,
    String? religion,
    String? role,
    String? frequency,
    String? startsWith,
    int count = 10,
  }) {
    final results = SearchEngine.search(
      gender: gender,
      religion: religion,
      role: role,
      frequency: frequency,
      startsWith: startsWith,
      maxResults: count,
      dataPath: customDataPath,
    );
    return results.map((r) => r.ar).toList();
  }

  Map<String, dynamic> stats() {
    final meta = DataLoader.loadBundle(customPath: customDataPath);
    final entries = LookupIndices.getAll(dataPath: customDataPath);
    int given = 0;
    int family = 0;
    int male = 0;
    int female = 0;

    for (final e in entries) {
      if (e.role == NameRole.given) given++;
      if (e.role == NameRole.family) family++;
      if (e.gender == Gender.male) male++;
      if (e.gender == Gender.female) female++;
    }

    return {
      'version': meta.version,
      'corpus_tokens': meta.corpusTokens,
      'corpus_students': meta.corpusStudents,
      'cohort_years': meta.cohortYears,
      'total_names': entries.length,
      'given_names': given,
      'family_names': family,
      'male_names': male,
      'female_names': female,
    };
  }

  BatchProcessor get batch => BatchProcessor(this);
}

class BatchProcessor {
  final EgyptianNames parent;
  BatchProcessor(this.parent);

  List<String> translate(List<String> names, {String? to}) {
    return names.map((n) => parent.translate(n, to: to)).toList();
  }

  List<dynamic> annotate(List<String> names) {
    return names.map((n) => parent.annotate(n)).toList();
  }

  List<String> correct(List<String> names) {
    return names.map((n) => parent.correct(n)).toList();
  }

  List<List<String>> split(List<String> names) {
    return names.map((n) => parent.split(n)).toList();
  }

  List<GenderDetection> detectGender(List<String> names) {
    return names.map((n) => parent.detectGender(n)).toList();
  }

  List<ReligionDetection> detectReligion(List<String> names) {
    return names.map((n) => parent.detectReligion(n)).toList();
  }

  List<String> tashkeel(List<String> names) {
    return names.map((n) => parent.tashkeel(n)).toList();
  }
}
