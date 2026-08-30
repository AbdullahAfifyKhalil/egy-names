using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text.Json;

namespace EgyptianNames
{
    /// <summary>
    /// Loader for the shared, cross-SDK rule config (<c>data/logic_config.json</c>,
    /// synced by scripts/sync-catalog.sh, same as names.json.gz). Single source of
    /// truth for every threshold and rule list that used to be hardcoded per
    /// language. Only pure algorithms (compound-token lookahead,
    /// first-personal-token-wins, corpus-share tie-break) stay as code, because
    /// they cannot be expressed as data.
    ///
    /// If the config file is missing or malformed, falls back to the values last
    /// known correct from the reference audits, so the library never hard-fails
    /// on a packaging mistake.
    /// </summary>
    public static class RulesConfig
    {
        public class InferRule
        {
            public string? Script { get; set; }
            public string? Match { get; set; }
            public List<string> Prefix { get; set; } = new List<string>();
            public List<string> Suffix { get; set; } = new List<string>();
            public List<string> Contains { get; set; } = new List<string>();
            public string Value { get; set; } = string.Empty;
            public double Confidence { get; set; }
        }

        private static readonly HashSet<string> FallbackNonPersonalAr = new HashSet<string>
        {
            "الله", "الرجل", "الرجال", "شربه", "لافندي", "لفندي", "ماء", "البيت",
        };

        private static readonly string[] FallbackUncertainMeaningMarkers =
        {
            "غير واضح", "لا يوجد معنى", "غير معروف",
            "قد يكون تحريف", "تحريفاً", "تحريفًا",
        };

        private static readonly string[] FallbackKunyaExemptPrefixes = { "أبو", "ابو", "أم", "ام" };
        private const double FallbackLowConfidenceShareEpsilon = 0.0001;

        private static bool _loaded;
        private static readonly object _lock = new object();

        private static HashSet<string> _nonPersonalAr = new HashSet<string>(FallbackNonPersonalAr);
        private static string[] _uncertainMeaningMarkers = FallbackUncertainMeaningMarkers;
        private static double _lowConfidenceShareEpsilon = FallbackLowConfidenceShareEpsilon;
        private static string[] _kunyaExemptPrefixes = FallbackKunyaExemptPrefixes;
        private static Dictionary<string, double> _inferThresholds = new Dictionary<string, double>
        {
            { "gender_min_p", 0.70 },
            { "muslim_min_p", 0.85 },
            { "christian_min_p", 0.90 },
            { "role_min_p", 0.88 },
        };
        private static Dictionary<string, List<InferRule>> _inferRules = new Dictionary<string, List<InferRule>>
        {
            { "gender", new List<InferRule>() },
            { "religion", new List<InferRule>() },
            { "role", new List<InferRule>() },
        };

        public static HashSet<string> NonPersonalAr
        {
            get { EnsureLoaded(); return _nonPersonalAr; }
        }

        public static IReadOnlyList<string> UncertainMeaningMarkers
        {
            get { EnsureLoaded(); return _uncertainMeaningMarkers; }
        }

        public static double LowConfidenceShareEpsilon
        {
            get { EnsureLoaded(); return _lowConfidenceShareEpsilon; }
        }

        public static IReadOnlyList<string> KunyaExemptPrefixes
        {
            get { EnsureLoaded(); return _kunyaExemptPrefixes; }
        }

        public static IReadOnlyDictionary<string, double> InferThresholds
        {
            get { EnsureLoaded(); return _inferThresholds; }
        }

        public static IReadOnlyList<InferRule> InferRules(string kind)
        {
            EnsureLoaded();
            return _inferRules.TryGetValue(kind, out var rules) ? rules : new List<InferRule>();
        }

        /// <summary>Force a reload on the next access (mainly for tests).</summary>
        public static void Reset()
        {
            lock (_lock)
            {
                _loaded = false;
            }
        }

