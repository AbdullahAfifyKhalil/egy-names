enum Gender {
  male('male'),
  female('female'),
  neutral('neutral');

  final String value;
  const Gender(this.value);

  static Gender fromCode(String code) {
    switch (code) {
      case 'm':
        return Gender.male;
      case 'f':
        return Gender.female;
      default:
        return Gender.neutral;
    }
  }

  static Gender? fromString(String? str) {
    if (str == null) return null;
    switch (str.toLowerCase()) {
      case 'male':
      case 'm':
        return Gender.male;
      case 'female':
      case 'f':
        return Gender.female;
      case 'neutral':
      case 'n':
        return Gender.neutral;
      default:
        return null;
    }
  }
}

enum Religion {
  muslim('muslim'),
  christian('christian'),
  neutral('neutral');

  final String value;
  const Religion(this.value);

  static Religion fromCode(String code) {
    switch (code) {
      case 'm':
        return Religion.muslim;
      case 'c':
        return Religion.christian;
      default:
        return Religion.neutral;
    }
  }

  static Religion? fromString(String? str) {
    if (str == null) return null;
    switch (str.toLowerCase()) {
      case 'muslim':
      case 'm':
        return Religion.muslim;
      case 'christian':
      case 'c':
        return Religion.christian;
      case 'neutral':
      case 'n':
        return Religion.neutral;
      default:
        return null;
    }
  }
}

enum NameRole {
  given('given'),
  family('family');

  final String value;
  const NameRole(this.value);

  static NameRole fromCode(String code) {
    return code == 'f' ? NameRole.family : NameRole.given;
  }

  static NameRole? fromString(String? str) {
    if (str == null) return null;
    switch (str.toLowerCase()) {
      case 'given':
      case 'g':
        return NameRole.given;
      case 'family':
      case 'f':
        return NameRole.family;
      default:
        return null;
    }
  }
}

enum FrequencyClass {
  common('common'),
  normal('normal'),
  rare('rare');

  final String value;
  const FrequencyClass(this.value);

  static FrequencyClass fromCode(String code) {
    switch (code) {
      case 'c':
        return FrequencyClass.common;
      case 'n':
        return FrequencyClass.normal;
      case 'r':
      default:
        return FrequencyClass.rare;
    }
  }

  static FrequencyClass? fromString(String? str) {
    if (str == null) return null;
    switch (str.toLowerCase()) {
      case 'common':
      case 'c':
        return FrequencyClass.common;
      case 'normal':
      case 'n':
        return FrequencyClass.normal;
      case 'rare':
      case 'r':
        return FrequencyClass.rare;
      default:
        return null;
    }
  }
}

class NameEntry {
  final String ar;
  final String en;
  final Gender gender;
  final Religion religion;
  final NameRole role;
  final List<String> arVariants;
  final List<String> enVariants;
  final List<double> slotPcts;
  final double corpusShare;
  final FrequencyClass frequency;
  final String tashkeel;
  final String meaningAr;
  final String meaningEn;

  NameEntry({
    required this.ar,
    required this.en,
    required this.gender,
    required this.religion,
    required this.role,
    required this.arVariants,
    required this.enVariants,
    required this.slotPcts,
    required this.corpusShare,
    required this.frequency,
    required this.tashkeel,
    required this.meaningAr,
    required this.meaningEn,
  });

  factory NameEntry.fromJson(Map<String, dynamic> json) {
    final ar = json['a'] as String;
    final en = json['e'] as String;
    final av = json['av'] as String? ?? '';
    final ev = json['ev'] as String? ?? '';
    final pRaw = json['p'] as List<dynamic>? ?? [];
    final pList = pRaw.map((e) => (e as num).toDouble()).toList();

    return NameEntry(
      ar: ar,
      en: en,
      gender: Gender.fromCode(json['g'] as String? ?? 'n'),
      religion: Religion.fromCode(json['r'] as String? ?? 'n'),
      role: NameRole.fromCode(json['l'] as String? ?? 'g'),
      arVariants: av.isNotEmpty ? av.split('|') : [ar],
      enVariants: ev.isNotEmpty ? ev.split('|') : [en],
      slotPcts: pList,
      corpusShare: (json['tp'] as num? ?? 0).toDouble(),
      frequency: FrequencyClass.fromCode(json['fc'] as String? ?? 'r'),
      tashkeel: json['t'] as String? ?? '',
      meaningAr: json['ma'] as String? ?? '',
      meaningEn: json['me'] as String? ?? '',
    );
  }
}

