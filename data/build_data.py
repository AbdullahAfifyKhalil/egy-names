#!/usr/bin/env python3
"""Build the compressed data bundle for the egyptian-names library.

Reads:
  - release 0.1/result/data_phase_11.csv
  - release 0.1/result/data_phase4_(correction-index).csv

Outputs:
  - library building/data/names.json.gz
  - library building/python/src/egyptian_names/data/names.json.gz  (copy)
"""

from __future__ import annotations

import csv
import gzip
import json
import shutil
import sys
from pathlib import Path

csv.field_size_limit(sys.maxsize)

ROOT = Path(__file__).resolve().parents[2]
P11 = ROOT / "release 0.1" / "result" / "data_phase_11.csv"
CORR = ROOT / "release 0.1" / "result" / "data_phase4_(correction-index).csv"

OUT_DIR = Path(__file__).resolve().parent
OUT_GZ = OUT_DIR / "names.json.gz"

PY_DATA_DIR = ROOT / "library building" / "python" / "src" / "egyptian_names" / "data"


def build() -> None:
    # ── 1. Load Phase 11 final library ──
    names = []
    with open(P11, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            names.append({
                "a": r["correct_ar_name"],
                "e": r["correct_en_name"],
                "g": r["gender"][0],       # m / f / n
                "r": r["religion"][0],      # m / c / n
                "l": r["name_role"][0],     # g / f
                "av": r["ar_variants"],
                "ev": r["english_variants"],
                "p": [
                    round(float(r["first_name_percentage"]), 2),
                    round(float(r["second_name_percentage"]), 2),
                    round(float(r["third_name_percentage"]), 2),
                    round(float(r["fourth_name_percentage"]), 2),
                    round(float(r["fifth_name_percentage"]), 2),
                    round(float(r["sixth_name_percentage"]), 2),
                    round(float(r["seventh_name_percentage"]), 2),
                    round(float(r["eighth_or_later_name_percentage"]), 2),
                ],
                "tp": round(float(r["total_count_percentage"]), 6),
                "fc": r["frequency_class"][0],   # c / n / r
                "t": r["name_tashkeel"],
                "ma": r["meaning_ar"],
                "me": r["meaning_en"],
            })

    print(f"Loaded {len(names)} name entries from Phase 11.")

    # ── 2. Load correction index ──
    corrections: dict[str, str] = {}
    if CORR.exists():
        with open(CORR, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                sf = r.get("surface_form", "").strip()
                cn = r.get("canonical_name", "").strip()
                if sf and cn and sf != cn:
                    corrections[sf] = cn
    print(f"Loaded {len(corrections)} correction entries.")

    # ── 3. Build the bundle ──
    bundle = {
        "version": "0.1.0",
        "corpus_tokens": 11032461,
        "corpus_students": 2465366,
        "cohort_years": [2024, 2025, 2026],
        "names": names,
        "corrections": corrections,
    }

    payload = json.dumps(bundle, ensure_ascii=False, separators=(",", ":"))
    raw_size = len(payload.encode("utf-8"))

    with gzip.open(OUT_GZ, "wt", encoding="utf-8", compresslevel=9) as gz:
        gz.write(payload)

    gz_size = OUT_GZ.stat().st_size
    print(f"Raw JSON: {raw_size:,} bytes ({raw_size / 1024 / 1024:.2f} MB)")
    print(f"Gzipped:  {gz_size:,} bytes ({gz_size / 1024 / 1024:.2f} MB)")
    print(f"Ratio:    {gz_size / raw_size * 100:.1f}%")

    # ── 4. Copy into Python package data dir ──
    PY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    dest = PY_DATA_DIR / "names.json.gz"
    shutil.copy2(OUT_GZ, dest)
    print(f"Copied to {dest}")

    print("Data bundle build complete.")


if __name__ == "__main__":
    build()
