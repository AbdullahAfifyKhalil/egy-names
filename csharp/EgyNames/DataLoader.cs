using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Reflection;
using System.Text.Json;

namespace EgyptianNames
{
    public class DataBundle
    {
        public string Version { get; set; } = "0.1.0";
        public int CorpusTokens { get; set; }
        public int CorpusStudents { get; set; }
        public List<int> CohortYears { get; set; } = new List<int>();
        public List<NameEntry> Names { get; set; } = new List<NameEntry>();
        public Dictionary<string, string> Corrections { get; set; } = new Dictionary<string, string>();
    }

    public static class DataLoader
    {
        private static DataBundle? _cachedBundle;
        private static readonly object _lock = new object();

        public static DataBundle LoadBundle(string? customPath = null)
        {
            if (_cachedBundle != null && customPath == null)
            {
                return _cachedBundle;
            }

            lock (_lock)
            {
                if (_cachedBundle != null && customPath == null)
                {
                    return _cachedBundle;
                }

                Stream? stream = null;

                if (!string.IsNullOrEmpty(customPath) && File.Exists(customPath))
                {
                    stream = File.OpenRead(customPath);
                }
                else
                {
                    // Check local relative directories
                    var possiblePaths = new[]
                    {
                        "Data/names.json.gz",
                        "names.json.gz",
                        Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Data", "names.json.gz"),
                        Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "names.json.gz")
                    };

                    foreach (var p in possiblePaths)
                    {
                        if (File.Exists(p))
                        {
                            stream = File.OpenRead(p);
                            break;
                        }
                    }

                    // Fallback to Embedded Resource
                    if (stream == null)
                    {
                        var assembly = Assembly.GetExecutingAssembly();
                        var resourceName = assembly.GetManifestResourceNames()
                            .FirstOrDefault(r => r.EndsWith("names.json.gz", StringComparison.OrdinalIgnoreCase));

                        if (resourceName != null)
                        {
                            stream = assembly.GetManifestResourceStream(resourceName);
                        }
                    }
                }

                if (stream == null)
                {
                    throw new FileNotFoundException("Could not locate names.json.gz data file as embedded resource or file.");
                }

                using (stream)
                using (var gzip = new GZipStream(stream, CompressionMode.Decompress))
                using (var doc = JsonDocument.Parse(gzip))
                {
                    var root = doc.RootElement;
                    var bundle = new DataBundle
                    {
                        Version = root.TryGetProperty("version", out var v) ? v.GetString() ?? "0.1.0" : "0.1.0",
                        CorpusTokens = root.TryGetProperty("corpus_tokens", out var ct) ? ct.GetInt32() : 0,
                        CorpusStudents = root.TryGetProperty("corpus_students", out var cs) ? cs.GetInt32() : 0
                    };

                    if (root.TryGetProperty("cohort_years", out var cy))
                    {
                        foreach (var y in cy.EnumerateArray())
                        {
                            bundle.CohortYears.Add(y.GetInt32());
                        }
                    }

                    if (root.TryGetProperty("corrections", out var corr))
                    {
                        foreach (var prop in corr.EnumerateObject())
                        {
                            bundle.Corrections[prop.Name] = prop.Value.GetString() ?? string.Empty;
                        }
                    }

                    if (root.TryGetProperty("names", out var namesArr))
                    {
                        foreach (var elem in namesArr.EnumerateArray())
                        {
                            var ar = elem.GetProperty("a").GetString() ?? string.Empty;
                            var en = elem.GetProperty("e").GetString() ?? string.Empty;
                            var gStr = elem.TryGetProperty("g", out var g) ? g.GetString() : "n";
                            var rStr = elem.TryGetProperty("r", out var r) ? r.GetString() : "n";
                            var lStr = elem.TryGetProperty("l", out var l) ? l.GetString() : "g";
                            var avStr = elem.TryGetProperty("av", out var av) ? av.GetString() : string.Empty;
                            var evStr = elem.TryGetProperty("ev", out var ev) ? ev.GetString() : string.Empty;
                            var fcStr = elem.TryGetProperty("fc", out var fc) ? fc.GetString() : "r";
                            var tStr = elem.TryGetProperty("t", out var t) ? t.GetString() : string.Empty;
                            var maStr = elem.TryGetProperty("ma", out var ma) ? ma.GetString() : string.Empty;
                            var meStr = elem.TryGetProperty("me", out var me) ? me.GetString() : string.Empty;
                            var tp = elem.TryGetProperty("tp", out var tpVal) ? tpVal.GetDouble() : 0.0;

                            var pList = new List<double>();
                            if (elem.TryGetProperty("p", out var pArr))
                            {
                                foreach (var pv in pArr.EnumerateArray())
                                {
                                    pList.Add(pv.GetDouble());
                                }
                            }

                            var gender = gStr == "m" ? Gender.Male : (gStr == "f" ? Gender.Female : Gender.Neutral);
                            var religion = rStr == "m" ? Religion.Muslim : (rStr == "c" ? Religion.Christian : Religion.Neutral);
                            var role = lStr == "f" ? NameRole.Family : NameRole.Given;
                            var freq = fcStr == "c" ? FrequencyClass.Common : (fcStr == "n" ? FrequencyClass.Normal : FrequencyClass.Rare);

                            var arVariants = !string.IsNullOrEmpty(avStr)
                                ? avStr.Split('|', StringSplitOptions.RemoveEmptyEntries).ToList()
                                : new List<string> { ar };

                            var enVariants = !string.IsNullOrEmpty(evStr)
                                ? evStr.Split('|', StringSplitOptions.RemoveEmptyEntries).ToList()
                                : new List<string> { en };

                            bundle.Names.Add(new NameEntry
                            {
                                Ar = ar,
                                En = en,
                                Gender = gender,
                                Religion = religion,
                                Role = role,
                                ArVariants = arVariants,
                                EnVariants = enVariants,
                                SlotPcts = pList,
                                CorpusShare = tp,
                                Frequency = freq,
                                Tashkeel = tStr ?? string.Empty,
                                MeaningAr = maStr ?? string.Empty,
                                MeaningEn = meStr ?? string.Empty
                            });
                        }
                    }

                    if (customPath == null)
                    {
                        _cachedBundle = bundle;
                    }

                    return bundle;
                }
            }
        }
    }
}
