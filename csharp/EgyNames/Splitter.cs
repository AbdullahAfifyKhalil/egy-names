using System;
using System.Collections.Generic;
using System.Linq;

namespace EgyptianNames
{
    public static class Splitter
    {
        private const double BaseSegmentCost = 1.0;
        private const double UnknownPenalty = 8.0;
        private const double LengthBonusPerChar = -0.05;

        private static readonly Dictionary<FrequencyClass, double> FreqBonus = new Dictionary<FrequencyClass, double>
        {
            { FrequencyClass.Common, -0.6 },
            { FrequencyClass.Normal, -0.2 },
            { FrequencyClass.Rare, 0.0 }
        };

        private static List<string> DpSegment(string text, string? dataPath = null)
        {
            var arIndex = LookupIndices.GetArForms(dataPath);
            var arNorm = LookupIndices.GetArNormForms(dataPath);

            int n = text.Length;
            var dpCost = new double[n + 1];
            var dpPrev = new int[n + 1];
            var dpKnown = new bool[n + 1];

            for (int i = 0; i <= n; i++)
            {
                dpCost[i] = double.PositiveInfinity;
                dpPrev[i] = -1;
                dpKnown[i] = false;
            }

            dpCost[0] = 0.0;
            dpPrev[0] = 0;
            dpKnown[0] = true;

            for (int i = 1; i <= n; i++)
            {
                int startJ = i > 30 ? i - 30 : 0;
                for (int j = startJ; j < i; j++)
                {
                    if (double.IsPositiveInfinity(dpCost[j])) continue;

                    string substr = text.Substring(j, i - j);
                    if (substr.Length < 2 && j > 0) continue;

                    if (!arIndex.TryGetValue(substr, out var entry))
                    {
                        arNorm.TryGetValue(LookupIndices.NormalizeAr(substr), out entry);
                    }

                    if (entry != null)
                    {
                        double bonus = FreqBonus.TryGetValue(entry.Frequency, out var fb) ? fb : 0.0;
                        double cost = dpCost[j] + BaseSegmentCost + bonus + LengthBonusPerChar * substr.Length;
                        if (cost < dpCost[i])
                        {
                            dpCost[i] = cost;
                            dpPrev[i] = j;
                            dpKnown[i] = true;
                        }
                    }
                    else
                    {
                        double cost = dpCost[j] + UnknownPenalty + substr.Length;
                        if (cost < dpCost[i])
                        {
                            dpCost[i] = cost;
                            dpPrev[i] = j;
                            dpKnown[i] = false;
                        }
                    }
                }
            }

            if (double.IsPositiveInfinity(dpCost[n]))
            {
                return new List<string> { text };
            }

            var segments = new List<string>();
            int pos = n;
            while (pos > 0)
            {
                int prev = dpPrev[pos];
                segments.Add(text.Substring(prev, pos - prev));
                pos = prev;
            }

            segments.Reverse();
            return segments;
        }

        public static List<string> Split(string fullName, string? dataPath = null)
        {
            if (string.IsNullOrWhiteSpace(fullName)) return new List<string>();

            string text = fullName.Trim();

            // If spaces exist, use simple whitespace splitting, but keep a
            // two-word compound lemma (e.g. kunya "Abu X") as one part instead
            // of two meaningless fragments.
            if (text.Contains(" "))
            {
                var raw = text.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                var outList = new List<string>();
                int i = 0;
                int n = raw.Length;
                while (i < n)
                {
                    if (i < n - 1)
                    {
                        var pair = $"{raw[i]} {raw[i + 1]}";
                        if (LookupIndices.LookupAr(pair, dataPath) != null || LookupIndices.LookupAr($"{raw[i]}{raw[i + 1]}", dataPath) != null)
                        {
                            outList.Add(pair);
                            i += 2;
                            continue;
                        }
                    }
                    outList.Add(raw[i]);
                    i++;
                }
                return outList;
            }

            if (LookupIndices.IsArabic(text))
            {
                var entry = LookupIndices.Lookup(text, dataPath);
                if (entry != null)
                {
                    return new List<string> { text };
                }
                return DpSegment(text, dataPath);
            }

            return new List<string> { text };
        }
    }
}
