package com.afify.egynames;

import com.afify.egynames.data.DataLoader;
import com.afify.egynames.engine.*;
import com.afify.egynames.index.LookupIndices;
import com.afify.egynames.index.Quality;
import com.afify.egynames.model.Models;

import java.util.*;
import java.util.stream.Collectors;

public class EgyptianNames {

    private final Long seed;
    private final String customDataPath;

    public EgyptianNames() {
        this(null, null);
    }

    public EgyptianNames(Long seed) {
        this(seed, null);
    }

    public EgyptianNames(Long seed, String customDataPath) {
        this.seed = seed;
        this.customDataPath = customDataPath;
    }

    // Core Methods

    public List<Models.GeneratedName> generate(int count, Models.Gender gender, Models.Religion religion, Integer length, boolean familyName, Models.FrequencyClass frequency, Long seed) {
        return Generator.generate(count, gender, religion, length, familyName, frequency, seed != null ? seed : this.seed, customDataPath);
    }

    public List<Models.GeneratedName> generate(int count, String gender, String religion) {
        return generate(count, Models.Gender.fromString(gender), Models.Religion.fromString(religion), null, true, null, null);
    }

    public List<Models.GeneratedName> generate(int count) {
        return generate(count, (Models.Gender) null, null, null, true, null, null);
    }

    public String translate(String name, String to) {
        return Translator.translate(name, to, customDataPath);
    }

    public String translate(String name) {
        return translate(name, null);
    }

    public List<Models.NameInfo> annotate(String name) {
        return Annotator.annotate(name, customDataPath);
    }

    public Models.NameInfo annotateSingle(String name) {
        return Annotator.annotateSingle(name, customDataPath);
    }

    public List<String> split(String fullName) {
        return Splitter.split(fullName, customDataPath);
    }

    public String tashkeel(String name, String dialect) {
        if (name == null || name.trim().isEmpty()) return name;
        String[] rawTokens = name.trim().split("\\s+");
        List<String> result = new ArrayList<>();
        boolean isEg = dialect != null && dialect.toLowerCase().startsWith("eg");

        for (int i = 0; i < rawTokens.length; i++) {
            String current = rawTokens[i];

            if (i < rawTokens.length - 1) {
                String next = rawTokens[i + 1];
                String compound = current + " " + next;
                String compoundNoSpace = current + next;
                Models.NameEntry compoundEntry = LookupIndices.lookupAr(compound, customDataPath);
                if (compoundEntry == null) {
                    compoundEntry = LookupIndices.lookupAr(compoundNoSpace, customDataPath);
                }
                if (compoundEntry != null) {
                    String val = isEg ? compoundEntry.tashkeelEg : compoundEntry.tashkeelStandard;
                    if (val != null && !val.isEmpty()) {
                        result.add(val);
                        i++;
                        continue;
                    }
                }
            }

            Models.NameEntry entry = LookupIndices.lookupAr(current, customDataPath);
            if (entry != null) {
                String val = isEg ? entry.tashkeelEg : entry.tashkeelStandard;
                result.add(val != null && !val.isEmpty() ? val : current);
            } else {
                result.add(current);
            }
        }

        return String.join(" ", result);
    }

    public String tashkeel(String name) {
        return tashkeel(name, "standard");
    }

    public String tashkeelEg(String name) {
        return tashkeel(name, "egyptian");
    }

    public String ipa(String name, String dialect) {
        if (name == null || name.trim().isEmpty()) return "";
        List<String> tokens = name.contains(" ") ? Arrays.asList(name.trim().split("\\s+")) : split(name);
        boolean isEg = dialect != null && dialect.toLowerCase().startsWith("eg");
        List<String> ipaParts = new ArrayList<>();

        for (String tok : tokens) {
            Models.NameEntry entry = LookupIndices.lookup(tok, customDataPath);
            if (entry != null) {
                String ipaVal = isEg ? entry.ipaEg : entry.ipaStandard;
                if (ipaVal != null && !ipaVal.isEmpty()) {
                    ipaParts.add(ipaVal.replaceAll("^[/|\\[]+|[/|\\]]+$", ""));
                } else {
                    ipaParts.add(tok);
                }
            } else {
                ipaParts.add(tok);
            }
        }

        String joined = String.join(" ", ipaParts);
        return isEg ? "[" + joined + "]" : "/" + joined + "/";
    }

    public String ipa(String name) {
        return ipa(name, "standard");
    }

    public String ipaEg(String name) {
        return ipa(name, "egyptian");
    }

