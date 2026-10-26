# Uniform rank-ten cluster bound for a single E8 projection fiber

This is a validated partial result. It does **not** establish optimality for arbitrary clusters having multiple projections to E8/sqrt(3).

Let K be an even integral rank-ten lattice of minimum at least 6 containing J=sqrt(3)E8. Set P=pi_(J perpendicular)(K), and T=P dual=K dual intersect J perpendicular. The sublattice J is automatically primitive by the rank-eight Hermite bound. Every nonzero vector of P has squared norm at least 10/3: subtracting a nearest J-vector from a lift uses the known squared glue radius 8/3 of J and min(K)>=6. Thus

    min(T dual)=min(P)>=c=10/3.

Write V=covol(T). Since det(K)=6561 det(P), the center-density ratio relative to the bare determinant-54675 rank-ten packing is

    R=(5/sqrt(3)) V s (1-beta/6)^19.

Suppose all s>=2 cluster points have the same projection to J dual. They then form a finite subset of one translate of the planar lattice T.

## Collinear clusters

Let a be the length of the primitive generator of T on the line of the cluster. A primitive dual vector perpendicular to this line has length a/V, so V/a<=1/sqrt(c). The segment containing the cluster has length at least (s-1)a and at most sqrt(beta). Hence

    sV <= [s/(s-1)] sqrt(beta/c) <=2 sqrt(beta/c),
    R <= sqrt(10 beta) (1-beta/6)^19.

The right-hand side is maximized at beta=2/13, with square

    (20/13)(38/39)^38 <1.

This covers every collinear cluster, uniformly over all planar lattices T with min(T dual)>=10/3.

## An elementary planar lattice anticode area bound

For any planar lattice T of covolume V, every noncollinear finite cluster of squared diameter beta satisfies

    s V <= (8/3) beta.                                  (1)

Here is a proof. Let C be its convex hull. Passing to all lattice points of C can only increase the cardinality, so let N=|C intersect T|>=s. Pick's theorem, after a linear change from T to Z^2, gives

    area(C)/V = I+B/2-1 >= (N-2)/2.

Thus NV<=2N area(C)/(N-2).

* If N=3, the hull is a triangle of diameter at most sqrt(beta), hence area<=sqrt(3) beta/4. Consequently NV<=3sqrt(3) beta/2 <(8/3)beta.
* If N=4, the hull is a triangle or quadrilateral. In either case area<=beta/2; for a quadrilateral this follows by expressing area as half the cross product of the diagonals, each of length at most sqrt(beta). Consequently NV<=2 beta <(8/3)beta.
* If N>=5, the planar isodiametric inequality gives area(C)<=pi beta/4. Hence NV<=5pi beta/6 <(8/3)beta, using pi<16/5.

This proves (1). The constants are deliberately loose and are not asserted to be optimal.

## Noncollinear single-fiber clusters

Applying (1),

    R <= [40/(3sqrt(3))] beta (1-beta/6)^19.

The maximum is attained at beta=3/10 and equals

    (4/sqrt(3))(19/20)^19 <1,

whose square is (16/3)(19/20)^38<1.

Therefore every nontrivial single-projection cluster, over **any determinant** rank-ten section containing sqrt(3)E8, gives strictly smaller guaranteed-radius density than the bare determinant-54675 packing.

No enumeration of sections or cluster points is involved. The proof uses only the established E8 glue radius, primitive dual spacing, Pick's theorem and the planar isodiametric inequality. A singleton is treated by the separate determinant lower bound D>=54675 in this E8-containing class.

## Remaining obstacle

When the projections are distinct, up to nine projected points can occur before beta=4/3. Different fibers have correlated planar shapes. Summing the valid single-fiber bounds is too weak near beta approximately 0.8. A complete all-determinant rank-ten theorem requires a sharper joint planar-fiber inequality, or a different argument. Neither this note nor its verifier claims to supply that missing step.

## Additional mixed-fiber lemma for beta<4/3

There is also a uniform result when every non-singleton projection fiber is collinear. The lines need not be parallel.

Assume there are M>=2 projections and beta<4/3, so 2/3<=beta<4/3 and M<=9. If every fiber is a singleton, the determinant bound D>=54675 gives

    R<=9(8/9)^19<1.

Otherwise let a=min_length(T), and let t>=u be the two largest fiber cardinalities. Because each fiber is collinear, its diameter is at least (s_i-1)a. Averaging the squared cross-distances of the four endpoints of two fibers gives

    beta>=2/3+(d_i^2+d_j^2)/4,
    a^2[(t-1)^2+(u-1)^2]<=4 Delta,
    Delta=beta-2/3.

Also V/a<=1/sqrt(c) as above and s<=t+(M-1)u. For integers t>=u>=1 with t>=2,

    [t+(M-1)u]/sqrt((t-1)^2+(u-1)^2)
    <=max(M+1,sqrt(2)M)<=9sqrt(2).

To prove the first inequality, put x=t-1>=y=u-1>=0. If y=0, the ratio is (M+x)/x<=M+1. If y>=1, put r=x/y>=1; the ratio is at most (2M-1+r)/sqrt(1+r^2), whose derivative is negative for r>=1 and M>=2. Its maximum is therefore sqrt(2)M.

Combining the bounds,

    R <=18sqrt(5 Delta)(1-beta/6)^19.

This function is maximized at beta=94/117. Its squared maximum is

    1620*(16/117)*(304/351)^38 <1,

and the unsquared maximum is 0.9693652420... . Thus all-determinant rank-ten clusters with beta<4/3 and all fibers collinear are excluded as improvements, even when the lines in different fibers have different orientations.

This additional lemma does not cover mixed clusters containing a noncollinear planar fiber, or general mixed clusters of larger diameter. Those cases remain open in this partial note.
