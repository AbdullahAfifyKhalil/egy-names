package com.afify.egynames.engine;

import com.afify.egynames.index.LookupIndices;
import com.afify.egynames.model.Models;

import java.util.Arrays;
import java.util.stream.Collectors;

public class Translator {

    public static String translateToken(String token, String to, String dataPath) {
        boolean srcIsAr = LookupIndices.isArabic(token);
        String target = to != null ? to : (srcIsAr ? "en" : "ar");

        if ("en".equalsIgnoreCase(target)) {
            Models.NameEntry entry = LookupIndices.lookupAr(token, dataPath);
            return entry != null ? entry.en : token;
        } else {
            Models.NameEntry entry = LookupIndices.lookupEn(token, dataPath);
            return entry != null ? entry.ar : token;
        }
    }

    public static String translate(String fullName, String to, String dataPath) {
        if (fullName == null || fullName.trim().isEmpty()) return fullName;
        String[] tokens = fullName.trim().split("\\s+");
        return Arrays.stream(tokens)
                .map(t -> translateToken(t, to, dataPath))
                .collect(Collectors.joining(" "));
    }
}
