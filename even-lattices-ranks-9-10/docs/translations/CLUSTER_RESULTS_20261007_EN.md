# New results on cluster extensions, 7 October 2026

> Historical note (26 October 2026): This is a complete English translation of the 7 October note `research_20261007/clusters/RESULTS_RU.md`. It preserves that note's scope and status. The subsequent 8 October proof establishes the global rank-ten equality classification and therefore removes the restriction to the E8-containing subclass for determinant-minimizing rank-ten lattices. The current manuscript and repository README specify the present scope. The independent reviews mentioned below were performed within this project; they were not external refereeing.

1. For the original lattice K9 of determinant 21870, the entire range of squared diameters 0 <= beta < 6 has been settled. Every nontrivial cluster in K9* gives a density, at the guaranteed radius sqrt(6 - beta)/2, strictly below the density of the ordinary packing obtained from the orthogonal complement of K9. The restriction beta <= 1 in the original preprint has been removed.

2. A stronger statement: the same negative result relative to the baseline density of K9 has been obtained for **all** even integral lattices of rank 9 with minimum >= 6 that contain sqrt(3)E8, at every determinant D >= 21870. There is no upper bound on D. Primitivity of the embedding of sqrt(3)E8 follows automatically from the rank-dependent Hermite bound. For every nontrivial cluster, the density ratio is bounded above by

   9(8/9)^(39/2) = 0.9052495585...

   This bound is not claimed to be sharp. Equality with the baseline density is possible only for a singleton cluster and D = 21870.

3. For the two nonisometric lattices of rank 10 and determinant 54675 containing sqrt(3)E8, the entire range beta < 6 has also been settled: a nontrivial cluster does not improve the ordinary packing obtained from the corresponding orthogonal complement. The second lattice has matrix [[G8,p,-p],[p^T,6,-1],[-p^T,-1,6]], where p = (-2,1,3,-1,1,0,1,-1). Applying this result to every equality case in this class uses the separate classification in `rank10/rank10_e8_theorem.txt`.

Method: projection of K* onto E8/sqrt(3) bounds the number of projections by the number of possible distances. The projection fibers are a one-dimensional lattice in rank 9, or A2/sqrt(5) in the two rank-ten cases. Bounds on the lengths between fiber endpoints control multiplicities. What remains is a collection of exact rational density inequalities. The only new finite enumeration in the fixed rank-ten proof consists of three exhaustive problems on 7, 13, and 19 points of the planar triangular lattice.

Checks: both standalone Python verifiers use the standard library, integers, and Fraction; all asserted strict comparisons have been checked exactly. The matrices of K9, the original K10, and the alternative K10 have the correct determinants and minimum 6, as checked by exhaustive exact enumeration of nonzero vectors of norm <= 5 together with a diagonal entry equal to 6. Two other agents independently reviewed the corresponding geometric proofs and repeated the exact checks.

Scope of the result: arbitrary rank-nine and rank-ten sections not containing sqrt(3)E8, larger determinants in rank 10, and the rank-five cluster-optimality problem for dimension 43 remain open. Furthermore, the density being optimized here uses the radius guaranteed by the formula 6 - beta. For a particular ambient lattice, the actual minimum of the packing may sometimes exceed this guarantee; such improvements require a separate check.

Proof sources: `all_E8_rank9_cluster_optimality_EN.md` and `fixed_section_cluster_optimality_EN.md`. Verifiers: `verify_all_E8_rank9_cluster_optimality.py` and `verify_fixed_section_cluster_optimality.py`. Machine-readable results: `all_E8_rank9_cluster_certificate.json` and `fixed_section_cluster_certificate.json`.
