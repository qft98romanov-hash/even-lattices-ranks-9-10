# Independent enumeration-completeness audit, 10 September 2026

## Verdict and limits

No omission-producing defect was found in the archived general extension
engine or its exact-arithmetic kernel. The algorithm has a complete
mathematical enumeration argument, and the independent finite tests below
agree with it. This finding concerns the general chain through rank seven,
the representative bridges, and the six surviving classes. It does not
replace the separate review of the classical Hermite bounds or the branch
specific rank-eight covering computations.

The crucial distinction is that `run_all_checks.sh` checks validity of the
listed lower/rank-seven data, while `run_full_regeneration.sh` reruns the
exhaustive search and compares the saved data. A static `PASS`, a list of
counts, or a SHA-256 hash alone does not establish that omitted objects do
not exist. The parent audit has assigned a separate full fresh regeneration
to settle that empirical completeness interface.

## Files inspected

`exact_lattice.py`, `extend_flag.py`, `extend_flag_chunk.py`,
`merge_flag_chunks.py`, `verify_flag_chunks.py`,
`verify_lower_flag_chain_exact.py`,
`verify_regenerated_frozen_bridges_exact.py`,
`verify_rank7_survivor_linkage_exact.py`, both run scripts, run-order and
claim-to-certificate documents, and the corresponding sections of the old
English manuscript. The archived inputs were not edited.

## Exact ellipsoid enumeration: proof of the implementation

For a positive definite rational matrix A, rational LDL decomposition gives

    A = L diag(D) L^T,
    x^T A x = sum_k D_k (x_k + sum_{i>k} L_{ik} x_i)^2,

with each D_k positive. The recursion fixes coordinates in descending order.
At each step, the already fixed terms are nonnegative and their exact sum
is subtracted from the exact bound. It therefore remains to enumerate all
integers z satisfying (z-c)^2 <= R, for c=a/b reduced and b>0. This is
equivalent to

    |bz-a| <= floor(sqrt(floor(b^2 R))).

The code uses Python's exact integer square root on the inner integer,
followed by exact ceiling/floor division. This interval is exact, including
its boundary; it is not a floating-point approximation or an inward rounded
interval. Every nonnegative summand decomposition is considered, so no
ellipsoid point can be omitted by the recursion.

The kernel uses arbitrary-precision integers and `Fraction`. No float,
tolerance, machine-word overflow, or approximate square root controls a
search decision. The unused `_ceil_sqrt_fraction` helper and a docstring
describing a superset interval are harmless historical remnants: the active
`_integer_interval` is exact.

## Exact discriminant-class tables

For an integral nonsingular Gram matrix G, the map

    p in Z^r -> G^{-1}p mod Z^r

has kernel G Z^r and exactly det(G) distinct values. Thus it identifies
Z^r/G Z^r with G^{-1}Z^r/Z^r. The code's coordinatewise fractional part is
canonical in [0,1), including negative inputs, since Python integer division
is floor division.

For each integral norm bound B, `enumerate_vectors(G^{-1},B)` enumerates
all points through that bound. Once all det(G) fingerprints have appeared,
each class has a witness of norm at most B. Every possible shorter witness
also has norm at most B and has already been enumerated. The recorded minima
are consequently exact. The finite cutoff at bound 20 raises an exception
if exceeded; it cannot silently skip a class or produce a successful
incomplete result.

The same reasoning establishes the exactness of `dual_minimum`: the first
nonempty complete integer-bounded ellipsoid contains a globally shortest
nonzero dual vector.

## Completeness of the one-vector generation

Let J be an even integral rank-r lattice with Gram G and minimum at least 6,
and J be primitive of corank one in K. Write K=J+Zv and v=y+z, where y is in
J* and z is perpendicular to span(J). Replacing v by v+x for x in J changes
y within its discriminant class and permits the canonical shortest witness
p used by the program. If mu=p^T G^{-1}p and s=||z||^2, the final diagonal
n=mu+s is even, and det(K)=det(G)s. This replacement preserves parity:
the change of squared norm is 2<y,x>+||x||^2, an even integer.

Thus every extension in [low,high] appears at an even integer n satisfying

    mu + low/det(G) <= n <= mu + high/det(G).

The code starts at the exact ceiling, rounds up to the next even integer,
and increments by two through the exact rational upper endpoint. The
determinant congruences only remove necessary-impossible values. The parent
minimal norm is inherited; for each nonzero layer m, the least norm is
m^2 s + mu(m[p]). Negative m give the same value because a class and its
opposite have the same minimum. For m^2 s >= 6, the test is automatic.
The loop over positive m with m^2 s < 6 is therefore both sufficient and
necessary, with the strict stopping inequality correct at equality.

The last coordinate covector belongs to K* and has norm 1/s. Enumerating all
nonzero dual vectors of norm at most 1/s and testing that their minimum
equals 1/s is precisely the shortest-normal condition. Equal-length dual
normals are allowed. This avoids losing lattices with nonunique shortest
dual vectors.

