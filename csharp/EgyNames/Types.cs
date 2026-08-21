using System;
using System.Collections.Generic;
using System.Linq;

namespace EgyptianNames
{
    public enum Gender
    {
        Male,
        Female,
        Neutral
    }

    public enum Religion
    {
        Muslim,
        Christian,
        Neutral
    }

    public enum NameRole
    {
        Given,
        Family
    }

    public enum FrequencyClass
    {
        Common,
        Normal,
        Rare
    }

    public class PetName
    {
        public string Ar { get; set; } = string.Empty;
        public string Tashkeel { get; set; } = string.Empty;
        public string En { get; set; } = string.Empty;
        public string Ipa { get; set; } = string.Empty;

        public PetName() { }

        public PetName(string ar, string tashkeel, string en, string ipa)
        {
            Ar = ar;
            Tashkeel = tashkeel;
            En = en;
            Ipa = ipa;
        }

        public override string ToString() => $"{Ar} ({Tashkeel}) - {En} {Ipa}";
    }

    public class NameEntry
    {
        public string Ar { get; set; } = string.Empty;
        public string En { get; set; } = string.Empty;
        public Gender Gender { get; set; }
        public Religion Religion { get; set; }
        public NameRole Role { get; set; }
        public List<string> ArVariants { get; set; } = new List<string>();
        public List<string> EnVariants { get; set; } = new List<string>();
        public List<double> SlotPcts { get; set; } = new List<double>();
        public double CorpusShare { get; set; }
        public FrequencyClass Frequency { get; set; }
        public string Tashkeel { get; set; } = string.Empty;
        public string TashkeelStandard { get; set; } = string.Empty;
        public string TashkeelEg { get; set; } = string.Empty;
        public string IpaStandard { get; set; } = string.Empty;
        public string IpaEg { get; set; } = string.Empty;
        public string MeaningAr { get; set; } = string.Empty;
        public string MeaningEn { get; set; } = string.Empty;
        public List<string> Dallaa { get; set; } = new List<string>();
        public List<string> DallaaAr { get; set; } = new List<string>();
        public List<string> DallaaTashkeel { get; set; } = new List<string>();
        public List<string> DallaaEn { get; set; } = new List<string>();
        public List<string> DallaaIpa { get; set; } = new List<string>();
        public string Root { get; set; } = "N/A";
        public string OriginType { get; set; } = "arabic_classical";
        public List<string> FamousFigures { get; set; } = new List<string>();
        public List<string> FamousFiguresAr { get; set; } = new List<string>();
        public List<string> FamousFiguresEn { get; set; } = new List<string>();
        public string TrendCategory { get; set; } = "classic_timeless";
    }

    public class NameInfo
    {
        public string Ar { get; set; } = string.Empty;
        public string En { get; set; } = string.Empty;
        public string Gender { get; set; } = string.Empty;
        public string Religion { get; set; } = string.Empty;
        public string Role { get; set; } = string.Empty;
        public string FrequencyClass { get; set; } = string.Empty;
        public double CorpusShare { get; set; }
        public string Tashkeel { get; set; } = string.Empty;
        public string TashkeelStandard { get; set; } = string.Empty;
        public string TashkeelEg { get; set; } = string.Empty;
        public string IpaStandard { get; set; } = string.Empty;
        public string IpaEg { get; set; } = string.Empty;
        public string? MeaningAr { get; set; }
        public string? MeaningEn { get; set; }
        public List<string> Dallaa { get; set; } = new List<string>();
        public List<string> DallaaAr { get; set; } = new List<string>();
        public List<string> DallaaTashkeel { get; set; } = new List<string>();
        public List<string> DallaaEn { get; set; } = new List<string>();
        public List<string> DallaaIpa { get; set; } = new List<string>();
        public string Root { get; set; } = "N/A";
        public string OriginType { get; set; } = "arabic_classical";
        public List<string> FamousFigures { get; set; } = new List<string>();
        public List<string> FamousFiguresAr { get; set; } = new List<string>();
        public List<string> FamousFiguresEn { get; set; } = new List<string>();
        public string TrendCategory { get; set; } = "classic_timeless";
        public IReadOnlyList<string> ArVariants { get; set; } = Array.Empty<string>();
        public IReadOnlyList<string> EnVariants { get; set; } = Array.Empty<string>();
        public IReadOnlyList<double> SlotDistribution { get; set; } = Array.Empty<double>();

