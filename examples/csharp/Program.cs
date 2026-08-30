using System;
using System.Linq;
using EgyptianNames;

namespace EgyNamesExample
{
    class Program
    {
        static void Main(string[] args)
        {
            var en = new EgyptianNamesEngine();

            Console.WriteLine("============================================================");
            Console.WriteLine(" Egyptian Names (egy-names) 0.3.6 — .NET / C#");
            Console.WriteLine("============================================================");

            Console.WriteLine("\n1. Generate a grounded chain:");
            foreach (var n in en.Generate(count: 3, length: 4, gender: Gender.Female, religion: Religion.Muslim))
            {
                Console.WriteLine($"   {n.Ar}  ({n.En})");
            }

            Console.WriteLine("\n2. Translate:");
            Console.WriteLine($"   {en.Translate("محمد أحمد علي الشناوي")}");

            Console.WriteLine("\n3. Correct:");
            Console.WriteLine($"   {en.Correct("احمد مصطفا عبد الرحيم")}");

            Console.WriteLine("\n4. Tashkeel and IPA:");
            Console.WriteLine($"   Standard: {en.Tashkeel("محمد عبدالرحمن")}");
            Console.WriteLine($"   Egyptian: {en.TashkeelEg("محمد عبدالرحمن")}");
            Console.WriteLine($"   IPA std:  {en.Ipa("جمال")}");
            Console.WriteLine($"   IPA eg:   {en.IpaEg("جمال")}");

            Console.WriteLine("\n5. Split a concatenated dump:");
            Console.WriteLine($"   [{string.Join(", ", en.Split("محمدأحمدعليحسنالشناوي"))}]");

            Console.WriteLine("\n6. Pet names and figures:");
            Console.WriteLine($"   dallaa: [{string.Join(", ", en.Dallaa("محمد", "tashkeel"))}]");
            Console.WriteLine($"   figures: {string.Join(" | ", en.FamousFigures("محمد", "en").Take(2))}");

            Console.WriteLine("\n7. Lookup:");
            Console.WriteLine($"   root={en.Root("محمد")} | origin={en.Origin("محمد")} | trend={en.Trend("محمد")}");
            var meaning = en.Meaning("محمد");
            if (meaning.HasValue)
            {
                Console.WriteLine($"   meaning: {meaning.Value.En}");
            }

            Console.WriteLine("\n8. Validity — personal names only:");
            Console.WriteLine($"   IsValid(\"محمد\")  = {en.IsValid("محمد")}");
            Console.WriteLine($"   IsValid(\"Mahmoud\") = {en.IsValid("Mahmoud")}");
            Console.WriteLine($"   IsValid(\"الله\")   = {en.IsValid("الله")}  // in the index, not a person");

            Console.WriteLine("\n9. First personal token wins:");
            Console.WriteLine($"   {en.DetectGender("فاطمة محمد علي")}");
            Console.WriteLine($"   {en.DetectReligion("مينا جرجس بطرس")}");

            Console.WriteLine("\n10. Chain, rank, uniqueness:");
            foreach (var p in en.AnalyzeChain("محمد أحمد علي الشناوي"))
            {
                Console.WriteLine($"   Slot {p.Slot}: {p.Name} — {p.Role}");
            }
            var rank = en.Rank("محمد");
            var uniq = en.Uniqueness("محمد أحمد علي الشناوي");
            Console.WriteLine($"   rank=#{rank?.Rank}  uniqueness={uniq.Score} ({uniq.Label})");
        }
    }
}
