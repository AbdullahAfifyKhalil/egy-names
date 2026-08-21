import 'package:egy_names/egy_names.dart';
import 'package:test/test.dart';

void main() {
  group('EgyNames Dart Tests', () {
    final en = EgyNames(seed: 42);

    test('Data statistics', () {
      final stats = en.stats();
      expect(stats['total_names'], greaterThan(30000));
      expect(stats['corpus_students'], greaterThan(2000000));
    });

    test('Generation works', () {
      final names = en.generate(count: 5);
      expect(names.length, equals(5));
      for (final n in names) {
        expect(n.ar.isNotEmpty, isTrue);
        expect(n.en.isNotEmpty, isTrue);
      }
    });

    test('Translation works in both directions', () {
      expect(en.translate('محمد أحمد علي'), equals('Mohamed Ahmed Ali'));
      expect(en.translate('Mohamed Ahmed Ali'), equals('محمد أحمد علي'));
    });

    test('Splitting DP segmentation', () {
      final splitResult = en.split('محمدأحمدعليحسنالشاذلي');
      expect(splitResult, equals(['محمد', 'أحمد', 'علي', 'حسن', 'الشاذلي']));
    });

    test('Correction & Tashkeel', () {
      expect(en.correct('احمد'), equals('أحمد'));
      expect(en.tashkeel('محمد عبدالرحمن'), equals('مُحَمَّد عَبْدُالرَّحْمَن'));
    });

    test('Meaning annotation', () {
      final meaning = en.meaning('محمد');
      expect(meaning, isNotNull);
      expect(meaning!['ar'], contains('المحمود'));
    });

    test('Creative gender and religion detection', () {
      final g = en.detectGender('مريم إبراهيم حسن');
      expect(g.gender, equals('female'));

      final r = en.detectReligion('جورج بطرس سمير ميخائيل');
      expect(r.religion, equals('christian'));
    });
  });
}
