#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

bundle_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cert="$bundle_root/certificate"
work=$(mktemp -d "${TMPDIR:-/tmp}/rank9-cert-regen.XXXXXXXX")

cleanup() {
  case "$work" in
    "${TMPDIR:-/tmp}"/rank9-cert-regen.*) rm -rf -- "$work" ;;
    *) echo "Refusing to remove unexpected path: $work" >&2 ;;
  esac
}
trap cleanup EXIT HUP INT TERM

cd "$cert"
echo "Regeneration workspace: $work"

python3 extend_flag.py rank1_seed.json "$work/rank2.json" \
  --low 27 --high 39 --modulus 4 --residues 0,3
python3 extend_flag.py "$work/rank2.json" "$work/rank3.json" \
  --low 108 --high 178 --modulus 2 --residues 0
python3 extend_flag.py "$work/rank3.json" "$work/rank4.json" \
  --low 324 --high 633 --modulus 4 --residues 0,1
python3 extend_flag.py "$work/rank4.json" "$work/rank5.json" \
  --low 972 --high 1894 --modulus 2 --residues 0
python3 extend_flag.py "$work/rank5.json" "$work/rank6.json" \
  --low 2187 --high 4647 --modulus 4 --residues 0,3

cmp "$work/rank2.json" rank2_exact_classes_regen.json
cmp "$work/rank3.json" rank3_exact_classes_regen.json
cmp "$work/rank4.json" rank4_exact_classes_regen.json
cmp "$work/rank5.json" rank5_isometry_classes_regen.json
cmp "$work/rank6.json" rank6_isometry_classes_regen.json
echo "LOWER_FLAG_BYTE_IDENTICAL"

python3 extend_flag_chunk.py rank6_isometry_classes.json "$work/rank7_chunk_000_035.json" \
  --start 0 --stop 35 --low 4374 --high 9492 --modulus 2 --residues 0
python3 extend_flag_chunk.py rank6_isometry_classes.json "$work/rank7_chunk_035_070.json" \
  --start 35 --stop 70 --low 4374 --high 9492 --modulus 2 --residues 0
python3 extend_flag_chunk.py rank6_isometry_classes.json "$work/rank7_chunk_070_105.json" \
  --start 70 --stop 105 --low 4374 --high 9492 --modulus 2 --residues 0
python3 extend_flag_chunk.py rank6_isometry_classes.json "$work/rank7_chunk_105_138.json" \
  --start 105 --stop 138 --low 4374 --high 9492 --modulus 2 --residues 0
python3 merge_flag_chunks.py "$work/rank7_merged.json" \
  "$work/rank7_chunk_000_035.json" "$work/rank7_chunk_035_070.json" \
  "$work/rank7_chunk_070_105.json" "$work/rank7_chunk_105_138.json"

# Chunk JSON contains only deterministic mathematical data and fixed
# filenames.  Exact byte comparison is therefore stronger than a count check.
cmp "$work/rank7_chunk_000_035.json" rank7_chunk_000_035.json
cmp "$work/rank7_chunk_035_070.json" rank7_chunk_035_070.json
cmp "$work/rank7_chunk_070_105.json" rank7_chunk_070_105.json
cmp "$work/rank7_chunk_105_138.json" rank7_chunk_105_138.json
cmp "$work/rank7_merged.json" rank7_merged.json

python3 verify_flag_chunks.py rank6_isometry_classes.json "$work/rank7_merged.json"
echo "FULL_EXACT_REGENERATION_BYTE_IDENTICAL"
