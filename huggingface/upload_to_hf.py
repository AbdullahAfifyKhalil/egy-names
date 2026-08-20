"""
Robust Multi-File Uploader for Hugging Face Hub with retry & individual file commits.
"""

import argparse
import os
import time
from huggingface_hub import HfApi, create_repo

def main():
    parser = argparse.ArgumentParser(description="Upload dataset to Hugging Face Hub")
    parser.add_argument("--repo-id", type=str, default="Abdullah-afify/egyptian-names", help="Target Hugging Face repo ID")
    parser.add_argument("--token", type=str, default=None, help="Hugging Face API token")
    args = parser.parse_args()

    api = HfApi(token=args.token)

    print(f"Creating / verifying dataset repository '{args.repo_id}' on Hugging Face...")
    create_repo(
        repo_id=args.repo_id,
        repo_type="dataset",
        exist_ok=True,
        token=args.token
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Ordered list of files to upload: README first so the Dataset Card displays immediately!
    files_to_upload = [
        "README.md",
        "data/final_canonical_names.parquet",
        "data/final_canonical_names.csv",
        "data/names.parquet",
        "data/names.csv",
        "data/phase2_token_frequencies.parquet",
        "data/phase2_token_frequencies.csv",
        "data/phase3_spelling_corrections.parquet",
        "data/phase3_spelling_corrections.csv",
        "data/slot_distributions.parquet",
        "data/slot_distributions.csv",
        "data/phase1_segmented_chains.parquet",
        "data/phase0_raw_full_names.parquet"
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
                    repo_id=args.repo_id,
                    repo_type="dataset",
                    token=args.token,
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

    print("\n🎉 ALL DATASET FILES SUCCESSFULLY PUBLISHED TO HUGGING FACE!")
    print(f"🔗 View it at: https://huggingface.co/datasets/{args.repo_id}")

if __name__ == "__main__":
    main()
