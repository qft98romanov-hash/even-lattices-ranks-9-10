# Computational audit report

**Audit date:** 29 October 2026 (Europe/Moscow). Machine timestamps are UTC and may therefore show 28 October.

**Reviewed source:** commit `0d8adc415ce93c7fd4448d48104e0b13b7c944f0` of `qft98romanov-hash/even-lattices-ranks-9-10`.

## Outcome and interpretation

All completed mathematical checks described below passed. A previously documented omission in a generic legacy extension helper is explicitly addressed in Section 5; the hardened implementation and its regression test are included in the replay. The original manuscript and certificate files were preserved. This audit combines newly implemented finite checks with reruns of existing algorithms; those two kinds of evidence are distinguished throughout. It is an AI-assisted computational audit, not independent human peer review or a proof-assistant formalization.

The add-on does not by itself establish that the infinite family of all even lattices has been reduced correctly to the enumerated cases. That conclusion depends on the mathematical reductions in the manuscript, reviewed in [COVERAGE_REVIEW_EN.md](docs/COVERAGE_REVIEW_EN.md), and on their external inputs. No computational contradiction was found in the checks performed.

## 1. Explicit lattice arithmetic

New code in `check_exact.py` uses exact integers and rational numbers. SymPy supplies exact linear algebra; a new `fractions.Fraction` LDL enumeration generates every vector within the stated squared-norm bound. No original verifier algorithm is imported. The common input JSON is extracted from matrix literals and records their source hashes.

| Lattice | Gram determinant | Minimum squared norm | Vectors of norm 6 | Norm 8 | Norm 10 |
| --- | ---: | ---: | ---: | ---: | ---: |
| K9 | 21,870 | 6 | 258 | 72 | 252 |
| K10 | 54,675 | 6 | 294 | 216 | 756 |
| K10_alt | 54,675 | 6 | 294 | 216 | 762 |

The complete coordinate lists through norm 10 are retained in `results/exact_vectors.json`. Positive definiteness is checked by exact leading principal minors; integrality and even diagonal entries establish that these are even integral lattices.

The Smith diagonals are:

- K9: `(1,1,3,3,3,3,3,3,30)`.
- K10: `(1,1,1,1,3,3,3,3,15,45)`.
- K10_alt: `(1,1,1,3,3,3,3,3,15,15)`.

In particular, the two rank-ten Gram matrices have ranks 4 and 3 over F3, respectively. These ranks are invariant under integral unimodular changes of basis and therefore certify nonisometry.

For each rank-ten lattice, exact dual enumeration finds minimum squared norm `2/5` and six shortest vectors spanning a two-dimensional space. All six pairing normals vanish on the first eight basis vectors. Each antipodal pair defines a primitive rank-nine kernel; all three kernels have determinant 21,870, minimum 6, and 258 minimal vectors. Explicit kernel bases are retained in the exact report.

For K9, outer products of the 129 antipodal pairs of minimal vectors span all 45 symmetric-matrix coordinates. The checker records an independently chosen nonzero 45-by-45 minor, with determinant 3. This checks perfection of this explicit form; it does not alone prove the global determinant bound.

### Why the enumeration is exhaustive

For an exact decomposition `G = L D L^T`, the quadratic form is a sum of positive rational multiples of squared shifted coordinates. Descending through the coordinates leaves an exact nonnegative residual budget. At each step the checker uses a conservative integer interval and rejects points only after evaluating the exact rational inequality. It uses no floating-point square root to decide an endpoint. Thus every integer vector inside the ellipsoid is visited, including boundary points.

An independently implemented box enumeration was used on 27 small positive-definite forms, including rational, scaled, and skew cases and a zero bound. All vector sets agreed, including 55 exact boundary points. This is a targeted implementation check, not a substitute for the interval argument.

## 2. PARI/GP cross-check

PARI/GP **2.19.0** was built from its official source archive using the native arithmetic kernel, without GMP or readline. The source archive hash, command, script hash and input hash are recorded in `results/pari_run.json`.

The GP program recalculates determinants, positive definiteness, shell counts, shortest dual-vector data, explicit isometries after a unimodular basis change, and automorphism generators. Every returned isometry/generator is checked against an exact Gram-matrix identity. The two rank-ten forms are also rejected as isometric.

The complete PARI coordinate sets, with both signs restored, were compared with the exact enumerator: **582**, **1,266**, and **1,272** nonzero vectors through norm 10, respectively. All sets agree, not merely their cardinalities. The comparison is reproducible with `compare_pari_vectors.py`.

PARI's `qfminim` documentation cautions that its floating-point enumeration is not unconditionally guaranteed. Accordingly, this run is corroboration; exhaustive completeness for these small-vector sets is supplied by the separate rational enumerator. Agreement between Sage's PARI backend and GP would not be a second independent enumeration engine.

