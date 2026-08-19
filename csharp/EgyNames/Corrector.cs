using System;
using System.Collections.Generic;
using System.Linq;

namespace EgyptianNames
{
    public static class Corrector
    {
        public static string CorrectToken(string token, string? dataPath = null)
        {
            if (string.IsNullOrWhiteSpace(token)) return token;
            string t = token.Trim();

            // 1. Direct surface correction pair
            string? canonical = LookupIndices.GetCorrection(t, dataPath);
            if (canonical != null) return canonical;

            // 2. Exact match in arabic index (including phonetic variants)
            var entry = LookupIndices.LookupAr(t, dataPath);
            if (entry != null) return entry.Ar;

            // 3. Normalized form lookup
            string norm = LookupIndices.NormalizeAr(t);
            var arNorm = LookupIndices.GetArNormForms(dataPath);
            if (arNorm.TryGetValue(norm, out var normEntry)) return normEntry.Ar;

            // 4. Trailing Alif / Alif Maqsura check
            if (norm.EndsWith("\u0627"))
            {
                string alt = norm.Substring(0, norm.Length - 1) + "\u064A";
                if (arNorm.TryGetValue(alt, out var altMatch)) return altMatch.Ar;
            }
            else if (norm.EndsWith("\u064A"))
            {
                string alt = norm.Substring(0, norm.Length - 1) + "\u0627";
                if (arNorm.TryGetValue(alt, out var altMatch)) return altMatch.Ar;
            }

            return t;
        }

        public static string Correct(string name, string? dataPath = null)
        {
            if (string.IsNullOrWhiteSpace(name)) return name;
            var tokens = name.Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            var result = new List<string>();

            for (int i = 0; i < tokens.Length; i++)
            {
                string current = tokens[i];

                // Check compound pair (e.g. "عبد" + "الرحيم" -> "عبدالرحيم")
                if (i < tokens.Length - 1)
                {
                    string next = tokens[i + 1];
                    string compound = $"{current} {next}";
                    string compoundNoSpace = $"{current}{next}";

                    var compoundEntry = LookupIndices.LookupAr(compound, dataPath) ?? LookupIndices.LookupAr(compoundNoSpace, dataPath);
                    if (compoundEntry != null)
                    {
                        result.Add(compoundEntry.Ar);
                        i++; // skip second part
                        continue;
                    }
                }

                result.Add(CorrectToken(current, dataPath));
            }

            return string.Join(" ", result);
        }
    }
}
