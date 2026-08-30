"""Export the current book to the Hugging Face dataset's CSV/parquet schema.

Regenerates data/final_canonical_names.{csv,parquet} to match this
session's fixes (collision resolution, compound-spacing corrections,
لامع gender fix) and adds two quality-audit columns
(`is_personal_name`, `is_low_confidence`) so downstream users can
reproduce the same filtering egy-names applies internally.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd  # noqa: E402

from egy_names._index import get_all  # noqa: E402
from egy_names._quality import is_low_confidence_entry, is_personal_entry  # noqa: E402

OUT_DIR = Path(__file__).parent.parent.parent / "hf_export"
OUT_DIR.mkdir(exist_ok=True)


def _v(x):
    return x.value if hasattr(x, "value") else x


def main() -> None:
    entries = get_all()
    rows = []
    for e in entries:
        rows.append(
            {
                "name_ar": e.ar,
                "name_en": e.en,
                "gender": e.gender.value if hasattr(e.gender, "value") else e.gender,
                "religion": e.religion.value if hasattr(e.religion, "value") else e.religion,
                "role": e.role.value if hasattr(e.role, "value") else e.role,
                "ar_variants": "|".join(e.ar_variants),
                "en_variants": "|".join(e.en_variants),
                **{f"slot{i+1}_pct": e.slot_pcts[i] if i < len(e.slot_pcts) else None for i in range(8)},
                "corpus_share_pct": e.corpus_share * 100,
                "frequency_class": _v(e.frequency),
                "tashkeel_standard": e.tashkeel,
                "tashkeel_eg": e.tashkeel_eg,
                "tashkeel": e.tashkeel,
                "ipa_standard": e.ipa_standard,
                "ipa_eg": e.ipa_eg,
                "meaning_ar": e.meaning_ar,
                "meaning_en": e.meaning_en,
                "dallaa": e.dallaa_ar,
                "dallaa_ar": e.dallaa_ar,
                "dallaa_tashkeel": e.dallaa_tashkeel,
                "dallaa_en": e.dallaa_en,
                "dallaa_ipa": e.dallaa_ipa,
                "root": e.root,
                "origin_type": e.origin_type,
                "famous_figures": e.famous_figures_ar,
                "famous_figures_ar": e.famous_figures_ar,
                "famous_figures_en": e.famous_figures_en,
                "trend_category": e.trend_category,
                "is_personal_name": is_personal_entry(e),
                "is_low_confidence": is_low_confidence_entry(e),
            }
        )

    df = pd.DataFrame(rows)
    csv_path = OUT_DIR / "final_canonical_names.csv"
    parquet_path = OUT_DIR / "final_canonical_names.parquet"
    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)
    print(f"wrote {len(df)} rows -> {csv_path}, {parquet_path}")
    print("is_personal_name False count:", (~df["is_personal_name"]).sum())
    print("is_low_confidence True count:", df["is_low_confidence"].sum())


if __name__ == "__main__":
    main()
