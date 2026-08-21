package com.afify.egynames.engine;

import com.afify.egynames.index.LookupIndices;
import com.afify.egynames.model.Models;

import java.util.*;

public class Splitter {

    private static final double BASE_SEGMENT_COST = 1.0;
    private static final double UNKNOWN_PENALTY = 8.0;
    private static final double LENGTH_BONUS_PER_CHAR = -0.05;

    private static final Map<Models.FrequencyClass, Double> FREQ_BONUS = Map.of(
            Models.FrequencyClass.COMMON, -0.6,
            Models.FrequencyClass.NORMAL, -0.2,
            Models.FrequencyClass.RARE, 0.0
    );

    private static List<String> dpSegment(String text, String dataPath) {
        Map<String, Models.NameEntry> arIndex = LookupIndices.getArForms(dataPath);
        Map<String, Models.NameEntry> arNorm = LookupIndices.getArNormForms(dataPath);

        int n = text.length();
        double[] dpCost = new double[n + 1];
        int[] dpPrev = new int[n + 1];

        Arrays.fill(dpCost, Double.POSITIVE_INFINITY);
        Arrays.fill(dpPrev, -1);

        dpCost[0] = 0.0;
        dpPrev[0] = 0;

        for (int i = 1; i <= n; i++) {
            int startJ = i > 30 ? i - 30 : 0;
            for (int j = startJ; j < i; j++) {
                if (Double.isInfinite(dpCost[j])) continue;

                String substr = text.substring(j, i);
                if (substr.length() < 2 && j > 0) continue;

                Models.NameEntry entry = arIndex.get(substr);
                if (entry == null) {
                    entry = arNorm.get(LookupIndices.normalizeAr(substr));
                }

                if (entry != null) {
                    double bonus = FREQ_BONUS.getOrDefault(entry.frequency, 0.0);
                    double cost = dpCost[j] + BASE_SEGMENT_COST + bonus + LENGTH_BONUS_PER_CHAR * substr.length();
                    if (cost < dpCost[i]) {
                        dpCost[i] = cost;
                        dpPrev[i] = j;
                    }
                } else {
                    double cost = dpCost[j] + UNKNOWN_PENALTY + substr.length();
                    if (cost < dpCost[i]) {
                        dpCost[i] = cost;
                        dpPrev[i] = j;
                    }
                }
            }
        }

        if (Double.isInfinite(dpCost[n])) {
            return List.of(text);
        }

        List<String> segments = new ArrayList<>();
        int pos = n;
        while (pos > 0) {
            int prev = dpPrev[pos];
            segments.add(text.substring(prev, pos));
            pos = prev;
        }

        Collections.reverse(segments);
        return segments;
    }

    public static List<String> split(String fullName, String dataPath) {
        if (fullName == null || fullName.trim().isEmpty()) return List.of();

        String text = fullName.trim();
        if (text.contains(" ")) {
            return Arrays.asList(text.split("\\s+"));
        }

        if (LookupIndices.isArabic(text)) {
            Models.NameEntry entry = LookupIndices.lookup(text, dataPath);
            if (entry != null) {
                return List.of(text);
            }
            return dpSegment(text, dataPath);
        }

        return List.of(text);
    }
}
