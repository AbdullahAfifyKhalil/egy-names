package com.afify.egynames.engine;

import com.afify.egynames.index.LookupIndices;
import com.afify.egynames.index.Quality;
import com.afify.egynames.model.Models;

import java.util.*;
import java.util.stream.Collectors;

public class Generator {

    private static final int DEFAULT_MIN_LEN = 4;
    private static final int DEFAULT_MAX_LEN = 5;

    private static List<Models.NameEntry> filterEntries(
            List<Models.NameEntry> entries,
            Models.Gender gender,
            Models.Religion religion,
            Models.NameRole role,
            Models.FrequencyClass frequency) {
        return entries.stream().filter(e -> {
            if (gender != null && e.gender != gender && e.gender != Models.Gender.NEUTRAL) return false;
            if (religion != null && e.religion != religion && e.religion != Models.Religion.NEUTRAL) return false;
            if (role != null && e.role != role) return false;
            if (frequency != null && e.frequency != frequency) return false;
            return Quality.isGeneratableEntry(e);
        }).collect(Collectors.toList());
    }

    private static Models.NameEntry weightedPick(List<Models.NameEntry> entries, int slotIdx, Random rng) {
        List<Models.NameEntry> candidates = new ArrayList<>();
        List<Double> weights = new ArrayList<>();
        double totalWeight = 0.0;

        for (Models.NameEntry e : entries) {
            double w = (slotIdx < e.slotPcts.size() ? e.slotPcts.get(slotIdx) : 0.0) * e.corpusShare;
            if (w > 0) {
                candidates.add(e);
                weights.add(w);
                totalWeight += w;
            }
        }

        if (candidates.isEmpty()) {
            for (Models.NameEntry e : entries) {
                double w = Math.max(e.corpusShare, 1e-9);
                candidates.add(e);
                weights.add(w);
                totalWeight += w;
            }
        }

        double r = rng.nextDouble() * totalWeight;
        for (int i = 0; i < candidates.size(); i++) {
            r -= weights.get(i);
            if (r <= 0) return candidates.get(i);
        }

        return candidates.get(candidates.size() - 1);
    }

    public static List<Models.GeneratedName> generate(
            int count,
            Models.Gender gender,
            Models.Religion religion,
            Integer length,
            boolean familyName,
            Models.FrequencyClass frequency,
            Long seed,
            String dataPath) {

        Random rng = seed != null ? new Random(seed) : new Random();
        List<Models.NameEntry> allEntries = LookupIndices.getAll(dataPath);

        List<Models.NameEntry> firstPool = filterEntries(allEntries, gender, religion, Models.NameRole.GIVEN, frequency);
        List<Models.NameEntry> patronPool = filterEntries(allEntries, Models.Gender.MALE, religion, Models.NameRole.GIVEN, frequency);
        List<Models.NameEntry> familyPool = filterEntries(allEntries, null, religion, Models.NameRole.FAMILY, frequency);

        if (firstPool.isEmpty()) firstPool = filterEntries(allEntries, gender, null, Models.NameRole.GIVEN, null);
        if (patronPool.isEmpty()) patronPool = filterEntries(allEntries, Models.Gender.MALE, null, Models.NameRole.GIVEN, null);
        if (familyPool.isEmpty()) familyPool = filterEntries(allEntries, null, null, Models.NameRole.FAMILY, null);

        List<Models.GeneratedName> results = new ArrayList<>();

        for (int c = 0; c < count; c++) {
            int chainLen = length != null ? length : (DEFAULT_MIN_LEN + rng.nextInt(DEFAULT_MAX_LEN - DEFAULT_MIN_LEN + 1));
            List<String> partsAr = new ArrayList<>();
            List<String> partsEn = new ArrayList<>();
            Set<String> seen = new HashSet<>();

            // Slot 1
            Models.NameEntry entry = weightedPick(firstPool, 0, rng);
            int attempts = 0;
            while (seen.contains(entry.ar) && attempts < 20) {
                entry = weightedPick(firstPool, 0, rng);
                attempts++;
            }
            partsAr.add(entry.ar);
            partsEn.add(entry.en);
            seen.add(entry.ar);

            // Patronymic slots 2 .. (N-1 or N)
            int patronEnd = familyName ? chainLen - 1 : chainLen;
            for (int slot = 1; slot < patronEnd; slot++) {
                int slotIdx = Math.min(slot, 7);
                entry = weightedPick(patronPool, slotIdx, rng);
                attempts = 0;
                while (seen.contains(entry.ar) && attempts < 20) {
                    entry = weightedPick(patronPool, slotIdx, rng);
                    attempts++;
                }
                partsAr.add(entry.ar);
                partsEn.add(entry.en);
                seen.add(entry.ar);
            }

            // Family name slot
            if (familyName && chainLen > 1) {
                int slotIdx = Math.min(chainLen - 1, 7);
                entry = weightedPick(familyPool, slotIdx, rng);
                attempts = 0;
                while (seen.contains(entry.ar) && attempts < 20) {
                    entry = weightedPick(familyPool, slotIdx, rng);
                    attempts++;
                }
                partsAr.add(entry.ar);
                partsEn.add(entry.en);
            }

            Models.GeneratedName gn = new Models.GeneratedName();
            gn.ar = String.join(" ", partsAr);
            gn.en = String.join(" ", partsEn);
            gn.partsAr = partsAr;
            gn.partsEn = partsEn;
            results.add(gn);
        }

        return results;
    }
}
