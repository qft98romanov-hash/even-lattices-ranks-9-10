ORIGINAL ALGORITHM REPLAY — 29 OCTOBER 2026 (EUROPE/MOSCOW)

This directory records fresh executions of the repository's existing algorithms.
It is separate from the newly implemented cross-system checks in this add-on.
The execution status and individual timings are in execution.json; the original
wrapper's run record is in wrapper_run.json when the complete run has finished.

The invoked command, from the nested project directory, is:

  python scripts/verify.py --full-global --replay-rank10-equality \
    --full-local-extensions --full-equality --workers 3

It runs the 21 routine checks with all four supported regeneration options,
resulting in 24 subprocess checks (the rank-ten equality option expands an
existing routine check rather than appending another one).

The source evidence is copied to a temporary directory. The source archive's
8,194 file hashes are checked before execution and checked again afterward.
Original certificate files are never overwritten by the replay.

Evidence in this directory:

- console.log and events.jsonl: captured wrapper output and per-event timing.
- execution.json: actual command, environment, status, per-check timings, and
  the exit code of the final source-manifest verification.
- logs/: only the logs corresponding to subprocess checks actually invoked now.
- generated_reports/: fresh reports and per-job records captured from the
  temporary execution tree after their owning verifier completed successfully.
- hashes_after.log: the final source-manifest check.
- cpp_execution.json, cpp_console.log, cpp_compile.log, cpp_stderr.log: a fresh
  compilation and execution of the original ambient-fiber C++ enumerator with
  assertions and undefined-behavior sanitization enabled. This output is checked
  against all archived case counts and witness vectors. The Python full replay
  independently uses arbitrary-precision integer arithmetic for the same search.

To generate a new capture without overwriting these published reports, run from
the repository root:

  python verification/2026-10-29/replay_original.py --workers 3
  python verification/2026-10-29/replay_ambient_cpp.py

The portable launchers write timestamped directories under the add-on's runs/.
The recorded executions used the equivalent path-bound capture drivers retained
in the working environment; the portable launchers expose output/worker options
and avoid overwriting an existing nonempty result directory.

SCOPE

All supported optional regenerations are not the same as every historical
calculation in the archive. In particular, the older rank-nine equality option
regenerates its new endpoint and equality-class searches while retaining its
documented dependence on the archived lower-rank baseline. The strict rank-ten
replay regenerates all 1,897 parent lists. The rank-ten equality replay regenerates
all 5,010 additional jobs. The ambient replay covers all 281 fibers over the fixed
printed K9 embedding, not all embeddings or ambient automorphism orbits.

These computations do not prove the external Hermite bound gamma_9 <= 2, do not
replace the mathematical completeness arguments, do not establish scientific
novelty, and do not constitute external peer review or proof-assistant checking.
