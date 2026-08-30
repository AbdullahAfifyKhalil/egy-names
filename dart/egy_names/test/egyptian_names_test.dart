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
      expect(en.tashkeel('محمد عبدالرحمن'), contains('مُحَمَّد'));
      expect(en.tashkeel('محمد عبدالرحمن'), contains('الرَّحْمَن'));
    });

    test('Meaning annotation', () {
      final meaning = en.meaning('محمد');
      expect(meaning, isNotNull);
      expect(meaning!['ar'], contains('المحمود'));
    });

    test('11D Features (Tashkeel Eg, IPA, Dallaa, Roots, Trends)', () {
      expect(en.tashkeelEg('محمد'), isNotEmpty);
      expect(en.ipa('جمال', dialect: 'standard'), startsWith('/'));
      expect(en.ipaEg('جمال'), startsWith('['));
      expect(en.dallaa('محمد'), contains('ميدو'));
      expect(en.root('محمد'), equals('ح-م-د'));
      expect(en.origin('محمد'), equals('arabic_classical'));
      expect(en.famousFigures('محمد'), isNotEmpty);
      expect(en.trend('محمد'), equals('classic_timeless'));
    });

    test('Creative gender and religion detection', () {
      final g = en.detectGender('مريم إبراهيم حسن');
      expect(g.gender, equals('female'));

      final r = en.detectReligion('جورج بطرس سمير ميخائيل');
      expect(r.religion, equals('christian'));
    });

    test('First given name wins; non-person surfaces are not valid', () {
      expect(en.detectGender('فاطمة محمد علي حسن').gender, equals('female'));
      expect(
        en.detectReligion('جورج علاءالدين عبدالمسيح دغيدي').religion,
        equals('christian'),
      );
      expect(en.isValid('الله'), isFalse);
      expect(en.translate('Mahmoud'), equals('محمود'));
    });
  });
}