## 3. GAP finite orbit calculation

GAP **4.12.1** was actually run. Its new checker performs exact rational LDL enumeration in E8, producing 26,641 vectors of squared norm at most 8, including zero. This covers all 6,561 residue classes modulo 3. Their least squared norms have distribution

`0: 1, 2: 240, 4: 2160, 6: 2240, 8: 1920`.

The group generated by the eight basis-root reflections has order **696,729,600**. Membership of the reflections belonging to all 120 antipodal root pairs is checked. A chosen deepest class has stabilizer order **362,880**. Its **561** admissible partner classes split into orbits of sizes **560** and **1**; the singleton is the negative class.

This is an independent finite check of the E8 gluing-orbit calculation. It does not itself prove that every determinant-minimizing rank-ten lattice contains the required E8 section.

## 4. Determinant windows and equality boundary

`check_windows.py` independently recomputes the exact Hermite-based windows, rounding and congruence restrictions, restored branches, boundary exclusions, and selected cluster arithmetic. It uses the archived parent lists as data, not the original checking algorithms.

| Rank | Strict-search upper bound | Equality-search upper bound |
| --- | ---: | ---: |
| 1 | 6 | 6 |
| 2 | 44 | 44 |
| 3 | 210 | 210 |
| 4 | 789 | 789 |
| 5 | 2,492 | 2,492 |
| 6 | 6,459 | 6,460 |
| 7 | 13,938 | 13,940 |
| 8 | 24,673 | 24,676 |
| 9 | 40,054 | 40,056 |
| 10 | 54,672 | 54,675 |

The equality boundary adds four previously pruned rank-seven flags with consecutive determinants 4,131 and 11,658, forcing the next determinant to be 24,676. The checker re-examines these branches; it does not simply reuse the strict-search pruning decisions.

All **4,952** boundary parent/target pairs were checked by a different finite-module enumeration using column Hermite normal form:

- 3,960 excluded by parent lifting;
- 956 excluded by next-step lifting;
- 11 excluded by quadratic content;
- 21 excluded by exhaustive HNF congruence enumeration;
- 4 excluded by exhaustive HNF enumeration and individually verified shorter-dual witnesses.

The HNF checks enumerate **324,852** quotient classes across the 25 remaining pairs. All 18 congruence-compatible classes in the witness cases are excluded by exact witness evaluation. The original parent-list generation is separately replayed by the original suite, described next; the new HNF checker does not regenerate that entire prefix independently.

The cluster check also reevaluates the endpoint inequalities using rational arithmetic, the relevant finite triangular anticodes, and the two-fiber separation calculation. The largest rank-ten density ratio covered by the stated reduction is

`9 (8/9)^19 = 0.9601621523027026 < 1`.

Its scope remains the manuscript's specified families at the standard guaranteed antipode radius. No bound for arbitrary clusters or all ambient realizations is asserted.

## 5. Original algorithm replay and ambient C++ rerun

The complete original wrapper finished with **PASS**: **24 mathematical checks**, with all supported optional regeneration modes selected. Total wall time was **2243.5 seconds**. The 8,194-file certificate manifest passed both the initial check and the final preservation check.

| Longer replay stage | Wall time |
| --- | ---: |
| `verify_equality.py` | 225.948 s |
| `verify_all_fixed_K9_extensions.py` | 342.741 s |
| `verify_global_rank10_certificate.py` | 820.108 s |
| `verify_equality_certificate.py` | 781.662 s |

The strict global run freshly regenerated **1,897 parent lists** and **115,627 raw matrices**. The rank-ten equality run freshly regenerated **5,010 jobs**. Newly generated matrices, ordered hashes, and finite decisions matched the retained certificate data. The complete command, per-job timings, raw logs and fresh generated reports are retained under `results/original_replay/`.

The C++ ambient enumerator was separately recompiled with GCC 13.3, assertions enabled, and the undefined-behavior sanitizer. It again processed **281 fibers** and **171,472,428 nodes**, giving **19 leaves and 19 norm-six witnesses**. The output matches the archived data and the fresh arbitrary-precision Python replay. No sanitizer diagnostics were produced.

The 19 objects are distinct primitive optimal supersections of the **fixed printed K9 embedding**. They are not 19 orbits under an ambient automorphism group, and they do not exclude the alternate rank-ten lattice at a different embedding.

The rank-ten full replay regenerates every scheduled parent-to-child list from the seed through rank nine. Archived choices of isometry representatives are retained, but explicit unimodular maps covering the raw forms are rechecked. The new HNF checker takes those parent lists as inputs; the combined original replay checks their generation.