    public List<String> dallaa(String name, String format) {
        Models.NameEntry entry = LookupIndices.lookup(name, customDataPath);
        if (entry == null) return Collections.emptyList();
        String fmt = format != null ? format.toLowerCase() : "plain";
        if ("tashkeel".equals(fmt) || "tashkeel_eg".equals(fmt) || "tk".equals(fmt)) {
            return entry.dallaaTashkeel != null && !entry.dallaaTashkeel.isEmpty() ? entry.dallaaTashkeel : (entry.dallaaAr != null ? entry.dallaaAr : Collections.emptyList());
        } else if ("en".equals(fmt) || "english".equals(fmt)) {
            return entry.dallaaEn != null ? entry.dallaaEn : Collections.emptyList();
        } else if ("ipa".equals(fmt) || "phonetic".equals(fmt)) {
            return entry.dallaaIpa != null ? entry.dallaaIpa : Collections.emptyList();
        }
        return entry.dallaaAr != null ? entry.dallaaAr : Collections.emptyList();
    }

    public List<String> dallaa(String name) {
        return dallaa(name, "plain");
    }

    public List<Models.PetName> dallaaInfo(String name) {
        Models.NameEntry entry = LookupIndices.lookup(name, customDataPath);
        if (entry == null || entry.dallaaAr == null || entry.dallaaAr.isEmpty()) {
            return Collections.emptyList();
        }
        List<Models.PetName> result = new ArrayList<>();
        for (int i = 0; i < entry.dallaaAr.size(); i++) {
            String ar = entry.dallaaAr.get(i);
            String tk = (entry.dallaaTashkeel != null && i < entry.dallaaTashkeel.size()) ? entry.dallaaTashkeel.get(i) : ar;
            String en = (entry.dallaaEn != null && i < entry.dallaaEn.size()) ? entry.dallaaEn.get(i) : "";
            String ipa = (entry.dallaaIpa != null && i < entry.dallaaIpa.size()) ? entry.dallaaIpa.get(i) : "";
            result.add(new Models.PetName(ar, tk, en, ipa));
        }
        return result;
    }

    public List<String> petNames(String name, String format) {
        return dallaa(name, format);
    }

    public List<String> petNames(String name) {
        return dallaa(name, "plain");
    }

    public String root(String name) {
        Models.NameEntry entry = LookupIndices.lookup(name, customDataPath);
        return (entry != null && entry.root != null && !"N/A".equalsIgnoreCase(entry.root)) ? entry.root : null;
    }

    public String origin(String name) {
        Models.NameEntry entry = LookupIndices.lookup(name, customDataPath);
        return entry != null ? entry.originType : null;
    }

    public List<String> famousFigures(String name, String lang) {
        Models.NameEntry entry = LookupIndices.lookup(name, customDataPath);
        if (entry == null) return Collections.emptyList();
        if (lang != null && lang.toLowerCase().startsWith("en")) {
            return entry.famousFiguresEn != null && !entry.famousFiguresEn.isEmpty() ? entry.famousFiguresEn : (entry.famousFiguresAr != null ? entry.famousFiguresAr : Collections.emptyList());
        }
        return entry.famousFiguresAr != null ? entry.famousFiguresAr : Collections.emptyList();
    }

    public List<String> famousFigures(String name) {
        return famousFigures(name, "ar");
    }

    public String trend(String name) {
        Models.NameEntry entry = LookupIndices.lookup(name, customDataPath);
        return entry != null ? entry.trendCategory : null;
    }

    public String correct(String name) {
        return Corrector.correct(name, customDataPath);
    }

    public Map<String, String> meaning(String name) {
        Models.NameEntry entry = LookupIndices.lookup(name, customDataPath);
        if (entry == null) return null;
        if ((entry.meaningAr == null || entry.meaningAr.isEmpty()) && (entry.meaningEn == null || entry.meaningEn.isEmpty())) {
            return null;
        }
        return Map.of("ar", entry.meaningAr != null ? entry.meaningAr : "", "en", entry.meaningEn != null ? entry.meaningEn : "");
    }

    public List<Models.NameInfo> families(int count, Models.FrequencyClass frequency, Models.Religion religion, String startsWith) {
        return SearchEngine.search(null, religion, Models.NameRole.FAMILY, frequency, startsWith, null, null, null, count, "corpus_share", customDataPath);
    }

    public List<Models.NameInfo> search(Models.Gender gender, Models.Religion religion, Models.NameRole role, Models.FrequencyClass frequency, String startsWith, String endsWith, String contains, Double minCorpusShare, int maxResults, String sortBy) {
        return SearchEngine.search(gender, religion, role, frequency, startsWith, endsWith, contains, minCorpusShare, maxResults, sortBy, customDataPath);
    }

    // Creative Methods

    public boolean isValid(String name) {
        Models.NameEntry entry = LookupIndices.lookup(name, customDataPath);
        return entry != null
                && Quality.isPersonalEntry(entry)
                && !Quality.isLowConfidenceEntry(entry);
    }

