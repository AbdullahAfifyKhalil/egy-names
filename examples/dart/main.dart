import 'package:egy_names/egy_names.dart';

void main() {
  final en = EgyptianNames();

  print('=' * 60);
  print(' Egyptian Names (egy_names) - Flutter / Dart Showcase');
  print('=' * 60);

  // 1. Generation
  print('\n1. Name Generation:');
  final names = en.generate(count: 3, length: 3, gender: 'female');
  for (final n in names) {
    print('   ${n.ar} (${n.en})');
  }

  // 2. Translation
  print('\n2. Transliteration:');
  print('   "محمد أحمد علي" -> ${en.translate("محمد أحمد علي")}');

  // 3. Correction
  print('\n3. Orthographic Correction:');
  print('   "احمد مصطفا عبد الرحيم" -> ${en.correct("احمد مصطفا عبد الرحيم")}');

  // 4. Tashkeel
  print('\n4. Tashkeel:');
  print('   "محمد عبدالرحمن" -> ${en.tashkeel("محمد عبدالرحمن")}');

  // 5. Splitting
  print('\n5. Splitting unspaced name:');
  print('   "محمدأحمدعليحسن" -> ${en.split("محمدأحمدعليحسن")}');
}
