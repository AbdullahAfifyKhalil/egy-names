import 'package:egy_names/egy_names.dart';

void main() {
  print('Initializing EgyNames in Dart...');
  final en = EgyNames(seed: 42);

  print('\n1. Data Stats:');
  final stats = en.stats();
  print('Loaded ${stats['total_names']} names.');
  if ((stats['total_names'] as int) < 30000) {
    throw Exception('Not enough names loaded');
  }

  print('\n2. Generation (5 random names):');
  final names = en.generate(count: 5, familyName: true);
  for (int i = 0; i < names.length; i++) {
    print('  ${i + 1}. ${names[i].ar}  --  ${names[i].en}');
  }

  print('\n3. Generating Female Christian Names:');
  final cNames = en.generate(count: 3, gender: 'female', religion: 'christian');
  for (final n in cNames) {
    print('  ${n.ar} (${n.en})');
  }

  print('\n4. Translation:');
  final t1 = en.translate('محمد أحمد علي');
  final t2 = en.translate('Mohamed Ahmed Ali');
  print('  محمد أحمد علي -> $t1');
  print('  Mohamed Ahmed Ali -> $t2');

  print('\n5. Splitting (DP Segmentation):');
  final s1 = en.split('محمد أحمد علي حسن الشاذلي');
  final s2 = en.split('محمدأحمدعليحسنالشاذلي'); // Concatenated
  final s3 = en.split('حسناء');
  print('  Spaced: $s1');
  print('  Concatenated: $s2');
  print('  Single name: $s3');

  print('\n6. Tashkeel:');
  final tk = en.tashkeel('محمد عبدالرحمن');
  print('  محمد عبدالرحمن -> $tk');

  print('\n7. Correction:');
  final c1 = en.correct('احمد');
  final c2 = en.correct('مصطفا');
  print('  احمد -> $c1');
  print('  مصطفا -> $c2');

  print('\n8. Annotation & Meaning:');
  final info = en.annotate('محمد') as NameInfo?;
  print('  محمد: ${info?.meaningAr}');

  print('\n9. Creative: Gender & Religion Detection:');
  final g1 = en.detectGender('مريم إبراهيم حسن');
  final r1 = en.detectReligion('جورج بطرس سمير ميخائيل');
  print('  مريم إبراهيم حسن -> $g1');
  print('  جورج بطرس سمير ميخائيل -> $r1');

  print('\n10. Creative: Chain Analysis:');
  final chain = en.analyzeChain('محمد أحمد علي حسن الشاذلي');
  for (final c in chain) {
    print('  $c');
  }

  print('\n11. Search:');
  final searchRes = en.search(startsWith: 'عبد', maxResults: 3);
  print('  Starts with عبد:');
  for (final r in searchRes) {
    print('    ${r.ar} (${r.en})');
  }

  print('\nAll Dart smoke tests passed successfully!');
}
