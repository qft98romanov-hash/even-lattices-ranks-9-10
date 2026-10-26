# Independent audit of the residual rank-seven branches

Date: 10 September 2026. Scope: branch logic, discriminant-class minima,
one-vector extension enumeration, exact arithmetic, opposite classes,
constants and the extremal rank-nine example. The original archive was read
without modifying its data. The full release replay and the global Hermite /
flag-window proof are audited separately.

## Verdict

No fatal gap was found in the branch closure argument. The finite class
tables are genuinely exhaustive, not sampled, and the exact interval
enumerators are mathematically sound. The branch implications do establish
that every continuation represented by the six surviving rank-seven classes
has determinant at least 21870. The example K9 independently has determinant
21870 and minimum 6.

There is one necessary notation correction and two small implementation /
exposition qualifications described below. None changes any determinant,
radius, class count, or branch conclusion.

## 1. Exact enumeration and completeness of class minima

For G integral and positive definite, a dual vector with integer pairing
column z has coordinate vector G^{-1}z, norm z^T G^{-1}z, and discriminant
fingerprint G^{-1}z modulo Z^n. Multiplying by det(G) gives the equivalent
integer fingerprint adj(G)z modulo det(G). Its image has exactly det(G)
elements, because it is naturally isomorphic to G^{-1}Z^n/Z^n.

Every radius routine enumerates the complete dual ellipsoid through B,
stores the smallest norm for each fingerprint, and asserts that exactly
det(G) fingerprints occurred. Every stored minimum is then exact: a missing
shorter vector would also have norm at most B and hence would have been
enumerated. Merely counting classes would not suffice without ellipsoid
completeness; both ingredients are present here.

The LDL identity is Q=L diag(D)L^T and

    x^T Q x = sum_i D_i (x_i + sum_{j>i} L_{ji} x_j)^2.

The backward recursive enumerators use precisely this identity. For a
rational center a/b and radius squared p/q, the permitted integer coordinate
z satisfies (bz-a)^2 <= b^2 p/q. Since bz-a is an integer, replacing the
right side by its floor before isqrt is exact, including boundary equality.
The older E7 variant uses a superset obtained with a ceiling and then tests
the exact quadratic inequality, which is also complete. The shifted-center
helper in rank9_exact_ldl.py has the correct sign and tail correction.

Independent checks in branch_independent_checks.py compare the enumerators
against complete Cartesian-product search with coordinate bounds derived
from Q^{-1}. All 51 tests passed, including fractional forms, nonzero rational
centers, an anisotropic sheared form, and exact-boundary cases.

## 2. One-vector extensions and layer tests

Write K=L+Zv where v=u+w, u lies in L tensor R, w is orthogonal to L,
u belongs to L*, c=u+L, and s=(w,w)>0. Then

    det(K)=det(L)s,
    min norm in the nonzero m-th layer = m^2 s + mu_L(mc).

Replacing v by v+l reduces u to a shortest representative of c and changes
the last Gram diagonal by an even integer. Thus enumerating all c and all
even last diagonals in the determinant window is exhaustive up to a
unimodular change of basis fixing L. No shortest representative multiplicity
needs to be retained: representatives in the same class differ by L.

The E7 and E6/H6318 enumerators test every m=1,...,ord(c). Once the zero-class
layer m=ord(c) satisfies ord(c)^2 s>=6, all higher positive m are automatic.
The general extend_flag.py instead tests all m with m^2 s<6. Both procedures
are complete and retain equality at norm 6. Their t or diagonal loops exceed
the bounds implied by the determinant windows; no larger diagonal is lost.

The radius bound is

    det(K) >= det(L) [6 - rho_glue(L)^2],
    rho_glue(L)^2 = max_{c in L*/L} mu_L(c).

This is a finite discriminant radius, not the continuous covering radius of
L in its ambient Euclidean space. The distinction must remain explicit.

## 3. The six residual branches

| (d6,d7) | Required finite result | Consequence |
|---|---|---|
| (2187,4374) | sqrt(3)E7 has 1375 labelled rank-eight extensions; four classes | Floors 32076,21870,21870,42282 |
| (2187,6318) | H6318 has 12 unrestricted labelled extensions, 2 of det12393 and 10 of det13689 | Floors 32076 and36504 |
| (2835,7722) | Only two unrestricted classes, opposite, both det13689 | No flag-compatible continuation |
| (4096,8192) | Glue radius squared7/2 | d8>=20480>15908 |
| (3240,8100) | Glue radius squared15/4 | d8>=18225>15908 |
| (3267,7986) | Glue radius squared25/6; two opposite flag-compatible det14641 presentations | One rank-eight class, radius squared36/11, d9>=39930 |

