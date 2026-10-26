# Results, dependencies, and remaining questions

This guide records the scope of the current English manuscript. It separates mathematical statements, external inputs, exact computational evidence, and work still to be done.

## Conventions

All lattices are positive definite unless explicitly stated otherwise. “Even integral” means that all pairings are integers and all squared norms are even integers. For a Gram matrix $G$,

$$\det L=\det G,\qquad \min L=\min_{0\ne x\in\mathbb Z^r}x^{\mathsf T}Gx.$$

Isometry classes are integral isometry classes: $G'=U^{\mathsf T}GU$ with $U\in\mathrm{GL}_r(\mathbb Z)$. “Minimum 6” refers to a squared norm, not a vector length. Center density omits the dimension-dependent volume of the unit ball; this does not affect comparisons in a fixed dimension.

## Rank nine

- The least determinant at minimum at least 6 is $21870$, attained by a unique isometry class $K_9$.
- Below $32076$, the determinant spectrum consists of $21870$, $26244$, and $30618$, with one isometry class at each value. All three contain $\sqrt3E_8$.
- The least determinant for a rank-nine lattice containing no $\sqrt3E_8$ is $32076$. No uniqueness assertion is made at that determinant.
- The equality lattice is identified with the previously known perfect-form similarity class $Q_{129}$. The exact perfection certificate has rank 45. This identification is not a claim that the lattice itself was newly discovered.

## Rank ten

- The least determinant at minimum at least 6 is $54675$.
- Exactly two isometry classes attain the minimum, denoted $K_{10}$ and $K_{10}^{\mathrm{alt}}$. Every minimizer contains $\sqrt3E_8$.
- The two matrices have ranks 4 and 3 modulo 3, respectively, and are therefore not integrally isometric. Each has 294 vectors of squared norm 6.
- Each minimizer contains exactly one copy of $\sqrt3E_8$ and exactly three primitive rank-nine sublattices of determinant $21870$, all isometric to $K_9$.
- The dual has exactly six minimal vectors, of squared norm $2/5$, generating $A_2/\sqrt5$. Their three sign pairs determine the three primitive rank-nine kernels.

The strict lower-bound search and the equality search are different certificates. Moving from determinant at most $54672$ to determinant $54675$ changes intermediate bounds and restores four previously pruned rank-seven flags. The equality proof explicitly handles these changes; equality classification is not inferred solely from the strict search.

## Packing and cluster applications

The determinant theorems prevent density improvements from smaller-determinant primitive sections in the standard unclustered constructions in dimensions 39 and 38, at the radius guaranteed by ambient minimum 6.

For a cluster of squared diameter $\beta<6$, all cluster comparisons here use the standard guaranteed antipode radius $\sqrt{6-\beta}/2$.

| Family | Proven comparison |
| --- | --- |
| Rank-nine sections containing $\sqrt3E_8$, at any determinant | A nontrivial finite cluster has density ratio at most $9(8/9)^{39/2}<1$ relative to the optimal unclustered rank-nine-section benchmark |
| Either rank-ten determinant minimizer | A nontrivial finite cluster has density ratio at most $9(8/9)^{19}=0.9601621523\ldots$ relative to its unclustered construction |
| Rank-ten sections containing $\sqrt3E_8$, at arbitrary determinant | Further partial exclusion results cover a single projected point at every diameter and collinear projection fibers for $\beta<4/3$ |

The numerical upper bounds are not claimed to be sharp. The statements cover all finite cluster sizes within their stated families. They do not bound a larger actual packing radius that might arise from a particular ambient embedding, and do not imply global sphere-packing optimality.

## Ambient embeddings

The printed matrices have exact checks of positive definiteness, integrality, evenness, unimodularity where applicable, section primitivity, complement determinants, and discriminant anti-isometries. The minimum 6 of the full rank-48 ambient lattices is imported from their published construction; a new exhaustive enumeration of the rank-48 shortest shell is not claimed.

For the fixed printed $K_9\subset P_{48p}$, exactly 19 distinct primitive rank-ten supersections attain determinant $54675$. All have the original type $K_{10}$, and the alternative type does not extend this marked copy of $K_9$. This is a count of sublattices, not of ambient automorphism orbits. It does not exclude the alternative type over some other embedding of $K_9$.

## External inputs

The global rank-ten proof and the strengthened rank-nine spectrum use the known bound $\gamma_9\leq2$ from Mathieu Dutour Sikirić and Wessel van Woerden, *The lattice packing problem in dimension 9 by Voronoi's algorithm*, [arXiv:2508.20719v2](https://arxiv.org/html/2508.20719v2). This is an external mathematical input, not a theorem proved by this repository.

The argument also uses the classical Hermite constants through dimension 8, uniqueness of the dimension-eight Hermite extremizer, and Mordell's inequality. The rank-nine minimum and uniqueness have an older certificate route that does not require the sharper dimension-nine theorem. The new global rank-ten search does not assume the older rank-nine lower-bound certificate.

The manuscript gives the definitions and proofs of the extension, gluing, shortest-dual-flag, and determinant-window statements used to reduce the problem to finite searches. Additional geometric results used in the cluster analysis, including the planar geometric inequalities, are identified there.

## What remains open

1. General cluster improvements in dimensions 38 and 39 outside the families just described, and cluster optimization in the other original dimensions, especially 43.
2. The analogous section question for $P_{48m}$ in Remark 2 of the original manuscript, with arbitrary embeddings distinguished from fixed lattices of order-three automorphisms.
3. Full primitive-embedding classifications under the automorphism groups of specified rank-48 lattices, including other embeddings of $K_9$ and the two rank-ten types.
4. Improvements exploiting actual separations larger than the standard guaranteed antipode separation in a particular ambient realization.

Independent external review and a definitive novelty assessment remain pending. These are verification and publication tasks, not claims that the completed rank-nine or rank-ten equality classifications remain mathematically open within the draft.

## What the certificates establish

The retained strict-search full replay regenerated 1,897 parent lists and 115,627 raw matrices. The equality computation generated 5,010 additional parent/window jobs. An independently implemented finite quadratic-module calculation covers 4,952 necessary parent/endpoint pairs. Further checks verify the exact linkage of the saved jobs, recovered flags, raw Gram matrices, terminal exclusions, and intrinsic structure of the two minimizers.

The preserved equality provenance records a fresh complete generation, not a second completed execution of the optional full equality replay. The programs supply an uncached replay option for readers who wish to regenerate those jobs.

The 8 October package records 21 successful routine checks. Internal independent implementations, exact arithmetic, and successful execution do not amount to external refereeing or formal proof-assistant certification. File hashes establish byte identity; the written coverage arguments establish why the finite searches address the mathematical problem.

