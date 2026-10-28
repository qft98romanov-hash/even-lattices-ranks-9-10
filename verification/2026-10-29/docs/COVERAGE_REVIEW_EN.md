# Independent coverage and boundary review

This is an internal mathematical and computational audit of the archived proof, not an external referee report or a formal proof-assistant verification. The reviewed source is the nested `even-lattices-ranks-9-10` project at repository commit `0d8adc415ce93c7fd4448d48104e0b13b7c944f0`. Source files have not been changed by this review.

**Outcome:** no mathematical coverage error was found in the specific arguments reviewed below. A newly written checker independently recomputed the determinant windows, the changes in old lifting prunes, all 4,952 new boundary-pair exclusions, and the cluster endpoint arithmetic. It returned `PASS`. This conclusion is conditional on the complete strict-search prefix, the separate classification in the subclass containing `sqrt(3) E8`, and the explicitly imported Hermite bounds. Those dependencies must not be replaced by checks of a few example Gram matrices.

The new checker is `../check_windows.py`; its machine-readable result and execution log are `../results/windows.json` and `../results/windows.log`. The run recorded in these files used Python 3.12.14 and SymPy 1.14.0, and took approximately 3 seconds. The JSON records the actual UTC start time, all input hashes, and the individual boundary decisions. The directory date is a package label; the recorded run time is authoritative.

## 1. Why shortest-dual flags cover arbitrary admissible lattices

Let `L` be a positive-definite integral lattice, and let `y` be a shortest nonzero vector of its dual. It is primitive in `L*`: otherwise division by an integer greater than one would give a shorter dual vector. Hence `(y,L)=Z`, and

$$
J=L\cap y^\perp
$$

is a primitive sublattice of corank one. The spacing of the orthogonal projection of `L` onto the line of `y` is `1/||y||`. Consequently, writing Gram determinants as `d`,

$$
d(J)=d(L)\,\|y\|^2.
$$

Apply the Hermite inequality to the **dual** lattice, whose determinant is `1/d(L)`:

$$
\|y\|^2\leq\gamma_r d(L)^{-1/r},
\qquad
d(J)\leq\gamma_r d(L)^{(r-1)/r}.
$$

This is an upper bound for the previous flag determinant. The direction is correct. Repeating the construction gives a primitive flag for every admissible lattice, and every flag member inherits the lower bound 6 for nonzero squared norms. Applying the primal Hermite inequality separately gives

$$
d(L_r)\geq 6^r/\gamma_r^r.
$$

There is no assumption that the lattice has a basis of minimal vectors. The rank-one seed `[6]` follows from the derived upper window and evenness. If the final lattice contains no copy of `sqrt(3) E8`, none of its flag members can contain such a copy. The rank-eight lower endpoint 6561 is therefore removed using the uniqueness of the rank-eight Hermite extremizer; the next determinant permitted by evenness is 6564.

**External dependencies:** the classical Hermite constants through rank eight, uniqueness of the rank-eight extremizer, Mordell's inequality, and the bound `gamma_9 <= 2`. In particular, this audit does not independently redo the published classification underlying `gamma_9 = 2`. The primary source is Mathieu Dutour Sikirić and Wessel van Woerden, [arXiv:2508.20719v2](https://arxiv.org/abs/2508.20719v2), revised 7 February 2026. Its abstract explicitly states `gamma_9 = 2` and the classification of 2,237,251,040 perfect similarity classes. The primary record was checked during the parent audit. This remains an external mathematical input even if every local computational check passes.

## 2. Exact determinant windows and the equality transition

For an even integral Gram matrix of odd rank, its determinant is even. In rank `2m` its determinant is congruent to 0 or `(-1)^m` modulo 4. Thus a rank-ten determinant strictly below 54675 is at most 54672.

Mordell's inequality and `gamma_9 <= 2` give `gamma_10 <= 2^(9/8)`. The first flag step can be checked without floating point:

