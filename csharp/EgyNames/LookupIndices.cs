using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace EgyptianNames
{
    public static class LookupIndices
    {
        private static bool _built = false;
        private static readonly object _lock = new object();

        private static readonly Dictionary<string, NameEntry> _arIndex = new Dictionary<string, NameEntry>(StringComparer.Ordinal);
        private static readonly Dictionary<string, NameEntry> _enIndex = new Dictionary<string, NameEntry>(StringComparer.OrdinalIgnoreCase);
        private static readonly Dictionary<string, NameEntry> _arNormIndex = new Dictionary<string, NameEntry>(StringComparer.Ordinal);
        private static readonly Dictionary<string, string> _correctionIndex = new Dictionary<string, string>(StringComparer.Ordinal);
        private static List<NameEntry> _allEntries = new List<NameEntry>();
        private static List<NameEntry> _rankedEntries = new List<NameEntry>();

        private static readonly Regex TashkeelRegex = new Regex(@"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]", RegexOptions.Compiled);
        private static readonly Regex TatweelRegex = new Regex(@"\u0640", RegexOptions.Compiled);
        private static readonly Regex AlefVariantsRegex = new Regex(@"[\u0622\u0623\u0625\u0671]", RegexOptions.Compiled);
        private static readonly Regex IsArabicRegex = new Regex(@"[\u0600-\u06FF\uFE70-\uFEFF]", RegexOptions.Compiled);

        public static string NormalizeAr(string text)
        {
            if (string.IsNullOrEmpty(text)) return string.Empty;
            var s = TashkeelRegex.Replace(text, "");
            s = TatweelRegex.Replace(s, "");
            s = AlefVariantsRegex.Replace(s, "\u0627");
            s = s.Replace('\u0649', '\u064A'); // ى -> ي
            s = s.Replace('\u0629', '\u0647'); // ة -> ه
            return s;
        }

        public static string NormalizeEn(string text)
        {
            if (string.IsNullOrEmpty(text)) return string.Empty;
            return text.ToLowerInvariant().Replace("-", "").Replace("'", "").Trim();
        }

        public static bool IsArabic(string text)
        {
            return !string.IsNullOrEmpty(text) && IsArabicRegex.IsMatch(text);
        }

        public static void EnsureBuilt(string? dataPath = null)
        {
            if (_built) return;

            lock (_lock)
            {
                if (_built) return;

                var bundle = DataLoader.LoadBundle(dataPath);
                _allEntries = bundle.Names;

                foreach (var entry in _allEntries)
                {
                    // AR
                    if (!_arIndex.ContainsKey(entry.Ar)) _arIndex[entry.Ar] = entry;
                    var normAr = NormalizeAr(entry.Ar);
                    if (!_arNormIndex.ContainsKey(normAr)) _arNormIndex[normAr] = entry;

                    foreach (var v in entry.ArVariants)
                    {
                        var stripped = v.Trim();
                        if (!string.IsNullOrEmpty(stripped))
                        {
                            if (!_arIndex.ContainsKey(stripped)) _arIndex[stripped] = entry;
                            var normV = NormalizeAr(stripped);
                            if (!_arNormIndex.ContainsKey(normV)) _arNormIndex[normV] = entry;
                        }
                    }

                    // EN
                    var normEn = NormalizeEn(entry.En);
                    if (!_enIndex.ContainsKey(normEn)) _enIndex[normEn] = entry;

                    foreach (var v in entry.EnVariants)
                    {
                        var stripped = v.Trim();
                        if (!string.IsNullOrEmpty(stripped))
                        {
                            var normV = NormalizeEn(stripped);
                            if (!_enIndex.ContainsKey(normV)) _enIndex[normV] = entry;
                        }
                    }
                }

                foreach (var kvp in bundle.Corrections)
                {
                    _correctionIndex[kvp.Key] = kvp.Value;
                }

                _rankedEntries = _allEntries.OrderByDescending(e => e.CorpusShare).ToList();
                _built = true;
            }
        }

        public static NameEntry? LookupAr(string name, string? dataPath = null)
        {
            EnsureBuilt(dataPath);
            if (string.IsNullOrWhiteSpace(name)) return null;
            string trimmed = name.Trim();

            // 1. Direct match
            if (_arIndex.TryGetValue(trimmed, out var entry)) return entry;

            // 2. Normalized match
            string norm = NormalizeAr(trimmed);
            if (_arNormIndex.TryGetValue(norm, out entry)) return entry;

            // 3. Alif / Alif Maqsura terminal phonetic equivalence
            if (norm.EndsWith("\u0627"))
            {
                string alt = norm.Substring(0, norm.Length - 1) + "\u064A";
                if (_arNormIndex.TryGetValue(alt, out var altEntry)) return altEntry;
            }
            else if (norm.EndsWith("\u064A"))
            {
                string alt = norm.Substring(0, norm.Length - 1) + "\u0627";
                if (_arNormIndex.TryGetValue(alt, out var altEntry)) return altEntry;
            }

            // 4. Space-less compound match
            string noSpace = trimmed.Replace(" ", "");
            if (noSpace != trimmed)
            {
                if (_arIndex.TryGetValue(noSpace, out var noSpaceEntry)) return noSpaceEntry;
                if (_arNormIndex.TryGetValue(NormalizeAr(noSpace), out var noSpaceNormEntry)) return noSpaceNormEntry;
            }

            return null;
        }

        public static NameEntry? LookupEn(string name, string? dataPath = null)
        {
            EnsureBuilt(dataPath);
            if (_enIndex.TryGetValue(NormalizeEn(name), out var entry)) return entry;
            return null;
        }

        public static NameEntry? Lookup(string name, string? dataPath = null)
        {
            EnsureBuilt(dataPath);
            return IsArabic(name) ? LookupAr(name, dataPath) : LookupEn(name, dataPath);
        }

        public static string? GetCorrection(string surface, string? dataPath = null)
        {
            EnsureBuilt(dataPath);
            return _correctionIndex.TryGetValue(surface, out var canonical) ? canonical : null;
        }

        public static IReadOnlyList<NameEntry> GetAll(string? dataPath = null)
        {
            EnsureBuilt(dataPath);
            return _allEntries;
        }

        public static IReadOnlyList<NameEntry> GetRanked(string? dataPath = null)
        {
            EnsureBuilt(dataPath);
            return _rankedEntries;
        }

        public static IReadOnlyDictionary<string, NameEntry> GetArForms(string? dataPath = null)
        {
            EnsureBuilt(dataPath);
            return _arIndex;
        }

        public static IReadOnlyDictionary<string, NameEntry> GetArNormForms(string? dataPath = null)
        {
            EnsureBuilt(dataPath);
            return _arNormIndex;
        }
    }
}
