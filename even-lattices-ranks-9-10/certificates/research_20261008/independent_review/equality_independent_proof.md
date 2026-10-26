# Independent equality proof: complete finite quadratic-module exclusion

**Status: PASS.** The additional rank-ten equality boundary is fully excluded
by an independent necessary-condition computation, without importing either
of the original one-vector extension implementations or their vector enumerator.
Together with the already audited complete strict-search prefix and the
E8-containing gluing theorem, this proves that every positive definite even
integral rank-ten lattice of squared minimum at least 6 and Gram determinant
54675 contains sqrt(3)E8, and that exactly two abstract isometry classes occur.
The external input gamma_9 <= 2 is retained. This is internal verification,
not outside refereeing or formal proof-assistant certification.

## 1. Data coverage

The independent checker recomputes the enlarged upper determinant windows

    6, 44, 210, 789, 2492, 6460, 13940, 24676, 40056, 54675.

It rechecks every old parent and raw-continuation prune against the enlarged
next upper bound. Exactly four old rank-seven raw forms are restored; no
other old prune becomes invalid. Each restored form has previous determinant
4131 and determinant 11658, forcing its next determinant to be exactly 24676
inside the enlarged window. The proof and exact indices are recorded in
`equality_boundary_coverage_argument.md` and
`equality_windows_and_recovered_prunes.json`.

The new finite-module check covers the following complete parent families:

| Child rank | Endpoint T | Parent family | Number |
|---|---:|---|---:|
| 6 | 6460 | all old rank-five representatives | 925 |
| 7 | 13940 | all old rank-six representatives | 3752 |
| 8 | 24676 | all 224 old eligible rank-seven representatives plus 4 restored raw forms | 228 |
| 9 | 40056 | all old eligible rank-eight representatives | 47 |
| Total | | | 4952 |

For ranks 6 and 7 a few necessary-condition candidates occur, but **every
one fails the next-rank lifting bound**. Thus no new endpoint parent can
continue inside the enlarged flag windows. Consequently no additional
full-window continuation can be missing at a later stage. This proves
inductively that the displayed parent families exhaust all necessary new
checks. The four restored rank-seven forms are separately included even
though they may be mutually isometric.

## 2. Finite quadratic-module obstruction

For an even parent Gram matrix G of rank r, write d=det(G) and A=adj(G).
The integral pairing vector p of a possible new basis vector determines

    c = A p modulo d,
    Q(c) = p^T A p modulo 2d.

Equal fingerprints differ by p' = p+Gz for an integer vector z. Since G is
even,

    p'^T A p' - p^T A p = 2d p^T z + d z^T Gz