$$
d_9^{40}\leq 2^{45} d_{10}^{36}.
$$

Each subsequent upper step is `d_(r-1)^r <= gamma_r^r d_r^(r-1)`, followed by the determinant congruence. The new checker computes integer roots with SymPy and verifies both adjacent powers against the exact rational input. It does not merely copy the archived window table.

| Rank | Strict upper bound | Equality upper bound | E8-free lower bound |
|---:|---:|---:|---:|
| 1 | 6 | 6 | 6 |
| 2 | 44 | 44 | 27 |
| 3 | 210 | 210 | 108 |
| 4 | 789 | 789 | 324 |
| 5 | 2492 | 2492 | 972 |
| 6 | 6459 | 6460 | 2187 |
| 7 | 13938 | 13940 | 4374 |
| 8 | 24673 | 24676 | 6564 |
| 9 | 40054 | 40056 | 19684 |
| 10 | 54672 | 54675 | Not used |

There are exactly four newly admitted determinant values: 6460, 13940, 24676 and 40056, in ranks six through nine. This fact alone would not justify reusing the old search: prunes based on the next rank's upper bound also need rechecking.

The new checker re-evaluated all 52,208 rank-seven, 18,110 rank-eight and 3,819 rank-nine raw lifting prunes, and all 3,252 whole-parent prunes. Exactly four rank-seven raw records revive; no other raw or whole-parent prune revives. They are children 606--609 of `rank7_parents/parent_3297.json`. Direct SymPy determinant calculations give

$$
d_6=4131,\qquad d_7=11658,\qquad
d_8\geq\frac{3\cdot11658^2}{4\cdot4131}
=\frac{3775249}{153}.
$$

The only congruence-admissible continuation at or below 24676 is 24676 itself. All four such continuations are independently excluded by the HNF calculation described below.

The lower rank-nine interval `[19684,24450]` must remain part of the base certificate. The next interval is `[24452,40054]`; the omitted integer 24451 is impossible because the rank is odd. The original 3,819 terminal records still require a rank-ten determinant of at least

$$
\frac{12966723}{212}>54675.
$$

Hence none becomes possible merely by changing the top endpoint from the strict bound to equality. The lower interval and complete generation of the old prefix are checked by the base/replay workflows; they are not independently regenerated by `check_windows.py`.

## 3. Why the extension generator is exhaustive

For a primitive corank-one extension of a lattice with Gram matrix `G`, an integral basis gives

$$
B=\begin{pmatrix}G&p\\p^{\mathsf T}&n\end{pmatrix},
\qquad d=\det G,\quad A=\operatorname{adj}(G),\quad
D=nd-p^{\mathsf T}Ap,
$$

where `p` is integral and `n` is even. Replacing `p` by `p+Gz`, with the corresponding change of `n`, is an integral change of the added basis vector. It is therefore sufficient to enumerate every class in `Z^r/G Z^r` and every allowed even diagonal. This is not a restriction to a special embedding.

For a class `a`, let `M_a/d` be its exact minimum in the dual lattice. If `s=D/d`, the minimum-norm condition for every nonzero layer is

$$
m^2D+M_{ma}\geq 6d
\quad\hbox{for every positive integer }m\hbox{ with }m^2D<6d.
$$

The zero class still needs its nonzero layers tested. Merely retaining an arbitrary representative of each class would be insufficient. The reviewed `fast_extend.py` instead enumerates a complete exact dual ball, enlarging its radius until all `d` classes are present, and takes the least norm found in each class. Every point outside that final ball is longer than every class minimum already found. It then tests all required layers and all even diagonal choices within the window.

The generator also checks that the supplied parent basis has the claimed shortest dual normal. Reduction to isometry representatives is safe only because every merge has a verified integral unimodular transport. The transport need not preserve the entire earlier marked flag: the next exhaustive extension stage concerns the abstract parent lattice, while the retained representative itself has a valid shortest-dual flag. These are distinct requirements, and the archived chain checks both.

