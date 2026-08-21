using System;
using System.Collections.Generic;
using System.Linq;

namespace EgyptianNames
{
    public class EgyptianNamesEngine
    {
        private readonly int? _seed;
        private readonly string? _customDataPath;

        public EgyptianNamesEngine(int? seed = null, string? customDataPath = null)
        {
            _seed = seed;
            _customDataPath = customDataPath;
        }

        // Core Methods

        public List<GeneratedName> Generate(
            int count = 1,
            Gender? gender = null,
            Religion? religion = null,
            int? length = null,
            bool familyName = true,
            FrequencyClass? frequency = null,
            int? seed = null)
        {
            return Generator.Generate(
                count: count,
                gender: gender,
                religion: religion,
                length: length,
                familyName: familyName,
                frequency: frequency,
                seed: seed ?? _seed,
                dataPath: _customDataPath
            );
        }

        public string Translate(string name, string? to = null)
        {
            return Translator.Translate(name, to, _customDataPath);
        }

        public List<NameInfo?> Annotate(string name)
        {
            return Annotator.Annotate(name, _customDataPath);
        }

        public NameInfo? AnnotateSingle(string name)
        {
            return Annotator.AnnotateSingle(name, _customDataPath);
        }

        public List<string> Split(string fullName)
        {
            return Splitter.Split(fullName, _customDataPath);
        }

        public string Tashkeel(string name, string dialect = "standard")
        {
            if (string.IsNullOrWhiteSpace(name)) return name;
            var rawTokens = name.Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            var result = new List<string>();
            bool isEg = dialect.ToLowerInvariant().StartsWith("eg");

            for (int i = 0; i < rawTokens.Length; i++)
            {
                string current = rawTokens[i];

                if (i < rawTokens.Length - 1)
                {
                    string next = rawTokens[i + 1];
                    string compound = $"{current} {next}";
                    string compoundNoSpace = $"{current}{next}";
                    var compoundEntry = LookupIndices.LookupAr(compound, _customDataPath) ?? LookupIndices.LookupAr(compoundNoSpace, _customDataPath);
                    if (compoundEntry != null)
                    {
                        var val = isEg ? compoundEntry.TashkeelEg : compoundEntry.TashkeelStandard;
                        if (!string.IsNullOrEmpty(val))
                        {
                            result.Add(val);
                            i++;
                            continue;
                        }
                    }
                }

                var entry = LookupIndices.LookupAr(current, _customDataPath);
                if (entry != null)
                {
                    var val = isEg ? entry.TashkeelEg : entry.TashkeelStandard;
                    result.Add(!string.IsNullOrEmpty(val) ? val : current);
                }
                else
                {
                    result.Add(current);
                }
            }

            return string.Join(" ", result);
        }

        public string TashkeelEg(string name) => Tashkeel(name, "egyptian");

        public string Ipa(string name, string dialect = "standard")
        {
            if (string.IsNullOrWhiteSpace(name)) return string.Empty;
            var tokens = name.Contains(' ') ? name.Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries).ToList() : Split(name);
            bool isEg = dialect.ToLowerInvariant().StartsWith("eg");
            var ipaParts = new List<string>();

            foreach (var tok in tokens)
            {
                var entry = LookupIndices.Lookup(tok, _customDataPath);
                if (entry != null)
                {
                    var ipaVal = isEg ? entry.IpaEg : entry.IpaStandard;
                    if (!string.IsNullOrEmpty(ipaVal))
                    {
                        ipaParts.Add(ipaVal.Trim('/', '[', ']'));
                    }
                    else
                    {
                        ipaParts.Add(tok);
                    }
                }
                else
                {
                    ipaParts.Add(tok);
                }
            }

            var joined = string.Join(" ", ipaParts);
            return isEg ? $"[{joined}]" : $"/{joined}/";
        }

        public string IpaEg(string name) => Ipa(name, "egyptian");

