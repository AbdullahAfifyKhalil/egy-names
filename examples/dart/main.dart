import 'package:egy_names/egy_names.dart';

void main() {
  final en = EgyNames();

  print('=' * 60);
  print(' Egyptian Names (egy_names) v0.3.2 — Dart / Flutter Showcase');
  print('=' * 60);

  print('\n1. Name Generation:');
  for (final n in en.generate(count: 3, length: 4, gender: 'female', religion: 'muslim')) {
    print('   ${n.ar}  (${n.en})');
  }

  print('\n2. Transliteration:');
  print('   "محمد أحمد علي الشناوي" -> ${en.translate("محمد أحمد علي الشناوي")}');

  print('\n3. Orthographic Correction:');
  print('   "احمد مصطفا عبد الرحيم" -> ${en.correct("احمد مصطفا عبد الرحيم")}');

  print('\n4. Dual Tashkeel & IPA:');
  print('   Standard: ${en.tashkeel("محمد عبدالرحمن")}');
  print('   Egyptian: ${en.tashkeelEg("محمد عبدالرحمن")}');
  print('   IPA std:  ${en.ipa("جمال")}');
  print('   IPA eg:   ${en.ipaEg("جمال")}');

  print('\n5. Splitting concatenated names:');
  print('   ${en.split("محمدأحمدعليحسنالشناوي")}');

  print('\n6. Pet names & famous figures:');
  print('   dallaa: ${en.dallaa("محمد", format: "tashkeel")}');
  print('   figures: ${en.famousFigures("محمد", lang: "en").take(2).toList()}');

  print('\n7. 14D lookup:');
  print('   root=${en.root("محمد")} | origin=${en.origin("محمد")} | trend=${en.trend("محمد")}');
  print('   meaning: ${en.meaning("محمد")?['en']}');

  print('\n8. Demographics:');
  print('   ${en.detectGender("فاطمة الزهراء")}');
  print('   ${en.detectReligion("مينا جرجس بطرس")}');

  print('\n9. Chain analysis, rank, uniqueness:');
  for (final p in en.analyzeChain('محمد أحمد علي الشناوي')) {
    print('   Slot ${p.slot}: ${p.name} — ${p.role}');
  }
  final rank = en.rank('محمد');
  final uniq = en.uniqueness('محمد أحمد علي الشناوي');
  print('   rank=#${rank?.rank}  uniqueness=${uniq.score} (${uniq.label})');
}