## 4. Finite quadratic modules and the new HNF check

For even `G`, the quadratic residue

$$
Q(p)=p^{\mathsf T}Ap\pmod {2d}
$$

is well defined on `Z^r/G Z^r`. Indeed, the change under `p -> p+Gz` is

$$
2d\,p^{\mathsf T}z+d\,z^{\mathsf T}Gz\equiv0\pmod {2d}.
$$

An even extension of determinant `T` therefore requires `Q(p) == -T (mod 2d)`. The archived breadth-first module traversal uses the valid update `Q(p+e_j)=Q(p)+2(Ap)_j+A_jj (mod 2d)`. This audit uses a different representation of the quotient.

SymPy computes a column Hermite normal form `H` of `G`. The checker independently verifies that `G^-1 H` is integral and unimodular, that `H` is upper triangular with positive diagonal, and that its diagonal product is `d`. Then

$$
0\leq p_i<H_{ii}
$$

is an exhaustive, nonredundant set of representatives for `Z^r/G Z^r`: reduce the bottom coordinate using the last column, and continue upwards. There are exactly `d` tuples. The checker evaluates `p^T A p` afresh on every tuple whenever this module step is needed.

Before enumerating the module, it may use the divisibility obstruction

$$
\gcd(2d,A_{11},\ldots,A_{rr},2A_{12},\ldots,2A_{r-1,r})\mid T.
$$

If this fails, no determinant-compatible class exists.

### The shortest-normal obstruction

The bordered inverse formula shows that a lifted parent dual vector indexed by a nonzero integer `q` can have norm

$$
q^{\mathsf T}G^{-1}q+
\frac{(m-p^{\mathsf T}G^{-1}q)^2}{T/d}.
$$

The prescribed new normal has squared norm `d/T`. Minimizing over the integer `m` gives the necessary inequality

$$
T(q^{\mathsf T}Aq)+\operatorname{dist}(p^{\mathsf T}Aq,d\mathbb Z)^2\geq d^2.
$$

A single strict violation excludes the class. The checker reads the old report only to obtain proposed nonzero integral `q` coordinates. It recomputes each matrix, adjugate, norm, residue and strict inequality; old status labels, class counts and exclusion decisions are not accepted as evidence. Completeness of the proposed witness list is unnecessary: the checker visits every compatible class and fails if no valid witness covers it.

### Two lifting bounds, including continuation

For any explicit parent dual vector of squared norm `a`, there is a lift with squared norm at most `a+1/(4s)`. Requiring the new normal of norm `1/s` to be shortest implies `s >= 3/(4a)`. Taking `a=d_prev/d` gives

$$
3d^2\leq4d_{\rm prev}T.
$$

For any child of determinant `T`, the normal perpendicular to its parent is an explicit dual vector of norm `d/T`. A further shortest-dual extension of determinant at most `U` must therefore satisfy

$$
3T^2\leq4dU.
$$

This second inequality is universal for the continuation and can be checked before enumerating any child classes. It remains valid even if the displayed child normal is not shortest: the lifting argument only needs an available dual vector. This early continuation check explains why the new audit's categories differ from the archived category counts.

### Fresh numerical outcome

The input consists of 925 rank-five parents, 3,752 rank-six parents, 224 rank-seven parents, 47 rank-eight parents, and the four restored rank-seven records: 4,952 pairs in total.

| Independently evaluated exclusion | Pairs |
|---|---:|
| Parent lifting bound | 3960 |
| Next lifting bound | 956 |
| Quadratic-content divisibility | 11 |
| Exhaustive HNF nonrepresentation | 21 |
| Exhaustive HNF classes with verified shorter-dual witnesses | 4 |
| **Total** | **4952** |

The 25 HNF jobs enumerate 324,852 quotient representatives. Exactly 18 determinant-compatible classes occur, all in four rank-seven parents, and every one has a checked shorter-dual witness. The four restored branches have no compatible class at all.

