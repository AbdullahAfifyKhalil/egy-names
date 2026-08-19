export function initCodePlayground(showToast: (msg: string) => void): void {
  const codePre = document.getElementById("playground-code") as HTMLElement;
  const copyBtn = document.getElementById("btn-copy-code") as HTMLButtonElement;
  const tabBtns = document.querySelectorAll<HTMLButtonElement>(".code-tab-btn");

  const SNIPPETS: Record<string, string> = {
    python: `# Install: pip install egy-names
from egy_names import EgyNames

# 1. Initialize engine
en = EgyNames()

# 2. Generate authentic Egyptian full names
names = en.generate(count=3, gender="male", religion="muslim", family_name=True)
for n in names:
    print(f"{n.ar}  --  {n.en}")

# 3. Translation
print(en.translate("محمد أحمد علي"))  # Mohamed Ahmed Ali

# 4. Intelligent space-less splitting (DP segmentation)
tokens = en.split("محمدأحمدعليحسنالشاذلي")
print(tokens)  # ['محمد', 'أحمد', 'علي', 'حسن', 'الشاذلي']

# 5. Tashkeel & orthographic correction
print(en.correct("احمد"))  # أحمد
print(en.tashkeel("محمد عبدالرحمن"))  # مُحَمَّد عَبْدُالرَّحْمَن

# 6. Creative AI inferences
print(en.detect_gender("مريم إبراهيم حسن"))  # female (0.57)
print(en.detect_religion("جورج بطرس سمير ميخائيل"))  # christian (0.75)`,

    typescript: `// Install: npm install egy-names
import { EgyNames } from "egy-names";

// 1. Initialize engine
const en = new EgyNames();

// 2. Generate authentic Egyptian full names
const names = en.generate({ count: 3, gender: "male", religion: "muslim", familyName: true });
for (const n of names) {
  console.log(\`\${n.ar}  --  \${n.en}\`);
}

// 3. Translation
console.log(en.translate("محمد أحمد علي")); // Mohamed Ahmed Ali

// 4. Intelligent space-less splitting (DP segmentation)
console.log(en.split("محمدأحمدعليحسنالشاذلي"));
// -> ['محمد', 'أحمد', 'علي', 'حسن', 'الشاذلي']

// 5. Tashkeel & orthographic correction
console.log(en.correct("احمد")); // أحمد
console.log(en.tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن

// 6. Creative AI inferences
console.log(en.detectGender("مريم إبراهيم حسن"));
console.log(en.detectReligion("جورج بطرس سمير ميخائيل"));`,

    dart: `// Install: dart pub add egy_names
import 'package:egy_names/egy_names.dart';

void main() {
  // 1. Initialize engine
  final en = EgyNames();

  // 2. Generate authentic Egyptian full names
  final names = en.generate(count: 3, gender: 'male', religion: 'muslim');
  for (final n in names) {
    print('\${n.ar}  --  \${n.en}');
  }

  // 3. Translation
  print(en.translate('محمد أحمد علي')); // Mohamed Ahmed Ali

  // 4. Intelligent space-less splitting (DP segmentation)
  print(en.split('محمدأحمدعليحسنالشاذلي'));
  // -> ['محمد', 'أحمد', 'علي', 'حسن', 'الشاذلي']

  // 5. Tashkeel & orthographic correction
  print(en.correct('احمد')); // أحمد
  print(en.tashkeel('محمد عبدالرحمن')); // مُحَمَّد عَبْدُالرَّحْمَن

  // 6. Creative AI inferences
  print(en.detectGender('مريم إبراهيم حسن'));
  print(en.detectReligion('جورج بطرس سمير ميخائيل'));
}`,

    csharp: `// Install: dotnet add package egy-names
using EgyNames;

// 1. Initialize engine
var en = new EgyNamesEngine();

// 2. Generate authentic Egyptian full names
var names = en.Generate(count: 3, gender: Gender.Male, religion: Religion.Muslim);
foreach (var n in names) {
    Console.WriteLine($"\${n.Ar}  --  \${n.En}");
}

// 3. Translation
Console.WriteLine(en.Translate("محمد أحمد علي")); // Mohamed Ahmed Ali

// 4. Intelligent space-less splitting (DP segmentation)
var tokens = en.Split("محمدأحمدعليحسنالشاذلي");
Console.WriteLine(string.Join(", ", tokens));

// 5. Tashkeel & orthographic correction
Console.WriteLine(en.Correct("احمد")); // أحمد
Console.WriteLine(en.Tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن

// 6. Creative AI inferences
Console.WriteLine(en.DetectGender("مريم إبراهيم حسن"));
Console.WriteLine(en.DetectReligion("جورج بطرس سمير ميخائيل"));`,

    java: `// Maven: <dependency><groupId>com.afify</groupId><artifactId>egy-names</artifactId><version>0.1.0</version></dependency>
import com.afify.egynames.EgyNames;

public class App {
    public static void main(String[] args) {
        // 1. Initialize engine
        EgyNames en = new EgyNames();

        // 2. Generate authentic Egyptian full names
        var names = en.generate(3, "male", "muslim");
        for (var n : names) {
            System.out.println(n.ar + "  --  " + n.en);
        }

        // 3. Translation
        System.out.println(en.translate("محمد أحمد علي")); // Mohamed Ahmed Ali

        // 4. Intelligent space-less splitting (DP segmentation)
        System.out.println(en.split("محمدأحمدعليحسنالشاذلي"));

        // 5. Tashkeel & orthographic correction
        System.out.println(en.correct("احمد")); // أحمد
        System.out.println(en.tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن

        // 6. Creative AI inferences
        System.out.println(en.detectGender("مريم إبراهيم حسن"));
        System.out.println(en.detectReligion("جورج بطرس سمير ميخائيل"));
    }
}`,
  };

  let currentLang = "python";

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentLang = btn.dataset.lang || "python";
      if (codePre) {
        codePre.textContent = SNIPPETS[currentLang] || "";
      }
    });
  });

  copyBtn?.addEventListener("click", () => {
    const code = codePre?.textContent;
    if (code) {
      navigator.clipboard.writeText(code);
      showToast(`Copied ${currentLang.toUpperCase()} snippet to clipboard!`);
    }
  });

  // Initial
  if (codePre) {
    codePre.textContent = SNIPPETS["python"];
  }
}
