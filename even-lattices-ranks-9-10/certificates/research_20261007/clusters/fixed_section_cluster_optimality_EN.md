# All-diameter cluster optimality for K9 and the E8-containing rank-ten equality lattices

**Scope.** This note proves that, for K9 and both determinant-54675 rank-ten equality types containing a primitive sqrt(3)E8, every nontrivial finite cluster S in its dual lattice with squared diameter beta<6 gives strictly smaller center density at the guaranteed antipode radius sqrt(6-beta)/2 than the singleton cluster over the same section. The original K10 is one of the two rank-ten types. This note does not assert optimality over higher-determinant sections or rank-ten sections not containing sqrt(3)E8. All diameters are included; there is no radius cap at beta=1, point cap, or clique-search cap.

The dimension of the packing is n=48-k. Relative to the bare packing from the same rank-k section K, the density factor of a cluster of s points and squared diameter beta is

    R = s (1-beta/6)^((48-k)/2).

We will bound s piecewise and prove R<1 for every s>1.

## Projection and fibers

Let J be the leading rank-eight sublattice of K9 or K10. Its Gram matrix is 3C, where C is an even positive-definite unimodular rank-eight Gram matrix. The exact verifier checks these properties, and also that C inverse is integral and even. Consequently squared distances in J dual belong to (2/3) Z. Orthogonal projection pi maps K dual into J dual: integrality of pairing with J proves this inclusion. Surjectivity is not needed.

The intersection T=K dual intersect span(J) orthogonal acts transitively on each nonempty projection fiber. Hence every fiber is a translate of T. In block coordinates with G=[A B; B^t D], A=Gram(J), the fiber Gram matrix is the inverse of the Schur complement D-B^t A inverse B. Direct rational calculation gives:

* K9: T has rank one and Gram matrix [3/10].
* K10: T has rank two and Gram matrix (1/5)[[2,-1],[-1,2]], namely A2/sqrt(5).

The projection and fiber distances add orthogonally. Thus all projected pairwise squared distances are nonnegative multiples of 2/3, and any full distance is at least its projected distance.

## An elementary bound for projected sets

An equidistant set in R8 has at most 9 points: translating one point to the origin gives a positive-definite Gram matrix for the other vectors.

For r=2 or 3, let P be a finite set with exactly r distinct positive squared distances d_1,...,d_r. For each x in P set

    f_x(y) = product_{i=1}^r (||x-y||^2-d_i).

Evaluation on P is diagonal with a nonzero diagonal; hence these polynomials are linearly independent. Since ||x-y||^2=||y||^2-2<x,y>+||x||^2, their span lies in

    sum_{j=0}^r ||y||^(2j) P_{<=r-j}(R8).

The dimension of this space is at most the sum of the dimensions of the summands. This gives the deliberately loose bounds

    r=2: |P| <= binom(10,2)+binom(9,1)+1 =55;
    r=3: |P| <= binom(11,3)+binom(10,2)+binom(9,1)+1 =220.

These arguments apply to arbitrary Euclidean point sets; no spherical hypothesis is involved. Fewer distance values only improve the bound.

Therefore a projected cluster has at most 9 points if beta<4/3, at most 55 if beta<2, and at most 220 if beta<8/3.

## The one-dimensional fiber for K9

Write a=sqrt(3/10). A fiber has spacing a and diameter at most sqrt(beta).

* If beta<6/5=4a^2, it contains at most two points.
* If beta<27/10=9a^2, it contains at most three points.
* If a fiber contains two points and another projection fiber is nonempty, the squared diameter is at least 2/3+a^2/4=89/120. Indeed any point is at squared distance at least a^2/4 from one endpoint of the first pair in the vertical coordinate.
* If two distinct fibers each contain two points, beta>=2/3+a^2=29/30. The maximum cross-distance between two intervals of length at least a is at least a.
* If two distinct fibers each contain three points, beta>=2/3+4a^2=28/15, by the same argument for intervals of length at least 2a.

For beta<2/3 there is only one projection point. For a nontrivial cluster beta>=3/10.

The resulting upper bounds are:

| beta interval, left closed and right open | upper bound B for s | reason |
|---|---:|---|
| [3/10,2/3) | 2 | one projection fiber |
| [2/3,7/10) | 9 | no multi-point fiber can coexist with another projection; 7/10<89/120 |
| [7/10,29/30) | 10 | at most 9 projections, at most one double fiber |
| [29/30,4/3) | 27 | at most 9 projections, at most 3 points per fiber |
| [4/3,28/15) | 111 | at most 55 projections; at most one triple fiber; s<=2*55+1 |
| [28/15,2) | 165 | at most 55 projections, each with at most 3 points |
| [2,5/2) | 660 | at most 220 projections, each with at most 3 points |
| [5/2,6) | 21870 | injection into K9 dual/K9 |

The injection in the last row follows from min(K9)=6: two distinct dual points in the same class modulo K9 differ by a nonzero vector of squared norm at least 6, impossible when beta<6. The group has order det(K9)=21870.

For every row, exact integer arithmetic verifies

    B^2 (1-left_endpoint/6)^39 < 1.

Monotonicity in beta then gives R<1 throughout the entire interval. No nontrivial cluster exists below beta=3/10. This proves the K9 assertion.

## The triangular fiber for K10

The fiber norm is (2/5)(u^2-uv+v^2). Its possible norms below 14/5 are 0,2/5,6/5,8/5. The exact maximum cardinalities of clusters in this two-dimensional lattice are:

