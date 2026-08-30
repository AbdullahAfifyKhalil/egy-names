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
pretty_name: Egyptian High School Students Grades & Degrees (2017–2026)
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
- config_name: year_2017
  data_files: "data/high_school_degrees_2017.parquet"
- config_name: year_2023
  data_files: "data/high_school_degrees_2023.parquet"
- config_name: year_2024
  data_files: "data/high_school_degrees_2024.parquet"
- config_name: year_2025
  data_files: "data/high_school_degrees_2025.parquet"
- config_name: year_2026
  data_files: "data/high_school_degrees_2026.parquet"
---

# Egyptian High School (Thanawya Amma) Students Degrees (2017–2026)
### *A Large-Scale National Demographic and Educational Dataset of 3,790,225 Student Records*

Published and maintained by **[Afify](https://afify.co)** and **[Abdullah Afify](https://github.com/AbdullahAfifyKhalil)**. Product page: **[afify.co/egy-names](https://afify.co/egy-names)**.

---

## Dataset Summary

This dataset compiles official national examination results for Egyptian General Secondary Education (*Thanawya Amma* / **الثانوية العامة**) across five major cohorts: **2017, 2023, 2024, 2025, and 2026**, comprising **3,790,225 student records**.

It serves as a primary empirical benchmark for:
- **Arabic Onomastics & NLP**: Full authentic personal naming patterns and patronymic chains across Egyptian governorates.
- **Educational & Statistical Analytics**: National grade distribution modeling, pass/fail trends, and cohort demographic shifts.

---

## Dataset Splits & Statistics

| Academic Year | Configuration Name | Record Count | Description |
|---|---|---|---|
|  **All Years (Combined)** | `default` / `all_years` | **3,790,225** | Complete unified dataset |
|  **2017 Academic Year** | `year_2017` | **540,110** | Historical graduation cohort |
|  **2023 Academic Year** | `year_2023` | **784,749** | Pre-reform examination cohort |
|  **2024 Academic Year** | `year_2024` | **734,990** | Recent graduation cohort |
|  **2025 Academic Year** | `year_2025` | **810,980** | Modern examination cohort |
|  **2026 Academic Year** | `year_2026` | **919,396** | Latest examination cohort |

---

## How to Use with `datasets`

```python
from datasets import load_dataset

# 1. Load the complete 5-cohort unified dataset (3.79M rows)
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

## Data Schema & Field Dictionary

| Field | Type | Description | Arabic Name | Example |
|---|---|---|---|---|
| `seating_no` | int64 | Official examination seat number | رقم الجلوس | `1029481` |
| `name` | string | Full student quad/quint name | اسم الطالب رباعي/خماسي | `محمد أحمد علي حسن الشرقاوي` |
| `school` | string | School name | اسم المدرسة | `مدرسة السعيدية الثانوية العسكرية بنين` |
| `stage` | string | Educational stage | المرحلة الدراسية | `الثانوية العامة` |
| `status` | string | Examination status | حالة الطالب | `ناجح` (Passed) / `دور ثان` (Retake) |
| `section` | string | Academic track / division | الشعبة | `علمي علوم` / `علمي رياضة` / `أدبي` |
| `total_score` | float64 | Total examination score obtained | المجموع الكلي | `385.5` |
| `percentage` | float64 | Overall percentage score | النسبة المئوية | `94.02` |
| `year` | int64 | Examination academic year | سنة الامتحان | `2026` |

---

## Research Citations & Licensing

This dataset is released under the **MIT License** and is free for academic, commercial, and research use.

```bibtex
@dataset{afify2026egyptian_grades,
  author       = {Abdullah Afify},
  title        = {Egyptian High School Students Grades & Degrees (2017–2026)},
  year         = {2026},
  publisher    = {Hugging Face},
  howpublished = {\url{https://huggingface.co/datasets/Abdullah-afify/egyptian-high-school-students-grades}}
}
```
