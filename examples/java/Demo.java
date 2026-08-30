package com.example;

import com.afify.egynames.EgyptianNames;
import com.afify.egynames.model.Models;
import java.util.List;
import java.util.Map;

public class Demo {
    public static void main(String[] args) {
        EgyptianNames en = new EgyptianNames();

        System.out.println("============================================================");
        System.out.println(" Egyptian Names (egy-names) 0.3.6 — Java");
        System.out.println("============================================================");

        System.out.println("\n1. Generate a grounded chain:");
        List<Models.GeneratedName> names = en.generate(3, "female", "muslim");
        for (Models.GeneratedName n : names) {
            System.out.println("   " + n.ar + "  (" + n.en + ")");
        }

        System.out.println("\n2. Translate:");
        System.out.println("   " + en.translate("محمد أحمد علي الشناوي"));

        System.out.println("\n3. Correct:");
        System.out.println("   " + en.correct("احمد مصطفا عبد الرحيم"));

        System.out.println("\n4. Tashkeel and IPA:");
        System.out.println("   Standard: " + en.tashkeel("محمد عبدالرحمن"));
        System.out.println("   Egyptian: " + en.tashkeelEg("محمد عبدالرحمن"));
        System.out.println("   IPA std:  " + en.ipa("جمال"));
        System.out.println("   IPA eg:   " + en.ipaEg("جمال"));

        System.out.println("\n5. Split a concatenated dump:");
        System.out.println("   " + en.split("محمدأحمدعليحسنالشناوي"));

        System.out.println("\n6. Pet names and figures:");
        System.out.println("   dallaa: " + en.dallaa("محمد", "tashkeel"));
        List<String> figures = en.famousFigures("محمد", "en");
        System.out.println("   figures: " + figures.subList(0, Math.min(2, figures.size())));

        System.out.println("\n7. Lookup:");
        System.out.println("   root=" + en.root("محمد") + " | origin=" + en.origin("محمد") + " | trend=" + en.trend("محمد"));
        Map<String, String> meaning = en.meaning("محمد");
        if (meaning != null) {
            System.out.println("   meaning: " + meaning.get("en"));
        }

        System.out.println("\n8. Validity — personal names only:");
        System.out.println("   isValid(\"محمد\")  = " + en.isValid("محمد"));
        System.out.println("   isValid(\"Mahmoud\") = " + en.isValid("Mahmoud"));
        System.out.println("   isValid(\"الله\")   = " + en.isValid("الله") + "  // in the index, not a person");

        System.out.println("\n9. First personal token wins:");
        System.out.println("   " + en.detectGender("فاطمة محمد علي"));
        System.out.println("   " + en.detectReligion("مينا جرجس بطرس"));

        System.out.println("\n10. Chain, rank, uniqueness:");
        for (Models.ChainPart p : en.analyzeChain("محمد أحمد علي الشناوي")) {
            System.out.println("   Slot " + p.slot + ": " + p.name + " — " + p.role);
        }
        Models.RankInfo rank = en.rank("محمد");
        Models.UniquenessScore uniq = en.uniqueness("محمد أحمد علي الشناوي");
        System.out.println("   rank=#" + rank.rank + "  uniqueness=" + uniq.score + " (" + uniq.label + ")");
    }
}
