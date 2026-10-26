CONFIDENTIAL RESEARCH CERTIFICATES — 8 OCTOBER 2026

Start with lattices_complete_EN.pdf or lattices_complete_RU.pdf. The matching
.txt files are complete LaTeX sources, byte-identical to the .tex files.
Select XeLaTeX in Overleaf. No bibliography download or external data service
is needed to compile these standalone reports.

This is an internal research package. Independent implementations inside this
project are not external refereeing or formal proof-assistant certification.
All minima below are squared norms; all determinants are Gram determinants.

FINAL MATHEMATICAL RESULTS

1. Among positive-definite even integral rank-nine lattices of minimum at
   least 6, the smallest determinant is 21870, with one integral isometry
   class K9. Below 32076, the determinant spectrum is exactly 21870, 26244,
   30618, one class at each value. The least determinant for a rank-nine
   lattice containing no sqrt(3)E8 is 32076; no uniqueness at 32076 is claimed.

2. For positive-definite even integral rank-ten lattices of minimum at least
   6, e10(6)=54675. The global equality classification is now complete:
   EVERY lattice with determinant 54675 contains sqrt(3)E8, and exactly TWO
   integral isometry classes occur. Their Gram ranks modulo 3 are 4 and 3.
   Thus the earlier restriction to the E8-containing subclass has been
   removed. The strict lower-bound search alone did not establish equality;
   the separate 8 October endpoint proof supplies the missing coverage.

3. Each of these two rank-ten lattices has exactly one sqrt(3)E8 sublattice.
   Its dual has exactly six minimal vectors, of squared norm 2/5, generating
   A2/sqrt(5). Their three sign pairs give exactly three primitive rank-nine
   sublattices of determinant 21870, all isometric to K9.

4. At the guaranteed antipode radius sqrt(6-beta)/2, every nontrivial finite
   cluster over ANY determinant-minimal rank-ten section has density ratio
   at most 9*(8/9)^19 = 0.9601621523027026... relative to its singleton
   construction. The guaranteed density loss is at least 3.9837847697297...%.
   This is a proved upper bound, not a sharpness assertion. Every beta<6
   and every finite cluster size is covered. The rank-nine cluster theorem
   covers ALL determinants in the sqrt(3)E8-containing family. Additional
   partial rank-ten results cover one projected point at every determinant,
   and collinear projection fibers for beta<4/3.

5. In a rank-48 even unimodular ambient lattice of minimum at least 6, a
   primitive rank-ten section K gives singleton center density
       (3/2)^19 / sqrt(det K) <= (3/2)^19 / sqrt(54675)
   in dimension 38 at radius sqrt(6)/2. Equality has precisely the two
   abstract section types above, subject to their existence in that ambient.
   This does not assert optimality among arbitrary sphere packings.

6. All printed ambient linear-algebra data were checked exactly, including
   primitivity, complement determinants and discriminant anti-isometries.
   Over the particular printed K9 inside P48p there are exactly 19 distinct
   primitive rank-ten supersections of determinant 54675. All have the
   original rank-ten type; the alternative type is absent over that K9.
   This is a count of actual sublattices, not ambient automorphism orbits.

7. K9 is the previously known perfect form type Q129. The package contains
   an exact perfectness certificate. No new-lattice or definitive priority
   claim is made.

INPUTS AND COVERAGE

The global rank-ten minimum, equality classification and the strengthened
rank-nine spectrum use the public theorem gamma9<=2 of Dutour Sikiric and
van Woerden, arXiv:2508.20719v2, together with classical Hermite constants
through rank 8. The new global proof does not depend on the older rank-nine
lower-bound certificate. That older proof is retained as a separate route.

The 7 October strict search covered 1897 parent lists and 115627 raw
matrices. Its actual full regeneration is retained. The equality proof
recomputes the enlarged windows
       6, 44, 210, 789, 2492, 6460, 13940, 24676, 40056, 54675.
Every previously pruned branch is rechecked. Four old rank-seven flags
reappear. An independent finite quadratic-module calculation covers all
4952 necessary parent/endpoint pairs and excludes every possible full flag
without sqrt(3)E8. It imports neither original extension implementation.
Separate exact extension generation and the saved-delta checker corroborate
the same conclusion. Read the proof and coverage arguments, not just PASS
markers or hash lists.

WHAT REMAINS OPEN

Complete primitive-embedding classifications under automorphism groups of
specified rank-48 lattices; general cluster optimization over higher-
determinant or other sections (including the dimension-43 rank-five problem);
possible larger actual radii in particular ambient lattices; external
scientific review and definitive novelty assessment. The global rank-ten
equality classification is no longer on this list.

REPRODUCTION

Verified using CPython 3.12 on Linux. The mathematical verifiers use only
the Python standard library. Keep assertions ENABLED: never use -O or -OO.
Run commands from the extracted package directory.

On a fresh extraction, check file identity first:
  python verify_file_hashes.py

Run the assembled exact checks:
  python verify_new_results.py

The default includes the old independent saved-chain audit, the new equality
delta audit, enlarged-window/prune audit, independent finite-module proof,
and independent intrinsic-structure/cluster audit. Some verifiers rewrite
their status JSON files and logs; hash differences after rerunning are
therefore expected. Hash identity does not prove mathematical correctness.

Optional complete regenerations:
  python verify_new_results.py --full-global --workers 7
  python verify_new_results.py --replay-rank10-equality --workers 7
  python verify_new_results.py --full-local-extensions
  python verify_new_results.py --full-equality

Flags may be combined. --full-global regenerates the 1897 strict-search
parent lists. --replay-rank10-equality regenerates every new endpoint job
directly and bypasses generator caches. --full-local-extensions replays all
281 ambient fibers. The historical --full-equality flag means the OLDER
rank-NINE boundary certificate, not the new rank-ten classification.
Parallel full replays use fork and require a compatible system such as
Linux, macOS or Linux under WSL; use fewer workers on smaller machines.

LAYOUT

research_20261007/  Prior audited computations, proofs and full-replay records.
research_20261008/rank10_equality/  New equality data, proof, and exact verifier.
research_20261008/independent_review/  Independently implemented equality proof.
research_20261008/consequences/  Intrinsic structure and quantitative cluster bound.
research_20261008/report_build/  Report build/QA records; disposable renders omitted.
local_replay_logs/  Actual checks from the assembled package.
prior_reports/ and PRIOR_20261007_*  Historical reports and status, superseded above.
source_main4.pdf  Original supplied manuscript.

Historical files retain their original wording, including once-open questions.
The current reports and this README provide the final scope. SHA256SUMS covers
every delivered file except itself. Preserve the entire directory structure.
