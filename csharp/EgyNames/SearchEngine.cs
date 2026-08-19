using System;
using System.Collections.Generic;
using System.Linq;

namespace EgyptianNames
{
    public static class SearchEngine
    {
        public static List<NameInfo> Search(
            Gender? gender = null,
            Religion? religion = null,
            NameRole? role = null,
            FrequencyClass? frequency = null,
            string? startsWith = null,
            string? endsWith = null,
            string? contains = null,
            double? minCorpusShare = null,
            int maxResults = 50,
            string sortBy = "corpus_share",
            string? dataPath = null)
        {
            var entries = LookupIndices.GetAll(dataPath);

            bool prefixAr = startsWith != null && LookupIndices.IsArabic(startsWith);
            bool suffixAr = endsWith != null && LookupIndices.IsArabic(endsWith);
            bool containsAr = contains != null && LookupIndices.IsArabic(contains);

            var filtered = entries.Where(e =>
            {
                if (gender.HasValue && e.Gender != gender.Value && e.Gender != Gender.Neutral) return false;
                if (religion.HasValue && e.Religion != religion.Value && e.Religion != Religion.Neutral) return false;
                if (role.HasValue && e.Role != role.Value) return false;
                if (frequency.HasValue && e.Frequency != frequency.Value) return false;
                if (minCorpusShare.HasValue && e.CorpusShare < minCorpusShare.Value) return false;

                if (!string.IsNullOrEmpty(startsWith))
                {
                    if (prefixAr)
                    {
                        if (!LookupIndices.NormalizeAr(e.Ar).StartsWith(LookupIndices.NormalizeAr(startsWith))) return false;
                    }
                    else
                    {
                        if (!LookupIndices.NormalizeEn(e.En).StartsWith(LookupIndices.NormalizeEn(startsWith))) return false;
                    }
                }

                if (!string.IsNullOrEmpty(endsWith))
                {
                    if (suffixAr)
                    {
                        if (!LookupIndices.NormalizeAr(e.Ar).EndsWith(LookupIndices.NormalizeAr(endsWith))) return false;
                    }
                    else
                    {
                        if (!LookupIndices.NormalizeEn(e.En).EndsWith(LookupIndices.NormalizeEn(endsWith))) return false;
                    }
                }

                if (!string.IsNullOrEmpty(contains))
                {
                    if (containsAr)
                    {
                        if (!LookupIndices.NormalizeAr(e.Ar).Contains(LookupIndices.NormalizeAr(contains))) return false;
                    }
                    else
                    {
                        if (!LookupIndices.NormalizeEn(e.En).Contains(LookupIndices.NormalizeEn(contains))) return false;
                    }
                }

                return true;
            }).ToList();

            if (sortBy.Equals("alphabetical", StringComparison.OrdinalIgnoreCase))
            {
                filtered = filtered.OrderBy(e => e.Ar, StringComparer.Ordinal).ToList();
            }
            else
            {
                filtered = filtered.OrderByDescending(e => e.CorpusShare).ToList();
            }

            return filtered.Take(maxResults).Select(NameInfo.FromEntry).ToList();
        }
    }
}
