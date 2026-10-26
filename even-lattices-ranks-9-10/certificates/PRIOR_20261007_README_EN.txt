CONFIDENTIAL RESEARCH ADDENDUM — 7 OCTOBER 2026

This package contains new exact computations and proofs. It is an internal
research result, not an external referee report, and it does not claim that
all original open problems have been solved.

ESTABLISHED IN THIS ADDENDUM

1. The rank-nine minimizer of Gram determinant at squared minimum at least
   six is unique up to integral isometry: K9, determinant21870. One proof
   retains the original exhaustive lower-bound package as a dependency.
   New equality endpoints4648,9494,15909 were excluded by exhaustive
   generation and also by a separately implemented finite-module method.
   An alternative proof using the public gamma9<=2 theorem and the new
   completed global search is independent of that old lower-bound package.

2. Importing the public theorem gamma9=2 from Dutour Sikiric–van Woerden,
   arXiv:2508.20719v2, the rank-nine determinant spectrum below32076 is
   exactly21870,26244,30618, one integral isometry class for each value.
   Thus the exact next determinant after K9 is26244. The minimum determinant
   among rank-nine lattices containing no sqrt(3)E8 is32076, with an explicit
   minimum-six witness. No uniqueness at32076 is asserted. The earlier gap
   through24450 is preserved as an intermediate result, not the final gap.

3. Every even integral rank-ten lattice of minimum at least six containing
   sqrt(3)E8 has determinant at least54675. There are exactly two isometry
   types attaining equality. Their Gram ranks modulo3 are4 and3.
   This is a complete result for that subclass, not for arbitrary rank ten.

4. The completed global flag search proves e10(6)=54675. This imports the
   public gamma9<=2 theorem, classical Hermite inputs through rank8, and
   the independently proved E8-containing rank-ten lower bound. The new
   search does NOT depend on the old rank-nine lower bound or gap proof:
   all even rank-nine parent determinants19684..40054 are covered directly.
   The low band is empty; all3819 candidates in the high band are excluded
   by the final exact lifting inequality. A separate implementation checked
   all windows, coverage maps, pruning inequalities and relevant dual minima.
   The earlier interval31595..54675 is retained only as historical progress.

5. No nontrivial finite antipode cluster over ANY rank-nine section
   containing sqrt(3)E8, of any determinant, improves the bare K9 center
   density at the guaranteed radius sqrt(6-beta)/2. Both rank-ten equality
   types likewise have no nontrivial cluster improvement at that radius.
   Every beta<6 is covered; no point-count or clique-search cap is used.
   Additional rank-ten bounds cover every determinant for clusters with
   one projected point, and for beta<4/3 when every projection fiber is
   collinear. These are partial extensions, not the full all-determinant
   rank-ten cluster theorem.

6. The printed ambient matrices and embeddings have been independently
   checked for their exact linear-algebra claims, including primitivity,
   complement determinants, and discriminant anti-isometries. The ambient
   minimum-six theorem and complete automorphism-orbit classifications
   remain separate. There are exactly19 distinct primitive determinant54675
   rank-ten supersections containing the particular printed K9 in P48p.
   All are isometric to the original K10; the alternative type is absent
   over this fixed K9. Every one of281 class pairs was exhaustively checked
   in two integer implementations, with171472428 nodes and19 leaves.
   This counts actual sublattices, not ambient automorphism-group orbits.
   This local theorem does not depend on the global rank-nine lower bound.

7. K9 is a previously known perfect form type Q129. Its perfectness is
   certified by a nonzero45-by-45 minor of minimal-vector outer products.
   Potential novelty lies in integral optimality and classifications, not
   in inventing a previously unknown K9. No definitive priority claim is made.

REMAINING OPEN

The global classification of rank-ten equality cases outside the
E8-containing subclass; complete primitive-embedding orbits in specified
rank48 lattices; clusters over sections outside the proved
families, including the rank5 problem in dimension43; external scientific
review and definitive novelty assessment. Larger actual packing radii in
particular ambients are outside the guaranteed-radius cluster statements.

REPRODUCTION

Use ordinary CPython3.12 or later with assertions ENABLED. Do not use -O
or -OO. Final proof verifiers require only the Python standard library.
Run from this directory:

  python verify_new_results.py

This reruns the new independent checks and the exact small certificates.
For the additional same-code complete regeneration of the new rank9
boundary analysis, use:

  python verify_new_results.py --full-equality

For the exhaustive replay of all 281 ambient fibers in the classification
of optimal extensions of the fixed printed K9, add:

  python verify_new_results.py --full-local-extensions

Both options may be combined. The full ambient replay takes several minutes.

To regenerate every one of the1897 parent lists in the global rank-ten
proof (115627 raw candidates), add:

  python verify_new_results.py --full-global --workers 7

Use fewer workers on a smaller machine. The full regeneration was actually
completed and matched every saved list. The default command independently
checks the complete saved chain without regenerating all extension lists.

The original lower-bound package and its own reproduction instructions are
retained under research_20261007/recovered/. It is a prerequisite of the
older classical-input route, not the new gamma9-based global proof.
A hash comparison alone is not a proof of exhaustive search.

The global rank-ten early_flags directory contains the completed strict
counterexample search. No rank-ten extensions need to be generated: every
remaining rank-nine flag is excluded by the necessary lifting bound.
Some intermediate logs retain their historical prefix/pending labels;
the final global proof and independent chain verification give the status.
Do not extend the strict search to a global equality classification:
the equality endpoint changes several determinant windows.

SHA256SUMS records file identity. Read the mathematical proof and coverage
arguments as well as the finite verification outputs.