class NameInfo {
  final String ar;
  final String en;
  final String gender;
  final String religion;
  final String role;
  final String frequencyClass;
  final double corpusShare;
  final String tashkeel;
  final String? meaningAr;
  final String? meaningEn;
  final List<String> arVariants;
  final List<String> enVariants;
  final List<double> slotDistribution;

  NameInfo({
    required this.ar,
    required this.en,
    required this.gender,
    required this.religion,
    required this.role,
    required this.frequencyClass,
    required this.corpusShare,
    required this.tashkeel,
    this.meaningAr,
    this.meaningEn,
    required this.arVariants,
    required this.enVariants,
    required this.slotDistribution,
  });

  factory NameInfo.fromEntry(NameEntry entry) {
    return NameInfo(
      ar: entry.ar,
      en: entry.en,
      gender: entry.gender.value,
      religion: entry.religion.value,
      role: entry.role.value,
      frequencyClass: entry.frequency.value,
      corpusShare: entry.corpusShare,
      tashkeel: entry.tashkeel,
      meaningAr: entry.meaningAr.isNotEmpty ? entry.meaningAr : null,
      meaningEn: entry.meaningEn.isNotEmpty ? entry.meaningEn : null,
      arVariants: List.unmodifiable(entry.arVariants),
      enVariants: List.unmodifiable(entry.enVariants),
      slotDistribution: List.unmodifiable(entry.slotPcts),
    );
  }

  Map<String, dynamic> toJson() => {
        'ar': ar,
        'en': en,
        'gender': gender,
        'religion': religion,
        'role': role,
        'frequency_class': frequencyClass,
        'corpus_share': corpusShare,
        'tashkeel': tashkeel,
        'meaning_ar': meaningAr,
        'meaning_en': meaningEn,
        'ar_variants': arVariants,
        'en_variants': enVariants,
        'slot_distribution': slotDistribution,
      };

  @override
  String toString() => 'NameInfo(ar: $ar, en: $en, gender: $gender, religion: $religion)';
}

class GeneratedName {
  final String ar;
  final String en;
  final List<String> partsAr;
  final List<String> partsEn;

  GeneratedName({
    required this.ar,
    required this.en,
    required this.partsAr,
    required this.partsEn,
  });

  Map<String, dynamic> toJson() => {
        'ar': ar,
        'en': en,
        'parts_ar': partsAr,
        'parts_en': partsEn,
      };

  @override
  String toString() => '$ar  --  $en';
}

class ChainPart {
  final String name;
  final int slot;
  final String role;
  final String detail;

  ChainPart({
    required this.name,
    required this.slot,
    required this.role,
    required this.detail,
  });

  Map<String, dynamic> toJson() => {
        'name': name,
        'slot': slot,
        'role': role,
        'detail': detail,
      };

  @override
  String toString() => 'Slot $slot: $name ($role - $detail)';
}

class GenderDetection {
  final String gender;
  final double confidence;

  GenderDetection({required this.gender, required this.confidence});

  Map<String, dynamic> toJson() => {
        'gender': gender,
        'confidence': confidence,
      };

  @override
  String toString() => 'GenderDetection(gender: $gender, confidence: ${confidence.toStringAsFixed(2)})';
}

class ReligionDetection {
  final String religion;
  final double confidence;

  ReligionDetection({required this.religion, required this.confidence});

  Map<String, dynamic> toJson() => {
        'religion': religion,
        'confidence': confidence,
      };

  @override
  String toString() => 'ReligionDetection(religion: $religion, confidence: ${confidence.toStringAsFixed(2)})';
}

class RankInfo {
  final int rank;
  final double percentile;
  final String corpusShare;
  final String description;

  RankInfo({
    required this.rank,
    required this.percentile,
    required this.corpusShare,
    required this.description,
  });

  Map<String, dynamic> toJson() => {
        'rank': rank,
        'percentile': percentile,
        'corpus_share': corpusShare,
        'description': description,
      };

  @override
  String toString() => 'RankInfo(rank: #$rank, percentile: ${percentile.toStringAsFixed(2)}%, description: $description)';
}

class UniquenessScore {
  final double score;
  final String label;
  final String note;

  UniquenessScore({
    required this.score,
    required this.label,
    required this.note,
  });

  Map<String, dynamic> toJson() => {
        'score': score,
        'label': label,
        'note': note,
      };

  @override
  String toString() => 'UniquenessScore(score: ${score.toStringAsFixed(3)}, label: $label, note: $note)';
}
