# Reproduction guide

## Environment

The preserved verification records were produced with CPython 3.12 on Linux. The mathematical verification scripts use only the Python standard library. The standalone manuscript is compiled with XeLaTeX.

Use ordinary Python with assertions enabled. Do not use `python -O`, `python -OO`, or the environment variable `PYTHONOPTIMIZE`. Several exact checks deliberately rely on assertions.

Parallel full regenerations use the `fork` multiprocessing start method. Use Linux, macOS, or Linux under WSL. Native Windows execution is not asserted for the complete suite; on Windows, WSL is the straightforward reproduction environment. The original development environment need not be reconstructed to read the data and proofs.

## Preserve the original evidence

The `certificates/` directory contains the complete preserved evidence bundle. Its `SHA256SUMS` refers to the files **inside that directory**, not to the later repository documentation or edited manuscript.

The repository wrapper first checks all 8,194 archived file hashes, then copies the bundle into a temporary directory and executes the mathematical checks there. This prevents the original verifiers' rewritten logs or status JSON files from changing the archived evidence. It saves the new console output, logs, and run record under `verification_runs/<timestamp>/`; that directory is ignored by Git.

The repository's `.gitattributes` disables automatic text conversion so that Git checkout does not silently change certified file bytes on Windows. Hash verification establishes byte identity, not mathematical correctness.

## Routine mathematical checks

Run from the repository root:

```bash
python scripts/verify.py
```

For a file-identity check without mathematical verification:

```bash
python scripts/verify.py --hashes-only
```

The default suite contains 21 checks covering the prior rank-nine and rank-ten work, the new equality-boundary proof, the independent finite-module calculation, and the intrinsic structure and cluster comparison. The original runner prints a `PASS` line for each successful invocation and ends with:

```text
ALL_SELECTED_NEW_RESULT_CHECKS_PASS
```

A nonzero exit code stops the suite and identifies the failed program and its log. The wrapper records the interpreter, platform, mode, elapsed time, and exit code. The complete routine suite was rerun successfully during repository preparation on 26 October 2026 with CPython 3.12.14 on Linux. No optional full regeneration is claimed for that packaging run.

A successful run should be read together with the written proof and the documented external assumptions. The included GitHub Actions workflow is manual-only; no hosted GitHub run is claimed by the preparation package.

## Optional full regenerations

Run these commands from the repository root. They retain the routine checks and add the indicated regeneration in a temporary copy. Worker counts may be reduced to suit the machine; the wrapper default is 2.

| Command | Additional work |
| --- | --- |
| `python scripts/verify.py --full-global --workers 4` | Regenerates all 1,897 parent lists of the strict global rank-ten search |
| `python scripts/verify.py --replay-rank10-equality --workers 4` | Regenerates the new global rank-ten equality jobs directly, bypassing generator caches |
| `python scripts/verify.py --full-local-extensions` | Replays all 281 ambient fibers for supersections of the fixed printed $K_9$ |
| `python scripts/verify.py --full-equality` | Regenerates the older **rank-nine** equality-boundary certificate |

The last flag is historical: `--full-equality` does **not** mean the new rank-ten equality classification. Flags may be combined. The ambient full replay is substantial: its retained exact run visited 171,472,428 nodes. Durations depend on the hardware and are not a guaranteed performance claim.

## Evidence map

All paths in this table are relative to `certificates/`.

| Mathematical component | Main entry point or record |
| --- | --- |
| File identity | `verify_file_hashes.py`, `SHA256SUMS` |
| Default assembled checks | `verify_new_results.py` |
| Rank-nine equality | `research_20261007/equality/verify_equality.py` |
| Independent rank-nine endpoint proof | `research_20261007/independent_review/check_equality_independent.py` |
| Rank-ten equality with an assumed $\sqrt3E_8$ sublattice | `research_20261007/rank10/verify_rank10_e8_classification.py` |
| Strict global rank-ten bound | `research_20261007/rank10/verify_global_rank10_certificate.py` |
| Independent saved-chain audit | `research_20261007/independent_review/check_rank10_global_chain.py` |
| Global rank-ten equality | `research_20261008/rank10_equality/verify_equality_certificate.py` |
| Enlarged windows and recovered prunes | `research_20261008/independent_review/check_equality_windows_and_recovered_prunes.py` |
| Independent finite quadratic-module proof | `research_20261008/independent_review/check_boundaries_by_quadratic_module.py` |
| Independent equality-job linkage | `research_20261008/independent_review/check_delta_chain_independent.py` |
| Intrinsic structure and cluster bound | `research_20261008/consequences/audit_two_types_and_cluster_gap.py` |
| Fixed ambient supersections | `research_20261007/embeddings/verify_all_fixed_K9_extensions.py` |
| Recorded package execution | `PACKAGE_VERIFICATION.txt`, `assembled_new_checks.json`, `local_replay_logs/` |

Read each mathematical argument alongside its verifier. In particular, `research_20261008/independent_review/equality_boundary_coverage_argument.md` explains why the changed equality windows and formerly pruned branches are covered.

## Direct use of the original programs

The original runner remains available inside `certificates/`. If you need to work with it directly, copy the directory first:

```bash
cp -a certificates ../lattice-certificates-verification
cd ../lattice-certificates-verification
python verify_file_hashes.py
python verify_new_results.py
```

Run the hash check before the mathematical checks, since the original programs may rewrite status files or logs. Their optional flags have the same names as the wrapper flags.

## Build the English PDF

From the repository root, using a TeX installation with XeLaTeX:

```bash
python scripts/build_paper.py
```

The helper runs three XeLaTeX passes to resolve the table of contents and cross-references, then writes `manuscript/paper.pdf` and synchronizes `manuscript/paper.txt` with the LaTeX source. Temporary build files remain under the ignored `build/` directory.

The bibliography is included in the source; no bibliography download is needed. In Overleaf, upload `paper.tex` (or copy the contents of `paper.txt` into `main.tex`) and select **XeLaTeX** as the compiler.

The `.txt` deliverable is a copy of the complete LaTeX source, not a plain-text mathematical rendering. If editing manually without running the build helper, keep the two source copies synchronized.

## Workflow references

The optional manual workflow uses the action interfaces documented by their
maintainers: [actions/checkout](https://github.com/actions/checkout) and
[actions/setup-python](https://github.com/actions/setup-python). Its Python
version is explicitly fixed to the verified 3.12 series. The local mathematical
suite was executed during packaging; the hosted workflow has not been run.