is divisible by 2d. Hence Q is well defined on the d-element discriminant
module. It can be enumerated by breadth-first search from c=0 using the
columns A e_j. The update is

    c' = c+A e_j modulo d,
    Q(c') = Q(c)+2c_j+A_jj modulo 2d.

The checker visits exactly d fingerprints and checks consistency whenever
a fingerprint is reached again. These generators span the entire image
of A modulo d, so the search covers every class. An even extension with
determinant T has an even last diagonal n and satisfies

    T = dn-p^T A p,

hence Q(c)=-T modulo 2d. If that value never occurs, no even extension of
determinant T exists at all. A quicker preliminary obstruction uses

    gcd(2d, A_11,...,A_rr, 2A_ij for i<j),

which must divide T. These are arithmetic obstructions only; they make no
assumption about shortest representatives or a minimal-vector basis.

## 3. Exact shortest-normal obstruction, independent implementation

The inverse Gram matrix of a bordered extension has squared dual norm

    q^T G^(-1)q + (m-p^T G^(-1)q)^2/(T/d).

The perpendicular dual normal has squared norm d/T. Choosing m nearest
to p^T G^(-1)q shows that a necessary and sufficient condition for this
normal to be shortest is

    T(q^T A q)+dist(c dot q, d Z)^2 >= d^2

for every nonzero integral q. Only q with T(q^T A q)<d^2 can violate it.
Thus the independent rational LDL enumerator lists the entire parent-dual
ball q^T G^(-1)q <= d/T and retains one vector from each sign pair. Exact
rational coordinate bounds and integer square roots prevent inward floating
rounding. For each compatible finite-module class, any vector violating
the displayed inequality supplies a direct shorter-dual witness.

The enumerator is the independently implemented routine in
`research_20261007/independent_review/check_rank10_global_chain.py`.
Neither `fast_extend.py`, `extend_flag.py`, nor `exact_lattice.py` is imported.
In fact, for exclusions the witnesses alone suffice; enumeration completeness
is needed only to interpret the surviving-class counts as exhaustive for
these necessary conditions.

## 4. First and next lifting obstructions

If the parent flag has preceding determinant d_prev, its last dual coordinate
has squared norm d_prev/d. Any extension normal that is shortest must satisfy

    3 d^2 <= 4 d_prev T.

This excludes many parents before finite-module enumeration. The inequality
uses an explicit nonzero parent-dual vector and does not need an independently
asserted value of the true parent-dual minimum.

Likewise, an extension of determinant T has an explicit normal dual vector
of norm d/T. If it were followed by another shortest-dual extension with
upper determinant U, a necessary condition would be

    3 T^2 <= 4 d U.

Every finite-module class surviving the previous checks at ranks 6 and 7
fails this latter condition. The actual lists are:

| Rank | Target T | Parent determinant d | Number of surviving classes |
|---|---:|---:|---:|
| 6 | 6460 | 1934 | 2 |
| 6 | 6460 | 1830 | 4 |
| 6 | 6460 | 1672 | 4 |
| 6 | 6460 | 1600 | 48 |
| 7 | 13940 | 4428 | 2 |
| 7 | 13940 | 4443 | 4 |
| 7 | 13940 | 4268 | 4 |
| 7 | 13940 | 4379 | 4 |
| 7 | 13940 | 4355 | 4 |
| 7 | 13940 | 4920 | 2 |

At rank 6 even the largest listed d gives

    3*6460^2 = 125194800 > 4*1934*13940 = 107839840.

At rank 7 even the largest listed d gives

    3*13940^2 = 582970800 > 4*4920*24676 = 485623680.

Therefore all 58 and 20 classes are excluded from a full rank-ten flag.
These counts refer to discriminant classes satisfying necessary conditions,
not distinct abstract isometry classes. The fresh original-generator
run produces exactly 58 and 20 raw flag matrices, respectively, providing
additional agreement but not a premise of this independent exclusion.

## 5. Complete exclusion counts

Every parent-target pair is assigned exactly one of the following methods:

| Target | Explicit parent-dual lifting | Polynomial content | Module nonrepresentation | Every compatible class has a shorter dual | Remaining classes fail next lifting |
|---:|---:|---:|---:|---:|---:|
| 6460 | 708 | 71 | 131 | 11 | 4 |
| 13940 | 3252 | 270 | 181 | 43 | 6 |
| 24676 | 0 | 117 | 96 | 15 | 0 |
| 40056 | 0 | 35 | 12 | 0 | 0 |
| Total | 3960 | 493 | 420 | 69 | 10 |

The four restored rank-seven forms are each ruled out by finite quadratic-
module nonrepresentation at T=24676. No shortest-dual flag extension of minimum 6 and determinant
24676 survives from any required rank-seven parent, and no even extension
of determinant 40056 survives from the required rank-eight family.

All 3819 old terminal rank-nine candidates remain excluded at the enlarged
rank-ten target: their smallest necessary next determinant is

    12966723/212 > 54675.

The saved old low band remains empty. No rank-nine parent is left that could
continue to the hypothetical E8-free determinant-54675 lattice.

## 6. Conclusion and reproducibility

Every equality lattice contains sqrt(3)E8. The already verified two-orbit
E8 gluing classification therefore becomes a **global classification**:
exactly the original K10 and its alternative occur. Their Gram ranks modulo
3 are 4 and 3, proving inequivalence independently of any chosen embedding
of E8.

Run ordinary Python, with assertions enabled:

    python research_20261008/independent_review/check_equality_windows_and_recovered_prunes.py
    python research_20261008/independent_review/check_boundaries_by_quadratic_module.py --workers 2

The latter actually completed all 4952 cases and ended with

    ALL_4952_EQUALITY_BOUNDARY_PARENT_TARGET_PAIRS_INDEPENDENTLY_EXCLUDED

Its machine-readable output records every parent index, source hashes,
exclusion type, finite-module residue set where applicable, witness counts,
surviving class fingerprints, and all decisive lifting integers. This
computational exclusion uses a second implementation and a different finite
arithmetic method from the extension generator. The old exhaustive search
prefix and its previously checked covering isometries remain explicit
premises; a boundary audit alone is not an independent regeneration of that
entire old prefix.
