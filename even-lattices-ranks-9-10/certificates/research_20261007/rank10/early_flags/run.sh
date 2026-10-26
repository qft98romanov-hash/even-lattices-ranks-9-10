#!/bin/bash
set -euo pipefail
ROOT=/workspace/scratch/e3fcbd7c9568/research_20261007
CERT="$ROOT/recovered/rank9_audit_evidence_20260910/audit_20260910/rank9_complete_certificates/certificate"
HERE="$ROOT/rank10/early_flags"
python -u "$CERT/extend_flag.py" "$CERT/rank1_seed.json" "$HERE/rank2.json" --low 27 --high 44 --modulus 4 --residues 0,3 > "$HERE/rank2.log"
python -u "$CERT/extend_flag.py" "$HERE/rank2.json" "$HERE/rank3.json" --low 108 --high 210 --modulus 2 --residues 0 > "$HERE/rank3.log"
python -u "$CERT/extend_flag.py" "$HERE/rank3.json" "$HERE/rank4.json" --low 324 --high 789 --modulus 4 --residues 0,1 > "$HERE/rank4.log"
python -u "$CERT/extend_flag.py" "$HERE/rank4.json" "$HERE/rank5.json" --low 972 --high 2492 --modulus 2 --residues 0 > "$HERE/rank5.log"
