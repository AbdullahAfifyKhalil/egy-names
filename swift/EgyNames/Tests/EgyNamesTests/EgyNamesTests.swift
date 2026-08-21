import XCTest
@testable import EgyNames

final class EgyNamesTests: XCTestCase {
    func testAllOperations() throws {
        let en = EgyptianNames()

        // 1. Data Stats
        let stats = en.stats()
        let total = stats["total_names"] as? Int ?? 0
        XCTAssertGreaterThan(total, 30000, "Loaded names should exceed 30,000")

        // 2. Generation
        let generated = en.generate(count: 3, length: 3, gender: "male", religion: "muslim")
        XCTAssertEqual(generated.count, 3)
        for g in generated {
            XCTAssertFalse(g.ar.isEmpty)
            XCTAssertFalse(g.en.isEmpty)
        }

        // 3. Translation
        let translated = en.translate("محمد أحمد علي")
        XCTAssertTrue(translated.contains("Mohamed") || translated.contains("Muhammad"))

        // 4. Correction
        let corrected = en.correct("احمد مصطفا عبد الرحيم")
        XCTAssertTrue(corrected.contains("أحمد"))
        XCTAssertTrue(corrected.contains("مصطفى"))
        XCTAssertTrue(corrected.contains("عبدالرحيم"))

        // 5. Tashkeel
        let tashkeeled = en.tashkeel("محمد عبدالرحمن")
        XCTAssertTrue(tashkeeled.contains("مُحَمَّد"))
        XCTAssertTrue(tashkeeled.contains("الرَّحْمَن"))

        // 5b. 11D Features
        let tkEg = en.tashkeelEg("محمد")
        XCTAssertFalse(tkEg.isEmpty)
        let ipaStd = en.ipa("جمال", dialect: "standard")
        XCTAssertTrue(ipaStd.hasPrefix("/"))
        let ipaEg = en.ipaEg("جمال")
        XCTAssertTrue(ipaEg.hasPrefix("["))
        let dl = en.dallaa("محمد")
        XCTAssertTrue(dl.contains("ميدو"))
        let rt = en.root("محمد")
        XCTAssertEqual(rt, "ح-م-د")
        let ot = en.origin("محمد")
        XCTAssertEqual(ot, "arabic_classical")
        let ff = en.famousFigures("محمد")
        XCTAssertFalse(ff.isEmpty)
        let tr = en.trend("محمد")
        XCTAssertEqual(tr, "classic_timeless")

        // 6. Splitting / DP Segmentation
        let parts = en.split("محمدأحمدعليحسنالشاذلي")
        XCTAssertGreaterThanOrEqual(parts.count, 3)

        // 7. Demographics
        let g = en.detectGender("مريم إبراهيم حسن")
        XCTAssertEqual(g.gender, "female")

        let r = en.detectReligion("جورج بطرس سمير ميخائيل")
        XCTAssertEqual(r.religion, "christian")

        // 8. Chain Analysis
        let chain = en.analyzeChain("محمد أحمد علي حسن الشاذلي")
        XCTAssertEqual(chain.count, 5)
        XCTAssertEqual(chain[0].role, "person")
        XCTAssertEqual(chain[4].role, "family_name")
    }
}
