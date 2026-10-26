# Reproducing the exact fixed-K9 ambient results

All main verification uses Python's standard library. Keep `embeddings/` beside `rank10/`; the latter supplies the archived exact E8 enumeration kernel `exact_lattice.py`. Do not use `python -O`, since verification assertions must remain enabled. No floating-point pruning or third-party numerical library is used by the exact Python verifiers.

## Portable verification from the included integer matrices

From the parent of `embeddings/` and `rank10/`:

    python embeddings/verify_ambient_embeddings.py --json
    python embeddings/verify_A10_extension_exact.py
    python embeddings/verify_A10_extension_exact.py --control
    python independent_review/check_fixed_k9_extension_coverage.py

The ambient verifier's `--json` mode is portable and checks the included `printed_matrices.json` directly. It does not need the manuscript PDF or its extraction path. Omitting `--json` additionally re-extracts the matrices from the original `source_extracted.txt` at its original workspace-relative path; that source-comparison step is not needed to check the supplied integer certificates.

The exact negative and control fibers each take roughly one second in the development environment. The independent coverage checker reconstructs561 admissible E8 classes, checks281 sign pairs, validates all19 ambient witnesses, and separately proves primitivity by gcd-one maximal minors. It does not repeat the complete39-dimensional search.

## Full independent replay of all 281 fibers

    python embeddings/verify_all_fixed_K9_extensions.py

The recorded run took397.17 seconds and completed171472428 recursion nodes. It reconstructed all rational prerequisites, compared every fiber's exact counts and actual vectors against the included C++ transcript, and certified19 distinct primitive supersections by their exact residual normals modulo sign.

Expected last line:

    ALL_281_FIBERS_VERIFIED 171472428 19 EXACTLY_19_DISTINCT_SUPERSECTIONS

The result is written to `all_fixed_K9_extensions_verified.json`. The verifier checkpoints after each completed fiber. This is a complete classification of optimal rank-10 supersections of the specific printed K9. It is not a classification of all K9 embeddings in P48p or of ambient automorphism-group orbits.

## Regenerating the exact input data

    python embeddings/prepare_A10_exact_cvp.py
    python embeddings/prepare_A10_exact_cvp.py --control
    python embeddings/prepare_all_fixed_K9_extensions.py

The first two generators use `A10_integer_fiber_basis.json`; include this file. It contains only an integer kernel basis and a lift. Its full-kernel property is checked independently, so the original heuristic reduction used to discover the basis is unnecessary.

The all-fiber generator also uses `ambient_embedding_certificates.json`, `printed_matrices.json`, `A10_exact_cvp_input.json`, and `rank10/exact_lattice.py`.

Optional C++ replay:

    g++ -O3 -std=c++17 -Wall -Wextra embeddings/search_A10_exact_cvp.cpp -o /tmp/check_single_fiber
    /tmp/check_single_fiber < embeddings/A10_exact_cvp_input.txt
    /tmp/check_single_fiber < embeddings/K10_control_exact_cvp_input.txt
    g++ -O3 -std=c++17 -Wall -Wextra embeddings/search_all_fixed_K9_extensions.cpp -o /tmp/check_all_fibers
    /tmp/check_all_fibers < embeddings/all_fixed_K9_extension_inputs.txt

Keep assertions enabled. Input-generation checks bound all fixed-width intermediate integers; the Python replay independently avoids all fixed-width assumptions.

## Files to retain in the final certificate package

Essential code, input, transcript and proof files:

- `verify_ambient_embeddings.py`
- `printed_matrices.json`
- `ambient_embedding_certificates.json`
- `verify_ambient_embeddings.log`
- `verify_ambient_embeddings_from_json.log`
- `A10_integer_fiber_basis.json`
- `prepare_A10_exact_cvp.py`
- `A10_exact_cvp_input.json`
- `A10_exact_cvp_input.txt`
- `K10_control_exact_cvp_input.json`
- `K10_control_exact_cvp_input.txt`
- `verify_A10_extension_exact.py`
- `verify_A10_extension_exact.log`
- `verify_K10_control_exact.log`
- `A10_exact_cvp_verified_result.json`
- `K10_control_exact_cvp_verified_result.json`
- `prepare_all_fixed_K9_extensions.py`
- `prepare_all_fixed_K9_extensions.log`
- `all_fixed_K9_extension_inputs.json`
- `all_fixed_K9_extension_inputs.txt`
- `search_A10_exact_cvp.cpp`
- `search_A10_exact_cvp.log`
- `search_K10_control_exact_cvp.log`
- `search_all_fixed_K9_extensions.cpp`
- `search_all_fixed_K9_extensions.log` — required by the full Python comparison
- `verify_all_fixed_K9_extensions.py`
- `verify_all_fixed_K9_extensions.log`
- `all_fixed_K9_extensions_verified.json`
- `independent_deep_class_crosscheck.json`
- `embedding_findings.md`
- `fixed_K9_19_sections_proof.md`
- `README_REPRO_EXACT.md`

Keep the adjacent `rank10/exact_lattice.py` and the independent-review coverage code/results. The independently generated `rank10/k9_deep_class_pairings.json` supplies an additional class-set cross-check.

Exploratory floating-point scripts/data, compiled binaries, and temporary checkpoint files are unnecessary. In particular, omit `prepare_A10_cvp.py`, `A10_cvp_search_data.json`, `A10_cvp_search_input.txt`, `search_cvp*`, `search_alternative*`, and the extension checkpoint JSON from the release package.
