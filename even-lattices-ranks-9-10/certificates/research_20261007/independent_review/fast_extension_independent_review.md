# Independent review of the exact fast extension kernel

Status: **PASS for the mathematical kernel under its stated input hypotheses.**

Reviewed sources: `rank10/fast_extend.py`, `rank10/fast_extension_proof.txt`, the archived `rank10/exact_lattice.py`, and the old `rank10/extend_flag.py`. Exact hashes and fresh targeted comparisons are in `fast_extension_independent_review.json`.

This is an independent derivation and code review of the optimized extension criterion. It is not a second independent implementation of vector enumeration and does not itself certify completion of the global rank-ten search.

## 1. Hypotheses and full discriminant-class coverage

The parent Gram matrix G must be positive definite, even integral, and have minimum at least 6. Its rank is positive. The supplied determinant interval has positive lower endpoint, and the modulus and allowed residues must include every determinant sought. These are input conditions supplied by the preceding verified flag stage.

Write d=det(G), A=adj(G), and G^{-1}=A/d. Integer pairing columns p represent classes in the discriminant group: two columns have identical A p modulo d if and only if their difference lies in G Z^r. Thus there are exactly d fingerprints. The complete parent-dual ball enumeration is repeated with increasing integer radius until all d fingerprints have appeared. At that point every class has a representative within the last ball, and every vector shorter than that representative also belongs to the ball. Taking the minimum in each class therefore gives its exact minimum M_a/d, not merely an upper bound. Starting at radius 4 is safe; no vector shorter than 4 is omitted. The radius-20 guard raises an exception and cannot turn unfinished coverage into an empty result.

For a shortest representative p of a class, put M=p^T A p and let n be the new diagonal entry. Then the child determinant is D=nd-M and the Schur complement is s=D/d. Every extension class can be put into this form by shifting its lift by a parent vector. The even-diagonal loop starts at the exact ceiling (M+D_low)/d, advances by 2, and ends at nd<=M+D_high. Hence it includes every allowed positive D in the interval, subject only to the explicit determinant congruence.

## 2. Exact primal minimum test, including all layers

A vector in the m-th nonzero layer has least squared norm

    m^2 s + M_(m a)/d = (m^2 D + M_(m a))/d.

The parent already has minimum at least 6. Opposite layers have the same minima. For positive m with m^2 D>=6d the condition is automatic, because class minima are nonnegative. Every other positive m is tested in the code. In particular, multiples for which m a=0 are included and use the zero-class minimum 0; they must not be omitted. The fingerprint multiplication modulo d is exactly the group multiplication needed here. Consequently the all-layer loop is equivalent to minimum at least 6.

## 3. Exact shortest-normal criterion

The child inverse quadratic form at integer dual coordinates (q,m) is

    q^T G^{-1}q + (m-p^T G^{-1}q)^2/s.

The perpendicular normal has squared norm 1/s=d/D. Put Q=q^T A q and t=p^T A q. Multiplication by dD shows that a lifted vector is shorter than the normal exactly when

    D Q + (d m-t)^2 < d^2.

For each q, the best integer m is obtained by distance to d Z. Writing rem=t mod d, the exact distance is min(rem,d-rem). This proves the implemented condition

    D Q + min(rem,d-rem)^2 >= d^2.

The case q=0 cannot produce a shorter nonzero vector: every nonzero integer m gives squared norm at least 1/s. If q is nonzero and DQ>=d^2, no lift can be shorter, so the code skips precisely a safe set. Equality is allowed, as required for a shortest vector rather than a uniquely shortest vector. Negating q leaves Q and the distance unchanged; retaining one sign from every pair loses no condition.

## 4. The single enclosing parent-dual ball

Suppose D>=D_low>0. Any q needing inspection satisfies

    q^T G^{-1}q = Q/d < d/D <= d/D_low.

The complete inclusive ball through d/D_low therefore contains every strict candidate for every determinant under consideration. Enumerating the boundary and then discarding DQ>=d^2 is safe. There is no inward numerical approximation: all bounds are fractions and all final comparisons are integer comparisons.

## 5. The lifting lower bound and parent flag check

Let mu be the parent-dual minimum. A shortest parent-dual vector has a child-dual lift of norm at most mu+1/(4s), by nearest-integer rounding of its last coordinate. If the normal is shortest, then

    1/s <= mu+1/(4s), hence s>=3/(4mu).

Thus replacing D_low by max(D_low,ceil(3d/(4mu))) is necessary for every accepted flag extension and cannot exclude one. Likewise a parent with D_high/d<3/(4mu) has no allowed child.

The kernel obtains the claimed mu as det(the leading rank-(r-1) block)/d and then enumerates every nonzero parent-dual vector through this exact value. It asserts that the minimum found equals the value. This checks the shortest-dual flag basis condition; the test does not silently assume it. Positive definiteness is also checked by the rational LDL factorization in enumeration. The parent minimum and integrality assumptions remain explicit upstream hypotheses.

## 6. Arithmetic and enumeration contract

All optimized-kernel norm comparisons use Python integers or `Fraction`; there is no fixed-width overflow or floating-point pruning. Conversion of dG^{-1} to integers is followed by exact equality assertions. The reused vector enumerator performs a rational LDL decomposition and computes complete integer coordinate intervals using integer square roots of exact rational inequalities. Its returned norms are exact. The old and new implementations share this enumerator, so their agreement is not an independent check of the enumerator itself.

## 7. Fresh direct checks

Four separate parent cases were run through the old and new extension routines: rank-one Gram [6]; rank-two Grams [[6,3],[3,6]] and [[6,0],[0,6]]; and rank-three Gram with diagonal 6 and off-diagonal 3. Their exact ordered child lists agreed, with respectively 9, 53, 5, and 190 children. Every one of the 257 accepted children was also checked by direct primal enumeration through norm 6 and by the old full child-dual inverse test. A deliberately incorrect parent flag basis [[8,0],[0,6]] was rejected by the assertion. These tests include nontrivial shortest-normal rejection: the orthogonal rank-two parent has 31 post-minimum candidates in the fast loop, of which only 5 pass the normal criterion.

The developer's saved six-case rank-eight comparison was also inspected: three positive and three empty parent outputs match the original ordered child lists. Those saved comparisons were not independently rerun as part of this review.

## 8. Scope of a complete search certificate

The resumable parallel driver's preliminary prune uses det(the leading block)/d before calling the kernel. For pruned parents, this is justified only by the preceding certificate that each supplied representative remains in a shortest-dual flag basis; it is not checked by a kernel call that was skipped. A final rank certificate must also cover every parent, use the intended determinant window/congruences, and validate cached-output metadata. At review time the driver's cache check included source and code hashes plus the window, but did not explicitly check modulus, residues, parent index, or parent Gram. Adding these checks, or verifying all cached records afterwards, is required before treating a resumed run as a fully verified global exhaustion. This is a certificate-bookkeeping requirement, not a defect in the integer extension criterion.

The cache concern was resolved during review: both generic drivers were patched to check the missing metadata. I then independently read every one of the 224 completed rank-eight parent records and verified the exact source/code hashes, window [6564,24673], modulus 4 and residues {0,1}, parent index, parent Gram, and child count. All passed, with 19481 total raw children. There were no preliminary parent prunes in this rank-eight stage. This check certifies its record matching, not a fresh rerun of all 224 enumerations.

Conclusion: the optimized mathematical kernel is complete and sound under its stated parent and search-window hypotheses. A global theorem additionally requires finished higher-rank exhaustion and its coverage/isometry/input certificates.
