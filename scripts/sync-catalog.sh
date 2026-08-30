#!/usr/bin/env bash
# Copy the canonical book into every full-book SDK.
# Edit data/names.json.gz, run this, then publish.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/data/names.json.gz"
CONFIG_SRC="$ROOT/data/logic_config.json"

if [[ ! -f "$SRC" ]]; then
  echo "missing canonical catalog: $SRC" >&2
  exit 1
fi
if [[ ! -f "$CONFIG_SRC" ]]; then
  echo "missing shared rule config: $CONFIG_SRC" >&2
  exit 1
fi

SRC_SIZE="$(wc -c < "$SRC" | tr -d ' ')"
CONFIG_SIZE="$(wc -c < "$CONFIG_SRC" | tr -d ' ')"

# Every dir that carries a copy of the book must also carry the rule
# config next to it — one list, kept in sync, so a change to either
# file only ever needs one entry here.
DEST_DIRS=(
  "$ROOT/python/src/egy_names/data"
  "$ROOT/typescript/src/data"
  "$ROOT/typescript/data"
  "$ROOT/dart/egy_names/lib/src/data"
  "$ROOT/php/egy-names/data"
  "$ROOT/java/egy-names/src/main/resources"
  "$ROOT/java/egy-names/src/main/resources/data"
  "$ROOT/csharp/EgyNames/Data"
  "$ROOT/cpp/egy_names/data"
  "$ROOT/swift/EgyNames/Sources/EgyNames/Resources"
  "$ROOT/faker-egy-names-php/data"
)

for dir in "${DEST_DIRS[@]}"; do
  mkdir -p "$dir"

  dest="$dir/names.json.gz"
  cp -f "$SRC" "$dest"
  dest_size="$(wc -c < "$dest" | tr -d ' ')"
  if [[ "$dest_size" != "$SRC_SIZE" ]]; then
    echo "size mismatch after copy: $dest ($dest_size != $SRC_SIZE)" >&2
    exit 1
  fi

  config_dest="$dir/logic_config.json"
  cp -f "$CONFIG_SRC" "$config_dest"
  config_dest_size="$(wc -c < "$config_dest" | tr -d ' ')"
  if [[ "$config_dest_size" != "$CONFIG_SIZE" ]]; then
    echo "size mismatch after copy: $config_dest ($config_dest_size != $CONFIG_SIZE)" >&2
    exit 1
  fi

  echo "synced $dest + $config_dest"
done

echo "catalog + rule config synced (${SRC_SIZE}B, ${CONFIG_SIZE}B) → ${#DEST_DIRS[@]} destinations"