        public List<string> Dallaa(string name, string format = "plain")
        {
            var entry = LookupIndices.Lookup(name, _customDataPath);
            if (entry == null) return new List<string>();
            var fmt = format.ToLowerInvariant();
            if (fmt == "tashkeel" || fmt == "tashkeel_eg" || fmt == "tk")
            {
                return entry.DallaaTashkeel.Count > 0 ? new List<string>(entry.DallaaTashkeel) : new List<string>(entry.DallaaAr);
            }
            else if (fmt == "en" || fmt == "english")
            {
                return new List<string>(entry.DallaaEn);
            }
            else if (fmt == "ipa" || fmt == "phonetic")
            {
                return new List<string>(entry.DallaaIpa);
            }
            return new List<string>(entry.DallaaAr);
        }

        public List<PetName> DallaaInfo(string name)
        {
            var entry = LookupIndices.Lookup(name, _customDataPath);
            if (entry == null || entry.DallaaAr.Count == 0) return new List<PetName>();
            var result = new List<PetName>();
            for (int i = 0; i < entry.DallaaAr.Count; i++)
            {
                var ar = entry.DallaaAr[i];
                var tk = i < entry.DallaaTashkeel.Count ? entry.DallaaTashkeel[i] : ar;
                var en = i < entry.DallaaEn.Count ? entry.DallaaEn[i] : string.Empty;
                var ipa = i < entry.DallaaIpa.Count ? entry.DallaaIpa[i] : string.Empty;
                result.Add(new PetName(ar, tk, en, ipa));
            }
            return result;
        }

        public List<string> PetNames(string name, string format = "plain") => Dallaa(name, format);

        public string? Root(string name)
        {
            var entry = LookupIndices.Lookup(name, _customDataPath);
            return (entry != null && entry.Root != "N/A") ? entry.Root : null;
        }

        public string? Origin(string name)
        {
            var entry = LookupIndices.Lookup(name, _customDataPath);
            return entry?.OriginType;
        }

        public List<string> FamousFigures(string name, string lang = "ar")
        {
            var entry = LookupIndices.Lookup(name, _customDataPath);
            if (entry == null) return new List<string>();
            if (lang.ToLowerInvariant().StartsWith("en"))
            {
                return entry.FamousFiguresEn.Count > 0 ? new List<string>(entry.FamousFiguresEn) : new List<string>(entry.FamousFiguresAr);
            }
            return new List<string>(entry.FamousFiguresAr);
        }

        public string? Trend(string name)
        {
            var entry = LookupIndices.Lookup(name, _customDataPath);
            return entry?.TrendCategory;
        }

        public string Correct(string name)
        {
            return Corrector.Correct(name, _customDataPath);
        }

        public (string Ar, string En)? Meaning(string name)
        {
            var entry = LookupIndices.Lookup(name, _customDataPath);
            if (entry == null) return null;
            if (string.IsNullOrEmpty(entry.MeaningAr) && string.IsNullOrEmpty(entry.MeaningEn)) return null;
            return (entry.MeaningAr, entry.MeaningEn);
        }

        public List<NameInfo> Families(
            int count = 50,
            FrequencyClass? frequency = null,
            Religion? religion = null,
            string? startsWith = null)
        {
            return SearchEngine.Search(
                role: NameRole.Family,
                maxResults: count,
                frequency: frequency,
                religion: religion,
                startsWith: startsWith,
                dataPath: _customDataPath
            );
        }

        public List<NameInfo> Search(
            Gender? gender = null,
            Religion? religion = null,
            NameRole? role = null,
            FrequencyClass? frequency = null,
            string? startsWith = null,
            string? endsWith = null,
            string? contains = null,
            double? minCorpusShare = null,
            int maxResults = 50,
            string sortBy = "corpus_share")
        {
            return SearchEngine.Search(
                gender: gender,
                religion: religion,
                role: role,
                frequency: frequency,
                startsWith: startsWith,
                endsWith: endsWith,
                contains: contains,
                minCorpusShare: minCorpusShare,
                maxResults: maxResults,
                sortBy: sortBy,
                dataPath: _customDataPath
            );
        }

        // Creative Methods

        public bool IsValid(string name)
        {
            return LookupIndices.Lookup(name, _customDataPath) != null;
        }

