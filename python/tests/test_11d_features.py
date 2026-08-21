import pytest
from egy_names import EgyNames

@pytest.fixture(scope="module")
def en():
    return EgyNames()

def test_tashkeel_dialects(en):
    # Standard vs Egyptian Tashkeel
    std = en.tashkeel("محمد", dialect="standard")
    eg = en.tashkeel("محمد", dialect="egyptian")
    eg_direct = en.tashkeel_eg("محمد")
    assert std != ""
    assert eg != ""
    assert eg == eg_direct

def test_ipa_transcriptions(en):
    # Standard vs Egyptian IPA
    ipa_std = en.ipa("جمال", dialect="standard")
    ipa_eg = en.ipa("جمال", dialect="egyptian")
    ipa_eg_direct = en.ipa_eg("جمال")
    
    assert ipa_std != ""
    assert ipa_eg != ""
    assert ipa_eg == ipa_eg_direct
    assert ipa_std.startswith("/") and ipa_std.endswith("/")
    assert ipa_eg.startswith("[") and ipa_eg.endswith("]")

def test_dallaa_and_pet_names(en):
    # Egyptian pet names (dallaa)
    dallaa_mohamed = en.dallaa("محمد")
    pet_mohamed = en.pet_names("محمد")
    assert isinstance(dallaa_mohamed, list)
    assert dallaa_mohamed == pet_mohamed
    assert "ميدو" in dallaa_mohamed or "حمو" in dallaa_mohamed

    # Tashkeel, English, IPA formats
    dl_tk = en.dallaa("محمد", format="tashkeel")
    dl_en = en.dallaa("محمد", format="en")
    dl_ipa = en.dallaa("محمد", format="ipa")
    assert len(dl_tk) == len(dallaa_mohamed)
    assert len(dl_en) == len(dallaa_mohamed)
    assert len(dl_ipa) == len(dallaa_mohamed)
    assert any("Mido" in x for x in dl_en)

    # dallaa_info objects
    info_list = en.dallaa_info("محمد")
    assert len(info_list) == len(dallaa_mohamed)
    assert info_list[0].ar != ""
    assert info_list[0].en != ""
    assert info_list[0].ipa != ""

def test_roots_and_origins(en):
    # Roots
    root_mohamed = en.root("محمد")
    assert root_mohamed in ["ح-م-د", "ح م د", "حمد"] or root_mohamed is not None

    # Origin
    origin_mohamed = en.origin("محمد")
    assert origin_mohamed is not None

def test_famous_figures_and_trends(en):
    # Famous figures (Arabic & English)
    figures_ar = en.famous_figures("محمد", lang="ar")
    figures_en = en.famous_figures("محمد", lang="en")
    assert isinstance(figures_ar, list)
    assert isinstance(figures_en, list)
    assert len(figures_ar) > 0
    assert any("صلاح" in f or "علي باشا" in f for f in figures_ar)
    assert any("Salah" in f or "Mohamed Ali" in f for f in figures_en)

    # Trend category
    trend = en.trend("محمد")
    assert trend in ["classic_timeless", "rising_modern", "vintage_heritage", "rare_toponymic", None]

def test_full_chain_ipa(en):
    full_ipa = en.ipa("محمد أحمد علي", dialect="egyptian")
    assert full_ipa.startswith("[") and full_ipa.endswith("]")
    assert len(full_ipa.split()) >= 3
