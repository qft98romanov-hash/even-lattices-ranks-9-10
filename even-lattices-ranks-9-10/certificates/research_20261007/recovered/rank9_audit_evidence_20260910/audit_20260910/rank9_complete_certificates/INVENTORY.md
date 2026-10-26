# Bundle inventory

The `certificate/` directory is deliberately flat because several autonomous
verifiers resolve their immutable inputs relative to their own location.

## Exact engines

- `exact_lattice.py`: Bareiss determinant, rational LDL enumeration, exact
  short-vector and integral-isometry routines;
- `rank9_exact_ldl.py`: independent exact ellipsoid enumerator used by branch
  checks;
- `extend_flag.py`: exhaustive primitive one-vector extension engine;
- `extend_flag_chunk.py`, `merge_flag_chunks.py`: resume-safe rank-seven
  enumeration and deterministic merge.

## Lower flag

The frozen and freshly regenerated JSON files for ranks 1--6 are both
included, together with raw extension lists. The bridge report contains
explicit `GL_n(Z)` maps between every regenerated and frozen representative.
The lower static audit checks all 3699 raw forms and their saved isometry
maps.

## Rank-seven enumeration and reduction

Four chunk JSON files cover the 138 rank-six parents exactly once. Their
merged output contains 2235 raw forms. The static audit, chunk manifest,
survivor-linkage report, 96 explicit `GL_7(Z)` maps, transcripts, and local
hash manifests are included.

## Residual branches and sharpness

The bundle contains autonomous exact scripts and transcripts for:

- the `sqrt(3)E_7` and determinant-6318 branches (independent targeted
  verifiers);
- the determinant-7722 and determinant-8192 branches;
- the determinant-7986 and determinant-8100 branches;
- the independent covering-radius computation for `sqrt(3)E_8`;
- the explicit rank-nine equality example `K_9`.

The larger `verify_e6_flag_branch_exact.py` is included as a supplemental
cross-check. It exhausts every rank-seven extension orbit of the
`sqrt(3)E_6` parent and independently recovers the E7 and H6318 conclusions.
Because the targeted verifiers already close the theorem, this substantially
heavier supplemental computation is not mandatory in `run_all_checks.sh`.

Files from exploratory searches, compiled binaries, NumPy-only experiments,
temporary checkpoints, and Python bytecode caches are intentionally omitted.