    /**
     * Gender of the person: the first personal, non-lineage given name.
     *
     * <p>Later tokens are father, grandfather, family — they do not vote. A
     * tie must not become male. Two-word compound lemmas (e.g. kunya "Abu X")
     * are recognized as one token, not two fragments.
     */
    public Models.GenderDetection detectGender(String fullName) {
        List<LookupIndices.CompoundToken> tokens = LookupIndices.compoundTokens(fullName, customDataPath);
        if (tokens.isEmpty()) return new Models.GenderDetection("neutral", 0.0);

        int skippedLineage = 0;
        for (int i = 0; i < tokens.size(); i++) {
            Models.NameEntry entry = tokens.get(i).entry;
            if (entry == null || !Quality.isPersonalEntry(entry) || Quality.isLowConfidenceEntry(entry)) continue;
            if (Quality.isLineageRole(entry)) {
                skippedLineage++;
                continue;
            }
            if (entry.gender == Models.Gender.NEUTRAL) {
                return new Models.GenderDetection("neutral", 0.6);
            }
            double confidence = (skippedLineage == 0 && i == 0) ? 1.0 : 0.85;
            return new Models.GenderDetection(entry.gender.getValue(), confidence);
        }
        return new Models.GenderDetection("neutral", 0.0);
    }

    /**
     * Religion of the person: the first given name, like gender.
     *
     * <p>A father, grandfather, or family surname from one community does not
     * override the person's own first name. Lineage tokens only vote if the
     * person's own name gives no distinctive signal. Two-word compound
     * lemmas (e.g. kunya "Abu X") are recognized as one token.
     */
    public Models.ReligionDetection detectReligion(String fullName) {
        List<LookupIndices.CompoundToken> tokens = LookupIndices.compoundTokens(fullName, customDataPath);
        if (tokens.isEmpty()) return new Models.ReligionDetection("neutral", 0.0);

        int skippedLineage = 0;
        for (int i = 0; i < tokens.size(); i++) {
            Models.NameEntry entry = tokens.get(i).entry;
            if (entry == null || !Quality.isPersonalEntry(entry) || Quality.isLowConfidenceEntry(entry)) continue;
            if (Quality.isLineageRole(entry)) {
                skippedLineage++;
                continue;
            }
            if (entry.religion == Models.Religion.NEUTRAL) continue;
            double confidence = (skippedLineage == 0 && i == 0) ? 1.0 : 0.9;
            return new Models.ReligionDetection(entry.religion.getValue(), confidence);
        }

        // The person's own given names carried no distinctive signal
        // (neutral or not found). Fall back to an aggregate vote across
        // every token, lineage included, rather than declaring neutral.
        double muslim = 0;
        double christian = 0;
        String first = null;

        for (LookupIndices.CompoundToken token : tokens) {
            Models.NameEntry entry = token.entry;
            if (entry == null || !Quality.isPersonalEntry(entry) || Quality.isLowConfidenceEntry(entry)) continue;
            if (entry.religion == Models.Religion.MUSLIM) {
                muslim++;
                if (first == null) first = "muslim";
            } else if (entry.religion == Models.Religion.CHRISTIAN) {
                christian++;
                if (first == null) first = "christian";
            }
        }

        if (muslim == 0 && christian == 0) return new Models.ReligionDetection("neutral", 0.0);
        double distinctive = muslim + christian;
        if (muslim > christian) return new Models.ReligionDetection("muslim", 0.5 * muslim / distinctive);
        if (christian > muslim) return new Models.ReligionDetection("christian", 0.5 * christian / distinctive);
        return new Models.ReligionDetection(first != null ? first : "neutral", 0.5);
    }

    public Models.RankInfo rank(String name) {
        Models.NameEntry entry = LookupIndices.lookup(name, customDataPath);
        if (entry == null) return null;

        List<Models.NameEntry> ranked = LookupIndices.getRanked(customDataPath);
        int total = ranked.size();

        for (int i = 0; i < total; i++) {
            if (ranked.get(i).ar.equals(entry.ar)) {
                int rankPos = i + 1;
                double percentile = (1.0 - (double)(rankPos - 1) / total) * 100.0;
                String desc = String.format("The #%d most common name in the Egyptian corpus", rankPos);
                if (rankPos <= 10) desc = "Top 10 — " + desc;
                else if (rankPos <= 100) desc = "Top 100 — " + desc;
                else if (rankPos <= 1000) desc = "Top 1000 — " + desc;

                Models.RankInfo info = new Models.RankInfo();
                info.rank = rankPos;
                info.percentile = Math.round(percentile * 100.0) / 100.0;
                info.corpusShare = String.format("%.4f%%", entry.corpusShare);
                info.description = desc;
                return info;
            }
        }
        return null;
    }

