package com.afify.egynames.engine;

import com.afify.egynames.index.LookupIndices;
import com.afify.egynames.model.Models;

import java.util.List;
import java.util.stream.Collectors;

public class SearchEngine {

    public static List<Models.NameInfo> search(
            Models.Gender gender,
            Models.Religion religion,
            Models.NameRole role,
            Models.FrequencyClass frequency,
            String startsWith,
            String endsWith,
            String contains,
            Double minCorpusShare,
            int maxResults,
            String sortBy,
            String dataPath) {

        List<Models.NameEntry> entries = LookupIndices.getAll(dataPath);

        boolean prefixAr = startsWith != null && LookupIndices.isArabic(startsWith);
        boolean suffixAr = endsWith != null && LookupIndices.isArabic(endsWith);
        boolean containsAr = contains != null && LookupIndices.isArabic(contains);

        List<Models.NameEntry> filtered = entries.stream().filter(e -> {
            if (gender != null && e.gender != gender && e.gender != Models.Gender.NEUTRAL) return false;
            if (religion != null && e.religion != religion && e.religion != Models.Religion.NEUTRAL) return false;
            if (role != null && e.role != role) return false;
            if (frequency != null && e.frequency != frequency) return false;
            if (minCorpusShare != null && e.corpusShare < minCorpusShare) return false;

            if (startsWith != null && !startsWith.isEmpty()) {
                if (prefixAr) {
                    if (!LookupIndices.normalizeAr(e.ar).startsWith(LookupIndices.normalizeAr(startsWith))) return false;
                } else {
                    if (!LookupIndices.normalizeEn(e.en).startsWith(LookupIndices.normalizeEn(startsWith))) return false;
                }
            }

            if (endsWith != null && !endsWith.isEmpty()) {
                if (suffixAr) {
                    if (!LookupIndices.normalizeAr(e.ar).endsWith(LookupIndices.normalizeAr(endsWith))) return false;
                } else {
                    if (!LookupIndices.normalizeEn(e.en).endsWith(LookupIndices.normalizeEn(endsWith))) return false;
                }
            }

            if (contains != null && !contains.isEmpty()) {
                if (containsAr) {
                    if (!LookupIndices.normalizeAr(e.ar).contains(LookupIndices.normalizeAr(contains))) return false;
                } else {
                    if (!LookupIndices.normalizeEn(e.en).contains(LookupIndices.normalizeEn(contains))) return false;
                }
            }

            return true;
        }).collect(Collectors.toList());

        if ("alphabetical".equalsIgnoreCase(sortBy)) {
            filtered.sort((a, b) -> a.ar.compareTo(b.ar));
        } else {
            filtered.sort((a, b) -> Double.compare(b.corpusShare, a.corpusShare));
        }

        return filtered.stream()
                .limit(maxResults)
                .map(Models.NameInfo::fromEntry)
                .collect(Collectors.toList());
    }
}
