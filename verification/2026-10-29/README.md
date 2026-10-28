# Additional computational verification — 29 October 2026

This add-on supplies independently written checks, fresh reruns, execution logs, and adapters for external mathematical software. It accompanies the existing manuscript and certificate archive without changing their bytes.

**[Audit report](AUDIT_REPORT_EN.md)** · [Mathematical coverage review](docs/COVERAGE_REVIEW_EN.md) · [CAS instructions](docs/CAS_GUIDE_EN.md) · [Checker review](results/checker_review/REVIEW.md) · [Machine-readable status](STATUS.json)

## What was actually executed

| Check | Status | Evidence |
| --- | --- | --- |
| New exact Python/SymPy lattice checks | PASS | [Report](results/exact.json), [log](results/exact.log) |
| New determinant-window, HNF and cluster arithmetic checks | PASS | [Report](results/windows.json), [log](results/windows.log) |
| PARI/GP 2.19.0; complete vector-set comparison with exact enumeration | PASS | [Run](results/pari_run.json), [comparison](results/pari_vector_comparison.json) |
| GAP 4.12.1; independent finite E8 orbit calculation | PASS | [Report](results/gap_orbits.json), [environment](results/gap_environment.json) |
| Original verification suite, with all supported optional regenerations | PASS | [Execution record](results/original_replay/execution.json), [console](results/original_replay/console.log) |
| Legacy rank-nine regeneration and hardened branch audit | PASS | [Report](results/legacy_rank9_replay/summary.json) |
| Recompiled ambient C++ enumeration, with undefined-behavior sanitizer | PASS | [Execution record](results/original_replay/cpp_execution.json) |
| New enumerator against complete small-box enumeration | PASS: 27 forms | [Report](results/checker_review/enumerator_adversarial.json) |
| Aggregate runner, including failure-detection controls | PASS | [Validation](results/runner_validation/validation.json) |
| Magma, SageMath and Julia/OSCAR adapters | NOT_RUN | [Instructions and scope](docs/CAS_GUIDE_EN.md) |

NOT_RUN means the mathematical software was unavailable in this environment. Static review and Python syntax checking are not execution of those systems. Sage's PARI-backed operations also do not constitute an independent backend from PARI/GP.

A previously documented omission in a generic legacy extension helper is addressed by a regression test and a hardened actual-branch replay; see Section 5 of the [audit report](AUDIT_REPORT_EN.md).

These results establish reproducibility and agreement for the listed finite computations. The global theorems still require the manuscript's completeness arguments and stated external inputs. External expert review, formal proof-assistant verification, and a comprehensive novelty assessment are not supplied by this add-on.

## Check the downloaded audit files

```bash
python verification/2026-10-29/verify_addon_hashes.py
```

This checks the retained snapshot against its SHA256 manifest. Fresh mathematical runs should use the runner below, which leaves that snapshot intact.

## Quick start

Keep the repository's existing directory layout. From its root:

```bash
python -m pip install -r verification/2026-10-29/requirements.txt
python verification/2026-10-29/run_checks.py --packages exact windows --require-all
```

With `gp` and `gap` installed and on PATH:

```bash
python verification/2026-10-29/run_checks.py --packages exact windows pari gap --require-all
```

With all optional systems available:

```bash
python verification/2026-10-29/run_checks.py --packages exact windows pari gap magma sage oscar --require-all
```

The runner accepts `--gp`, `--gap`, `--magma`, `--sage`, and `--julia` executable paths. See `python verification/2026-10-29/run_checks.py --help`. Install Oscar in the Julia environment used by that executable before selecting `oscar`; the [CAS guide](docs/CAS_GUIDE_EN.md) also gives a direct command with an explicit Julia project.

Each run regenerates inputs in a fresh temporary copy and writes its own `runs/<UTC timestamp>/run.json` and logs. It does not overwrite retained `results/`. Missing engines are recorded as NOT_RUN, and `--require-all` makes that an unsuccessful process exit. A zero engine exit code alone is insufficient: a required completion marker and, where applicable, a fresh successful JSON report are checked.

On Windows, the first command pair works with ordinary Python after installing the pinned SymPy dependency. GAP, PARI, and the original multiprocessing replay are easiest to run in WSL/Linux. Do not use Python `-O` or `-OO`, which disable assertions.

## Repeat the longer original computations

From the repository root:

```bash
cd even-lattices-ranks-9-10
python scripts/verify.py --full-global --replay-rank10-equality --full-local-extensions --full-equality --workers 3
```

The additional `run_legacy_rank9.py` launcher regenerates the older rank-nine baseline and repeats its mandatory and hardened checks, because these are not all covered by the main wrapper. It also writes to a fresh `runs/` directory.

The original wrapper verifies 8,194 file hashes and works in a temporary copy. The add-on's `replay_original.py` additionally captures timings, generated reports, and preservation evidence in a fresh run directory; `replay_ambient_cpp.py` recompiles and reruns the ambient C++ enumerator. Consult their `--help` output. These are finite reruns supported by the original wrapper, not a claim to regenerate every historical or external calculation from scratch.

[GitHub Actions instructions](docs/CI.md) explain the quick-check workflow. That workflow has not yet run on GitHub as part of this local audit.

## Data conventions and provenance

All matrices are Gram matrices: the squared norm of an integer coordinate column is `x^T G x`. A determinant means the Gram determinant, not its square root. Shell counts include both signs and exclude the zero vector unless explicitly listed.

`export_inputs.py` extracts matrix literals using AST/JSON parsing; it does not import the original mathematical verifier. The language-specific exporters create inputs from this common exact JSON. The reports record source hashes, software versions, commands, and scope. `SOURCE_COMMIT.txt` identifies the reviewed Git commit; `SHA256SUMS.txt` covers the added files.

The original manuscript and certificate subtree remains unchanged. No new claim of optimality among all sphere packings, ambient embedding-orbit classification, or general cluster optimality is made here.
