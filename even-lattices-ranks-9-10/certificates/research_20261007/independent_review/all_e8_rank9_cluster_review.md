# Independent internal audit: arbitrary-determinant rank-nine E8 sections

7 October 2026.

## Verdict

**PASS.** The expanded theorem in `../clusters/all_E8_rank9_cluster_optimality_EN.md` is supported by a valid geometric argument and exact strict inequalities. It treats every determinant, every finite cardinality, and every squared diameter below 6. It is substantially stronger than the earlier fixed-K9 theorem. No upper bound on the section determinant or finite enumeration of larger-determinant sections is assumed.

Precisely: if K is a positive definite even integral rank-nine lattice of minimum squared norm at least 6 containing a primitive copy of J=`sqrt(3)E8`, then for a nonempty finite S in K dual of squared diameter beta<6,

`|S| (6-beta)^(39/2)/(2^39 sqrt(det K)) <= 6^(39/2)/(2^39 sqrt(21870))`.

Equality is possible only for a singleton S and determinant 21870. The theorem is about the density at the guaranteed antipode radius. It does not establish global optimality over rank-nine sections that lack J, or exclude a particular ambient construction having a larger actual minimum than this radius guarantee.

## Projection, normalization, and fiber checks

Primitivity permits a basis of J to extend to one of K. The determinant identity gives a scalar Schur complement `det K/6561`. Consequently `K* intersect J^perp` has step `tau=sqrt(6561/det K)`, and every nonempty projection fiber is a translate of this group. This statement is about the ambient dual fiber, even when S occupies a sparse subset of it.

Projection is into J dual because every dual vector pairs integrally with every element of J. It need not be onto. Since E8 is even unimodular, all nonzero projected squared distances are positive multiples of 2/3. The proven determinant lower bound gives `tau<=sqrt(3/10)`. The normalized ratio `sqrt(10/3)*tau*|S|*(1-beta/6)^(39/2)` is correct.

For a fiber containing s_i selected points, define the lower span `l_i=(s_i-1)tau`. Its actual span can be larger. This causes no gap: l_i is at most the actual span, and the maximum vertical cross-distance of two intervals is at least half the sum of their actual spans, hence at least `(l_i+l_j)/2`. Thus inequality (1) is valid for arbitrary finite fiber subsets. The identity `tau*|S|=M*tau+sum l_i` uses the defined lower spans, so it too is exact.

The primitive hypothesis can be removed without changing the conclusion. Indeed the saturation J' in K is rank eight with minimum at least 6. If its index over J is m, then `det J'=6561/m^2`. The classical rank-eight Hermite bound `gamma8=2` gives `det J'>=(6/2)^8=6561`, hence m=1. Thus every copy of `sqrt(3)E8` in a minimum-six K is automatically primitive. Leaving primitivity in the statement is nevertheless harmless.

## Cardinality deductions

The projected r-distance bound used here follows by the stated polynomial evaluation argument: the polynomials indexed by projected points evaluate diagonally with nonzero entries, and their span is contained in the sum of spaces `||y||^(2j) P_{<=r-j}(R8)`. Summing their dimensions gives `binom(9+r,r)`; overlaps make this only weaker, not invalid. The special one-distance simplex bound is 9. Therefore the counts 55, 220, 715, and 24310 on their stated half-open beta intervals are valid without any spherical hypothesis.

For `2/3<=beta<4/3`, if a fiber is multiple, the largest two fiber sizes t>=u satisfy t>=2,u>=1 and `tau(t+u-2)<=2 sqrt(beta-2/3)`. The inequality

`t+(M-1)u <= (M+1)(t+u-2)`

is valid: the right side minus the left side equals `M(t-2)+2(u-1)>=0`. This also covers u=1 and only one multiple fiber. The resulting bound `tau*|S|<=20 sqrt(beta-2/3)` is valid. When every fiber is singleton the separate bound `9 f(2/3)` is used. No division by a zero denominator occurs.

For `4/3<=beta<2`, calling a fiber heavy when `l_i>sqrt(beta-4/3)` forces projections of any two heavy fibers to be at distance squared 2/3: distance 4/3 would violate inequality (1), and no other positive projected distance occurs. Thus at most nine fibers are heavy. If h<=9 are heavy and M<=55 total, then

`sum l_i <= (M-h)sqrt(beta-4/3)+h sqrt(beta) <=46 sqrt(beta-4/3)+9 sqrt(beta)`.

The second inequality follows from `sqrt(beta)>=sqrt(beta-4/3)`, including cases M<55 or h<9. This is the only replacement requiring a little care, and its direction is correct. The half-open interval splitting at 3/2 covers all relevant endpoints.

For beta>=2 the universal bound `s_i<=1+sqrt(beta)/tau` and the stated projected cardinalities suffice. The jump to the deliberately weak uniform bound 24310 at beta=3 is justified because there are at most eight positive projected distances below 6. It does not assert there are eight at beta=3.

## Exact maximizations and checks

For fixed c, the squared variable factor is `(beta-c)(1-beta/6)^39`. On c<beta<6 its derivative has the sign of `6+39c-40beta`, so the unique maximum is at `(6+39c)/40`. This proves the two global maximizations at 3/20 and 4/5, rather than relying on numeric sampling.

For the other intervals, upper bounds on square-root terms use the right endpoint and the decreasing density factor uses the left endpoint. These majorants need not be attained together; they remain valid upper bounds. Every proposed rational square-root majorant has been checked by squaring, and all eight final squared density bounds are strictly less than one.

I wrote and executed `check_all_e8_rank9_clusters.py`, which imports none of the cluster proof's code and derives these counts, critical points, majorants, and rational inequalities independently. Its JSON/log files record PASS. This finite arithmetic replay supplements the geometric argument; it is not claimed to mechanically prove the geometric argument.

## Retained inputs and limits

The theorem uses the antipode density formula, the arithmetic and determinant of J, and the minimum determinant lower bound 21870 in the J-containing class. It does not need uniqueness of K9, though the separately established uniqueness identifies the equality section. The restricted determinant bound can also be obtained from the certified maximum J-dual coset minimum 8/3.

This report is an independent internal review with a separate arithmetic implementation. It is not outside refereeing or a novelty certification.
