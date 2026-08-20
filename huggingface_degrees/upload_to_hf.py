"""
Uploader for Egyptian High School Students Degrees Dataset to Hugging Face Hub.
"""

import os
import time
from huggingface_hub import HfApi, create_repo

def main():
    repo_id = "Abdullah-afify/egyptian-high-school-students-grades"
    api = HfApi()

    print(f"Creating / verifying dataset repository '{repo_id}' on Hugging Face...")
    create_repo(
        repo_id=repo_id,
        repo_type="dataset",
        exist_ok=True
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))

    files_to_upload = [
        "README.md",
        "data/high_school_degrees_2024.parquet",
        "data/high_school_degrees_2025.parquet",
        "data/high_school_degrees_2026.parquet",
        "data/high_school_degrees_all_years.parquet"
    ]

    for rel_path in files_to_upload:
        full_path = os.path.join(base_dir, rel_path)
        if not os.path.exists(full_path):
            print(f"Skipping {rel_path} (not found)")
            continue

        file_size_mb = os.path.getsize(full_path) / (1024 * 1024)
        print(f"\n📤 Uploading {rel_path} ({file_size_mb:.2f} MB)...")

        for attempt in range(1, 4):
            try:
                api.upload_file(
                    path_or_fileobj=full_path,
                    path_in_repo=rel_path,
                    repo_id=repo_id,
                    repo_type="dataset",
                    commit_message=f"Add {rel_path}"
                )
                print(f"✅ Successfully uploaded {rel_path}")
                break
            except Exception as e:
                print(f"⚠️ Attempt {attempt} failed: {e}")
                if attempt < 3:
                    time.sleep(3)
                else:
                    print(f"❌ Failed to upload {rel_path}")

    print("\n🎉 HIGH SCHOOL STUDENTS DEGREES DATASET SUCCESSFULLY PUBLISHED TO HUGGING FACE!")
    print(f"🔗 View it at: https://huggingface.co/datasets/{repo_id}")

if __name__ == "__main__":
    main()
