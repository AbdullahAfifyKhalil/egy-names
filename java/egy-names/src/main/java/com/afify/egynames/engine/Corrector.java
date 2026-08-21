package com.afify.egynames.engine;

import com.afify.egynames.index.LookupIndices;
import com.afify.egynames.model.Models;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Corrector {

    public static String correctToken(String token, String dataPath) {
        if (token == null || token.trim().isEmpty()) return token;
        String t = token.trim();

        // 1. Direct surface correction pair
        String canonical = LookupIndices.getCorrection(t, dataPath);
        if (canonical != null) return canonical;

        // 2. Exact match in arabic index (including phonetic variants)
        Models.NameEntry entry = LookupIndices.lookupAr(t, dataPath);
        if (entry != null) return entry.ar;

        // 3. Normalized form lookup
        String norm = LookupIndices.normalizeAr(t);
        Map<String, Models.NameEntry> arNorm = LookupIndices.getArNormForms(dataPath);
        Models.NameEntry normEntry = arNorm.get(norm);
        if (normEntry != null) return normEntry.ar;

        // 4. Trailing Alif / Alif Maqsura check
        if (norm.endsWith("\u0627")) {
            String alt = norm.substring(0, norm.length() - 1) + "\u064A";
            Models.NameEntry altMatch = arNorm.get(alt);
            if (altMatch != null) return altMatch.ar;
        } else if (norm.endsWith("\u064A")) {
            String alt = norm.substring(0, norm.length() - 1) + "\u0627";
            Models.NameEntry altMatch = arNorm.get(alt);
            if (altMatch != null) return altMatch.ar;
        }

        return t;
    }

    public static String correct(String name, String dataPath) {
        if (name == null || name.trim().isEmpty()) return name;
        String[] rawTokens = name.trim().split("\\s+");
        List<String> result = new ArrayList<>();

        for (int i = 0; i < rawTokens.length; i++) {
            String current = rawTokens[i];

            // Check compound pair (e.g. "عبد" + "الرحيم" -> "عبدالرحيم")
            if (i < rawTokens.length - 1) {
                String next = rawTokens[i + 1];
                String compound = current + " " + next;
                String compoundNoSpace = current + next;

                Models.NameEntry compoundEntry = LookupIndices.lookupAr(compound, dataPath);
                if (compoundEntry == null) {
                    compoundEntry = LookupIndices.lookupAr(compoundNoSpace, dataPath);
                }

                if (compoundEntry != null) {
                    result.add(compoundEntry.ar);
                    i++; // skip second part
                    continue;
                }
            }

            result.add(correctToken(current, dataPath));
        }

        return String.join(" ", result);
    }
}
