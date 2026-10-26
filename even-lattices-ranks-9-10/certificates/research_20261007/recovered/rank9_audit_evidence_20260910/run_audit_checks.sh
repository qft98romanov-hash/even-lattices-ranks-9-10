#!/usr/bin/env bash
set -euo pipefail

bundle_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$bundle_root"
export PYTHONDONTWRITEBYTECODE=1

python3 -c 'import sys; sys.exit(0 if __debug__ else "ERROR: Python assertions must be enabled; remove -O and PYTHONOPTIMIZE.")'
sha256sum -c SHA256SUMS

echo "[1/5] Independent enumeration kernels and low-rank extensions"
python3 audit_20260910/test_enumeration_independent.py

echo "[2/5] Independent residual-branch and K9 checks"
python3 audit_20260910/branch_independent_checks.py

echo "[3/5] Exact windows and the independent 64-point sharpness proof"
python3 audit_20260910/verify_theory_and_sharpness.py

echo "[4/5] Regression for the omitted nonzero zero-class layer"
python3 audit_20260910/topdown_zero_layer_regression.py

echo "[5/5] Hardened top-down branch verification"
python3 audit_20260910/verify_rank7_topdown_hardened.py

echo "ALL_SUPPLEMENTARY_AUDIT_CHECKS_PASS"
