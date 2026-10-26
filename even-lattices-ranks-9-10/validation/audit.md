# Repository preparation audit

Date: 26 October 2026.

This audit concerns portability, package integrity, language coverage, and re-execution of the supplied checks. It is not a new proof of the mathematical claims, external peer review, or a claim that the optional complete generation searches were rerun.

## Source identity

The recovered source archive is `lattice_certificates_complete_20261008.zip`, SHA256:

```text
7b08027eed3dd5388f86a5fba259e10ad5a3fabd91ec585758e7b9bad2fc5306
```

Its extracted directory contains 8,195 files and 71,949,818 bytes, including 7,817 JSON files, 83 Python files, two C++ sources, and four shell scripts. The fresh package's `verify_file_hashes.py` passed all 8,194 listed file hashes. File hashes establish identity, not mathematical correctness.

## Checks actually run

The complete directory was copied to an isolated runtime directory. From that copy, the command

```sh
python3 verify_new_results.py
```

completed with exit code 0 and `ALL_SELECTED_NEW_RESULT_CHECKS_PASS`. All 21 default check invocations passed, on CPython 3.12.14 under Linux. Elapsed time was approximately 142.87 seconds, measured from the process start timestamp to the final suite-log write. The full log is `routine_suite.log`; the environment, source hashes, results, and modified-file inventory are recorded in `routine_verification.json`.

These invocations include the original independent rank-ten saved-chain check, the global equality certificate check, enlarged endpoint/prune coverage, the independent finite quadratic-module exclusion, the independent saved-delta linkage check, and the intrinsic structure and cluster bound audit. No optional full-regeneration flag was supplied in this run.

The run rewrote 11 status/log files and added 12 runtime files, mostly Python bytecode caches. Therefore the public entrypoint should operate on a temporary copy and leave the archived certificate directory unchanged. Existing output files must not be treated as immutable input merely because their names contain `verified`.

## Dependencies and platform

The mathematical verifiers import only Python's standard library and local modules supplied in the package. They require no downloaded data or third-party numerical package. Assertions must remain enabled: do not use `python -O`, `python -OO`, or an equivalent `PYTHONOPTIMIZE` setting.

The documented and tested platform is CPython 3.12 on Linux. The two parallel optional searches explicitly request the multiprocessing `fork` context; Linux or Linux under WSL is the conservative recommendation for a Windows user. macOS has a `fork` context, but was not tested in this preparation. Native Windows compatibility of the full package is not established.

The archived report-rendering helper has separate dependencies: Pillow, pypdf, XeLaTeX, and Poppler. Those are not mathematical-verifier dependencies. C++ source files are retained as historical computational evidence; the default verification suite uses Python and does not require compiling them.

## Optional searches

| Option to `verify_new_results.py` | Meaning |
| --- | --- |
| `--full-global --workers N` | Regenerate all 1,897 strict rank-ten parent lists. |
| `--replay-rank10-equality --workers N` | Regenerate the additional rank-ten equality endpoint jobs, bypassing generator caches. |
| `--full-local-extensions` | Replay all 281 fibers over the fixed printed ambient K9 section. |
| `--full-equality` | Regenerate the older **rank-nine** equality-boundary certificate. |

The final option's historical name must be explained because it does not mean the global rank-ten equality proof. Multiple options may be combined. `--workers N` must have N >= 1. The root runner passes its worker count to the two optional full-search tools; the independent finite-module check in the default suite has its own default of two workers.

## Package structure and immutable evidence

Preserve the original directory hierarchy and all original bytes under a dedicated `certificates/` subtree. The source manifest covers every original file except itself, and proof components contain further explicit source-hash dependencies. Removing data or translating files in place would invalidate those provenance checks. A full preserved bundle is therefore preferable to an unvalidated attempt to identify a smaller transitive dependency closure.

Place the current English manuscript, reader documentation, supplementary translations, repository instructions, and safe verification wrapper outside the immutable subtree. Label older reports and older statements of open problems as historical. The new manuscript and current status document should be the reader's default entrypoint.

Two historical exploratory helpers contain hardcoded paths:

- `research_20261007/equality/explore.py`
- `research_20261007/rank10/early_flags/run.sh`

Neither is called by the supported root verification entrypoints. Retain them as historical records, but do not recommend them as portable commands. Other detected absolute paths occur in historical logs, manuscript examples, or archived build records; they do not prevent the default suite from running in the isolated directory.

## English-language coverage

Seventeen text files contain Cyrillic. Most are archived Russian reports or explanatory notes with corresponding English versions. Two report-authoring scripts embed both language variants. The mathematical verifier source and its comments are English.

The sole Russian reader-facing note without a same-stem English counterpart was `research_20261007/clusters/RESULTS_RU.md`. Its full English translation is supplied separately as `docs/translations/CLUSTER_RESULTS_20261007_EN.md`, with a clearly marked historical note explaining that the later global rank-ten equality result supersedes its restricted equality-class statement. The original remains unchanged in the evidence archive.

## Privacy and unrelated material

A text-pattern scan found no token-like API credentials, private-key blocks, or password assignments. The scan is not a formal security guarantee. The email addresses in `source_extracted.txt` are the three original manuscript authors' publication contact metadata; they are not access credentials. They may also appear in the original source PDF. The archive contains research material and historical verification/build records; no unrelated project file was identified in this inventory.

The package is prepared for the author's review and eventual repository creation. This audit did not create a remote repository, publish files, send messages, or obtain external review.

## Machine-readable records

- `inventory.json`: file counts, extensions, import inventory, language inventory, historical absolute-path locations, and scan results.
- `routine_verification.json`: the actual re-execution result and its scope.
- `routine_suite.log`: complete runner output for the successful 21-invocation run.

The source package's own recorded full-generation and historical review evidence remains distinct from the checks repeated during repository preparation.

## Repository wrapper validation

The repository-level command `python3 scripts/verify.py` was also run from the final repository tree. It first passed the archived manifest check, then copied the evidence to a temporary directory, dispatched all 21 default invocations, and returned exit code 0 after 118.633 seconds. The original certificate tree subsequently passed all 8,194 hashes again. No full-regeneration flags were used. The successful wrapper record is `wrapper_run.json`; its console output is `repository_wrapper.log`.

During that run, code review found that the wrapper's original log-copy operation also copied 20 archived logs that had not been executed in the current invocation. The shipped wrapper was corrected to derive the selected log filenames from its current `RUN` lines. The already-running process had loaded the earlier log-copy code, so it was not described as a full execution of the patched wrapper. The final log-selection algorithm was then checked separately against the actual successful trace: exactly 21 unique log filenames were selected, and all 21 exist. The resulting record is `wrapper_log_selection_check.json`; only those 21 fresh logs are provided under `validation/routine_logs/`. This narrow correction did not change dispatch, proof execution, or certificate isolation.

The repository's `.gitattributes` disables automatic text conversion, preserving the byte hashes when cloning on systems that would otherwise convert line endings.
