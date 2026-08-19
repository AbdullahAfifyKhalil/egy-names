using System;
using System.Linq;

namespace EgyptianNames
{
    public static class Translator
    {
        public static string TranslateToken(string token, string? to = null, string? dataPath = null)
        {
            bool srcIsAr = LookupIndices.IsArabic(token);
            string target = to ?? (srcIsAr ? "en" : "ar");

            if (target.Equals("en", StringComparison.OrdinalIgnoreCase))
            {
                var entry = LookupIndices.LookupAr(token, dataPath);
                return entry != null ? entry.En : token;
            }
            else
            {
                var entry = LookupIndices.LookupEn(token, dataPath);
                return entry != null ? entry.Ar : token;
            }
        }

        public static string Translate(string fullName, string? to = null, string? dataPath = null)
        {
            if (string.IsNullOrWhiteSpace(fullName)) return fullName;
            var tokens = fullName.Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            var translated = tokens.Select(t => TranslateToken(t, to, dataPath));
            return string.Join(" ", translated);
        }
    }
}