All optional modes supported by the original wrapper were selected. A separate legacy rank-nine replay was added because the wrapper's rank-nine equality option regenerates only the added endpoint cases and otherwise uses its September baseline.

The separate legacy run **passed all three jobs** in 300.0 seconds overall: full regeneration (244.0 seconds), mandatory certificate checks (273.1 seconds, run concurrently), and the supplementary hardened audit (55.9 seconds). It regenerated 3,699 lower-rank raw forms through rank six and all 138 rank-six parent extensions producing 2,235 rank-seven raw forms. All six residual branches and all five supplementary audit programs passed. All 123 source files remained unchanged; newly regenerated retained data were byte-identical. The report and raw logs are in `results/legacy_rank9_replay/`.

### Known legacy helper omission and its hardened replacement

The older generic helper `allowed_one_vector_extensions` in `verify_rank7_topdown.py` omitted the first nonzero layer whose glue class returns to zero. If the class order is `h` and the orthogonal squared height is `s`, that layer requires `h^2 s >= 6`. Checking only centered nonzero residues does not establish this condition in general.

This is a real, previously documented implementation limitation, not a newly disproved theorem. The retained regression example has parent Gram matrix `diag(22,6,6,6,6)`, glue-class order 2, and `s=1/2`: the old helper accepts an extension of determinant 14,256, but its second layer has squared norm 2. The hardened helper rejects it by testing `h*h*s < 6`.

For the actual legacy branches, a separately verified discriminant-radius bound gives `s >= 6 - 93/22 = 39/22 > 3/2`, so every `h >= 2` automatically satisfies the missing condition. For `h=1`, the zero-class minimum is zero and the allowed even last diagonal is at least 6. The hardened actual-branch replay checks the result with the missing test explicitly restored. The current rank-ten generator instead checks every positive layer with `m^2 D < 6d`, including layers returning to the zero class, and does not share this omission.

The historical source files remain intact for provenance. Use the hardened implementation when reusing the generic legacy helper. Full external computations and redundant historical exploratory cross-checks are not claimed to have been repeated.

## 6. Unexecuted adapters and automated checks

The Magma, SageMath, and Julia/OSCAR scripts were written and statically reviewed against official APIs, but those engines were unavailable. Their retained records say **NOT_RUN**, not PASS. Magma uses proof-enabled shortest-vector routines and an unrescaled dual; Sage uses the correct Hessian `2G`; OSCAR checks explicit primitive sublattices, complements, and finite quadratic gluing data. Execution may still expose engine-version or namespace issues; the scripts become evidence only after successful recorded runs.

The aggregate runner was actually tested with exact Python, PARI and GAP. It verifies completion markers and fresh reports, and compares complete PARI/exact vector lists. Intentional negative controls showed that a missing required engine gives exit code 2 / NOT_RUN, while an executable returning zero without the mathematical completion marker gives exit code 1 / FAIL. These intentional controls are not failed mathematical tests.

The proposed GitHub Actions workflow runs routine original checks and the four available independent checks. It was prepared locally and has not run on GitHub in this audit. It does not perform the long optional replay on every push.

## 7. External inputs and remaining review

The rank-ten argument uses the Hermite bound `gamma_9 <= 2`. The primary source was checked: Mathieu Dutour Sikirić and Wessel van Woerden, *The lattice packing problem in dimension 9 by Voronoi's algorithm*, [arXiv:2508.20719v2](https://arxiv.org/abs/2508.20719v2), revised 7 February 2026. That work reports `gamma_9 = 2` from a classification of 2,237,251,040 perfect lattices. This audit did not reproduce that external computation.

Other theoretical inputs include the classical lower-dimensional Hermite constants, the rank-eight equality characterization by E8, and Mordell-type inequalities. The audit checks how the bounds are used and rounded, while treating the underlying theorems as cited inputs.

The following are not claimed here: a formal verification of the whole manuscript, independent expert acceptance, a comprehensive priority/novelty search, a classification of all primitive ambient embedding orbits, the P48m section problem, unrestricted cluster optimality, or optimality among all sphere packings in dimensions 38 and 39.

## 8. Reproducibility and file preservation

Use the commands in [README.md](README.md) and [CAS_GUIDE_EN.md](docs/CAS_GUIDE_EN.md). Raw reports, successful execution logs, package/source provenance, checker review, and intentional runner controls are retained under `results/`. Fresh runs are written under ignored `runs/` directories.

The original certificate manifest contains 8,194 files. Its identity checks are kept separate from mathematical tests: a matching hash establishes byte identity, not correctness. The new `SHA256SUMS.txt` covers the add-on; source matrices additionally carry their individual provenance hashes.

No certificate or manuscript file is changed by this update. The root README links to the audit, and the new workflow and `verification/` directory supply the additional checks.
