# Original questions and motivation

The starting point is the supplied manuscript *Optimal Extensions of Cross-Sections: Sphere Packings in Dimensions 38 to 43* by Ivan Dorofeev, Xiaoming Sun, and Chengu Wang. Its original text is preserved as [`certificates/source_main4.pdf`](../certificates/source_main4.pdf), with a searchable extraction in [`source_extracted.txt`](../certificates/source_extracted.txt).

Section 7, “Open problems,” is an **unnumbered discussion**. The numbering below organizes that discussion; it is not an original numbered problem list. Remark 2 supplies a separate embedding question.

## Why determinant minimization matters

Let $\Lambda$ be an extremal even unimodular lattice of rank 48 with minimum squared norm 6, and let $K\subset\Lambda$ be a primitive rank-$r$ section. The orthogonal complement has dimension $n=48-r$ and Gram determinant $\det K$. At the radius $\sqrt6/2$ guaranteed by the ambient minimum, its center density is

$$\delta_n(K)=\frac{(3/2)^{n/2}}{\sqrt{\det K}}.$$

Thus a smaller section determinant gives a larger center density. Every such section is itself even and integral with minimum squared norm at least 6. The integral determinant problem therefore supplies a restriction on every admissible ambient section, even before one asks which abstract lattices can be embedded in a particular ambient lattice.

## 1. Can a smaller rank-nine section improve dimension 39?

Section 7 asks whether a rank-nine section with determinant below $21870$ exists. The manuscript distinguishes the lower-dimensional lattice-record benchmark $19683=3^9$ from the actual integral-section question: the natural rescaled laminated candidate at that benchmark is not integral.

The corresponding abstract problem is to determine $e_9(6)$. The present draft gives $e_9(6)=21870$ and a unique isometry class attaining equality. Consequently, there is no even integral section with a smaller determinant that could improve the standard unclustered construction at the guaranteed radius.

The equality classification strengthens the original minimum question. It is not a classification of every even integral rank-nine lattice of minimum at least 6 at arbitrary determinant.

## 2. Can a smaller rank-ten section improve dimension 38?

Section 7 similarly asks for determinant below $54675$ in rank ten. It distinguishes the lattice-record benchmark $3^{11}/4=44286.75$: an integral determinant at most $44286$ would also improve that lower-dimensional record, whereas an integer determinant from $44287$ to $54674$ could improve dimension 38 without doing so.

The corresponding abstract problem is to determine $e_{10}(6)$. The present draft gives $e_{10}(6)=54675$ and exactly two equality classes up to isometry. Every minimizer contains $\sqrt3E_8$; the classification is global, rather than restricted to lattices assumed in advance to contain that sublattice.

The original manuscript constructs one equality type in the relevant ambient setting. The existence and orbit classification of all embeddings of the second abstract type are separate questions.

## 3. Can antipode clusters improve the constructions further?

The original manuscript already closes the **unclustered** route in dimensions 40, 41, and 42, and also in dimension 43. It explicitly leaves cluster improvements possible. In dimension 43 its six-point antipode cluster is essential to the stated improvement.

For a finite cluster $S\subset K^*$ of squared diameter $\beta<6$, the standard antipode construction gives the guaranteed center density

$$\delta_n(S,K)=\frac{|S|}{\sqrt{\det K}}\left(\frac{6-\beta}{4}\right)^{n/2}.$$

The present draft excludes improvements over the optimal unclustered benchmark for all rank-nine sections containing $\sqrt3E_8$, and for both determinant-minimizing rank-ten types. It gives additional partial estimates for larger-determinant rank-ten sections containing $\sqrt3E_8$.

General cluster optimization remains open, including rank-nine sections without $\sqrt3E_8$, larger-determinant rank-ten sections outside the covered cluster configurations, and the other dimensions, especially the six-point construction in dimension 43. A larger actual radius for a particular ambient realization is also outside the guaranteed-radius comparison.

## 4. Does the analogous section exist in $P_{48m}$?

Remark 2 explains an order-three automorphism construction with fixed lattice $\sqrt3(E_8\perp E_8)$ in $P_{48p}$, $P_{48q}$, and $P_{48n}$. It leaves the corresponding question for $P_{48m}$ unresolved.

There are two distinct issues: the existence of an analogous section as an abstract sublattice of $P_{48m}$, and its realization as the fixed lattice of a suitable order-three automorphism. Failure to find the latter would not by itself exclude the former. The unverified automorphism enumeration mentioned in the original remark is not used as a proof of nonexistence.

This question is not settled by the present package. The printed rank-five section used for dimension 43 in $P_{48m}$ is a different object and does not answer Remark 2.

## Additional questions arising from the investigation

The exact equality classifications, the intrinsic structure of the rank-ten minimizers, and the count of 19 optimal supersections of one fixed printed $K_9\subset P_{48p}$ go beyond the original minimum questions. They do not constitute a full classification of primitive embeddings into rank-48 lattices.

External expert review and the assessment of novelty are outstanding research and publication tasks, rather than further mathematical conjectures.

