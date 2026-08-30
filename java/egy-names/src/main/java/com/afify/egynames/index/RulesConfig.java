package com.afify.egynames.index;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.*;

/**
 * Loader for the shared, cross-SDK rule config ({@code logic_config.json}).
 *
 * <p>Mirrors {@code python/src/egy_names/_rules_config.py}: a single source of
 * truth for non-personal surfaces, low-confidence detection thresholds, and
 * the (currently unused by Java) ML-abstention thresholds/rule tables. If the
 * config file is missing or malformed, falls back to the values last known
 * correct, so the library never hard-fails on a packaging mistake.
 */
public final class RulesConfig {

    private static final Set<String> NON_PERSONAL_AR_FALLBACK = Set.of(
            "الله", "الرجل", "الرجال", "شربه", "لافندي", "لفندي", "ماء", "البيت"
    );

    private static final List<String> UNCERTAIN_MEANING_MARKERS_FALLBACK = List.of(
            "غير واضح", "لا يوجد معنى", "غير معروف",
            "قد يكون تحريف", "تحريفاً", "تحريفًا"
    );

    private static final double LOW_CONFIDENCE_SHARE_EPSILON_FALLBACK = 0.0001;

    private static final List<String> KUNYA_EXEMPT_PREFIXES_FALLBACK = List.of("أبو", "ابو", "أم", "ام");

    private static final Map<String, Double> INFER_THRESHOLDS_FALLBACK = Map.of(
            "gender_min_p", 0.70,
            "muslim_min_p", 0.85,
            "christian_min_p", 0.90,
            "role_min_p", 0.88
    );

    private static volatile Set<String> nonPersonalAr;
    private static volatile List<String> uncertainMeaningMarkers;
    private static volatile Double lowConfidenceShareEpsilon;
    private static volatile List<String> kunyaExemptPrefixes;
    private static volatile Map<String, Double> inferThresholds;
    private static volatile Map<String, List<JsonNode>> inferRules;

    private RulesConfig() {}

    private static synchronized JsonNode load() {
        try {
            InputStream is = RulesConfig.class.getClassLoader().getResourceAsStream("logic_config.json");
            if (is == null) {
                is = RulesConfig.class.getResourceAsStream("/logic_config.json");
            }
            if (is == null && new File("src/main/resources/logic_config.json").exists()) {
                is = new FileInputStream("src/main/resources/logic_config.json");
            }
            if (is == null) {
                return null;
            }
            try (InputStream stream = is) {
                ObjectMapper mapper = new ObjectMapper();
                return mapper.readTree(stream);
            }
        } catch (Exception e) {
            return null;
        }
    }

    private static List<String> asStringList(JsonNode node) {
        List<String> out = new ArrayList<>();
        if (node != null && node.isArray()) {
            for (JsonNode n : node) {
                out.add(n.asText());
            }
        }
        return out;
    }

    private static synchronized void ensureLoaded() {
        if (nonPersonalAr != null) return;

        JsonNode root = load();
        JsonNode quality = root != null ? root.get("quality") : null;

        if (quality != null && quality.has("non_personal_ar")) {
            nonPersonalAr = new HashSet<>(asStringList(quality.get("non_personal_ar")));
        } else {
            nonPersonalAr = new HashSet<>(NON_PERSONAL_AR_FALLBACK);
        }

        if (quality != null && quality.has("uncertain_meaning_markers")) {
            uncertainMeaningMarkers = asStringList(quality.get("uncertain_meaning_markers"));
        } else {
            uncertainMeaningMarkers = UNCERTAIN_MEANING_MARKERS_FALLBACK;
        }

        if (quality != null && quality.has("low_confidence_share_epsilon")) {
            lowConfidenceShareEpsilon = quality.get("low_confidence_share_epsilon").asDouble();
        } else {
            lowConfidenceShareEpsilon = LOW_CONFIDENCE_SHARE_EPSILON_FALLBACK;
        }

        if (quality != null && quality.has("kunya_exempt_prefixes")) {
            kunyaExemptPrefixes = asStringList(quality.get("kunya_exempt_prefixes"));
        } else {
            kunyaExemptPrefixes = KUNYA_EXEMPT_PREFIXES_FALLBACK;
        }

        JsonNode thresholdsNode = root != null ? root.get("infer_thresholds") : null;
        if (thresholdsNode != null) {
            Map<String, Double> m = new HashMap<>();
            Iterator<Map.Entry<String, JsonNode>> fields = thresholdsNode.fields();
            while (fields.hasNext()) {
                Map.Entry<String, JsonNode> f = fields.next();
                if (f.getValue().isNumber()) {
                    m.put(f.getKey(), f.getValue().asDouble());
                }
            }
            inferThresholds = m.isEmpty() ? INFER_THRESHOLDS_FALLBACK : m;
        } else {
            inferThresholds = INFER_THRESHOLDS_FALLBACK;
        }

        Map<String, List<JsonNode>> rules = new HashMap<>();
        JsonNode rulesNode = root != null ? root.get("infer_rules") : null;
        for (String kind : List.of("gender", "religion", "role")) {
            List<JsonNode> list = new ArrayList<>();
            if (rulesNode != null && rulesNode.has(kind) && rulesNode.get(kind).isArray()) {
                for (JsonNode n : rulesNode.get(kind)) {
                    list.add(n);
                }
            }
            rules.put(kind, list);
        }
        inferRules = rules;
    }

    public static Set<String> nonPersonalAr() {
        ensureLoaded();
        return nonPersonalAr;
    }

    public static List<String> uncertainMeaningMarkers() {
        ensureLoaded();
        return uncertainMeaningMarkers;
    }

    public static double lowConfidenceShareEpsilon() {
        ensureLoaded();
        return lowConfidenceShareEpsilon;
    }

    public static List<String> kunyaExemptPrefixes() {
        ensureLoaded();
        return kunyaExemptPrefixes;
    }

    public static Map<String, Double> inferThresholds() {
        ensureLoaded();
        return inferThresholds;
    }

    /** Rule table for 'gender' | 'religion' | 'role'. Loaded for forward compatibility only. */
    public static List<JsonNode> inferRules(String kind) {
        ensureLoaded();
        return inferRules.getOrDefault(kind, Collections.emptyList());
    }
}
