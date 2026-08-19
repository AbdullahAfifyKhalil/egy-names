/**
 * Egyptian Names (egy-names) TypeScript / Node.js Demo
 * Run: npm install egy-names && npx ts-node demo.ts
 */

import { EgyptianNames } from 'egy-names';

async function main() {
  const en = new EgyptianNames();

  console.log('='.repeat(60));
  console.log(' Egyptian Names (egy-names) - TypeScript Showcase');
  console.log('='.repeat(60));

  // 1. Generation
  console.log('\n1. Name Generation:');
  const names = en.generate({ count: 3, length: 3, gender: 'female' });
  names.forEach(n => console.log(`   ${n.ar}  (${n.en})`));

  // 2. Translation
  console.log('\n2. Transliteration:');
  console.log(`   'محمد أحمد علي' -> ${en.translate('محمد أحمد علي')}`);

  // 3. Correction
  console.log('\n3. Orthographic Correction:');
  console.log(`   'احمد مصطفا عبد الرحيم' -> ${en.correct('احمد مصطفا عبد الرحيم')}`);

  // 4. Tashkeel
  console.log('\n4. Tashkeel:');
  console.log(`   'محمد عبدالرحمن' -> ${en.tashkeel('محمد عبدالرحمن')}`);

  // 5. Splitting
  console.log('\n5. Splitting concatenated Arabic:');
  console.log(`   'محمدأحمدعليحسن' -> ${JSON.stringify(en.split('محمدأحمدعليحسن'))}`);

  // 6. Chain Analysis
  console.log('\n6. Patronymic Chain:');
  en.analyzeChain('محمد أحمد علي حسن الشاذلي').forEach(p => {
    console.log(`   Slot ${p.slot}: ${p.name} - ${p.detail}`);
  });
}

main();