The two det15309 lattices in the E7 branch have different exact kissing
numbers (138 and126), so the count of four abstract isometry types is
justified, not only the count of orbit types. The pairing-coordinate root
reflections used for E6 and E7 are integer unimodular isometries of G^{-1};
all 13 generating matrices were checked independently using rational matrix
multiplication. It is not necessary that they generate the entire
automorphism group: their orbits suffice for a covering by isometry types.

The top-down det7722 certificate explicitly verifies that its two classes
sum to zero and constructs an integer matrix T with det(T)=-1 and
T^T J_plus T=J_minus. It then verifies the isometry to J13689. This closes the
previously noted logical weakness of merely reporting opposite classes.

The critical flag qualification is

    d8 >= 3*7722^2/(4*2835) = 552123/35 > 13689.

Thus neither unrestricted J13689 extension belongs to the chosen
shortest-dual flag. The redundant radius floor36504 is valid as well, but
these extensions must never be called flag-compatible. Similarly the
H6318 children of determinant12393 fail the flag bound d8>=13689.
The det7986 children of determinant14641 do pass the shortest-normal check.

All six groups have distinct d7, so no hidden identification is needed to
claim six classes. The survivor-linkage report gives an explicit GL7(Z)
map for each of the 96 raw survivors to its associated branch target.
Passing to an abstract isometry class does not lose relevant extensions:
every one-vector extension transfers along the isometry. The old embedded
rank-six parent need not be preserved for these subsequent branch bounds.

## 4. E8 equality and K9 sharpness

For L=sqrt(3)E8, unimodularity identifies L*/L with E8/3E8. The exact E8
shell enumeration through norm8 covers all3^8=6561 residues. Its minimum
distribution is 1,240,2160,2240,1920 at norms0,2,4,6,8. Consequently
rho_glue(L)^2=8/3 and every min6 continuation has determinant at least21870.
This equality branch is handled separately from the d8>=6564 window.

The K9 determinant was independently evaluated by the full Leibniz formula,
rather than the archive's Bareiss algorithm, and equals21870. All principal
leading minors are positive. A second exact enumerator agrees with the
general enumerator through norm6: exactly258 nonzero vectors occur, all of
norm6. Thus positive definiteness, minimum6 and sharpness are established.
No uniqueness of K9 follows from these checks.

## 5. Corrections and qualifications for the new manuscript

1. **Scaling notation:** the Gram matrix 4 C_E7^{-1} represents **2 E7***
   under the ordinary Euclidean scaling convention. Calling this lattice
   "4 E7*" is incorrect unless a nonstandard Gram-scaling convention is
   explicitly declared. Use H8192, with Gram(H8192)=4 C_E7^{-1}, and optionally
   H8192 congruent to2 E7*. The numerical certificates are unaffected.

2. **Generic top-down layer helper:** allowed_one_vector_extensions in
   verify_rank7_topdown.py tests only m=1,...,floor(h/2). It does not explicitly
   test the nonzero zero-class layer m=h. As a generic routine this is
   incomplete. In this concrete application it is harmless: every candidate
   with h>=2 passes the m=1 test, so s>=6-rho^2, and all four parent radii are
   at most93/22<9/2; hence h^2 s>=4(6-93/22)>6. For h=1, mu=0 and the diagonal
   loop starts at6, so s>=6. The manuscript should include this explanation,
   or a future derivative should change the loop to all m with m^2s<6.

3. **Existence-only shell tests:** minimum_vectors(G,6) checks existence of
   norm6 vectors, not absence of norm2 or4. Some supplemental E6/H6318 code
   uses it in assertions that should not be described alone as a minimum
   certificate. The full theorem already has min6 from the survivor linkage
   and the layer criterion. In addition, this audit directly enumerated
   all vectors through norm5 for H6318,J12393,J13689,J14580,J15309a,J15309b;
   there are no nonzero vectors. No conclusion is lost.

## Reproducible auxiliary audit

Files: branch_independent_checks.py, branch_independent_checks.transcript.
Run with ordinary Python3; no third-party dependencies. Final line:

    ALL_INDEPENDENT_BRANCH_CHECKS_PASS

