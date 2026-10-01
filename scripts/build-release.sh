#!/usr/bin/env bash
# Zips every pack under packs/ into dist/<id>-<version>.zip with its files at the top level, checks each zip with msime-pack, and writes dist/SHA256SUMS.txt. The zips are reproducible: members are sorted, timestamps are fixed and no extra attributes are stored.
# Usage: scripts/build-release.sh <path to msime-pack>
set -euo pipefail
cd "$(dirname "$0")/.."

pack_tool=$(realpath "${1:?usage: scripts/build-release.sh <path to msime-pack>}")
rm -rf dist
mkdir dist

shopt -s nullglob
for dir in packs/*/; do
  dir=${dir%/}
  out=$("$pack_tool" validate "$dir")
  # "ok <id> <kind> <version>"
  read -r _ id _ version <<<"$out"
  zip_path=$PWD/dist/$id-$version.zip
  (
    cd "$dir"
    find . -maxdepth 1 -type f ! -name '.*' -exec touch -h -t 198001010000 {} +
    find . -maxdepth 1 -type f ! -name '.*' -printf '%f\n' | LC_ALL=C sort | TZ=UTC zip -X -q "$zip_path" -@
  )
  "$pack_tool" validate "$zip_path"
done

(cd dist && if compgen -G '*.zip' >/dev/null; then sha256sum -- *.zip > SHA256SUMS.txt; fi)
ls -l dist
