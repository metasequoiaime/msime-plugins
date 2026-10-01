#!/usr/bin/env bash
# Checks every pack under packs/ and every template under templates/ with msime-pack, which applies exactly the rules the input method imports by. On top of that it checks what only this repository cares about: a pack's folder name equals its id, and README.md lists it.
# Usage: scripts/check-packs.sh <path to msime-pack>
set -euo pipefail
cd "$(dirname "$0")/.."

pack_tool=${1:?usage: scripts/check-packs.sh <path to msime-pack>}
failed=0

check() {
  local dir=$1 listed=$2 out id
  if ! out=$("$pack_tool" validate "$dir"); then
    echo "$out"
    failed=1
    return
  fi
  echo "$out"
  # "ok <id> <kind> <version>"
  id=$(cut -d' ' -f2 <<<"$out")
  if [[ $(basename "$dir") != "$id" && $listed == yes ]]; then
    echo "error $dir: the folder name must equal the id \"$id\""
    failed=1
  fi
  if [[ $listed == yes ]] && ! grep -qF "packs/$id" README.md; then
    echo "error $dir: add a row for packs/$id to the pack list in README.md"
    failed=1
  fi
}

shopt -s nullglob
for dir in templates/*/; do check "${dir%/}" no; done
for dir in packs/*/; do check "${dir%/}" yes; done
exit "$failed"