| fiber squared diameter interval | maximum cardinality |
|---|---:|
| [2/5,6/5) | 3 |
| [6/5,8/5) | 4 |
| [8/5,14/5) | 7 |

These three small assertions have complete exact clique certificates. Translate one cluster point to zero. The closed balls at radii squared 2/5,6/5,8/5 contain respectively 7,13,19 points. The verifier enumerates all subsets of the size needed to contradict the bound, with no cap: respectively 20,495,31824 subsets. It also supplies a cluster attaining each bound. Completeness of the ball enumeration follows from

    2(u^2-uv+v^2) >= (3/2)u^2,
    2(u^2-uv+v^2) >= (3/2)v^2;

norm<14/5 implies |u|,|v|<=3. All 49 coordinate pairs in this box are checked, and the graph uses exact integer distances.

A double fiber and any other projection imply beta>=2/3+(2/5)/4=23/30, using the midpoint bound.

For two different multi-point fibers choose nonzero within-fiber difference vectors a,b in T. With their midpoints subtracted, the four cross differences are z plus the vectors (+/-a +/-b)/2. Opposite pairs show that the maximum squared norm of these cross differences is at least

    max(||a+b||^2,||a-b||^2)/4.

This is at least 3/10 for every pair of nonzero T-vectors a,b. If either norm is at least 6/5, the weaker bound (||a||^2+||b||^2)/4 is already at least 2/5. Otherwise both norms equal 2/5; their inner product has absolute value at least 1/5, as follows directly from the six roots of A2. The exact verifier checks all 36 root pairs.

Consequently, for distinct multi-point fibers with projections p,q,

    beta >= ||p-q||^2 + 3/10.

It follows that:

* beta<29/30 permits at most one multi-point fiber.
* beta<49/30 forces the projections of all multi-point fibers to be mutually at squared distance 2/3. There are therefore at most nine such fibers, even when the set of all projections admits distances 4/3.

The complete table is:

| beta interval, left closed and right open | B | reason |
|---|---:|---|
| [2/5,2/3) | 3 | one projection fiber |
| [2/3,23/30) | 9 | either all fibers singleton, or only one projection |
| [23/30,29/30) | 11 | at most 9 projections, at most one triple fiber |
| [29/30,6/5) | 27 | at most 9 projections, fibers of size at most 3 |
| [6/5,4/3) | 36 | at most 9 projections, fibers of size at most 4 |
| [4/3,8/5) | 82 | at most 55 projections, at most 9 multi-point fibers of size at most 4 |
| [8/5,49/30) | 109 | at most 55 projections, at most 9 multi-point fibers of size at most 7 |
| [49/30,2) | 385 | at most 55 projections, fibers of size at most 7 |
| [2,8/3) | 1540 | at most 220 projections, fibers of size at most 7 |
| [8/3,6) | 54675 | injection into K10 dual/K10 |

For every row the verifier checks exactly

    B^2 (1-left_endpoint/6)^38 < 1.

There is no nontrivial cluster below beta=2/5. The intervals cover every possible nontrivial cluster diameter below 6. This proves the K10 assertion.

## What has and has not been established

The original manuscript's restriction beta<=1 is removed for the displayed K9 and K10. The result concerns the antipode packing radius guaranteed by 6-beta. It does not rule out a particular ambient configuration admitting a larger radius because the lower bound on projected pair distances is not attained.

This proof covers the additional nonisometric determinant-54675 rank-ten type described below, but does not cover arbitrary larger-determinant rank-nine or rank-ten sections, rank-ten sections without sqrt(3)E8, or the rank-five section used for dimension 43. If uniqueness of the minimum-determinant rank-nine lattice is separately proved, its combination with the present K9 theorem covers all minimum-determinant rank-nine sections, but still does not cover larger-determinant sections.

Files: verify_fixed_section_cluster_optimality.py; fixed_section_cluster_certificate.json; verify_fixed_section_cluster_optimality.transcript. The verifier is standalone Python using standard-library exact rational arithmetic. It also checks all three displayed matrices have minimum exactly 6 by complete exact enumeration through squared norm 5 and an exhibited diagonal entry 6.

## Structural generalization

No step of the geometric proof uses the glue character or surjectivity of projection. Thus the rank-ten conclusion also holds for every positive-definite even integral lattice K of rank 10 with minimum at least 6 and determinant 54675 that contains a primitive sublattice J with Gram 3C as above and whose perpendicular dual fiber K dual intersect span(J) orthogonal is isometric to A2/sqrt(5). Equivalently, in a basis extending a basis of J, its Schur complement is integrally equivalent to (5/3)[[2,1],[1,2]]. Any further determinant-54675 equality type having these structural properties is covered, whether or not it is isometric to the displayed K10. The analogous generalization holds in rank nine with determinant 21870 and perpendicular dual fiber Gram [3/10].


The second rank-ten representative is explicitly

    [[G8, p, -p], [p^t, 6, -1], [-p^t, -1, 6]],

where G8 is the leading block of K9 and p=(-2,1,3,-1,1,0,1,-1)^t. Its Schur complement is the same as that of the original K10. The verifier checks determinant 54675, minimum 6, and equality of the two Schur complements. Therefore the entire cluster argument applies unchanged to both representatives. The assertion that these are all determinant-54675 rank-ten types containing primitive sqrt(3)E8 depends on the separate equality classification in `../rank10/rank10_e8_theorem.txt`; the present cluster proof itself only needs the structural hypotheses above.
