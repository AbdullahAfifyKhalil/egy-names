package com.afify.egynames.index;

import com.afify.egynames.data.DataLoader;
import com.afify.egynames.model.Models;

import java.util.*;
import java.util.regex.Pattern;

public class LookupIndices {

    private static boolean built = false;
    private static final Map<String, Models.NameEntry> arIndex = new HashMap<>();
    private static final Map<String, Models.NameEntry> enIndex = new HashMap<>();
    private static final Map<String, Models.NameEntry> arNormIndex = new HashMap<>();
    private static final Map<String, String> correctionIndex = new HashMap<>();
    private static List<Models.NameEntry> allEntries = new ArrayList<>();
    private static List<Models.NameEntry> rankedEntries = new ArrayList<>();

    private static final Pattern TASHKEEL_PATTERN = Pattern.compile("[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]");
    private static final Pattern TATWEEL_PATTERN = Pattern.compile("\u0640");
    private static final Pattern ALEF_VARIANTS_PATTERN = Pattern.compile("[\u0622\u0623\u0625\u0671]");
    private static final Pattern IS_ARABIC_PATTERN = Pattern.compile("[\u0600-\u06FF\uFE70-\uFEFF]");

    public static String normalizeAr(String text) {
        if (text == null || text.isEmpty()) return "";
        String s = TASHKEEL_PATTERN.matcher(text).replaceAll("");
        s = TATWEEL_PATTERN.matcher(s).replaceAll("");
        s = ALEF_VARIANTS_PATTERN.matcher(s).replaceAll("\u0627");
        s = s.replace('\u0649', '\u064A'); // ى -> ي
        s = s.replace('\u0629', '\u0647'); // ة -> ه
        return s;
    }

    public static String normalizeEn(String text) {
        if (text == null || text.isEmpty()) return "";
        return text.toLowerCase().replace("-", "").replace("'", "").trim();
    }

    private static void claimEn(String key, Models.NameEntry entry) {
        Models.NameEntry existing = enIndex.get(key);
        if (existing == null || entry.corpusShare > existing.corpusShare) {
            enIndex.put(key, entry);
        }
    }

    /**
     * Second-pass Arabic-variant claim: skip if the key is a canonical key of
     * ANY entry (canonical spellings win unconditionally), otherwise keep the
     * higher corpus_share among competing variant claims.
     */
    private static void claimArVariant(
            Map<String, Models.NameEntry> index,
            Set<String> canonicalKeys,
            String key,
            Models.NameEntry entry) {
        if (canonicalKeys.contains(key)) return;
        Models.NameEntry existing = index.get(key);
        if (existing == null || entry.corpusShare > existing.corpusShare) {
            index.put(key, entry);
        }
    }

    public static boolean isArabic(String text) {
        return text != null && !text.isEmpty() && IS_ARABIC_PATTERN.matcher(text).find();
    }

    public static synchronized void ensureBuilt(String dataPath) {
        if (built) return;

        DataLoader.DataBundle bundle = DataLoader.loadBundle(dataPath);
        allEntries = Collections.unmodifiableList(bundle.names);

        // Pass 1: every entry's own canonical ar/normalized-ar spelling binds
        // unconditionally, and canonical keys are recorded so variant claims
        // (pass 2) can never displace a canonical binding.
        Set<String> canonicalArKeys = new HashSet<>();
        Set<String> canonicalArNormKeys = new HashSet<>();
        for (Models.NameEntry entry : allEntries) {
            arIndex.put(entry.ar, entry);
            canonicalArKeys.add(entry.ar);

            String normAr = normalizeAr(entry.ar);
            arNormIndex.put(normAr, entry);
            canonicalArNormKeys.add(normAr);
        }

        // Pass 2: variant spellings compete on corpus_share, but never win
        // over a canonical spelling of any entry.
        for (Models.NameEntry entry : allEntries) {
            for (String v : entry.arVariants) {
                String stripped = v.trim();
                if (!stripped.isEmpty()) {
                    claimArVariant(arIndex, canonicalArKeys, stripped, entry);
                    claimArVariant(arNormIndex, canonicalArNormKeys, normalizeAr(stripped), entry);
                }
            }

            claimEn(normalizeEn(entry.en), entry);

            for (String v : entry.enVariants) {
                String stripped = v.trim();
                if (!stripped.isEmpty()) {
                    claimEn(normalizeEn(stripped), entry);
                }
            }
        }

        correctionIndex.putAll(bundle.corrections);

        List<Models.NameEntry> sorted = new ArrayList<>(allEntries);
        sorted.sort((a, b) -> Double.compare(b.corpusShare, a.corpusShare));
        rankedEntries = Collections.unmodifiableList(sorted);

        built = true;
    }