“Excluded” here means that the pair cannot occur in a complete admissible shortest-dual flag reaching the required top determinant. It does **not** mean that every possible intermediate extension is nonexistent. In fact, the original extension replay finds 58 new rank-six and 20 new rank-seven raw matrices; they fail to continue. That distinction is essential.

The new boundary calculation supplies an alternative finite-module implementation, not an independent regeneration of the full prefix. Parent-list completeness, the treatment of the old determinant ranges, and the classification of the `sqrt(3) E8` subclass remain separate dependencies.

## 5. What replay does and does not establish

The static strict-search verifier checks determinant bounds, Gram matrices, shortest dual minima, exact prune inequalities, parent linkage, manifests and unimodular transports. Some completeness assertions about generated lists are represented in the static path by saved logs/statistics. A static `PASS` alone must not be described as fresh exhaustive generation.

Inspection of the optional replay functions confirms that they call `extend_parent` again for each scheduled parent, then compare newly produced matrices or digests against the archived expected output. They do not use the saved child list as the returned generation result. In-memory caching of exact matrix calculations is harmless memoization, not reuse of archived child enumeration results.

Replaying the audited original generator is stronger than checking its old logs, but it still shares the original generation algorithm. The new HNF calculation reduces shared implementation for the equality boundary. Neither activity is independent external refereeing, nor does it formalize the mathematics in a proof assistant. Record replay status separately from static-check status and from external review.

## 6. Cluster bounds: verified arithmetic and precise scope

The manuscript's cluster comparison uses the radius guaranteed by the ambient minimum, namely `sqrt(6-beta)/2`. The comparison does not imply an upper bound for every actual packing radius available from additional ambient geometry.

For rank-nine sections containing `sqrt(3) E8`, projection to `E8*/sqrt(3)` has nonzero squared distances in multiples of `2/3`, and fibers are one-dimensional. The fiber-spacing and diameter inequalities in the manuscript have the correct direction. The few-distance bound in dimension eight follows from evaluation polynomials: if there are at most `r` positive distances, then `|P| <= binomial(9+r,r)`. The polynomial space used in this argument is an upper bound on dimension; no equality of those spaces is required. The equidistant special case has at most nine points.

The critical points of the one-dimensional fiber estimates occur at the stated values `3/20` and `4/5`. The checker compares the squares of all eight interval bounds against the common upper bound

$$
81(8/9)^{39}<1.
$$

For the two rank-ten determinant minimizers, the fiber is the triangular lattice `A2/sqrt(5)`. The checker independently performs exact maximum-clique enumeration in the translated triangular-lattice balls for `u^2-uv+v^2 <= 1,3,4`. The balls have 7, 13 and 19 points and the maximum anticode sizes are 3, 4 and 7. The coordinate box `[-3,3]^2` is exhaustive for these radii because `u^2-uv+v^2 >= 3u^2/4` and likewise for `v`.

All 36 pairs of minimal triangular directions independently give the required midpoint lower bound `3/10`. The thresholds `23/30`, `29/30` and `49/30` are consistent with the stated horizontal and vertical constraints. Every rank-ten interval endpoint comparison was evaluated as an exact rational number and is bounded by

$$
9(8/9)^{19}<1.
$$

For the final diameter interval, injection into the discriminant group is valid because distinct points whose difference belongs to the section lattice would have squared distance at least 6, whereas the cluster diameter is strictly below 6.

These checks support the stated cluster theorem for rank-nine sections containing `sqrt(3) E8`, and for the rank-ten determinant minimizers, using the guaranteed radius. They do not settle clusters over arbitrary other sections, or packings whose actual radius exceeds that guaranteed value. The machine checker verifies endpoint arithmetic and the small finite fiber problems; the geometric reductions themselves were reviewed mathematically rather than formalized.