        public GenderDetection DetectGender(string fullName)
        {
            if (string.IsNullOrWhiteSpace(fullName))
                return new GenderDetection { Gender = "neutral", Confidence = 0.0 };

            var tokens = fullName.Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            if (tokens.Length == 0)
                return new GenderDetection { Gender = "neutral", Confidence = 0.0 };

            double maleScore = 0;
            double femaleScore = 0;
            double neutralScore = 0;
            double totalWeight = 0;

            for (int i = 0; i < tokens.Length; i++)
            {
                var entry = LookupIndices.Lookup(tokens[i], _customDataPath);
                if (entry == null) continue;

                double w = i == 0 ? 4.0 : (i == 1 ? 2.0 : 1.0);
                totalWeight += w;

                if (entry.Gender == Gender.Male) maleScore += w;
                else if (entry.Gender == Gender.Female) femaleScore += w;
                else neutralScore += w;
            }

            if (totalWeight == 0)
                return new GenderDetection { Gender = "neutral", Confidence = 0.0 };

            double maxScore = Math.Max(maleScore, Math.Max(femaleScore, neutralScore));
            double confidence = maxScore / totalWeight;

            if (maxScore == maleScore) return new GenderDetection { Gender = "male", Confidence = confidence };
            if (maxScore == femaleScore) return new GenderDetection { Gender = "female", Confidence = confidence };
            return new GenderDetection { Gender = "neutral", Confidence = confidence };
        }

        public ReligionDetection DetectReligion(string fullName)
        {
            if (string.IsNullOrWhiteSpace(fullName))
                return new ReligionDetection { Religion = "neutral", Confidence = 0.0 };

            var tokens = fullName.Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            if (tokens.Length == 0)
                return new ReligionDetection { Religion = "neutral", Confidence = 0.0 };

            double muslimScore = 0;
            double christianScore = 0;
            double neutralScore = 0;
            double totalWeight = 0;

            for (int i = 0; i < tokens.Length; i++)
            {
                var entry = LookupIndices.Lookup(tokens[i], _customDataPath);
                if (entry == null) continue;

                double w = 1.0;
                totalWeight += w;

                if (entry.Religion == Religion.Muslim) muslimScore += w;
                else if (entry.Religion == Religion.Christian) christianScore += w;
                else neutralScore += w;
            }

            if (totalWeight == 0)
                return new ReligionDetection { Religion = "neutral", Confidence = 0.0 };

            double maxScore = Math.Max(muslimScore, Math.Max(christianScore, neutralScore));
            double confidence = maxScore / totalWeight;

            if (maxScore == muslimScore) return new ReligionDetection { Religion = "muslim", Confidence = confidence };
            if (maxScore == christianScore) return new ReligionDetection { Religion = "christian", Confidence = confidence };
            return new ReligionDetection { Religion = "neutral", Confidence = confidence };
        }

        public RankInfo? Rank(string name)
        {
            var entry = LookupIndices.Lookup(name, _customDataPath);
            if (entry == null) return null;

            var ranked = LookupIndices.GetRanked(_customDataPath);
            int total = ranked.Count;

            for (int i = 0; i < total; i++)
            {
                if (ranked[i].Ar == entry.Ar)
                {
                    int rankPos = i + 1;
                    double percentile = (1.0 - (double)(rankPos - 1) / total) * 100.0;
                    string desc = $"The #{rankPos} most common name in the Egyptian corpus";
                    if (rankPos <= 10) desc = $"Top 10 — {desc}";
                    else if (rankPos <= 100) desc = $"Top 100 — {desc}";
                    else if (rankPos <= 1000) desc = $"Top 1000 — {desc}";

                    return new RankInfo
                    {
                        Rank = rankPos,
                        Percentile = Math.Round(percentile, 2),
                        CorpusShare = $"{entry.CorpusShare:F4}%",
                        Description = desc
                    };
                }
            }
            return null;
        }

