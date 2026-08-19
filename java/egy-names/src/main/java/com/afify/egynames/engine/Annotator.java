package com.afify.egynames.engine;

import com.afify.egynames.index.LookupIndices;
import com.afify.egynames.model.Models;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Annotator {

    public static Models.NameInfo annotateSingle(String name, String dataPath) {
        Models.NameEntry entry = LookupIndices.lookup(name, dataPath);
        return entry != null ? Models.NameInfo.fromEntry(entry) : null;
    }

    public static List<Models.NameInfo> annotate(String name, String dataPath) {
        if (name == null || name.trim().isEmpty()) return List.of();
        String[] tokens = name.trim().split("\\s+");
        return Arrays.stream(tokens)
                .map(t -> annotateSingle(t, dataPath))
                .collect(Collectors.toList());
    }
}