## 7. Embeddings: nineteen sublattices are not nineteen orbits

The count of 19 concerns the specific marked rank-nine section in the printed ambient `P_48p` lattice. It does not quantify over every possible embedding of that rank-nine lattice into every rank-48 ambient lattice.

The 561 oriented glue classes are paired by the involution `b -> a-b`. Its unique fixed class is `b=-a`, so there are `(561+1)/2 = 281` unoriented targets. The claimed 19 solutions and 262 empty targets depend on complete enumeration of the indicated affine closest-vector fibers, not solely on the finite class count. That full replay is handled by the separate verification workflow, not by `check_windows.py`.

Smith normal form establishes saturation of the displayed embeddings. Pairwise distinct ambient normals up to sign distinguish actual primitive sublattices. This does **not** classify them into automorphism orbits of the ambient lattice. The results must remain worded as “19 distinct primitive rank-ten sublattices containing the fixed marked section”, unless an additional orbit computation is supplied.

No new exhaustive proof that the whole rank-48 ambient lattice has minimum 6 is supplied here. The embedding statements use the printed ambient data and the stated minimum hypothesis; intrinsic minimum checks of the resulting sections are separate computations.

## 8. Remaining verification obligations

No new mathematical contradiction was identified in this scoped audit. The following boundaries should remain prominent in any release:

1. The external Hermite input and the complete strict-search prefix remain dependencies of the global theorem; example matrices cannot certify the lower bound.
2. Static certificate validation, fresh generation with the original algorithm, and the new HNF boundary checker are distinct forms of evidence. Report exactly which were run.
3. The new HNF checker trusts the archived parent lists as inputs and uses archived shorter-dual coordinates only as candidates whose validity is recomputed. It does not trust old exclusion outcomes.
4. The `sqrt(3) E8` classification, rank-nine equality-orbit proof, and affine rank-48 enumeration require their own checks; they are not consequences of the new window checker alone.
5. Cluster optimality for arbitrary other sections, the distinction between guaranteed and actual radii, and classification modulo ambient automorphisms remain outside the proved scope described here.
6. External human review and a primary-literature novelty assessment are still separate from an internal AI-assisted audit.

Run the new check from the repository root with:

```sh
python verification/2026-10-29/check_windows.py
```

It requires SymPy. It imports none of the archived generator/verifier modules and writes only its own report. A failure raises an exception; critical checks are not disabled by Python's `-O` option.

## 9. Additional completed replay of the historical rank-nine base

Inspection found a precise limitation in the top-level runner: even with every optional flag, `verify_new_results.py --full-equality` regenerates the **additional rank-nine equality searches**, not the earlier September strict-search certificate on which that historical proof route relies. The current global rank-ten proof has a different, complete flag prefix and does not depend on this older rank-nine theorem. Its `--full-global` option schedules fresh generation from the rank-one seed through all current rank-nine intervals, including the low ranks. The remaining reuse there consists of choices of isometry representatives with rechecked covering maps, not omission of fresh parent-to-child generation.

To check the historical route as well, this audit ran three additional runners in separate disposable copies of `certificates/research_20261007/recovered/rank9_audit_evidence_20260910`. All passed. The 123 preserved source files were hashed before and after and remained unchanged; the disposable copies also contained no changed deterministic source/report files after execution.

| Freshly executed historical runner | Result | Wall time |
|---|---|---:|
| `run_full_regeneration.sh` | Byte-identical regenerated lists | 243.979 s |
| `run_all_checks.sh` | All mandatory certificates passed | 273.067 s |
| `run_audit_checks.sh` | All five supplementary audits passed | 55.931 s |

At most two single-process runners ran concurrently. Total elapsed time was 299.995 seconds, so the individual times are not isolated-machine benchmarks. Actual UTC times, process exit codes, log hashes and source integrity are recorded in `../results/legacy_rank9_replay/summary.json` and its accompanying logs. The reusable launcher is `../run_legacy_rank9.py`; future runs default to a fresh UTC-stamped directory and refuse a nonempty explicit output directory. The retained run used the earlier default `results/legacy_rank9_replay`.

