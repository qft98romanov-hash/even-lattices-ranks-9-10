# Minimum Determinants of Even Integral Lattices
## Ranks Nine and Ten · Applications to Sphere Packings

**Prepared by Ivan Dorofeev · Working research draft**

Exact determinant bounds, classification of equality cases, and computational certificates motivated by sphere packings in dimensions 38 and 39.

**[Read the paper (PDF)](even-lattices-ranks-9-10/manuscript/paper.pdf)** · [LaTeX source](even-lattices-ranks-9-10/manuscript/paper.tex) · [Source as TXT](even-lattices-ranks-9-10/manuscript/paper.txt) · [Results and scope](even-lattices-ranks-9-10/docs/RESULTS_AND_SCOPE.md) · [Certificates](even-lattices-ranks-9-10/certificates/) · **[Additional verification](verification/2026-10-29/README.md)**

> **Research status.** The manuscript and exact computational evidence are available for review. Independent external mathematical review and confirmation of novelty remain pending. The work was developed with assistance from ChatGPT; it has not been formalized in a proof assistant.

## Abstract

Motivated by primitive sections of extremal even unimodular lattices of rank 48, we study the smallest Gram determinant of a positive-definite even integral lattice with minimum squared norm at least 6. The draft establishes minimum determinants **21,870 in rank nine** and **54,675 in rank ten**, with **one** and **two** isometry classes of minimizers, respectively. The proofs combine structural arguments involving $\sqrt{3}E_8$ with exhaustive finite searches in exact arithmetic; the rank-ten argument uses the external Hermite bound $\gamma_9\leq 2$. These results exclude improvements to the standard unclustered constructions in dimensions 39 and 38 through smaller-determinant primitive sections, at the radius guaranteed by the ambient minimum. At the standard guaranteed antipode radius, further results exclude nontrivial antipode-cluster improvements for rank-nine sections containing $\sqrt{3}E_8$ and for both rank-ten determinant minimizers. General cluster optimization remains open.

## Acknowledgements

I am deeply grateful to **Xiaoming Sun** and **Chengu Wang** for our collaboration on [*Optimal Extensions of Cross-Sections: Sphere Packings in Dimensions 38 to 43*](even-lattices-ranks-9-10/certificates/source_main4.pdf). The constructions and open questions developed in that work provided the starting point and motivation for the present investigation.

## The problem and the main results

For each positive integer $r$, let $e_r(6)$ denote the smallest Gram determinant among all positive-definite even integral lattices of rank $r$ in which every nonzero vector has squared norm at least 6.

Here the determinant is the **Gram determinant** (the square of the covolume), and the minimum is a **squared norm**.

| Rank | Minimum determinant established in the draft | Equality cases up to isometry |
| :--- | ---: | :--- |
| 9 | **21,870** | **One** class, $K_9$ |
| 10 | **54,675** | **Two** classes, $K_{10}$ and $K_{10}^{\mathrm{alt}}$ |

The rank-ten classification is global: containment of $\sqrt{3}E_8$ is a conclusion, not an extra hypothesis. Each of the two minimizers contains a unique copy of $\sqrt{3}E_8$ and exactly three primitive rank-nine sublattices of determinant 21,870.

The rank-nine minimizer belongs to the previously known perfect-form similarity class $Q_{129}$; the lattice itself is not claimed as a new discovery. The question here concerns its extremality in the specified even-integral class and the classification of equality cases.

### Why this matters for sphere packings

For a primitive rank-$r$ section $K$ of a rank-48 extremal even unimodular lattice, the complementary dimension is $n=48-r$. At the sphere radius $\sqrt{6}/2$ guaranteed by the ambient minimum, the center density is

$$
\delta_n(K)=\frac{(3/2)^{n/2}}{\sqrt{\det K}}.
$$

A smaller section determinant would therefore give a denser construction. The determinant results close this route in dimensions **39** and **38**. They do **not** assert optimality among all sphere packings in those dimensions.

[Read the original questions and their precise relation to these results →](even-lattices-ranks-9-10/docs/ORIGINAL_QUESTIONS.md)

## How the proofs work

1. **Reduce the infinite problem to finite searches.** Hermite bounds and chains of primitive sections obtained from shortest dual vectors give explicit determinant windows.
2. **Enumerate and exclude in exact arithmetic.** Integer and rational calculations, saved Gram matrices, and independently implemented checks cover the necessary finite cases.
3. **Classify equality by gluing.** Discriminant classes of $\sqrt{3}E_8$ determine the possible minimizers. The rank-ten equality search separately handles boundary cases that are absent from the strict lower-bound search.
4. **Derive geometric consequences.** The structure of the minimizers gives restrictions on embeddings and on antipode clusters at the standard guaranteed radius.

