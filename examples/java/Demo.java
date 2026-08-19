package com.example;

import com.afify.egynames.EgyptianNames;
import com.afify.egynames.model.Models;
import java.util.List;

public class Demo {
    public static void main(String[] args) {
        EgyptianNames en = new EgyptianNames();

        System.out.println("============================================================");
        System.out.println(" Egyptian Names (egy-names) - Java Showcase");
        System.out.println("============================================================");

        // 1. Generation
        System.out.println("\n1. Name Generation:");
        List<Models.GeneratedName> names = en.generate(3, 3, "male", "muslim", -1);
        for (Models.GeneratedName n : names) {
            System.out.println("   " + n.ar + "  (" + n.en + ")");
        }

        // 2. Translation
        System.out.println("\n2. Transliteration:");
        System.out.println("   'محمد أحمد علي' -> " + en.translate("محمد أحمد علي"));

        // 3. Correction
        System.out.println("\n3. Correction:");
        System.out.println("   'احمد مصطفا عبد الرحيم' -> " + en.correct("احمد مصطفا عبد الرحيم"));

        // 4. Tashkeel
        System.out.println("\n4. Tashkeel:");
        System.out.println("   'محمد عبدالرحمن' -> " + en.tashkeel("محمد عبدالرحمن"));

        // 5. Splitting
        System.out.println("\n5. Splitting:");
        System.out.println("   'محمدأحمدعليحسن' -> " + en.split("محمدأحمدعليحسن"));
    }
}
