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
            Console.WriteLine(" Egyptian Names (egy-names) v0.3.2 — .NET / C# Showcase");
            Console.WriteLine("============================================================");

            Console.WriteLine("\n1. Name Generation:");
            foreach (var n in en.Generate(count: 3, length: 4, gender: Gender.Female, religion: Religion.Muslim))
            {
                Console.WriteLine($"   {n.Ar}  ({n.En})");
            }

            Console.WriteLine("\n2. Transliteration:");
            Console.WriteLine($"   'محمد أحمد علي الشناوي' -> {en.Translate("محمد أحمد علي الشناوي")}");

            Console.WriteLine("\n3. Orthographic Correction:");
            Console.WriteLine($"   'احمد مصطفا عبد الرحيم' -> {en.Correct("احمد مصطفا عبد الرحيم")}");

            Console.WriteLine("\n4. Dual Tashkeel & IPA:");
            Console.WriteLine($"   Standard: {en.Tashkeel("محمد عبدالرحمن")}");
            Console.WriteLine($"   Egyptian: {en.TashkeelEg("محمد عبدالرحمن")}");
            Console.WriteLine($"   IPA std:  {en.Ipa("جمال")}");
            Console.WriteLine($"   IPA eg:   {en.IpaEg("جمال")}");

            Console.WriteLine("\n5. Splitting concatenated names:");
            Console.WriteLine($"   [{string.Join(", ", en.Split("محمدأحمدعليحسنالشناوي"))}]");

            Console.WriteLine("\n6. Pet names & famous figures:");
            Console.WriteLine($"   dallaa: [{string.Join(", ", en.Dallaa("محمد", "tashkeel"))}]");
            Console.WriteLine($"   figures: {string.Join(" | ", en.FamousFigures("محمد", "en").Take(2))}");

            Console.WriteLine("\n7. 14D lookup:");
            Console.WriteLine($"   root={en.Root("محمد")} | origin={en.Origin("محمد")} | trend={en.Trend("محمد")}");
            var meaning = en.Meaning("محمد");
            if (meaning.HasValue)
            {
                Console.WriteLine($"   meaning: {meaning.Value.En}");
            }

            Console.WriteLine("\n8. Demographics:");
            Console.WriteLine($"   {en.DetectGender("فاطمة الزهراء")}");
            Console.WriteLine($"   {en.DetectReligion("مينا جرجس بطرس")}");

            Console.WriteLine("\n9. Chain analysis, rank, uniqueness:");
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
