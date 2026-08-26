package com.example;

import com.afify.egynames.EgyptianNames;
import com.afify.egynames.model.Models;
import java.util.List;
import java.util.Map;

public class Demo {
    public static void main(String[] args) {
        EgyptianNames en = new EgyptianNames();

        System.out.println("============================================================");
        System.out.println(" Egyptian Names (egy-names) v0.3.2 — Java Showcase");
        System.out.println("============================================================");

        System.out.println("\n1. Name Generation:");
        List<Models.GeneratedName> names = en.generate(3, "female", "muslim");
        for (Models.GeneratedName n : names) {
            System.out.println("   " + n.ar + "  (" + n.en + ")");
        }

        System.out.println("\n2. Transliteration:");
        System.out.println("   'محمد أحمد علي الشناوي' -> " + en.translate("محمد أحمد علي الشناوي"));

        System.out.println("\n3. Orthographic Correction:");
        System.out.println("   'احمد مصطفا عبد الرحيم' -> " + en.correct("احمد مصطفا عبد الرحيم"));

        System.out.println("\n4. Dual Tashkeel & IPA:");
        System.out.println("   Standard: " + en.tashkeel("محمد عبدالرحمن"));
        System.out.println("   Egyptian: " + en.tashkeelEg("محمد عبدالرحمن"));
        System.out.println("   IPA std:  " + en.ipa("جمال"));
        System.out.println("   IPA eg:   " + en.ipaEg("جمال"));

        System.out.println("\n5. Splitting concatenated names:");
        System.out.println("   " + en.split("محمدأحمدعليحسنالشناوي"));

        System.out.println("\n6. Pet names & famous figures:");
        System.out.println("   dallaa: " + en.dallaa("محمد", "tashkeel"));
        List<String> figures = en.famousFigures("محمد", "en");
        System.out.println("   figures: " + figures.subList(0, Math.min(2, figures.size())));

        System.out.println("\n7. 14D lookup:");
        System.out.println("   root=" + en.root("محمد") + " | origin=" + en.origin("محمد") + " | trend=" + en.trend("محمد"));
        Map<String, String> meaning = en.meaning("محمد");
        if (meaning != null) {
            System.out.println("   meaning: " + meaning.get("en"));
        }

        System.out.println("\n8. Demographics:");
        System.out.println("   " + en.detectGender("فاطمة الزهراء"));
        System.out.println("   " + en.detectReligion("مينا جرجس بطرس"));

        System.out.println("\n9. Chain analysis, rank, uniqueness:");
        for (Models.ChainPart p : en.analyzeChain("محمد أحمد علي الشناوي")) {
            System.out.println("   Slot " + p.slot + ": " + p.name + " — " + p.role);
        }
        Models.RankInfo rank = en.rank("محمد");
        Models.UniquenessScore uniq = en.uniqueness("محمد أحمد علي الشناوي");
        System.out.println("   rank=#" + rank.rank + "  uniqueness=" + uniq.score + " (" + uniq.label + ")");
    }
}
