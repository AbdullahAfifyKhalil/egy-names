---
language:
- ar
- en
license: mit
tags:
- egyptian
- arabic
- names
- onomastics
- text-classification
- gender-classification
- religion-classification
- tabular-classification
- egy-names
datasets:
- Abdullah-afify/egyptian-names
pipeline_tag: text-classification
library_name: scikit-learn
---

# egy-names ML Fallback Classifier

**A precision-calibrated fallback model for Egyptian names that are not in the [`egy-names`](https://afify.co/egy-names) catalog.**

`egy-names` is a book-first engine: 44,626 hand-annotated Egyptian name lemmas with empirical gender, religion, generational-slot, and role labels, derived from 15.88M+ real name records ([dataset](https://huggingface.co/datasets/Abdullah-afify/egyptian-names)). The book is always tried first and is always the ground truth.

This model exists **only** for the names the book has never seen — foreign surnames, rare spellings, brand-new coinages. It infers `gender`, `religion`, and `role` from morphology and character n-grams, and every prediction it returns is explicitly labeled `inferred: true` so a caller can never confuse a guess with an attested fact.

## Why this model is different from a typical classifier

Most name-classification models are tuned to maximize aggregate accuracy. This one is tuned to **maximize precision at the moment it chooses to speak**, and to **abstain (`unknown` / `neutral`) rather than guess** when it isn't confident enough. That distinction matters for names, where a confidently wrong gender or religion label is worse than no label at all.

Abstention thresholds were not picked by feel — they were measured directly with a held-out precision-at-threshold calibration script and recalibrated after an initial pass under-delivered on its own promise (`role="given"` was returning only 81.8% precision, `religion="christian"` only 89.4%, at the original cutoffs):

| Class | Abstention threshold | Measured precision at that threshold |
|---|---|---|
| gender = male | p ≥ 0.70 | 93.3% |
| gender = female | p ≥ 0.70 | 95.5% |
| religion = muslim | p ≥ 0.85 | 96.6% |
| religion = christian | p ≥ 0.90 | 95.1% |
| role = given | p ≥ 0.88 | 93.0% |

## Architecture

- **Features:** character n-grams (TF-IDF) over the normalized surface form, plus hand-built morphological flags (script, common Arabic/English prefixes and suffixes, length, diacritic presence).
- **Classifiers:** three independent multinomial logistic regression heads — one each for gender, religion, and role — trained on the book's own 44,626 lemmas (excluding low-confidence/fabricated rows) as ground truth.
- **Rule pre-checks:** a small set of high-precision prefix/suffix rules (e.g. `عبد`-prefixed compounds → male/Muslim with very high confidence) run before the statistical model and short-circuit it when they fire — the same rule table the book-index detectors use, shared via [`logic_config.json`](https://github.com/AbdullahAfifyKhalil/egy-names/blob/main/data/logic_config.json).
- **Nearest-neighbor grounding:** every inferred name is also matched to its closest known book entry by Levenshtein distance, so callers can see *why* the model guessed what it guessed.
- **Abstention:** below the calibrated threshold, the model returns `unknown` (religion/role) or `neutral` (gender) rather than force a label.

## Files

- `infer_model.json.gz` — the exported model weights (TF-IDF vocabulary/IDF, logistic regression coefficients for all three heads) in a small, dependency-free JSON format, runnable from any language without needing scikit-learn at inference time.

## Intended use

Fallback-only inference for names absent from the `egy-names` catalog, inside the [`egy-names`](https://github.com/AbdullahAfifyKhalil/egy-names) Python SDK's `identify()`/`identify_all()` API. Not intended as a standalone general-purpose name classifier outside that context — it was trained and calibrated specifically against Egyptian-Arabic naming patterns.

The book is always tried first. This model can still be wrong. Guesses are marked `inferred: true`. When confidence is low, it abstains.

## Training data

[`Abdullah-afify/egyptian-names`](https://huggingface.co/datasets/Abdullah-afify/egyptian-names) — the same 44,626-lemma canonical catalog that powers the `egy-names` library, filtered to exclude non-personal and low-confidence/fabricated rows before training.

## License

MIT — free for academic, commercial, and research use.

```bibtex
@misc{afify2026egynames_fallback,
  author       = {Abdullah Afify},
  title        = {egy-names ML Fallback Classifier},
  year         = {2026},
  publisher    = {Hugging Face},
  howpublished = {\url{https://huggingface.co/Abdullah-afify/egy-names-fallback-classifier}}
}
```
