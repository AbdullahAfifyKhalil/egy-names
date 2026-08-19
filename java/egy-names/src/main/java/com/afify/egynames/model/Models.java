package com.afify.egynames.model;

import java.util.Collections;
import java.util.List;

public class Models {

    public enum Gender {
        MALE("male"),
        FEMALE("female"),
        NEUTRAL("neutral");

        private final String value;
        Gender(String value) { this.value = value; }
        public String getValue() { return value; }

        public static Gender fromCode(String code) {
            if ("m".equalsIgnoreCase(code)) return MALE;
            if ("f".equalsIgnoreCase(code)) return FEMALE;
            return NEUTRAL;
        }

        public static Gender fromString(String str) {
            if (str == null) return null;
            if ("male".equalsIgnoreCase(str) || "m".equalsIgnoreCase(str)) return MALE;
            if ("female".equalsIgnoreCase(str) || "f".equalsIgnoreCase(str)) return FEMALE;
            if ("neutral".equalsIgnoreCase(str) || "n".equalsIgnoreCase(str)) return NEUTRAL;
            return null;
        }
    }

    public enum Religion {
        MUSLIM("muslim"),
        CHRISTIAN("christian"),
        NEUTRAL("neutral");

        private final String value;
        Religion(String value) { this.value = value; }
        public String getValue() { return value; }

        public static Religion fromCode(String code) {
            if ("m".equalsIgnoreCase(code)) return MUSLIM;
            if ("c".equalsIgnoreCase(code)) return CHRISTIAN;
            return NEUTRAL;
        }

        public static Religion fromString(String str) {
            if (str == null) return null;
            if ("muslim".equalsIgnoreCase(str) || "m".equalsIgnoreCase(str)) return MUSLIM;
            if ("christian".equalsIgnoreCase(str) || "c".equalsIgnoreCase(str)) return CHRISTIAN;
            if ("neutral".equalsIgnoreCase(str) || "n".equalsIgnoreCase(str)) return NEUTRAL;
            return null;
        }
    }

    public enum NameRole {
        GIVEN("given"),
        FAMILY("family");

        private final String value;
        NameRole(String value) { this.value = value; }
        public String getValue() { return value; }

        public static NameRole fromCode(String code) {
            return "f".equalsIgnoreCase(code) ? FAMILY : GIVEN;
        }

        public static NameRole fromString(String str) {
            if (str == null) return null;
            if ("family".equalsIgnoreCase(str) || "f".equalsIgnoreCase(str)) return FAMILY;
            return GIVEN;
        }
    }

    public enum FrequencyClass {
        COMMON("common"),
        NORMAL("normal"),
        RARE("rare");

        private final String value;
        FrequencyClass(String value) { this.value = value; }
        public String getValue() { return value; }

        public static FrequencyClass fromCode(String code) {
            if ("c".equalsIgnoreCase(code)) return COMMON;
            if ("n".equalsIgnoreCase(code)) return NORMAL;
            return RARE;
        }

        public static FrequencyClass fromString(String str) {
            if (str == null) return null;
            if ("common".equalsIgnoreCase(str) || "c".equalsIgnoreCase(str)) return COMMON;
            if ("normal".equalsIgnoreCase(str) || "n".equalsIgnoreCase(str)) return NORMAL;
            if ("rare".equalsIgnoreCase(str) || "r".equalsIgnoreCase(str)) return RARE;
            return null;
        }
    }

    public static class NameEntry {
        public String ar;
        public String en;
        public Gender gender;
        public Religion religion;
        public NameRole role;
        public List<String> arVariants;
        public List<String> enVariants;
        public List<Double> slotPcts;
        public double corpusShare;
        public FrequencyClass frequency;
        public String tashkeel;
        public String meaningAr;
        public String meaningEn;
    }

    public static class NameInfo {
        public String ar;
        public String en;
        public String gender;
        public String religion;
        public String role;
        public String frequencyClass;
        public double corpusShare;
        public String tashkeel;
        public String meaningAr;
        public String meaningEn;
        public List<String> arVariants;
        public List<String> enVariants;
        public List<Double> slotDistribution;

        public static NameInfo fromEntry(NameEntry entry) {
            NameInfo info = new NameInfo();
            info.ar = entry.ar;
            info.en = entry.en;
            info.gender = entry.gender.getValue();
            info.religion = entry.religion.getValue();
            info.role = entry.role.getValue();
            info.frequencyClass = entry.frequency.getValue();
            info.corpusShare = entry.corpusShare;
            info.tashkeel = entry.tashkeel;
            info.meaningAr = (entry.meaningAr != null && !entry.meaningAr.isEmpty()) ? entry.meaningAr : null;
            info.meaningEn = (entry.meaningEn != null && !entry.meaningEn.isEmpty()) ? entry.meaningEn : null;
            info.arVariants = Collections.unmodifiableList(entry.arVariants);
            info.enVariants = Collections.unmodifiableList(entry.enVariants);
            info.slotDistribution = Collections.unmodifiableList(entry.slotPcts);
            return info;
        }
    }

    public static class GeneratedName {
        public String ar;
        public String en;
        public List<String> partsAr;
        public List<String> partsEn;

        @Override
        public String toString() {
            return ar + "  --  " + en;
        }
    }

    public static class ChainPart {
        public String name;
        public int slot;
        public String role;
        public String detail;

        @Override
        public String toString() {
            return "Slot " + slot + ": " + name + " (" + role + " - " + detail + ")";
        }
    }

    public static class GenderDetection {
        public String gender;
        public double confidence;

        public GenderDetection(String gender, double confidence) {
            this.gender = gender;
            this.confidence = confidence;
        }

        @Override
        public String toString() {
            return String.format("GenderDetection(gender=%s, confidence=%.2f)", gender, confidence);
        }
    }

    public static class ReligionDetection {
        public String religion;
        public double confidence;

        public ReligionDetection(String religion, double confidence) {
            this.religion = religion;
            this.confidence = confidence;
        }

        @Override
        public String toString() {
            return String.format("ReligionDetection(religion=%s, confidence=%.2f)", religion, confidence);
        }
    }

    public static class RankInfo {
        public int rank;
        public double percentile;
        public String corpusShare;
        public String description;

        @Override
        public String toString() {
            return String.format("Rank #%d (%.2f%%) - %s", rank, percentile, description);
        }
    }

    public static class UniquenessScore {
        public double score;
        public String label;
        public String note;

        @Override
        public String toString() {
            return String.format("Uniqueness(score=%.3f, label=%s, note=%s)", score, label, note);
        }
    }
}