    public static Models.NameEntry lookupAr(String name, String dataPath) {
        ensureBuilt(dataPath);
        if (name == null || name.trim().isEmpty()) return null;
        String trimmed = name.trim();

        // 1. Direct match
        Models.NameEntry direct = arIndex.get(trimmed);
        if (direct != null) return direct;

        // 2. Normalized match
        String norm = normalizeAr(trimmed);
        Models.NameEntry normMatch = arNormIndex.get(norm);
        if (normMatch != null) return normMatch;

        // 3. Alif / Alif Maqsura terminal phonetic equivalence
        if (norm.endsWith("\u0627")) {
            String alt = norm.substring(0, norm.length() - 1) + "\u064A";
            Models.NameEntry altMatch = arNormIndex.get(alt);
            if (altMatch != null) return altMatch;
        } else if (norm.endsWith("\u064A")) {
            String alt = norm.substring(0, norm.length() - 1) + "\u0627";
            Models.NameEntry altMatch = arNormIndex.get(alt);
            if (altMatch != null) return altMatch;
        }

        // 4. Space-less compound match
        String noSpace = trimmed.replaceAll("\\s+", "");
        if (!noSpace.equals(trimmed)) {
            Models.NameEntry noSpaceMatch = arIndex.get(noSpace);
            if (noSpaceMatch != null) return noSpaceMatch;
            Models.NameEntry noSpaceNormMatch = arNormIndex.get(normalizeAr(noSpace));
            if (noSpaceNormMatch != null) return noSpaceNormMatch;
        }

        return null;
    }

    public static Models.NameEntry lookupEn(String name, String dataPath) {
        ensureBuilt(dataPath);
        return enIndex.get(normalizeEn(name));
    }

    public static Models.NameEntry lookup(String name, String dataPath) {
        ensureBuilt(dataPath);
        return isArabic(name) ? lookupAr(name, dataPath) : lookupEn(name, dataPath);
    }

    public static String getCorrection(String surface, String dataPath) {
        ensureBuilt(dataPath);
        return correctionIndex.get(surface);
    }

    public static List<Models.NameEntry> getAll(String dataPath) {
        ensureBuilt(dataPath);
        return allEntries;
    }

    public static List<Models.NameEntry> getRanked(String dataPath) {
        ensureBuilt(dataPath);
        return rankedEntries;
    }

    public static Map<String, Models.NameEntry> getArForms(String dataPath) {
        ensureBuilt(dataPath);
        return arIndex;
    }

    public static Map<String, Models.NameEntry> getArNormForms(String dataPath) {
        ensureBuilt(dataPath);
        return arNormIndex;
    }

    /** One resolved token of a compound-aware split: its surface text and its book entry (may be null). */
    public static final class CompoundToken {
        public final String text;
        public final Models.NameEntry entry;

        public CompoundToken(String text, Models.NameEntry entry) {
            this.text = text;
            this.entry = entry;
        }
    }

    /**
     * Split on whitespace, but merge an adjacent pair into one lemma when the
     * book has it as a two-word compound (e.g. kunya "Abu X").
     *
     * <p>Mirrors Python's {@code _compound_tokens}: greedy pairwise lookahead
     * tries {@code lookupAr(word[i] + " " + word[i+1])} then
     * {@code lookupAr(word[i] + word[i+1])} before falling back to a single
     * token resolved via the general {@code lookup}.
     */
    public static List<CompoundToken> compoundTokens(String fullName, String dataPath) {
        List<CompoundToken> out = new ArrayList<>();
        if (fullName == null || fullName.trim().isEmpty()) return out;

        String[] raw = fullName.trim().split("\\s+");
        int n = raw.length;
        int i = 0;
        while (i < n) {
            if (i < n - 1) {
                String pair = raw[i] + " " + raw[i + 1];
                Models.NameEntry pairEntry = lookupAr(pair, dataPath);
                if (pairEntry == null) {
                    pairEntry = lookupAr(raw[i] + raw[i + 1], dataPath);
                }
                if (pairEntry != null) {
                    out.add(new CompoundToken(pair, pairEntry));
                    i += 2;
                    continue;
                }
            }
            out.add(new CompoundToken(raw[i], lookup(raw[i], dataPath)));
            i += 1;
        }
        return out;
    }
}