        public static NameInfo FromEntry(NameEntry entry)
        {
            return new NameInfo
            {
                Ar = entry.Ar,
                En = entry.En,
                Gender = entry.Gender.ToString().ToLowerInvariant(),
                Religion = entry.Religion.ToString().ToLowerInvariant(),
                Role = entry.Role.ToString().ToLowerInvariant(),
                FrequencyClass = entry.Frequency.ToString().ToLowerInvariant(),
                CorpusShare = entry.CorpusShare,
                Tashkeel = entry.Tashkeel,
                TashkeelStandard = entry.TashkeelStandard,
                TashkeelEg = entry.TashkeelEg,
                IpaStandard = entry.IpaStandard,
                IpaEg = entry.IpaEg,
                MeaningAr = string.IsNullOrEmpty(entry.MeaningAr) ? null : entry.MeaningAr,
                MeaningEn = string.IsNullOrEmpty(entry.MeaningEn) ? null : entry.MeaningEn,
                Dallaa = new List<string>(entry.DallaaAr),
                DallaaAr = new List<string>(entry.DallaaAr),
                DallaaTashkeel = new List<string>(entry.DallaaTashkeel),
                DallaaEn = new List<string>(entry.DallaaEn),
                DallaaIpa = new List<string>(entry.DallaaIpa),
                Root = entry.Root,
                OriginType = entry.OriginType,
                FamousFigures = new List<string>(entry.FamousFiguresAr),
                FamousFiguresAr = new List<string>(entry.FamousFiguresAr),
                FamousFiguresEn = new List<string>(entry.FamousFiguresEn),
                TrendCategory = entry.TrendCategory,
                ArVariants = entry.ArVariants.ToList(),
                EnVariants = entry.EnVariants.ToList(),
                SlotDistribution = entry.SlotPcts.ToList()
            };
        }
    }

    public class GeneratedName
    {
        public string Ar { get; set; } = string.Empty;
        public string En { get; set; } = string.Empty;
        public List<string> PartsAr { get; set; } = new List<string>();
        public List<string> PartsEn { get; set; } = new List<string>();

        public override string ToString() => $"{Ar}  --  {En}";
    }

    public class ChainPart
    {
        public string Name { get; set; } = string.Empty;
        public int Slot { get; set; }
        public string Role { get; set; } = string.Empty;
        public string Detail { get; set; } = string.Empty;

        public override string ToString() => $"Slot {Slot}: {Name} ({Role} - {Detail})";
    }

    public class GenderDetection
    {
        public string Gender { get; set; } = "neutral";
        public double Confidence { get; set; }

        public override string ToString() => $"GenderDetection(gender: {Gender}, confidence: {Confidence:F2})";
    }

    public class ReligionDetection
    {
        public string Religion { get; set; } = "neutral";
        public double Confidence { get; set; }

        public override string ToString() => $"ReligionDetection(religion: {Religion}, confidence: {Confidence:F2})";
    }

    public class RankInfo
    {
        public int Rank { get; set; }
        public double Percentile { get; set; }
        public string CorpusShare { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;

        public override string ToString() => $"Rank #{Rank} ({Percentile:F2}%) - {Description}";
    }

    public class UniquenessScore
    {
        public double Score { get; set; }
        public string Label { get; set; } = string.Empty;
        public string Note { get; set; } = string.Empty;

        public override string ToString() => $"Uniqueness(score: {Score:F3}, label: {Label})";
    }
}
