# GitHub Actions verification

The workflow `.github/workflows/verify-lattices.yml` is prepared for GitHub
Actions. **It has not yet been executed on GitHub Actions.** Local YAML/command
validation is not evidence of a successful hosted run.

It runs on Ubuntu 24.04 with Python 3.12, installs SymPy from the pinned
`verification/2026-10-29/requirements.txt`, and installs Ubuntu's `pari-gp`,
`gap-core`, and `gap-libs` packages. Actual package versions are retained in
the artifact. Automatic triggers cover changes to the certificate archive,
verification wrapper, supplementary checks, dependency requirements, or this
workflow. A manual `workflow_dispatch` trigger is also available.

The two verification stages are:

1. `python scripts/verify.py --workers 2`, from the nested project directory.
   This checks the certificate hashes and runs the original default suite of
   21 mathematical checks in a temporary copy.
2. `python run_checks.py --packages exact windows pari gap --require-all
   --timeout 1200`, from the supplementary directory. This performs fresh
   exact rational/SymPy checks, window and cluster checks, PARI cross-checks,
   and GAP orbit checks. When exact and PARI checks both succeed, the runner
   also compares their actual vector sets. Here `windows` refers to the
   mathematical enumeration windows, not the Windows operating system.

Missing requested engines, failed assertions, missing completion markers, and
invalid or missing fresh result reports fail the supplementary stage. It is
still attempted after a failure of the routine stage if dependency setup
succeeded. A failure of either verification stage keeps the job unsuccessful.
Each supplementary command has a 1,200-second timeout; the whole job has a
60-minute limit.

The workflow clears only its two run-output directories before executing the
checks. It preserves the original certificate archive and retained audit
snapshot. An `always()` upload step collects fresh `verification_runs/` and
`runs/` records, logs, regenerated inputs, and output reports, including those
produced before a failure. If setup fails before any results exist, the
artifact step reports that no files were found; that is not verification
success. Artifacts expire after 30 days unless separately archived.

This is the routine suite plus the selected independent checks, **not a full
regeneration** of all historical certificates. It does not request
`--full-global`, `--replay-rank10-equality`, `--full-local-extensions`, or
`--full-equality`, and does not execute Magma, SageMath, or OSCAR. A successful
run covers only these computations; it is not external peer review, a proof
of scientific novelty, or a new global classification theorem. PARI remains
a corroborating enumeration backend with the limitations described in
[CAS_GUIDE_EN.md](CAS_GUIDE_EN.md).

The workflow token has only `contents: read`; checkout credentials are not
persisted. It does not commit generated files or publish a release.