## Safety of the global pruning

For a shortest u in J*, choose c in [-1/2,1/2] so that u+c y0 is in K*,
where y0 is the perpendicular dual normal of norm 1/s. Since u is nonzero,
the lift is nonzero. Orthogonality gives a dual vector of norm at most
lambda_1(J*)+1/(4s). If y0 is shortest, then

    1/s <= lambda_1(J*) + 1/(4s),
    s >= 3/(4 lambda_1(J*)).

The implementation only discards a parent when the prescribed upper
determinant makes this necessary lower bound impossible. Equality is not
discarded. The related rank-seven survivor bound
3*d7^2/(4*d6) <= 15908 follows because the preceding flag step fixes
lambda_1(L7*)=d6/d7. The static verifier independently verifies that property
for every saved raw child before the linkage result is used.

## Isometry reduction and flag completeness

The short-shell signature is used only as a necessary invariant and uses
one common cutoff for all forms. Collisions are resolved by exhaustive
basis-image search. Each source basis vector has a prescribed norm, so all
possible images occur in the target ellipsoid through the largest source
basis norm. Inner products are enforced as the recursion proceeds. The
first-image sign restriction is safe because simultaneous negation is
always an automorphism. A positive match is checked by the full matrix
identity X^T Rep X=Raw and det(X)=+/-1.

For completeness of a lower-bound proof, positive isometries linking every
raw input to some representative are sufficient: accidental failure to
merge isometric objects would only cause redundant work. The implementation
also supplies exhaustive negative isometry tests where a claimed class
count needs them. The regenerated/frozen bridge verifier checks a bijective
set of explicit GL_n(Z) maps, including all 138 rank-six classes.

Replacing a parent by an isometric representative does not discard the
existence of its earlier flag. Transport the earlier flag by that isometry;
future extensions depend on the parent lattice, not on a distinguished
stored basis. The future shortest-dual condition is intrinsic. Thus one
representative per parent isometry class suffices.

The six surviving classes have different rank-seven determinants. Exact
maps therefore establish both that each group is one class and that the six
groups are pairwise distinct. Replacing all 96 raw survivors by six classes
does not omit a branch. The rank-eight follow-up may deliberately
overenumerate extensions of these representatives; this is safe for a
universal lower bound, provided flag-incompatible results are described
correctly in the mathematical text.

## Chunk and replay interfaces

The merger sorts parent intervals, requires the first interval to start at
zero, requires each next interval to start where the previous one stopped,
and requires the final endpoint to equal the total parent count. Each
chunk must list precisely its completed interval and agree on the input
hash and determinant settings. Hence the ranges cannot conceal an omitted
parent or a duplicated parent interval.

Fresh full replay writes into a new temporary directory, eliminating any
dependence on old resume checkpoints. The lower outputs do not serialize
the differing temporary input filenames. Chunk outputs use basenames that
the replay script deliberately keeps fixed. The ordered search and exact
representative selection are deterministic, so the byte comparisons are
well formed and stronger than checking only totals.

The static lower verifier checks all listed raw forms and all positive GL
maps but never calls `extend_parent`. The static rank-seven verifier calls
it only with `--rerun`. These are complementary validity checks, not
standalone certificates of exhaustive generation. Documentation should
state both gates explicitly. Python must be run without `-O`, since the
verifiers use assertions.

## Independent tests performed in this audit

`test_enumeration_independent.py` was created outside the archive. Its
reference enumerator uses adjugate inversion via recursive Laplace
determinants and the coordinate bound

    |x_i|^2 <= B (A^{-1})_ii,

then exhaustively tests the entire integer coordinate box using direct
quadratic-form evaluation. It does not use the archived LDL enumeration
for its reference answer.

The tests completed successfully:

1. 10,000 rational integer-interval cases.
2. 36 exact-boundary cases with centres near +/-10^100.
3. 100 positive definite rational ellipsoids of ranks one through four,
   comparing the complete sorted point sets and norms.
4. 60 arbitrary integer determinants through rank six, comparing Bareiss
   against an independent recursive determinant.
5. Exact class minima for [6] and all five rank-two parent representatives.
6. An independently implemented one-vector enumerator using box searches
   for the primal and dual conditions, recovering all 7 rank-two raw forms
   and all 52 rank-three raw forms, with complete matrix-list agreement.

The terminal result was `ALL_INDEPENDENT_ENUMERATION_KERNEL_TESTS_PASS`.
These finite tests support the static algorithm proof; they are not a
replacement for that proof or for the separately assigned complete replay.

## Suggested report wording

The renewed audit should distinguish: (a) the mathematical completeness
proof, (b) source-level exact-arithmetic review, (c) independent low-rank
and kernel cross-checks, (d) full regeneration against released data, and
(e) verification of each released branch certificate. It should not call
the entire pipeline an independent software implementation merely because
the data were rerun: the full replay intentionally reuses the archived
generator, while the new independent box enumerator covers only the
specified kernels and low-rank stages.
