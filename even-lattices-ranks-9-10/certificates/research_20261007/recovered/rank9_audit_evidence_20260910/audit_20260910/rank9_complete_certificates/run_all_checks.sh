#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

bundle_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$bundle_root"

echo "[1/11] Verifying released-file hashes"
sha256sum -c SHA256SUMS

cd certificate

echo "[2/11] Verifying the sharp rank-nine example"
python3 verify_rank9_extremal_example_exact.py

echo "[3/11] Verifying regenerated-to-frozen lower-flag bridges"
python3 verify_regenerated_frozen_bridges_exact.py

echo "[4/11] Auditing all 3699 lower-flag raw extensions and GL maps"
python3 verify_lower_flag_chain_exact.py

echo "[5/11] Auditing all 2235 saved rank-seven extensions"
python3 verify_flag_chunks.py rank6_isometry_classes.json rank7_merged.json

echo "[6/11] Verifying all 96 survivor-to-class linkage maps"
python3 verify_rank7_survivor_linkage_exact.py

echo "[7/11] Independently verifying the sqrt(3)E7 branch"
python3 verify_e7_branch_exact.py

echo "[8/11] Verifying the determinant-6318 branch"
python3 verify_h6318_branch_exact.py

echo "[9/11] Verifying the determinant-7722 and 8192 branches"
python3 verify_rank7_topdown.py

echo "[10/11] Verifying the determinant-7986 and 8100 branches"
python3 verify_rank7_residuals_exact.py

echo "[11/11] Independently verifying rho(sqrt(3)E8)^2 = 8/3"
python3 verify_sqrt3_e8_covering_radius_exact.py

echo "ALL_RELEASED_EXACT_CERTIFICATES_PASS"
