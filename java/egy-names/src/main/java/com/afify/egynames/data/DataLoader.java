package com.afify.egynames.data;

import com.afify.egynames.model.Models;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.*;
import java.util.zip.GZIPInputStream;

public class DataLoader {

    public static class DataBundle {
        public String version;
        public int corpusTokens;
        public int corpusStudents;
        public List<Integer> cohortYears = new ArrayList<>();
        public List<Models.NameEntry> names = new ArrayList<>();
        public Map<String, String> corrections = new HashMap<>();
    }

    private static DataBundle cachedBundle = null;

    public static synchronized DataBundle loadBundle(String customPath) {
        if (cachedBundle != null && customPath == null) {
            return cachedBundle;
        }

        try {
            InputStream is = null;
            if (customPath != null && new File(customPath).exists()) {
                is = new FileInputStream(customPath);
            } else {
                is = DataLoader.class.getClassLoader().getResourceAsStream("names.json.gz");
                if (is == null) {
                    is = DataLoader.class.getResourceAsStream("/names.json.gz");
                }
                if (is == null && new File("src/main/resources/names.json.gz").exists()) {
                    is = new FileInputStream("src/main/resources/names.json.gz");
                }
            }

            if (is == null) {
                throw new IllegalStateException("Could not find names.json.gz resource or file.");
            }

            try (GZIPInputStream gzip = new GZIPInputStream(is)) {
                ObjectMapper mapper = new ObjectMapper();
                JsonNode root = mapper.readTree(gzip);

                DataBundle bundle = new DataBundle();
                bundle.version = root.has("version") ? root.get("version").asText() : "0.1.0";
                bundle.corpusTokens = root.has("corpus_tokens") ? root.get("corpus_tokens").asInt() : 0;
                bundle.corpusStudents = root.has("corpus_students") ? root.get("corpus_students").asInt() : 0;

                if (root.has("cohort_years")) {
                    for (JsonNode y : root.get("cohort_years")) {
                        bundle.cohortYears.add(y.asInt());
                    }
                }

                if (root.has("corrections")) {
                    Iterator<Map.Entry<String, JsonNode>> fields = root.get("corrections").fields();
                    while (fields.hasNext()) {
                        Map.Entry<String, JsonNode> field = fields.next();
                        bundle.corrections.put(field.getKey(), field.getValue().asText());
                    }
                }

                if (root.has("names")) {
                    for (JsonNode elem : root.get("names")) {
                        Models.NameEntry entry = new Models.NameEntry();
                        entry.ar = elem.has("a") ? elem.get("a").asText() : "";
                        entry.en = elem.has("e") ? elem.get("e").asText() : "";
                        entry.gender = Models.Gender.fromCode(elem.has("g") ? elem.get("g").asText() : "n");
                        entry.religion = Models.Religion.fromCode(elem.has("r") ? elem.get("r").asText() : "n");
                        entry.role = Models.NameRole.fromCode(elem.has("l") ? elem.get("l").asText() : "g");
                        entry.frequency = Models.FrequencyClass.fromCode(elem.has("fc") ? elem.get("fc").asText() : "r");
                        entry.tashkeel = elem.has("t") ? elem.get("t").asText() : entry.ar;
                        entry.tashkeelStandard = elem.has("t") ? elem.get("t").asText() : entry.ar;
                        entry.tashkeelEg = elem.has("te") ? elem.get("te").asText() : entry.tashkeelStandard;
                        entry.ipaStandard = elem.has("is") ? elem.get("is").asText() : "";
                        entry.ipaEg = elem.has("ie") ? elem.get("ie").asText() : "";
                        entry.meaningAr = elem.has("ma") ? elem.get("ma").asText() : "";
                        entry.meaningEn = elem.has("me") ? elem.get("me").asText() : "";
                        entry.root = elem.has("rt") ? elem.get("rt").asText() : "N/A";
                        entry.originType = elem.has("ot") ? elem.get("ot").asText() : "arabic_classical";
                        entry.trendCategory = elem.has("tc") ? elem.get("tc").asText() : "classic_timeless";
                        entry.corpusShare = elem.has("tp") ? elem.get("tp").asDouble() : 0.0;

                        String dla = elem.has("dla") ? elem.get("dla").asText() : (elem.has("dl") ? elem.get("dl").asText() : "");
                        entry.dallaaAr = !dla.isEmpty() ? Arrays.asList(dla.split("\\|")) : Collections.emptyList();
                        entry.dallaa = entry.dallaaAr;

                        String dlt = elem.has("dlt") ? elem.get("dlt").asText() : "";
                        entry.dallaaTashkeel = !dlt.isEmpty() ? Arrays.asList(dlt.split("\\|")) : Collections.emptyList();

                        String dle = elem.has("dle") ? elem.get("dle").asText() : "";
                        entry.dallaaEn = !dle.isEmpty() ? Arrays.asList(dle.split("\\|")) : Collections.emptyList();

                        String dli = elem.has("dli") ? elem.get("dli").asText() : "";
                        entry.dallaaIpa = !dli.isEmpty() ? Arrays.asList(dli.split("\\|")) : Collections.emptyList();

                        String ffa = elem.has("ffa") ? elem.get("ffa").asText() : (elem.has("ff") ? elem.get("ff").asText() : "");
                        entry.famousFiguresAr = !ffa.isEmpty() ? Arrays.asList(ffa.split("\\|")) : Collections.emptyList();
                        entry.famousFigures = entry.famousFiguresAr;

                        String ffe = elem.has("ffe") ? elem.get("ffe").asText() : "";
                        entry.famousFiguresEn = !ffe.isEmpty() ? Arrays.asList(ffe.split("\\|")) : Collections.emptyList();

                        String av = elem.has("av") ? elem.get("av").asText() : "";
                        String ev = elem.has("ev") ? elem.get("ev").asText() : "";

                        entry.arVariants = !av.isEmpty() ? Arrays.asList(av.split("\\|")) : List.of(entry.ar);
                        entry.enVariants = !ev.isEmpty() ? Arrays.asList(ev.split("\\|")) : List.of(entry.en);

                        List<Double> pList = new ArrayList<>();
                        if (elem.has("p")) {
                            for (JsonNode pv : elem.get("p")) {
                                pList.add(pv.asDouble());
                            }
                        }
                        entry.slotPcts = pList;

                        bundle.names.add(entry);
                    }
                }

                if (customPath == null) {
                    cachedBundle = bundle;
                }
                return bundle;
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to load EgyptianNames dataset", e);
        }
    }
}
