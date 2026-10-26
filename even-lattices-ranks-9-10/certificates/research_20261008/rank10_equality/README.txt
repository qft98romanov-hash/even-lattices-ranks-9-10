CONFIDENTIAL RANK-TEN GLOBAL EQUALITY CERTIFICATE, 8 October 2026

Mathematical statement:
Under gamma_9 <= 2 and the standard rank <= 8 Hermite inputs, every even
integral rank-10 minimum-six lattice has determinant >= 54675; precisely
two isometry classes attain equality. Both contain sqrt(3)E8.

Read global_equality_theorem_EN.txt for the complete coverage argument.
The older strict search and E8 equality classification are dependencies in
../../research_20261007/rank10. Relative directory structure is essential.

Actual work recorded in this continuation:
- Fresh full exact generation of all new boundary extension lists.
- Exact reevaluation of old lifting exclusions, including four recovered
  rank-seven raw matrices.
- Independent finite-quadratic-module boundary exclusions with a separate
  short-dual-vector enumerator, in ../independent_review.
- Direct static certificate validation of all new records.

Core commands (Python standard library, assertions enabled):
  python verify_equality_certificate.py
  python verify_equality_certificate.py --replay --workers 5

The first checks the complete old strict chain without mutating old evidence,
then the new delta chain. If a package-wide verifier already checked the
strict chain, use --skip-base to avoid repeating it.
The --replay switch truly recomputes every new matrix list; it never treats
cached job records as a rerun. A full separate replay is optional and must
not be inferred from the initial fresh generation. The latest JSON status
reports accurately which mode was run. A full replay, if invoked, additionally
saves equality_full_replay_record.json. Initial fresh-generation provenance
is separately saved in equality_fresh_generation_record.json.

Generation driver run_delta.py is resumable and DOES use cached job records;
it is not the independent replay command. process_delta.py assembles newly
admitted parents and reevaluates every old raw lifting exclusion. The jobs
folder preserves a record for all 5010 parent/window jobs, including exact
immediate prunes; the 4952 boundary parent/determinant pairs of the independent
method exclude the extra 58 already-pruned rank-seven continuation jobs.
No new isometry deduplication is needed: all four recovered raw rank-seven
parents are kept separately.

The two equality Gram matrices, E8 class computation, and their distinct
ranks modulo 3 are in the older rank10_e8_certificate.json. Global equality
classification does not classify ambient rank-48 automorphism orbits, does
not establish unrestricted dimension-38 sphere-packing optimality, and does
not substitute for external human review or a novelty assessment.
