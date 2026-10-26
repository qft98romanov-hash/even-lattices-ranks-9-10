# Independent review of the fixed-section cluster proof

Reviewed: ../clusters/fixed_section_cluster_optimality_EN.md and ../clusters/verify_fixed_section_cluster_optimality.py. Replayed exact certificate successfully; transcript stored as cluster_independent_replay.log.

The proof is valid for all finite clusters in the duals of the displayed K9 and original K10, and all squared diameters beta<6, at the radius sqrt(6-beta)/2 guaranteed by the antipode construction. This does not exclude larger radii particular to a given ambient embedding.

Checks of the mathematical reduction:

* The projection lies in J* for J with Gram3C. Since C inverse is integral even, projected squared distances are multiples of2/3. Surjectivity is unnecessary.
* Every nonempty full dual projection fiber is a translate of T=K*∩span(J)-perp. In block coordinates, T has Gram equal to the inverse Schur complement; the exact matrices3/10 and(1/5)A2 were checked.
* The elementary polynomial interpolation space used by the draft gives valid, albeit nonsharp, projected few-distance bounds55 and220. It does not require points to lie on one sphere.
* A pair in one fiber and a point in another give the midpoint thresholds89/120 (K9) and23/30 (K10).
* K9 double-double and triple-triple fiber thresholds29/30 and28/15 are correct, including equality boundaries.
* For K10, four cross-fiber differences give the lower bound max(||a+b||²,||a-b||²)/4. This is at least3/10 for nonzero A2/sqrt5 vectors. If one is not a root, norm sum alone gives at least2/5; if both are roots, abs inner product≥1/5 gives3/10. Therefore the9-multiple-fiber bound below49/30 is valid.
* The finite triangular anticodes are exhaustive: translate to zero; for Q<14 all coordinates have magnitude≤3. The next positive squared norm after8/5 is14/5. The exact maxima3,4,7 are certified by checking every forbidden-size subset and giving witnesses.
* All table intervals are contiguous and left-closed/right-open. Each cardinality bound is valid at its left endpoint. Strict endpoint inequalities use rational integer arithmetic and monotonicity covers the whole interval.
* For beta<6, distinct cluster points have distinct classes modulo K because minK=6, giving cardinality at most detK in the final interval.

No mathematical error found. Suggested only that the radius qualification be placed at the start as well as the end.

A shorter optional projected-set lemma, not needed to change the working certificates: An s-distance set S in R^n has size at most binom(n+s,s). Suppose otherwise; choose nonzero coefficients c_x annihilating all evaluation sums of monomials degree≤s. Put P(x,y)=product_j(a_j-||x-y||²), where a_j are its distinct positive squared distances. Its total degree in(x,y) is2s, so every monomial x^alpha y^beta has |alpha|≤s or|beta|≤s. Hence sum_{x,y}c_x c_y P(x,y)=0. But all off-diagonal values vanish and all diagonal values equal the positive number product_j a_j. This contradicts sum c_x²>0. This gives45 and165 for n8,s2,3; the manuscript's weaker55 and220 already suffice.

Update after the author's extension: the alternative determinant54675 lattice has the same leading3C block and the same triangular dual fiber, so every geometric argument and interval bound applies without modification. Its min6, determinant, and fiber matrix are now also checked by the standalone verifier; the updated verifier was replayed and passed. Therefore both equality types of the sqrt3E8-containing rank-ten subclass are covered. The independent review still does not turn this into a statement for arbitrary rank-ten sections.
