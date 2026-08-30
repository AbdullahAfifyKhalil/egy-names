using System;
using System.Collections.Generic;

namespace EgyptianNames
{
    /// <summary>
    /// Compound-aware whitespace tokenizer shared by gender/religion detection
    /// and splitting.
    /// </summary>
    public static class NameTokenizer
    {
        /// <summary>
        /// Split on whitespace, but merge an adjacent pair into one lemma when
        /// the book has it as a two-word compound (e.g. kunya "Abu X").
        ///
        /// A handful of book entries are legitimately two words (roughly 800
        /// "Abu X" kunya/family lemmas plus a few compound given names). A
        /// blind whitespace split treats them as two meaningless fragments,
        /// breaking gender/religion detection and split() on names that
        /// contain one. Greedy pairwise lookahead, same approach tashkeel()
        /// already uses for "عبد الرحمن"-style pairs.
        /// </summary>
        public static List<(string Text, NameEntry? Entry)> CompoundTokens(string fullName, string? dataPath = null)
        {
            var result = new List<(string Text, NameEntry? Entry)>();
            if (string.IsNullOrWhiteSpace(fullName)) return result;

            var raw = fullName.Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            int i = 0;
            int n = raw.Length;
            while (i < n)
            {
                if (i < n - 1)
                {
                    var pair = $"{raw[i]} {raw[i + 1]}";
                    var pairEntry = LookupIndices.LookupAr(pair, dataPath) ?? LookupIndices.LookupAr($"{raw[i]}{raw[i + 1]}", dataPath);
                    if (pairEntry != null)
                    {
                        result.Add((pair, pairEntry));
                        i += 2;
                        continue;
                    }
                }
                result.Add((raw[i], LookupIndices.Lookup(raw[i], dataPath)));
                i++;
            }
            return result;
        }
    }
}
