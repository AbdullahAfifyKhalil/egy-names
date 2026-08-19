using System;
using EgyNames;

namespace EgyNamesExample
{
    class Program
    {
        static void Main(string[] args)
        {
            var en = new EgyptianNames();

            Console.WriteLine("============================================================");
            Console.WriteLine(" Egyptian Names (egy-names) - .NET / C# Showcase");
            Console.WriteLine("============================================================");

            // 1. Generation
            Console.WriteLine("\n1. Realistic Name Generation:");
            var names = en.Generate(count: 3, length: 3, gender: "male", religion: "muslim");
            foreach (var n in names)
            {
                Console.WriteLine($"   {n.Ar}  --  {n.En}");
            }

            // 2. Translation
            Console.WriteLine("\n2. Transliteration:");
            Console.WriteLine($"   'محمد أحمد علي' -> {en.Translate("محمد أحمد علي")}");

            // 3. Correction
            Console.WriteLine("\n3. Orthographic Correction:");
            Console.WriteLine($"   'احمد مصطفا عبد الرحيم' -> {en.Correct("احمد مصطفا عبد الرحيم")}");

            // 4. Tashkeel
            Console.WriteLine("\n4. Tashkeel:");
            Console.WriteLine($"   'محمد عبدالرحمن' -> {en.Tashkeel("محمد عبدالرحمن")}");

            // 5. Splitting unspaced name
            Console.WriteLine("\n5. Concatenated Name Segmentation:");
            var parts = en.Split("محمدأحمدعليحسنالشاذلي");
            Console.WriteLine($"   'محمدأحمدعليحسنالشاذلي' -> [{string.Join(", ", parts)}]");
        }
    }
}
