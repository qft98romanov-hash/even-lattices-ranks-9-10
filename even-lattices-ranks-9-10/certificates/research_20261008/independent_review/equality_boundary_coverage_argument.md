# Internal audit of the passage from the strict rank-ten bound to equality

Confidential research continuation, 8 October 2026. **Status: PASS.** This note
states the coverage argument for the completed global equality proof. All
additional boundary computations have finished. The independent finite-module
proof and full exact results are recorded in `equality_independent_proof.md`;
all 4952 parent-target pairs are excluded.

Let L be an even integral positive definite lattice of rank 10, squared
minimum at least 6, and Gram determinant 54675. Assume the external Hermite
bound gamma_9 <= 2. If L contains sqrt(3)E8, the already checked gluing theorem
classifies it as one of two inequivalent lattices. To prove that these are all
global equality cases, it suffices to exclude L containing no such E8 copy.

Choose successive primitive kernels of shortest dual vectors. Writing d_r
for their Gram determinants, d_(r-1) = d_r min(L_r*) and hence

    d_(r-1) <= gamma_r d_r^((r-1)/r).

The classical Hermite constants through rank 8, gamma_9 <= 2 and Mordell's
inequality gamma_10 <= 2^(9/8) give, with exact congruence-aware rounding,

    rank:   1  2    3    4     5     6      7      8      9      10
    upper:  6  44 210  789  2492  6460  13940  24676  40056  54675.

The lower endpoints remain the same as for the strict search. In particular,
rank 8 starts at 6564 because determinant 6561 would force sqrt(3)E8. Rank 9
starts at 19684 using only gamma_9 <= 2 and odd-rank determinant parity.

Compared with the strict search at rank-ten upper bound 54672, the only new
admissible determinant endpoints are 6460, 13940, 24676, and 40056 in ranks
6, 7, 8, and 9 respectively. Ranks 1--5 are completely unchanged.

## Why the old final obstruction is not by itself enough

A lifting exclusion for a rank-r flag parent J reads

    3 d_r^2 > 4 d_(r-1) U_(r+1).

Increasing U_(r+1) can invalidate a previously correct exclusion even when
d_r is within its old window. Therefore a proof that merely searches the
four new determinant endpoints from the old surviving parent lists would
be incomplete. Every old lifting prune must be reevaluated at the new upper
bound; all recovered parents require continuations.

The independent exact scan of every saved old lifting record finds:

* all old prunes of whole parent searches remain valid;
* all old raw rank-eight and rank-nine continuation prunes remain valid;
* exactly four old raw rank-seven continuation prunes become eligible.

Those four matrices occur in old rank7 parent file 3297, child indices
606--609. Each has d_6=4131 and d_7=11658. Its lifting bound on a further
rank-eight determinant is

    d_8 >= 3*11658^2/(4*4131) = 3775249/153.

This number is strictly between 24673 and 24676. Rank-eight determinant
congruence then forces d_8=24676 inside the enlarged window. Thus a search
at precisely that endpoint suffices for each of these four restored forms.
It is harmless to retain duplicate isometry types here.

The actual files and their hashes, the complete scanned record counts,
and all exact comparisons are in equality_windows_and_recovered_prunes.json.
Its companion checker independently recomputes the windows using rational
integer powers and scans all old saved prune records.

## Complete delta search by induction

Every new or restored possible parent must be handled by one of the
following disjoint sources, although duplicates across isometric forms do
not hurt completeness.

1. Rank 6: all old rank-five representatives at determinant 6460. Lower
   determinants are already covered by the old raw lists and isometries.
2. Rank 7: every old rank-six representative at determinant 13940; every
   newly admitted rank-six parent over the full enlarged rank-seven window;
   and every old raw rank-seven form recovered by the enlarged next-rank
   lifting bound. The four recovered forms listed above must be included.
3. Rank 8: every old rank-seven representative at determinant 24676; every
   newly admitted or recovered rank-seven parent over its required window;
   and any recovered old raw rank-eight forms (the independent scan finds
   none). For the four known recovered rank-seven forms the required window
   is the singleton 24676 by the preceding inequality.
4. Rank 9: every old rank-eight representative at determinant 40056; every
   newly admitted rank-eight parent over the full enlarged rank-nine window;
   and any recovered old raw rank-nine forms (the independent scan finds
   none). The existing low-band search [19684,24450] remains part of the old
   full coverage and cannot be discarded without a separate reason.
5. Rank 10: all old and new rank-nine records are tested against the new
   upper determinant 54675. Any record satisfying the necessary lifting
   inequality must be extended further or otherwise rigorously excluded.

An exact isometry to an old surviving representative permits reusing its
covered old interval; only its new endpoint requires a new search. The map
must be unimodular and checked by integer Gram multiplication. A numerical
signature match is insufficient. No new isometry classification is needed
if every new branch is simply retained and exhausted.

At any step, a parent's old flag basis has certified normal dual minimum
min(J*)=d_(r-1)/d_r. The extension generator rechecks this exact identity.
The old and new finite extension algorithm permits every even last diagonal
in the determinant interval, enumerates all discriminant classes, tests all
nonzero layers m with m^2 D < 6d, and checks that the new normal is shortest.
Thus it does not assume the original rank-ten lattice has a basis of minimal
vectors, nor that its chosen shortest-dual flag contains an optimal rank-nine
lattice. These are crucial completeness points.

## Conclusion of the completed exclusion

Every new boundary continuation is now excluded, and all old terminal
lifting inequalities remain strict at 54675. Therefore every determinant-54675
lattice under consideration contains sqrt(3)E8. The separate E8 gluing theorem
gives exactly two
abstract integral isometry classes. Their Gram ranks over F_3 are 4 and 3,
so they cannot become isometric after forgetting the chosen E8 embeddings.

This equality result does not classify embeddings into any fixed ambient
rank-48 lattice, establish universal sphere-packing optimality in dimension
38, replace the external gamma_9 theorem, or provide outside human review.
