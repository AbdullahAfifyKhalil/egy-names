using System;
using System.Collections.Generic;
using System.Linq;

namespace EgyptianNames
{
    public static class Generator
    {
        private const int DefaultMinLen = 4;
        private const int DefaultMaxLen = 5;

        private static List<NameEntry> FilterEntries(
            IEnumerable<NameEntry> entries,
            Gender? gender = null,
            Religion? religion = null,
            NameRole? role = null,
            FrequencyClass? frequency = null)
        {
            return entries.Where(e =>
            {
                if (gender.HasValue && e.Gender != gender.Value && e.Gender != Gender.Neutral) return false;
                if (religion.HasValue && e.Religion != religion.Value && e.Religion != Religion.Neutral) return false;
                if (role.HasValue && e.Role != role.Value) return false;
                if (frequency.HasValue && e.Frequency != frequency.Value) return false;
                return true;
            }).ToList();
        }

        private static NameEntry WeightedPick(List<NameEntry> entries, int slotIdx, Random rng)
        {
            var candidates = new List<NameEntry>();
            var weights = new List<double>();
            double totalWeight = 0.0;

            foreach (var e in entries)
            {
                double w = (slotIdx < e.SlotPcts.Count ? e.SlotPcts[slotIdx] : 0.0) * e.CorpusShare;
                if (w > 0)
                {
                    candidates.Add(e);
                    weights.Add(w);
                    totalWeight += w;
                }
            }

            if (candidates.Count == 0)
            {
                foreach (var e in entries)
                {
                    double w = Math.Max(e.CorpusShare, 1e-9);
                    candidates.Add(e);
                    weights.Add(w);
                    totalWeight += w;
                }
            }

            double r = rng.NextDouble() * totalWeight;
            for (int i = 0; i < candidates.Count; i++)
            {
                r -= weights[i];
                if (r <= 0) return candidates[i];
            }

            return candidates[candidates.Count - 1];
        }

        public static List<GeneratedName> Generate(
            int count = 1,
            Gender? gender = null,
            Religion? religion = null,
            int? length = null,
            bool familyName = true,
            FrequencyClass? frequency = null,
            int? seed = null,
            string? dataPath = null)
        {
            var rng = seed.HasValue ? new Random(seed.Value) : new Random();
            var allEntries = LookupIndices.GetAll(dataPath);

            var firstPool = FilterEntries(allEntries, gender, religion, NameRole.Given, frequency);
            var patronPool = FilterEntries(allEntries, Gender.Male, religion, NameRole.Given, frequency);
            var familyPool = FilterEntries(allEntries, null, religion, NameRole.Family, frequency);

            if (firstPool.Count == 0) firstPool = FilterEntries(allEntries, gender, role: NameRole.Given);
            if (patronPool.Count == 0) patronPool = FilterEntries(allEntries, Gender.Male, role: NameRole.Given);
            if (familyPool.Count == 0) familyPool = FilterEntries(allEntries, role: NameRole.Family);

            var results = new List<GeneratedName>();

            for (int c = 0; c < count; c++)
            {
                int chainLen = length ?? rng.Next(DefaultMinLen, DefaultMaxLen + 1);
                var partsAr = new List<string>();
                var partsEn = new List<string>();
                var seen = new HashSet<string>(StringComparer.Ordinal);

                // Slot 1
                var entry = WeightedPick(firstPool, 0, rng);
                int attempts = 0;
                while (seen.Contains(entry.Ar) && attempts < 20)
                {
                    entry = WeightedPick(firstPool, 0, rng);
                    attempts++;
                }
                partsAr.Add(entry.Ar);
                partsEn.Add(entry.En);
                seen.Add(entry.Ar);

                // Patronymic slots 2 .. (N-1 or N)
                int patronEnd = familyName ? chainLen - 1 : chainLen;
                for (int slot = 1; slot < patronEnd; slot++)
                {
                    int slotIdx = Math.Min(slot, 7);
                    entry = WeightedPick(patronPool, slotIdx, rng);
                    attempts = 0;
                    while (seen.Contains(entry.Ar) && attempts < 20)
                    {
                        entry = WeightedPick(patronPool, slotIdx, rng);
                        attempts++;
                    }
                    partsAr.Add(entry.Ar);
                    partsEn.Add(entry.En);
                    seen.Add(entry.Ar);
                }

                // Family name slot
                if (familyName && chainLen > 1)
                {
                    int slotIdx = Math.Min(chainLen - 1, 7);
                    entry = WeightedPick(familyPool, slotIdx, rng);
                    attempts = 0;
                    while (seen.Contains(entry.Ar) && attempts < 20)
                    {
                        entry = WeightedPick(familyPool, slotIdx, rng);
                        attempts++;
                    }
                    partsAr.Add(entry.Ar);
                    partsEn.Add(entry.En);
                }

                results.Add(new GeneratedName
                {
                    Ar = string.Join(" ", partsAr),
                    En = string.Join(" ", partsEn),
                    PartsAr = partsAr,
                    PartsEn = partsEn
                });
            }

            return results;
        }
    }
}
