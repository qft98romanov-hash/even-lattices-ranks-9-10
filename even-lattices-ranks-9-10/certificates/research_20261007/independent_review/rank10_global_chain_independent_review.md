# Independent audit of the completed global rank-ten determinant proof

**Status: PASS.** The completed strict-counterexample search supports

\[
e_{10}(6)=54675
\]

for positive-definite even integral rank-ten lattices of squared minimum at least 6. The proof uses the published/preprint theorem \(\gamma_9=2\), the classical Hermite constants through rank eight and rank-eight equality classification, the separately verified \(\sqrt3E_8\)-containing subclass theorem, and the newly completed exact extension computations. **It does not use the previous rank-nine minimum theorem, uniqueness proof, or determinant-gap theorem.**

This is an internal independent mathematical/code/data audit. It is not external refereeing, and it does not independently regenerate every complete extension list with a second implementation.

## 1. Exact mathematical reduction

Let \(L\) be a strict counterexample with determinant \(D<54675\). The determinant of an even integral rank-ten Gram matrix is congruent to 0 or 3 modulo 4; hence \(D\le54672\). The sharp subclass theorem implies that \(L\) contains no copy of \(\sqrt3E_8\).

Choose a saturated flag by taking the orthogonal complement of a shortest primitive dual vector at each step. If \(d_r\) is the rank-r determinant, then

\[
d_{r-1}=d_r\,m(L_r^*)\le\gamma_r d_r^{(r-1)/r}.
\]

Mordell's inequality gives \(\gamma_{10}\le\gamma_9^{9/8}=2^{9/8}\). Exact integer-power comparisons, followed by the required determinant congruences, give the upper windows

| Rank | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Upper determinant | 6 | 44 | 210 | 789 | 2492 | 6459 | 13938 | 24673 | 40054 | 54672 |

In particular the first comparison is \(d_9^{40}\le2^{45}54672^{36}\). The checker verifies the integer floor, the next integer's failure, and every subsequent rounded endpoint.

The classical lower determinants in ranks one through seven are 6, 27, 108, 324, 972, 2187, and 4374. Rank eight has lower determinant 6561; equality forces \(\sqrt3E_8\), which a counterexample cannot contain. The next allowed rank-eight determinant is 6564. Independently of any earlier rank-nine result, \(\gamma_9=2\) gives

\[
d_9\ge6^9/2^9=19683.
\]

Odd-rank even integral determinants are even, so the rank-nine lower bound is 19684. The search covers its entire required interval by the two even-determinant windows [19684,24450] and [24452,40054]. Their numerical meeting point has no mathematical significance and introduces no dependency on the old gap theorem.

## 2. Why the lifting exclusions are valid

For a parent \(J\) of determinant \(d_r\), the stored flag basis has dual minimum \(\mu=d_{r-1}/d_r\). A one-rank extension with Schur complement \(s=d_{r+1}/d_r\) has perpendicular dual normal of squared norm \(1/s\). A shortest vector of \(J^*\) has a lift of squared norm at most \(\mu+1/(4s)\), by choosing its last integer pairing nearest to the required real number. If the normal is shortest, then

\[
1/s\le\mu+1/(4s),\qquad
d_{r+1}\ge\frac{3d_r^2}{4d_{r-1}}.
\]

Every exact exclusion compares \(3d_r^2\) against \(4d_{r-1}U_{r+1}\), with a strict greater-than sign. Equality is retained. This argument applies to actual shortest-dual flags; the extension generators explicitly test that condition, and the audit independently reenumerates all retained-parent dual minima and every final rank-nine dual minimum.

## 3. Full recorded coverage

| Stage | Raw records | Excluded before next stage | Retained records | Covering representatives |
|---|---:|---:|---:|---:|
| Rank 2 | 9 | — | 9 | 6 |
| Rank 3 | 102 | — | 102 | 31 |
| Rank 4 | 729 | — | 729 | 161 |
| Rank 5 | 6934 | — | 6934 | 925 |
| Rank 6 | 28284 | — | 28284 | 3752 |
| Rank 7 | 56269 | 52208 | 4061 | 224 |
| Rank 8 | 19481 | 18110 | 1371 | 47 |
| Rank 9, upper band | 3819 | 3819 | 0 | 0 |

