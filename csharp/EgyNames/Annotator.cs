using System;
using System.Collections.Generic;
using System.Linq;

namespace EgyptianNames
{
    public static class Annotator
    {
        public static NameInfo? AnnotateSingle(string name, string? dataPath = null)
        {
            var entry = LookupIndices.Lookup(name, dataPath);
            return entry != null ? NameInfo.FromEntry(entry) : null;
        }

        public static List<NameInfo?> Annotate(string name, string? dataPath = null)
        {
            if (string.IsNullOrWhiteSpace(name)) return new List<NameInfo?>();
            var tokens = name.Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            return tokens.Select(t => AnnotateSingle(t, dataPath)).ToList();
        }
    }
}