        private static void EnsureLoaded()
        {
            if (_loaded) return;
            lock (_lock)
            {
                if (_loaded) return;
                try
                {
                    Load();
                }
                catch
                {
                    // Malformed or unreadable config: keep the hardcoded fallback.
                }
                finally
                {
                    _loaded = true;
                }
            }
        }

        private static void Load()
        {
            using var stream = OpenConfigStream();
            if (stream == null) return;

            using var doc = JsonDocument.Parse(stream);
            var root = doc.RootElement;

            if (root.TryGetProperty("quality", out var quality))
            {
                if (quality.TryGetProperty("non_personal_ar", out var npa))
                {
                    _nonPersonalAr = new HashSet<string>(StringArray(npa));
                }
                if (quality.TryGetProperty("uncertain_meaning_markers", out var umm))
                {
                    _uncertainMeaningMarkers = StringArray(umm).ToArray();
                }
                if (quality.TryGetProperty("low_confidence_share_epsilon", out var lcse))
                {
                    _lowConfidenceShareEpsilon = lcse.GetDouble();
                }
                if (quality.TryGetProperty("kunya_exempt_prefixes", out var kep))
                {
                    _kunyaExemptPrefixes = StringArray(kep).ToArray();
                }
            }

            if (root.TryGetProperty("infer_thresholds", out var thresholds))
            {
                var parsed = new Dictionary<string, double>(_inferThresholds);
                foreach (var prop in thresholds.EnumerateObject())
                {
                    if (prop.Value.ValueKind == JsonValueKind.Number)
                    {
                        parsed[prop.Name] = prop.Value.GetDouble();
                    }
                }
                _inferThresholds = parsed;
            }

            if (root.TryGetProperty("infer_rules", out var inferRules))
            {
                var parsed = new Dictionary<string, List<InferRule>>();
                foreach (var kind in new[] { "gender", "religion", "role" })
                {
                    parsed[kind] = inferRules.TryGetProperty(kind, out var arr)
                        ? arr.EnumerateArray().Select(ParseRule).ToList()
                        : new List<InferRule>();
                }
                _inferRules = parsed;
            }
        }

        private static InferRule ParseRule(JsonElement elem)
        {
            return new InferRule
            {
                Script = elem.TryGetProperty("script", out var s) ? s.GetString() : null,
                Match = elem.TryGetProperty("match", out var m) ? m.GetString() : null,
                Prefix = elem.TryGetProperty("prefix", out var p) ? StringArray(p).ToList() : new List<string>(),
                Suffix = elem.TryGetProperty("suffix", out var sf) ? StringArray(sf).ToList() : new List<string>(),
                Contains = elem.TryGetProperty("contains", out var c) ? StringArray(c).ToList() : new List<string>(),
                Value = elem.TryGetProperty("value", out var v) ? v.GetString() ?? string.Empty : string.Empty,
                Confidence = elem.TryGetProperty("confidence", out var cf) ? cf.GetDouble() : 0.0,
            };
        }

        private static IEnumerable<string> StringArray(JsonElement elem)
        {
            if (elem.ValueKind == JsonValueKind.String)
            {
                var v = elem.GetString();
                if (v != null) yield return v;
                yield break;
            }
            if (elem.ValueKind != JsonValueKind.Array) yield break;
            foreach (var item in elem.EnumerateArray())
            {
                var v = item.GetString();
                if (v != null) yield return v;
            }
        }

        private static Stream? OpenConfigStream()
        {
            var possiblePaths = new[]
            {
                "Data/logic_config.json",
                "logic_config.json",
                Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Data", "logic_config.json"),
                Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "logic_config.json"),
            };

            foreach (var p in possiblePaths)
            {
                if (File.Exists(p))
                {
                    return File.OpenRead(p);
                }
            }

            var assembly = Assembly.GetExecutingAssembly();
            var resourceName = assembly.GetManifestResourceNames()
                .FirstOrDefault(r => r.EndsWith("logic_config.json", StringComparison.OrdinalIgnoreCase));

            return resourceName != null ? assembly.GetManifestResourceStream(resourceName) : null;
        }
    }
}
