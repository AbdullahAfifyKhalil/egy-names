#!/usr/bin/env bash
# Copy the canonical book into every full-book SDK.
# Edit data/names.json.gz, run this, then publish.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/data/names.json.gz"

if [[ ! -f "$SRC" ]]; then
  echo "missing canonical catalog: $SRC" >&2
  exit 1
fi

SRC_SIZE="$(wc -c < "$SRC" | tr -d ' ')"

DESTS=(
  "$ROOT/python/src/egy_names/data/names.json.gz"
  "$ROOT/typescript/src/data/names.json.gz"
  "$ROOT/typescript/data/names.json.gz"
  "$ROOT/dart/egy_names/lib/src/data/names.json.gz"
  "$ROOT/php/egy-names/data/names.json.gz"
  "$ROOT/java/egy-names/src/main/resources/names.json.gz"
  "$ROOT/java/egy-names/src/main/resources/data/names.json.gz"
  "$ROOT/csharp/EgyNames/Data/names.json.gz"
  "$ROOT/cpp/egy_names/data/names.json.gz"
  "$ROOT/swift/EgyNames/Sources/EgyNames/Resources/names.json.gz"
)

for dest in "${DESTS[@]}"; do
  mkdir -p "$(dirname "$dest")"
  cp -f "$SRC" "$dest"
  dest_size="$(wc -c < "$dest" | tr -d ' ')"
  if [[ "$dest_size" != "$SRC_SIZE" ]]; then
    echo "size mismatch after copy: $dest ($dest_size != $SRC_SIZE)" >&2
    exit 1
  fi
  echo "synced $dest"
done

echo "catalog synced ($SRC_SIZE bytes) → ${#DESTS[@]} destinations"