Before generating rank seven, 3252 of the 3752 rank-six representatives are excluded by the same exact lifting inequality; every one of the remaining 500 parents has a completed output. All 224 parents at the rank-eight step and all 47 parents at the upper rank-nine step have completed outputs.

The independent checker verifies the complete parent logs and exact raw-parent linkage in ranks two through six, including all 925 parents of the rank-six generation. Rank-six generation completed and saved its entire raw list before the originally started slow deduplication was interrupted; the subsequent fast covering-isometry file covers all 28284 records.

For later stages it verifies every source hash, code hash, manifest entry, parent index and matrix, determinant window/congruence, and raw count. It checks that the union of completed and safely excluded parents is exactly the full input index set, with no duplicates. It reconstructs every retained-origin list and every exclusion list and compares them exactly with the saved records.

All **41490** covering isometries are checked by integer multiplication \(U^T H U=G\) and \(|\det U|=1\). Every chosen representative is also checked to be an unchanged raw Gram matrix; thus it retains an actual flag basis. Pairwise inequivalence is not needed for coverage or exclusion: extra redundant representatives would only increase the search. Filtering before finding isometry representatives is safe because the tested invariant is the actual dual minimum, expressed through the certified flag determinants.

## 4. Independent removal of the old rank-nine dependency

For the lower rank-nine window [19684,24450], 45 of the 47 rank-eight parents are excluded by exact lifting inequalities. The only two remaining parents have determinants 14641 and 13689.

The independent checker uses its own rational triangular vector enumeration, with exact integer coordinate intervals, to enumerate the dual ball of squared radius 4 in each parent. It obtains:

| Parent index | Determinant | Enumerated vectors, including zero | Distinct discriminant classes |
|---|---:|---:|---:|
| 20 | 14641 | 139441 | 14641 |
| 44 | 13689 | 130261 | 13689 |

The fingerprint is \(\operatorname{adj}(G)p\bmod d\), so precisely d classes exist. Covering all d classes by vectors of squared norm at most 4 proves that every class has minimum at most 4. Any extension of determinant at most 24450 therefore has a nonzero first-layer vector of squared norm at most

\[
4+24450/14641=83014/14641<6
\]

or

\[
4+24450/13689=26402/4563<6,
\]

respectively. This independently proves the two empty extension outputs without relying on their absence of listed children. Together with the 45 exact exclusions it closes the whole lower band. A second audit agent independently obtained the same complete class-ball certificates using separate code in `check_rank9_low_by_radius.py`.

## 5. Final contradiction and exact scope

For all 3819 upper-band rank-nine records, the independent checker recomputes the complete short-dual ball through the claimed normal norm and confirms that this normal is shortest. It then recomputes every rank-ten lifting lower bound. The smallest is exactly

\[
\min\frac{3d_9^2}{4d_8}=\frac{12966723}{212}>54672.
\]

Thus no strict counterexample can continue to rank ten. The two already verified \(\sqrt3E_8\)-containing constructions have determinant 54675 and minimum 6, giving the matching upper bound.

This proves the exact global minimum. It **does not classify all global equality cases**. At determinant 54675 the upper flag windows change, so a separate equality search is required to exclude further types without \(\sqrt3E_8\). The existing classification of exactly two equality types applies to the \(\sqrt3E_8\)-containing subclass.

## 6. Reproduction and limitations of independence

Run, with ordinary Python 3 and assertions enabled:

    python research_20261007/independent_review/check_rank10_global_chain.py

The final run returned PASS in approximately 34 seconds. It independently enumerated the dual minima of **8966 distinct matrices**, checked every stored covering isometry and exact exclusion, and independently proved the two lower-band class-radius bounds. Outputs are `rank10_global_chain_independent_verified.json` and `rank10_global_chain_independent.log`.

The generating extension routines were separately reviewed in `fast_extension_independent_review.md`; their code hashes are fixed in the audit output. A complete second independent regeneration of every extension list was not performed by this checker. Hence the computational proof consists of the reviewed exhaustive-generation arguments and recorded executions, together with this independently verified coverage/linear-algebra/pruning chain. The previous rank-nine minimum/gap certificates are not among its premises.
