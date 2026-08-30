import 'package:egy_names/egy_names.dart';

void main() {
  final en = EgyNames();

  print('=' * 60);
  print(' Egyptian Names (egy_names) 0.3.6 — Dart');
  print('=' * 60);

  print('\n1. Generate a grounded chain:');
  for (final n in en.generate(count: 3, length: 4, gender: 'female', religion: 'muslim')) {
    print('   ${n.ar}  (${n.en})');
  }

  print('\n2. Translate:');
  print('   ${en.translate("محمد أحمد علي الشناوي")}');

  print('\n3. Correct:');
  print('   ${en.correct("احمد مصطفا عبد الرحيم")}');

  print('\n4. Tashkeel and IPA:');
  print('   Standard: ${en.tashkeel("محمد عبدالرحمن")}');
  print('   Egyptian: ${en.tashkeelEg("محمد عبدالرحمن")}');
  print('   IPA std:  ${en.ipa("جمال")}');
  print('   IPA eg:   ${en.ipaEg("جمال")}');

  print('\n5. Split a concatenated dump:');
  print('   ${en.split("محمدأحمدعليحسنالشناوي")}');

  print('\n6. Pet names and figures:');
  print('   dallaa: ${en.dallaa("محمد", format: "tashkeel")}');
  print('   figures: ${en.famousFigures("محمد", lang: "en").take(2).toList()}');

  print('\n7. Lookup:');
  print('   root=${en.root("محمد")} | origin=${en.origin("محمد")} | trend=${en.trend("محمد")}');
  print('   meaning: ${en.meaning("محمد")?['en']}');

  print('\n8. Validity — personal names only:');
  print('   isValid("محمد")  = ${en.isValid("محمد")}');
  print('   isValid("Mahmoud") = ${en.isValid("Mahmoud")}');
  print('   isValid("الله")   = ${en.isValid("الله")}  // in the index, not a person');

  print('\n9. First personal token wins:');
  print('   ${en.detectGender("فاطمة محمد علي")}');
  print('   ${en.detectReligion("مينا جرجس بطرس")}');

  print('\n10. Chain, rank, uniqueness:');
  for (final p in en.analyzeChain('محمد أحمد علي الشناوي')) {
    print('   Slot ${p.slot}: ${p.name} — ${p.role}');
  }
  final rank = en.rank('محمد');
  final uniq = en.uniqueness('محمد أحمد علي الشناوي');
  print('   rank=#${rank?.rank}  uniqueness=${uniq.score} (${uniq.label})');
}
