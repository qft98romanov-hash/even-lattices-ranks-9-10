# Even Integral Lattices of Ranks Nine and Ten

**Working research draft with exact computational certificates.** This package was prepared on 26 October 2026 from the completed research records of 7–8 October 2026. It is intended for mathematical review and repository preparation. Independent external review and a definitive assessment of novelty remain pending.

The project addresses the determinant questions arising in *Optimal Extensions of Cross-Sections: Sphere Packings in Dimensions 38 to 43* by Ivan Dorofeev, Xiaoming Sun, and Chengu Wang. The present package has been prepared for Ivan Dorofeev with assistance from ChatGPT. The attribution of the original manuscript does not establish a final author list for a future standalone paper.

## Read first

- [English manuscript, PDF](manuscript/paper.pdf)
- [LaTeX source](manuscript/paper.tex) and [the same source as a `.txt` file](manuscript/paper.txt)
- [Original questions and their relation to the results](docs/ORIGINAL_QUESTIONS.md)
- [Results, assumptions, and remaining questions](docs/RESULTS_AND_SCOPE.md)
- [Reproduction instructions](docs/REPRODUCIBILITY.md)
- [AI assistance and review status](docs/AI_ASSISTANCE_AND_REVIEW.md)
- [Quick guide to creating the repository](docs/GETTING_STARTED.md)
- [English reading map, including the earlier full theory](docs/ENGLISH_READING_MAP.md)

## Main statements

All lattices below are positive definite, even, and integral. Their minimum means the minimum **squared norm**, and their determinant is the **Gram determinant**, the square of the covolume. Write

$$e_r(6)=\min\{\det L:\operatorname{rank}L=r,\ \min L\geq6\}.$$

| Problem | Result in the draft |
| --- | --- |
| Rank-nine minimum | $e_9(6)=21870$, with one isometry class attaining equality |
| Rank-ten minimum | $e_{10}(6)=54675$, with exactly two isometry classes attaining equality |
| Structure of either rank-ten minimizer | A unique sublattice isometric to $\sqrt3E_8$ and exactly three primitive rank-nine sublattices of determinant $21870$ |
| Clusters over rank-ten minimizers | Every nontrivial cluster has guaranteed density ratio at most $9(8/9)^{19}<1$ relative to its unclustered construction |
| Rank-nine clusters containing $\sqrt3E_8$ | No nontrivial cluster, at any section determinant, reaches the optimal unclustered rank-nine-section benchmark at the guaranteed antipode radius |
| A fixed embedding in $P_{48p}$ | Exactly 19 distinct primitive optimal rank-ten supersections of the specified printed $K_9$; all have the original rank-ten type |

The rank-ten minimum and equality classification use the external Hermite bound $\gamma_9\leq2$, together with classical lower-dimensional Hermite constants. See [the dependency discussion](docs/RESULTS_AND_SCOPE.md#external-inputs).

The packing application excludes improvements obtained from **smaller-determinant primitive sections** in the standard unclustered construction in dimensions 39 and 38, at the radius guaranteed by the ambient minimum. It does not establish optimality among all sphere packings. The cluster statements concern explicitly specified families and the standard guaranteed antipode radius. The 19 supersections are actual sublattices, not 19 ambient automorphism orbits.

## Check the certificates

The recorded verification environment is CPython 3.12 on Linux. The mathematical verifiers use the Python standard library. Keep assertions enabled; do not run Python with `-O` or `-OO`.

From the repository root:

```bash
python scripts/verify.py
```

This checks the 8,194 archived file hashes and runs the default suite of 21 mathematical checks in a temporary copy, preserving the certificate files. New logs and the run record are saved under `verification_runs/`. For a file-identity check only, use `python scripts/verify.py --hashes-only`. The routine suite was rerun successfully during preparation of this package on 26 October 2026; full regenerations were not repeated during that packaging run. Optional regenerations and platform details are documented in [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md).

## Repository layout

| Path | Contents |
| --- | --- |
| `manuscript/` | Current English manuscript and its editable LaTeX sources |
| `docs/` | English guide to the questions, claims, scope, and reproduction |
| `scripts/` | Certificate-preserving verification wrapper and manuscript build helper |
| `certificates/` | Preserved complete research bundle: exact programs, matrices, finite tables, logs, proofs, and historical reports |
| `validation/` | Actual packaging checks, routine verification transcripts, and manuscript build records |

The certificate bundle deliberately retains historical files, including earlier reports and their original language. The current English manuscript and the present documentation state the current mathematical scope. Historical statements that a problem was still open must be read with their dates.

## Attribution, status, and reuse

The rank-nine lattice is identified with the previously known perfect-form similarity class $Q_{129}$; the lattice itself is not claimed as a new discovery. The proposed contribution is the discrete even-integral determinant problem, its equality classification, and the stated additional results.

No open-source or open-content license is selected in this preparation package. Licensing and the final author list are to be settled by the relevant rights holders. See [the short repository preparation checklist](docs/PUBLICATION_CHECKLIST.md).

