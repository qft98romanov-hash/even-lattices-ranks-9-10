# Fresh computational replay, 10 September 2026

## Scope and environment

The released archive was recovered, verified and copied to an isolated
`replay_copy/` directory. The recovered source files were not edited. The
replay uses CPython 3.12.14 on Linux x86_64, with optimization level zero and
assertions enabled (`__debug__ == True`, `PYTHONOPTIMIZE` unset).

This is a fresh execution of the released algorithms and a fresh exhaustive
regeneration of their inputs. It is not a wholly separate implementation of
every algorithm. The accompanying mathematical and source-code audits are
needed to assess the completeness and correctness of the underlying logic.

## Integrity checks: PASS

* ZIP size: 330039 bytes.
* ZIP SHA-256:
  `608cf4b022d448476028d56f002485ec39c1893b2a2e797458838c64db11d8b3`.
* ZIP member CRC check: PASS (`ZipFile.testzip() is None`).
* All 83 entries in the released `SHA256SUMS` manifest passed before replay.

The environment and initial outcomes are recorded in
`replay_metadata.json` and `replay_initial_hash_check.log`.

## Mandatory verifier replay: PASS

The unmodified `run_all_checks.sh` completed in `replay_copy/` with exit
status 0 and terminal marker `ALL_RELEASED_EXACT_CERTIFICATES_PASS`.
The measured wall time was 252.900911 seconds; completion time was
2026-09-10 07:42:19 UTC. Fresh combined output is recorded in
`replay_run_all_checks_20260910.log`; exit status and wall time are
recorded in `replay_run_all_checks_result.json`.

The script checks the sharp K9 example, all regenerated-to-frozen bridges,
all lower-flag raw forms and GL maps, all saved rank-seven extensions, all
96 survivor linkages, the six residual branches, and the independent
discriminant-class radius calculation for sqrt(3)E8.

## Full regeneration: PASS

The unmodified `run_full_regeneration.sh` completed with exit status 0
and terminal marker `FULL_EXACT_REGENERATION_BYTE_IDENTICAL`.
The measured wall time was 230.929221 seconds; completion time was
2026-09-10 07:42:18 UTC. It regenerated the lower flag through rank six
and all four rank-six-to-seven chunks, then compared the output with
the released files byte for byte. Fresh output is recorded in
`replay_full_regeneration_20260910.log`; exit status and wall time are
recorded in `replay_full_regeneration_result.json`.

The two runners were executed concurrently; the wall times are not
benchmark measurements on a dedicated idle machine.

| Generated rank | Raw extensions | Isometry representatives |
|---|---:|---:|
| 2 | 7 | 5 |
| 3 | 52 | 14 |
| 4 | 279 | 47 |
| 5 | 1456 | 118 |
| 6 | 1905 | 138 |

All five regenerated principal JSON files matched byte for byte. The
four disjoint rank-seven chunks had 102, 0, 1868 and 265 raw children;
the merged set contained 2235 raw children from all 138 rank-six
parents. All four chunk files and the merged file matched byte for
byte. The regenerated merged file SHA-256 is
`19d489d4a12aa58b61b2dce4dce547c270f9d1414f766409edc3862d0b4577d8`.

The line `generator rerun = False` near the end of this log belongs to
the final static verifier invoked after regeneration; it means that
this final verifier did not itself rerun the generator. The preceding
log records the actual generation of every lower-rank parent and all
138 rank-six parents, followed by the explicit byte comparisons.

In addition to the comparisons built into that script, the five freshly
generated raw files for ranks 2--6 have already been compared byte for
byte with the released `.raw` files. All five comparisons passed. Their
hashes are recorded in `replay_regenerated_raw_comparisons.json`.

## Post-replay integrity: PASS

After both runners completed, all 83 released manifest entries still
passed in the replay copy. All 83 manifest entries also passed in the
original recovered source directory, confirming that the audit left
the released source files unchanged. The logs are
`replay_final_hash_check.log` and
`replay_source_unchanged_hash_check.log`.

Hashes for the fresh audit logs and metadata are collected in
`replay_evidence_SHA256SUMS`.

## Limitations of this replay

* A passing hash check establishes file identity, not mathematical truth.
* A passing execution establishes that the released assertions pass for
  the supplied or regenerated data, not by itself that every proof lemma
  or enumeration bound is valid.
* This replay does not reprove classical Hermite bounds or Mordell's
  inequality.
* The supplementary full E6 branch cross-check is not part of the
  mandatory runner and has not been rerun in this replay. Its necessary
  conclusions are covered by the targeted E7 and H6318 programs.
* The result concerns the determinant optimum for even positive definite
  integral rank-nine lattices of minimum at least six; it is not a
  uniqueness theorem or a complete rank-nine classification.