    public List<Models.ChainPart> analyzeChain(String fullName) {
        if (fullName == null || fullName.trim().isEmpty()) return List.of();
        String[] tokens = fullName.trim().split("\\s+");
        List<Models.ChainPart> parts = new ArrayList<>();
        int n = tokens.length;

        for (int i = 0; i < n; i++) {
            String t = tokens[i];
            Models.NameEntry entry = LookupIndices.lookup(t, customDataPath);
            int slot = i + 1;

            String roleLabel;
            String detail;

            if (i == 0) {
                roleLabel = "person";
                detail = "The individual's given name";
            } else if (i == n - 1 && entry != null && entry.role == Models.NameRole.FAMILY) {
                roleLabel = "family_name";
                detail = "Family/tribal surname";
            } else if (i == 1) {
                roleLabel = "father";
                detail = "Father's name";
            } else if (i == 2) {
                roleLabel = "grandfather";
                detail = "Paternal grandfather";
            } else if (i == 3) {
                roleLabel = "great_grandfather";
                detail = "Great-grandfather";
            } else {
                roleLabel = "ancestor";
                detail = "Ancestor (generation " + i + ")";
            }

            Models.ChainPart cp = new Models.ChainPart();
            cp.name = t;
            cp.slot = slot;
            cp.role = roleLabel;
            cp.detail = detail;
            parts.add(cp);
        }

        return parts;
    }

    public Models.UniquenessScore uniqueness(String fullName) {
        if (fullName == null || fullName.trim().isEmpty()) {
            Models.UniquenessScore u = new Models.UniquenessScore();
            u.score = 0.5;
            u.label = "unknown";
            u.note = "Empty input";
            return u;
        }

        String[] tokens = fullName.trim().split("\\s+");
        List<Double> shares = new ArrayList<>();
        int unknownCount = 0;

        for (String t : tokens) {
            Models.NameEntry entry = LookupIndices.lookup(t, customDataPath);
            if (entry != null) shares.add(entry.corpusShare);
            else unknownCount++;
        }

        if (shares.isEmpty()) {
            Models.UniquenessScore u = new Models.UniquenessScore();
            u.score = 1.0;
            u.label = "unknown";
            u.note = "None of the name parts are in the Egyptian corpus";
            return u;
        }

        double logSum = 0;
        for (double s : shares) logSum += Math.log(Math.max(s, 1e-9));
        double logMean = logSum / shares.size();

        double maxLog = 2.6;
        double minLog = -9.2;
        double score = 1.0 - (logMean - minLog) / (maxLog - minLog);
        score = Math.max(0.0, Math.min(1.0, score));
        score = Math.min(1.0, score + unknownCount * 0.15);

        String label;
        String note;
        if (score < 0.2) {
            label = "extremely_common";
            note = "Each part is among the most common names nationally";
        } else if (score < 0.4) {
            label = "common";
            note = "Well-known name parts with high national frequency";
        } else if (score < 0.6) {
            label = "moderate";
            note = "A mix of common and less common name parts";
        } else if (score < 0.8) {
            label = "distinctive";
            note = "Contains uncommon or regionally specific names";
        } else {
            label = "highly_unique";
            note = "Rare name combination — distinctive family heritage";
        }

        Models.UniquenessScore u = new Models.UniquenessScore();
        u.score = Math.round(score * 1000.0) / 1000.0;
        u.label = label;
        u.note = note;
        return u;
    }

    public Map<String, Object> stats() {
        DataLoader.DataBundle meta = DataLoader.loadBundle(customDataPath);
        List<Models.NameEntry> entries = LookupIndices.getAll(customDataPath);

        Map<String, Object> map = new HashMap<>();
        map.put("version", meta.version);
        map.put("corpus_tokens", meta.corpusTokens);
        map.put("corpus_students", meta.corpusStudents);
        map.put("cohort_years", meta.cohortYears);
        map.put("total_names", entries.size());
        map.put("given_names", entries.stream().filter(e -> e.role == Models.NameRole.GIVEN).count());
        map.put("family_names", entries.stream().filter(e -> e.role == Models.NameRole.FAMILY).count());
        map.put("male_names", entries.stream().filter(e -> e.gender == Models.Gender.MALE).count());
        map.put("female_names", entries.stream().filter(e -> e.gender == Models.Gender.FEMALE).count());
        return map;
    }

    public static class EgyNames extends EgyptianNames {
        public EgyNames() { super(); }
        public EgyNames(Long seed) { super(seed); }
        public EgyNames(Long seed, String customDataPath) { super(seed, customDataPath); }
    }
}
