# Exact regeneration and verification order

All commands below are run from the `certificate/` directory.  They write
new files, so use a disposable copy when reproducing the full enumeration.

## 1. Regenerate the lower flag

```bash
python3 extend_flag.py rank1_seed.json rank2_exact_classes_regen.json \
  --low 27 --high 39 --modulus 4 --residues 0,3
python3 extend_flag.py rank2_exact_classes_regen.json rank3_exact_classes_regen.json \
  --low 108 --high 178 --modulus 2 --residues 0
python3 extend_flag.py rank3_exact_classes_regen.json rank4_exact_classes_regen.json \
  --low 324 --high 633 --modulus 4 --residues 0,1
python3 extend_flag.py rank4_exact_classes_regen.json rank5_isometry_classes_regen.json \
  --low 972 --high 1894 --modulus 2 --residues 0
python3 extend_flag.py rank5_isometry_classes_regen.json rank6_isometry_classes_regen.json \
  --low 2187 --high 4647 --modulus 4 --residues 0,3
python3 verify_regenerated_frozen_bridges_exact.py
```

Expected class counts are `5, 14, 47, 118, 138`.  The bridge verifier must
end with `ALL_REGENERATED_FROZEN_EXACT_BRIDGES_OK`.

## 2. Regenerate rank-six to rank-seven chunks

The ranges are disjoint and may be executed in parallel:

```bash
python3 extend_flag_chunk.py rank6_isometry_classes.json rank7_chunk_000_035.json \
  --start 0 --stop 35 --low 4374 --high 9492 --modulus 2 --residues 0
python3 extend_flag_chunk.py rank6_isometry_classes.json rank7_chunk_035_070.json \
  --start 35 --stop 70 --low 4374 --high 9492 --modulus 2 --residues 0
python3 extend_flag_chunk.py rank6_isometry_classes.json rank7_chunk_070_105.json \
  --start 70 --stop 105 --low 4374 --high 9492 --modulus 2 --residues 0
python3 extend_flag_chunk.py rank6_isometry_classes.json rank7_chunk_105_138.json \
  --start 105 --stop 138 --low 4374 --high 9492 --modulus 2 --residues 0
python3 merge_flag_chunks.py rank7_all_raw.json \
  rank7_chunk_000_035.json rank7_chunk_035_070.json \
  rank7_chunk_070_105.json rank7_chunk_105_138.json
```

The merged raw count must be 2235.  Next run the static chunk verifier named
in `CLAIMS_TO_CERTIFICATES.md`.

## 3. Verify survivor linkage and branch closure

Run, in the order listed in `run_all_checks.sh`, the exact survivor-linkage
verifier, the targeted `sqrt(3)E_7` and `H_6318` verifiers, the residual
verifier, the top-down verifier for determinants 7722 and 8192, and the
independent `sqrt(3)E_8` covering-radius check.

The final unified audit must cover the six pairs

```text
(2187,4374), (2187,6318), (2835,7722),
(4096,8192), (3240,8100), (3267,7986).
```

No theorem claim should be accepted merely from a transcript: each transcript
is pinned to its script and inputs by `SHA256SUMS`, and the scripts themselves
must exit successfully.