The random tests are regression checks, not substitutes for the mathematical
completeness proof above. Full verification of the global optimum additionally
requires the separately audited determinant windows, complete lower flag
enumeration and raw-to-class linkage; this report does not claim to replace
those steps.

## Isolated implementation correction and fresh replay

The requested corrected code is provided outside the unchanged original
archive as verify_rank7_topdown_hardened.py, with a focused unified diff in
verify_rank7_topdown_hardened.patch. The sole logic change adds the missing
test h^2*s>=6 before the centered nonzero class-layer test. A full fresh
execution completed with `ALL EXACT CHECKS PASSED`; its transcript is
**byte-for-byte identical** to the archived topdown transcript (`cmp` exit0).
Thus the correction changes no application result. File hashes are recorded
in topdown_hardening_sha256.txt.

The issue is a real generic-helper defect, not merely speculative. The exact
regression topdown_zero_layer_regression.py constructs the diagonal parent
G=diag(22,6,6,6,6), determinant28512, with its complete analytically computed
28512-element discriminant-minimum table. The class c=(1/2,0,0,0,0) has
order2 and minimum11/2. Set last diagonal6 and s=1/2. The resulting extension
has determinant14256 and its first layer has minimum6; the archived helper
accepts it. However the vector (1,0,0,0,0,-2) has norm2 in this extension,
because the omitted second layer has minimum4s=2. The hardened helper
correctly excludes it. The regression finishes with
`ZERO_CLASS_LAYER_REGRESSION_PASS`.

This example has parent rank5 and is outside the four actual top-down
rank-seven branches. Their radii force s>3/2, which is why the original
theorem's branch conclusion survives the generic-helper correction.

## Final review of the bilingual theory manuscripts

The mathematical content of output/rank9_audit_theory_RU.txt was reviewed
through its final appendices and bibliography; the completed English
manuscript's branch, sharpness, ambient-lattice, audit and reproduction
sections were also reviewed. No remaining fatal mathematical defect was
identified. In particular:

* The Schur, class-layer, primitive-dual flag, Mordell, determinant-window,
  lifting, exact-interval and induction arguments are logically compatible.
* The 64-tuple K9 argument is valid: a hypothetical norm2 vector has integral
  coordinates of absolute value at most2 by Cauchy--Schwarz and the displayed
  diagonal of C^{-1}. Modulo3 this leaves exactly64 tuples. Their minimum
  norm is8. The congruence modulo6 excludes every other possible shorter
  norm, and all layers with |m|>=2 are automatically longer than6.
* All displayed residual Gram matrices, extension columns, branch constants
  and the 64-tuple norm distribution agree with the certificates.
* The RU Cartan matrix is a different valid ordering of E7. Its rows1,...,7
  correspond to archived rows(7,6,5,4,3,1,2), checked entry by entry; its
  determinant is2. Consequently the displayed Gram4C^{-1} is isometric to
  the archived determinant8192 representative.
* The determinant identity for orthogonal complements is valid under the
  explicitly stated primitive/unimodular hypotheses. The final RU revision
  now also assumes an even ambient lattice for the packing consequence and
  defines U=span_R K, so rank(L)=39 and the projection-surjectivity argument
  have their required hypotheses. EN states the same conditions correctly.
* The inherited-radius central-density bound is correctly simplified to
  3^16/(2^20 sqrt(5)). Both versions distinguish this consequence from global
  optimality of arbitrary39-dimensional packings, larger-radius variants,
  cluster constructions and ambient-embedding classification.
* The English quotation of all three paragraphs of the supplied source's
  Section7 matches recovered/source_main.txt, with its displayed mathematical
  formulas restored. These quoted historical/source claims are not presented
  as newly audited packing or contemporary literature results.
* The runtime claims distinguish the complete same-code regeneration from
  independent smaller checks, and distinguish hashes from exhaustive-search
  completeness. The optional full E6 subtree is not falsely described as
  independently rerun; the actually needed E7 and H6318 targets were replayed.

Four local wording issues discovered during this read were corrected in
the RU manuscript: (i) y in J* gives integral cross-pairings but the new
diagonal must also be integral; (ii) the order1 residue-list example has an
empty list, not a nonempty list; (iii) explicit remainder assertions in
Bareiss were attributed to exact_lattice.py, not every autonomous variant;
(iv) the138 parents were correctly labeled rank6 for the rank6-to7 step.
The corresponding extension-integrality qualification is present in EN.

This review assesses mathematical content and stated scope. Final document
compilation and page-layout inspection are separate delivery checks.
