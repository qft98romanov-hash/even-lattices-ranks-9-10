# Exact general lower bounds for rank ten

Historical bounds, superseded by the completed global search of 7 October 2026,
which proves e_10(6)=54675. See the adjacent rank10 global proof and independent
chain audit. This file preserves the successive lower bounds and their inputs;
its strongest intermediate interval was31595≤e_10(6)≤54675.
All determinants below are Gram determinants; all minima are squared norms.

Assume the independently audited rank-nine input e_9(6)=21870. Let L be a positive definite even integral lattice of rank ten and minimum at least six, and put D=det L. Choose a shortest nonzero dual vector y in L*. It is primitive, since a proper integral multiple could not be shortest. The kernel J=L∩y-perp is a primitive rank-nine sublattice. It remains even and integral and has minimum at least six because it is a subset of L. Thus det J≥21870. The usual primitive-section identity gives det J=D||y||²=D min L*. The Hermite inequality on the arbitrary Euclidean lattice L* gives min L*≤γ_10 D^(-1/10). Consequently

21870 ≤ γ_10 D^(9/10),
D ≥ (21870/γ_10)^(10/9).

This use of e_9 is valid: it is applied to the actual unrescaled integral sublattice J. It is NOT legitimate to replace γ_9 for arbitrary Euclidean lattices by 6/21870^(1/9).

An even integral lattice of rank 2m has determinant congruent to 0 or (-1)^m modulo four. For rank ten, D≡0 or3 modulo4. The following endpoint calculations use this congruence.

## Input A: classical Hermite constants through dimension eight

γ_8=2 and two applications of Mordell give γ_9≤2^(8/7), γ_10≤2^(9/7). Hence D≥24661.03800168..., or D≥24663 with the congruence. This endpoint is certified by integer powers: compare 2^90 D^63 with 21870^70.

## Input B: a published exact rational upper bound

Arnold Neumaier, "Bounding basis reduction properties", Designs, Codes and Cryptography 84 (2017), 237–259. DOI 10.1007/s10623-016-0273-9.
https://link.springer.com/article/10.1007/s10623-016-0273-9

Appendix, Theorem 3.4(i) gives (γ_n−1)/(n−1)≤1/7 for every n>2. Part(ii) says equality occurs precisely at n=8. It follows rigorously that γ_10<16/7. This yields

D > (7·21870/16)^(10/9) =26493.59748167...,
D≥26495.

The endpoint uses only the strict integer comparison 16^10 D^9 > (7·21870)^10. No rounded Rogers or Cohn–Elkies table is used here. Neumaier's theorem imports their verified bounds in its own proof.

## Input C: the public dimension-nine theorem

Mathieu Dutour Sikirić and Wessel van Woerden, "The lattice packing problem in dimension 9 by Voronoi’s algorithm", arXiv:2508.20719v2, 7 February2026, Corollary1.
https://arxiv.org/html/2508.20719v2

Their computational classification proves γ_9=2. Taking that theorem as an external input, Mordell gives γ_10≤2^(9/8), and therefore

D≥21870^(10/9)/2^(5/4)=27910.44165330...,
D≥27911.

The endpoint is certified by the integer comparison 2^45 D^36 ≥21870^40. We have not independently regenerated their roughly2.237billion-form classification. This is an explicitly cited external theorem, not an unproved conjecture, but it is a larger dependency than the classical-only argument.

## Remaining determinant window

Since a known witness has D=54675, the combined results give

26495≤e_10(6)≤54675

using only the published Neumaier input, and

27911≤e_10(6)≤54675

using the public γ_9=2 theorem as well. Any strict counterexample to the upper endpoint has D≤54672 by the same congruence.

For such a counterexample its shortest-dual rank-nine parent has determinant bounded above by44774 using inputA,41976 using inputB, or40054 using inputC. These are exact integer endpoints, and the parent determinant is even.

These larger windows are why the old rank-nine search cannot simply be reused to claim rank-ten optimality: that old search excluded rank-nine determinant below21870 and its rank-eight window was tailored to that top determinant. Rank-ten parents may have rank-nine determinant as large as40054 even with inputC.

## Other approaches examined

