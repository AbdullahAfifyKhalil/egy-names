import 'package:egy_names/egy_names.dart';

void main() {
  final en = EgyNames();

  // 1. Generate culturally authentic Egyptian full names
  print('--- Name Generation ---');
  final names = en.generate(count: 3, gender: 'male', religion: 'muslim');
  for (final n in names) {
    print('${n.ar}  --  ${n.en}');
  }

  // 2. Translation & Correction
  print('\n--- Translation & Correction ---');
  print(en.translate('محمد أحمد علي')); // Mohamed Ahmed Ali
  print(en.correct('احمد مصطفا عبد الرحيم')); // أحمد مصطفى عبدالرحيم
  print(en.tashkeel('محمد عبدالرحمن')); // مُحَمَّد عَبْدُالرَّحْمَن

  // 3. Intelligent Splitting
  print('\n--- Concatenated Name Splitting ---');
  final segments = en.split('محمدأحمدعليحسنالشاذلي');
  print(segments); // [محمد, أحمد, علي, حسن, الشاذلي]

  // 4. Metadata Annotation
  print('\n--- Name Annotation ---');
  final info = en.annotate('محمد');
  if (info != null) {
    print('Gender: ${info.gender}, Religion: ${info.religion}');
    print('Meaning: ${info.meaningAr}');
  }

  // 5. Gender & Religion Inferences
  print('\n--- Inferences ---');
  print(en.detectGender('مريم إبراهيم حسن'));
  print(en.detectReligion('جورج بطرس سمير ميخائيل'));
}