The historical strict-search windows are ranks two through eight:

| Rank | Historical determinant window | Fresh lower-chain raw forms | Isometry representatives |
|---:|---:|---:|---:|
| 2 | 27--39 | 7 | 5 |
| 3 | 108--178 | 52 | 14 |
| 4 | 324--633 | 279 | 47 |
| 5 | 972--1894 | 1456 | 118 |
| 6 | 2187--4647 | 1905 | 138 |
| 7 | 4374--9492 | 2235 | Six continuing classes |
| 8 | 6564--15908 | Separate branch classifications | Not a single combined list |

Thus the replay regenerated all 3,699 lower-chain raw forms in ranks two through six and all 2,235 rank-seven forms from all 138 rank-six parents. Every principal regenerated list and rank-seven chunk matched the archived output byte for byte. The mandatory runner checked the bridges between regenerated and frozen representatives, all covering maps, all 96 surviving rank-seven linkage maps, and the six residual branches: `sqrt(3) E7`, determinant 6318, determinant 7722, determinant 8192, determinant 7986 and determinant 8100. It also independently recalculated the discriminant-class radius of `sqrt(3) E8`.

These are precisely the historical inputs previously read by the equality addendum: `rank5_isometry_classes.json` with 118 parents, `rank6_isometry_classes.json` with 138 parents, `rank7_merged.json` with 2,235 raw children, `rank7_survivor_linkage_exact.json`, and the rank-eight branch classifications. Their fresh base replay is now separate from, and complementary to, replay of the additional equality endpoints 4648, 9494 and 15909.

### Previously known omitted zero-class layer

The September package transparently preserves a real generic defect in the old `verify_rank7_topdown.py::allowed_one_vector_extensions` helper. It was used in the historical certificate, so it should not be described as an unused exploratory routine. For a glue class of order `h`, the old helper tested centered nonzero residues `m=1,...,floor(h/2)` but omitted the first nonzero layer with zero discriminant class, `m=h`. That layer requires

$$
h^2s\geq6.
$$

The fresh regression reproduced the counterexample with parent Gram matrix `diag(22,6,6,6,6)`, cross vector `(11,0,0,0,0)`, last diagonal 6, glue order 2 and `s=1/2`. The bordered determinant is 14256. The old helper accepts this candidate, but the vector `(1,0,0,0,0,-2)` has squared norm 2. The hardened helper rejects it. This is a genuine generic omission, previously identified in the archived September audit, not a newly discovered failure of the determinant theorem.

For the actual top-down proof branches, the omission is harmless for an explicit mathematical reason: the relevant exact class radii are at most `93/22`, so `s >= 6-93/22 = 39/22 > 3/2`. If `h >= 2`, this forces `h^2 s > 6`. If `h=1`, the class minimum is zero and the even last diagonal is at least 6, hence `s >= 6`. The new audit copy `verify_rank7_topdown_hardened.py` nonetheless restores the missing condition explicitly with `if h*h*s < 6: continue`, making the helper correct outside those particular branches as well.

Both the regression and the complete hardened actual-branch computation were freshly executed. The resulting hardened transcript is byte-identical to both archived original and archived hardened branch transcripts. This comparison and the regression markers are recorded in `../results/legacy_rank9_replay/hardened_branch_comparison.json`. The current global generator `fast_extend.py` already checks **every** positive layer satisfying `m^2 D < 6d`, including layers with zero discriminant class, and does not contain this omission.

The optional larger, redundant `sqrt(3) E6` cross-check is not part of these mandatory runners and was not rerun. Its necessary consequences are covered by the targeted E7 and determinant-6318 branch programs. Historical exploratory computations and the external perfect-form classification are likewise not represented as newly regenerated computations.