The same shortest-dual flag lifting inequality gives D≥3(det J)^2/(4 det H), where H is the shortest-dual rank-eight parent of J. Without sharper structural restrictions on the pair (H,J), combining this with general Hermite bounds does not reach54675. A Bergé–Martinet bound c_10 on sqrt(minL minL*) would imply D≥6·21870/c_10²; no sharp enough certified universal c_10 was established here. Modular theta-series methods would require controlling the varying discriminant form and level; the theta weight alone does not imply the desired determinant bound.

The separate rank10_search investigation proves the sharp bound54675 for lattices containing sqrt3 E8. This report does not assert that every rank-ten minimizer or every potential counterexample contains sqrt3 E8.

## Exact arithmetic certificate

Run `python verify_rank10_bounds.py` with ordinary Python. No floating arithmetic or optional packages are used. The script outputs `EXACT_INTEGER_ENDPOINTS_PASS` and generates the companion JSON with all endpoints.

## Refinement using the new equality and codimension-two theorems

The following improvement imports TWO NEW COMPANION RESULTS, beyond e_9(6)=21870:

1. Every rank-nine even integral lattice of minimum at least6 and determinant21870 is isometric to K9; in particular, it contains sqrt(3)E8.
2. Every rank-ten even integral lattice of minimum at least6 containing sqrt(3)E8 has determinant at least54675.

If D<54675, result2 shows L cannot contain sqrt(3)E8. Therefore its shortest-dual parent J cannot have determinant21870, by result1. Since detJ is even, detJ≥21872. Replacing21870 by21872 in the preceding inequalities gives stronger global lower bounds (the case D≥54675 satisfies them automatically):

* Classical Mordell input: D≥24664.
* Neumaier's published bound: D≥26499.
* Public γ_9=2 theorem plus Mordell: D≥27915.

The unrounded threshold in the last case is

21872^(10/9)/2^(5/4)=27913.27766239... .

The integers27914 are not permitted modulo4, so the first allowed value is27915. This is checked exactly by 2^45 D^36≥21872^40; the integer ceil of the real threshold is27914, and congruence raises it to27915.

These refined numbers should only be used alongside the two companion proofs. Without the rank-nine equality classification, merely knowing e_9=21870 does not justify excluding determinant21870 for J.

## Intermediate refinement: the first certified rank-nine gap

A further companion result, `equality/rank9_gap.py`, imports γ_9=2 and proves that every even integral rank-nine lattice of minimum at least6 and determinant at most24444 is K9. The exact arithmetic behind the preserved rank-eight window is

2^9·24444^8 <15909^9 ≤2^9·24446^8.

The finite part checks all rank-nine extensions of the three surviving rank-eight parents in that window; the only attained determinant through24444 is21870, with the already-classified unique K9 type. The other old rank-eight branches have extension determinant floors above24444.

A strict rank-ten counterexample D<54675 contains no sqrt(3)E8, so its rank-nine parent is not K9. The new gap theorem therefore forces detJ≥24446. Using γ_10≤2^(9/8), we obtain

D≥24446^(10/9)/2^(5/4)=31586.31470763...,
D≥31587.

Thus this intermediate version of the gap gives

31587≤e_10(6)≤54675,

with explicit dependencies on the public γ_9=2 theorem, the new finite rank-nine gap certificate, and the E8-containing rank-ten determinant theorem. The endpoint uses exact integer powers:2^45D^36≥24446^40. The first integer satisfying it is31587, already3mod4. No global rank-ten optimality assertion follows.

## FINAL stable bound:31595, superseding31587

The completed equality-boundary addendum validates the rank-eight endpoint15909 and all newly admitted lower-rank flags. Since rank-eight even lattice determinants are0 or1mod4, the next possible determinant is15912. The exact inequality

2^9·24450^8 <15912^9 ≤2^9·24452^8

therefore extends the rank-nine gap cutoff to24450. The updated complete class scan (equality/rank9_gap.py/.json and rank9_gap_proof_EN.txt) finds only determinant21870, in the same1920+1+2 labelled extensions, all isometric to K9.

A non-K9 rank-nine parent consequently has determinant≥24452. The final strongest rank-ten conclusion is

31595≤e_10(6)≤54675.

Indeed24452^(10/9)/2^(5/4)=31594.92872639..., and the exact comparison2^45D^36≥24452^40 first holds at the integer31595. This integer is3mod4. The proof dependencies remain explicit: public γ_9=2, the completed rank-nine gap and equality certificates, and the rank-ten E8-containing theorem. Neither this refined lower bound nor the subclass classification proves the exact global rank-ten minimum.