The manuscript explains why the searches are exhaustive; the certificates allow the finite calculations to be checked. The rank-ten proof uses the known bound $\gamma_9\leq 2$ as an [external input](even-lattices-ranks-9-10/docs/RESULTS_AND_SCOPE.md#external-inputs).

## Further results and remaining questions

- **Cluster bounds.** Nontrivial finite clusters cannot improve the optimal unclustered benchmark for rank-nine sections containing $\sqrt{3}E_8$, at any determinant, or for either rank-ten determinant minimizer. These comparisons use the standard guaranteed antipode radius.
- **A fixed ambient embedding.** The specified copy of $K_9$ in $P_{48p}$ has exactly **19** primitive optimal rank-ten supersections, all of the original type. This counts sublattices extending that fixed copy, not ambient automorphism orbits.
- **Still open.** Cluster optimization outside the covered families, including the original dimension-43 question; the section question for $P_{48m}$; full primitive-embedding orbit classifications; and possible gains from larger actual separations in particular ambient realizations.

[Full statements, assumptions, dependencies, and open questions →](even-lattices-ranks-9-10/docs/RESULTS_AND_SCOPE.md)

## Additional computational audit

A new [verification package](verification/2026-10-29/README.md) provides exact Python/SymPy checks, an actual PARI/GP cross-check, an actual GAP orbit calculation, and fresh reruns of the original verification suite. The new checks agree on the explicit lattice invariants and short-vector lists; the independent boundary checker covers all **4,952** equality-boundary pairs.

The [audit report](verification/2026-10-29/AUDIT_REPORT_EN.md) distinguishes newly implemented checks, reruns of the existing algorithms, and unexecuted adapters. It also documents a known legacy helper limitation and the regression and hardened-branch checks addressing it. Magma, SageMath, and Julia/OSCAR scripts are supplied but marked **NOT_RUN**. The [GitHub Actions workflow](.github/workflows/verify-lattices.yml) is prepared for routine checks and the independent quick checks; its first hosted run is still pending.

These computational checks support reproducibility. The global mathematical conclusions continue to depend on the manuscript's completeness arguments and external inputs, and external expert review remains pending.

## Read and reproduce

| To explore… | Start here |
| :--- | :--- |
| Definitions, theory, and proofs | [English manuscript (PDF)](even-lattices-ranks-9-10/manuscript/paper.pdf) |
| Earlier proofs and supporting reports | [English reading map](even-lattices-ranks-9-10/docs/ENGLISH_READING_MAP.md) |
| Exact programs, matrices, and finite tables | [Certificate archive](even-lattices-ranks-9-10/certificates/) |
| Verification commands and full regeneration options | [Reproducibility guide](even-lattices-ranks-9-10/docs/REPRODUCIBILITY.md) |
| New exact/CAS checks and coverage audit | [Additional verification](verification/2026-10-29/README.md) |
| Recorded checks and build logs | [Validation records](even-lattices-ranks-9-10/validation/) |
| AI assistance and review status | [Provenance and review](even-lattices-ranks-9-10/docs/AI_ASSISTANCE_AND_REVIEW.md) |

<details>
<summary><strong>Run the routine certificate checks</strong></summary>

The project files are in the `even-lattices-ranks-9-10/` subdirectory. From the root of your clone, run:

```bash
cd even-lattices-ranks-9-10
python scripts/verify.py
```

The recorded verification environment is **CPython 3.12 on Linux**; the mathematical verifiers use the standard library. Keep assertions enabled: do not use `-O` or `-OO`. See the reproducibility guide for platform details and the longer regeneration runs.

The routine command checks **8,194 archived file hashes** and executes **21 mathematical checks** in a temporary copy. The recorded routine run on **26 October 2026** passed all 21 checks. The [new audit](verification/2026-10-29/AUDIT_REPORT_EN.md) records a fresh run with all supported optional regeneration modes, together with additional independent checks. Hash checks establish file identity; they do not replace the mathematical completeness arguments.

</details>

---

**Manuscript edition:** 26 October 2026 · **Research snapshot:** 8 October 2026 · **Computational audit and front page:** 29 October 2026 (Moscow; execution logs use UTC).

For attribution and reuse, see [the citation guide](even-lattices-ranks-9-10/docs/CITATION.md) and [NOTICE](even-lattices-ranks-9-10/NOTICE.md). No open-source or open-content license has been selected.