        public List<ChainPart> AnalyzeChain(string fullName)
        {
            if (string.IsNullOrWhiteSpace(fullName)) return new List<ChainPart>();

            var tokens = fullName.Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            var parts = new List<ChainPart>();
            int n = tokens.Length;

            for (int i = 0; i < n; i++)
            {
                string t = tokens[i];
                var entry = LookupIndices.Lookup(t, _customDataPath);
                int slot = i + 1;

                string roleLabel = "";
                string detail = "";

                if (i == 0)
                {
                    roleLabel = "person";
                    detail = "The individual's given name";
                }
                else if (i == n - 1 && entry != null && entry.Role == NameRole.Family)
                {
                    roleLabel = "family_name";
                    detail = "Family/tribal surname";
                }
                else if (i == 1)
                {
                    roleLabel = "father";
                    detail = "Father's name";
                }
                else if (i == 2)
                {
                    roleLabel = "grandfather";
                    detail = "Paternal grandfather";
                }
                else if (i == 3)
                {
                    roleLabel = "great_grandfather";
                    detail = "Great-grandfather";
                }
                else
                {
                    roleLabel = "ancestor";
                    detail = $"Ancestor (generation {i})";
                }

                parts.Add(new ChainPart
                {
                    Name = t,
                    Slot = slot,
                    Role = roleLabel,
                    Detail = detail
                });
            }

            return parts;
        }

        public UniquenessScore Uniqueness(string fullName)
        {
            if (string.IsNullOrWhiteSpace(fullName))
                return new UniquenessScore { Score = 0.5, Label = "unknown", Note = "Empty input" };

            var tokens = fullName.Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            var shares = new List<double>();
            int unknownCount = 0;

            foreach (var t in tokens)
            {
                var entry = LookupIndices.Lookup(t, _customDataPath);
                if (entry != null) shares.Add(entry.CorpusShare);
                else unknownCount++;
            }

            if (shares.Count == 0)
                return new UniquenessScore { Score = 1.0, Label = "unknown", Note = "None of the name parts are in the Egyptian corpus" };

            double logSum = shares.Sum(s => Math.Log(Math.Max(s, 1e-9)));
            double logMean = logSum / shares.Count;

            const double maxLog = 2.6;
            const double minLog = -9.2;
            double score = 1.0 - (logMean - minLog) / (maxLog - minLog);
            score = Math.Max(0.0, Math.Min(1.0, score));
            score = Math.Min(1.0, score + unknownCount * 0.15);

            string label;
            string note;
            if (score < 0.2)
            {
                label = "extremely_common";
                note = "Each part is among the most common names nationally";
            }
            else if (score < 0.4)
            {
                label = "common";
                note = "Well-known name parts with high national frequency";
            }
            else if (score < 0.6)
            {
                label = "moderate";
                note = "A mix of common and less common name parts";
            }
            else if (score < 0.8)
            {
                label = "distinctive";
                note = "Contains uncommon or regionally specific names";
            }
            else
            {
                label = "highly_unique";
                note = "Rare name combination — distinctive family heritage";
            }

            return new UniquenessScore
            {
                Score = Math.Round(score, 3),
                Label = label,
                Note = note
            };
        }

        public Dictionary<string, object> Stats()
        {
            var meta = DataLoader.LoadBundle(_customDataPath);
            var entries = LookupIndices.GetAll(_customDataPath);

            return new Dictionary<string, object>
            {
                { "version", meta.Version },
                { "corpus_tokens", meta.CorpusTokens },
                { "corpus_students", meta.CorpusStudents },
                { "cohort_years", meta.CohortYears },
                { "total_names", entries.Count },
                { "given_names", entries.Count(e => e.Role == NameRole.Given) },
                { "family_names", entries.Count(e => e.Role == NameRole.Family) },
                { "male_names", entries.Count(e => e.Gender == Gender.Male) },
                { "female_names", entries.Count(e => e.Gender == Gender.Female) }
            };
        }
    }

    public class EgyNamesEngine : EgyptianNamesEngine
    {
        public EgyNamesEngine(int? seed = null, string? customDataPath = null) : base(seed, customDataPath) { }
    }

    public class EgyNames : EgyptianNamesEngine
    {
        public EgyNames(int? seed = null, string? customDataPath = null) : base(seed, customDataPath) { }
    }
}
