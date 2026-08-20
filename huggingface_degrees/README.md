---
language:
- ar
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- tabular-classification
- tabular-regression
- text-classification
- feature-extraction
task_ids:
- named-entity-recognition
- text-scoring
pretty_name: Egyptian High School Students Grades & Degrees (2024–2026)
tags:
- arabic
- egypt
- education
- high-school
- thanawya-amma
- grades
- degrees
- national-results
- onomastics
- afify-corporation
license: mit
configs:
- config_name: default
  data_files: "data/high_school_degrees_all_years.parquet"
- config_name: all_years
  data_files: "data/high_school_degrees_all_years.parquet"
- config_name: year_2024
  data_files: "data/high_school_degrees_2024.parquet"
- config_name: year_2025
  data_files: "data/high_school_degrees_2025.parquet"
- config_name: year_2026
  data_files: "data/high_school_degrees_2026.parquet"
---

# 🇪🇬 Egyptian High School (Thanawya Amma) Students Degrees (2024–2026)
### *A Large-Scale National Demographic and Educational Dataset of 2,465,366 Student Records*

Published and maintained by **[Afify Corporation](https://afify.co)** (`afify.co`) and **[Abdullah Afify](https://github.com/AbdullahAfifyKhalil)**.

---

## 📊 Dataset Summary

This dataset compiles official national examination results for Egyptian General Secondary Education (*Thanawya Amma* / **الثانوية العامة**) across three consecutive academic years: **2024, 2025, and 2026**, comprising **2,465,366 student records**.

It serves as a primary empirical benchmark for:
- **Arabic Onomastics & NLP**: Full authentic personal naming patterns and patronymic chains across Egyptian governorates.
- **Educational & Statistical Analytics**: National grade distribution modeling, pass/fail trends, and cohort demographic shifts.

---

## 📁 Dataset Splits & Statistics

| Academic Year | Configuration Name | Record Count | Total Exam Takers |
|---|---|---|---|
| 📅 **All Years (Combined)** | `default` / `all_years` | **2,465,366** | 100% |
| 🎓 **2024 Academic Year** | `year_2024` | **734,990** | First cohort |
| 🎓 **2025 Academic Year** | `year_2025` | **810,980** | Second cohort |
| 🎓 **2026 Academic Year** | `year_2026` | **919,396** | Third cohort |

---

## 🚀 How to Use with `datasets`

```python
from datasets import load_dataset

# 1. Load the complete 3-year unified dataset (2.46M rows)
dataset = load_dataset("Abdullah-afify/egyptian-high-school-students-grades")
print(dataset["train"][0])

# 2. Load a specific academic cohort (e.g. 2026 results)
cohort_2026 = load_dataset("Abdullah-afify/egyptian-high-school-students-grades", "year_2026")
print(f"Total 2026 students: {len(cohort_2026['train']):,}")
```

### Direct Pandas / PyArrow Loading:

```python
import pandas as pd

# Load all years
df = pd.read_parquet("data/high_school_degrees_all_years.parquet")
print(df.head())
```

---

## 🧬 Data Schema & Field Dictionary

| Field | Type | Description | Arabic Name | Example |
|---|---|---|---|---|
| `academic_year` | int64 | Cohort academic year (2024, 2025, 2026) | سنة الامتحان | `2026` |
| `seating_no` | int64 | Official national examination seating number | رقم الجلوس | `2001970` |
| `arabic_name` | string | Full student quad/quint name | اسم الطالب رباعي / خماسي | `احمد محمود السيد عبدالجواد السيد` |
| `total_degree` | float64 | Total examination score obtained | المجموع الكلي للدرجات | `290.0` |
| `student_case_desc` | string | Official status result | حالة الطالب | `ناجح دور أول` |

---

## 🏢 About Afify Corporation
This dataset is curated and released by **[Afify Corporation](https://afify.co)** (`afify.co`), a technology and media enterprise innovating across software, hardware systems, and digital media, leveraging advanced engineering and artificial intelligence.

- 🌐 **Corporate Portal**: [afify.co](https://afify.co)
- 🐙 **GitHub Organization**: [github.com/AbdullahAfifyKhalil](https://github.com/AbdullahAfifyKhalil)
- 📦 **Open Source Libraries**: [`egy-names` on GitHub](https://github.com/AbdullahAfifyKhalil/egy-names)

---

## 📜 License & Citation

Licensed under the **MIT License**.

```bibtex
@dataset{afify_high_school_grades_2026,
  author = {Abdullah Afify and Afify Corporation},
  title = {Egyptian High School Students Degrees & National Examination Results (2024-2026)},
  year = {2026},
  publisher = {Hugging Face},
  url = {https://huggingface.co/datasets/Abdullah-afify/egyptian-high-school-students-grades}
}
```
