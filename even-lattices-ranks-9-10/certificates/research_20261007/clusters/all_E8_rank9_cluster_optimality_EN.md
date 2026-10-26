# No antipode improvement from any rank-nine section containing sqrt(3)E8

## Statement and scope

Let K be any even integral positive-definite rank-nine lattice of minimum at least 6 which contains a primitive sublattice J isometric to sqrt(3)E8. Write D=det K. The established determinant bound D>=21870 is used here (its restricted J-containing case also follows directly from the glue radius of J).

For every finite cluster S in K dual with squared diameter beta<6 and s=|S|, the antipode center density at the guaranteed radius sqrt(6-beta)/2 satisfies

    delta(S,K) <= 6^(39/2)/(2^39 sqrt(21870)).

Equality requires s=1 and D=21870. Thus neither a nontrivial cluster over K9 nor any larger-determinant J-containing rank-nine section can improve the bare K9 density. This is still restricted to sections containing primitive sqrt(3)E8. It does not prove optimality over arbitrary rank-nine sections or over ambient packings with a larger actual minimum than the guaranteed one.

## Primitivity is automatic

The adjective primitive can be dropped from the hypothesis. If J is any embedded copy of sqrt(3)E8, let Jbar=K intersect span(J) be its saturation and let m=[Jbar:J]. Then min(Jbar)>=6 and det(Jbar)=6561/m^2. The exact rank-eight Hermite bound gamma8=2 gives det(Jbar)>=(6/2)^8=6561, whence m=1. Thus every such embedded J is already primitive.

## Projection and normalization

Orthogonal projection maps K dual into J dual=(1/sqrt(3))E8. All nonzero projected squared distances belong to (2/3)Z. Each projection fiber is a translate of a one-dimensional lattice of step length

    tau = sqrt(6561/D) <= tau0 = sqrt(3/10).

The density relative to the bare determinant-21870 packing is

    R = s sqrt(21870/D) (1-beta/6)^(39/2)
      = sqrt(10/3) tau s f(beta),
    f(beta)=(1-beta/6)^(39/2).

Write M for the number of distinct projected points and s_i>=1 for the fiber cardinalities, so s=sum s_i. A fiber of s_i points has span at least

    l_i=(s_i-1)tau,

and l_i<=sqrt(beta). For two different fibers, the largest vertical cross-distance is at least (l_i+l_j)/2. Consequently

    beta >= projected_distance_squared + (l_i+l_j)^2/4.       (1)

The elementary interpolation-polynomial bound from the fixed-section proof gives at most binom(9+r,r) projected points when at most r positive distances occur. For one distance the sharper elementary simplex bound is 9. In particular:

    beta<4/3: M<=9;
    beta<2: M<=55;
    beta<8/3: M<=220;
    beta<3: M<=715;
    beta<6: M<=24310.

The latter two follow from r<=4 and r<=8, respectively.

## One projection point

If M=1 and s>=2, then beta>=(s-1)^2 tau^2. It follows that

    R <= [s/(s-1)] sqrt(10 beta/3) f(beta).

The function sqrt(beta) f(beta) attains its global maximum on (0,6) at beta=3/20. Since s/(s-1)<=2,

    R <= sqrt(2) (39/40)^(39/2) <1.

This is an exact inequality because its square is 2(39/40)^39<1. If s=1, beta=0 and R=sqrt(21870/D)<=1, with equality exactly D=21870.

## Multiple projections and beta<4/3

Necessarily beta>=2/3. If all fibers are singleton, then

    R <=9 f(2/3)<1.

Otherwise let t>=u be the largest two fiber cardinalities. Thus t>=2, u>=1, M>=2, and s<=t+(M-1)u. Equation (1) gives

    tau(t+u-2) <=2 sqrt(beta-2/3).

The elementary inequality

    [t+(M-1)u]/(t+u-2) <= M+1

holds because the difference after clearing the denominator is M(t-2)+2(u-1)>=0. Therefore

    tau s <=2(M+1)sqrt(beta-2/3) <=20 sqrt(beta-2/3),
    R <=20 sqrt((10/3)(beta-2/3)) f(beta).

The last function has its maximum for beta>=2/3 at beta=4/5. Its value there is

    (40/3)(13/15)^(39/2) <1.

Squaring reduces the claim to (1600/9)(13/15)^39<1, checked exactly.

## Diameters 4/3<=beta<2: heavy fibers

Put b=sqrt(beta-4/3). Call a fiber heavy if l_i>b. By (1), projections of two heavy fibers cannot be at squared distance 4/3: their sum of spans exceeds 2b. Their projected squared distance must therefore be 2/3. There are at most nine heavy fibers.

Since there are at most 55 fibers in total and each span is at most sqrt(beta),

    tau s = M tau + sum_i l_i
          <=55 tau0 +46 sqrt(beta-4/3)+9 sqrt(beta).

Normalizing by tau0 yields

    R <= [55+46 sqrt((10/3)(beta-4/3))+9 sqrt(10 beta/3)] f(beta).

For 4/3<=beta<3/2, use sqrt(5/9)<3/4 and sqrt(5)<9/4 to get

    R < (439/4) f(4/3)<1.

For 3/2<=beta<2, use sqrt(20/9)<3/2 and sqrt(20/3)<8/3 to get

    R <148 f(3/2)<1.

Both final comparisons are exact after squaring.

## Larger diameters

The universal fiber bound s_i<=1+sqrt(beta)/tau gives

    tau s <= M(tau0+sqrt(beta)),
    R <= M(1+sqrt(10 beta/3))f(beta).

Use the projected point counts and simple rational square-root bounds:

| beta interval | M bound | bound R<=B f(left) |
|---|---:|---:|
| [2,8/3) | 220 | B=880, using sqrt(80/9)<3 |
| [8/3,3) | 715 | B=12155/4, using sqrt(10)<13/4 |
| [3,6) | 24310 | B=133705, using sqrt(20)<9/2 |

Each resulting upper bound is strictly less than one, verified by exact rational powers. These intervals, together with the earlier cases, cover all beta<6.

No discriminant group size or upper bound on D is needed in this proof. The only use of the section determinant is tau<=sqrt(3/10). There is no finite search through the infinitely many larger-determinant sections.

## Certificate

`verify_all_E8_rank9_cluster_optimality.py` checks all arithmetic constants, projection dimension bounds, square-root majorants, and density inequalities exactly. The two differentiations yielding beta=3/20 and beta=4/5 are shown in the script algebraically: for (beta-c)^(1/2)(1-beta/6)^(39/2), the critical point solves 6-beta=39(beta-c), hence beta=(6+39c)/40.


A quantitative consequence of the displayed bounds is that every nontrivial cluster in this entire rank-nine family has density ratio at most 9(8/9)^(39/2)=0.9052495585... relative to the bare determinant-21870 packing. This upper bound is not claimed to be sharp. The verifier compares all case bounds to its square exactly.
