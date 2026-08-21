package com.afify.egynames;

import com.afify.egynames.model.Models;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class EgyptianNamesTest {

    private static EgyptianNames en;

    @BeforeAll
    public static void setUp() {
        en = new EgyptianNames();
    }

    @Test
    public void testStats() {
        Map<String, Object> stats = en.stats();
        assertNotNull(stats);
        int total = (int) stats.get("total_names");
        assertTrue(total > 30000, "Loaded names should exceed 30,000");
    }

    @Test
    public void testTashkeelAnd11D() {
        String tk = en.tashkeel("محمد عبدالرحمن");
        assertTrue(tk.contains("مُحَمَّد"));
        assertTrue(tk.contains("الرَّحْمَن"));

        String tkEg = en.tashkeelEg("محمد");
        assertFalse(tkEg.isEmpty());

        String ipaStd = en.ipa("جمال", "standard");
        assertTrue(ipaStd.startsWith("/"));

        String ipaEg = en.ipaEg("جمال");
        assertTrue(ipaEg.startsWith("["));

        List<String> dallaa = en.dallaa("محمد");
        assertTrue(dallaa.contains("ميدو"));

        String root = en.root("محمد");
        assertEquals("ح-م-د", root);

        String origin = en.origin("محمد");
        assertEquals("arabic_classical", origin);

        List<String> figures = en.famousFigures("محمد");
        assertFalse(figures.isEmpty());

        String trend = en.trend("محمد");
        assertEquals("classic_timeless", trend);
    }

    @Test
    public void testGenerationAndDemographics() {
        List<Models.GeneratedName> names = en.generate(3, "male", "muslim");
        assertEquals(3, names.size());

        Models.GenderDetection g = en.detectGender("مريم إبراهيم حسن");
        assertEquals("female", g.gender);

        Models.ReligionDetection r = en.detectReligion("جورج بطرس سمير ميخائيل");
        assertEquals("christian", r.religion);
    }
}
