# Independent theoretical audit, 10 September 2026

Scope: recovered English manuscript and the mathematical interfaces of the released certificate programs. This audit did not assume that a printed PASS established correctness. It independently reconstructed the reduction, checked all numerical window endpoints by integer powers, and recomputed all 2235 rank-seven determinants using a new rational Gaussian elimination routine.

## Verdict

No fatal error was found in the theoretical implication from complete finite extension enumeration to the claimed bound det(L) >= 21870. The saturated-dual flag, Hermite windows, discriminant-layer criterion, lifting inequality, and final branch exclusions are sound with the explicit hypotheses below. The finite-enumeration completeness and implementation still require the separate code audit/replay.

The recovered exposition and one supplementary verifier contain real defects that should be corrected rather than silently reported as an entirely clean audit:

1. **Scaling notation.** The det-8192 lattice has Gram matrix 4 C_E7^{-1}; as a Euclidean lattice it is **2 E7***, not 4 E7*. Indeed det(t E7*) = t^14/2. Thus det(2 E7*) = 8192, while det(4 E7*) = 134217728. The original label mixes scaling of vectors with scaling of Gram matrices. This is a notation error, not an error in the matrices or determinant bound. Use H_8192 = 2 E7* and explicitly declare that its Gram matrix is 4 C_E7^{-1}. Preserve old filenames as legacy identifiers if desired.
2. **Omitted hypotheses in the one-vector proposition.** Its iff statements require the parent J to be even integral and min(J) >= 6. Without the first assumption, making the added diagonal even does not make K even; without the second, testing nonzero layers does not control the parent layer m=0. All actual flag parents satisfy the hypotheses, so the theorem proof survives. State them directly.
3. **Generic centered-layer shortcut is incomplete.** In `verify_rank7_topdown.py::allowed_one_vector_extensions`, the loop m=1,...,floor(h/2) for a class of order h omits the nonzero zero-class layer m=h. The additional requirement h^2 s >= 6 is necessary. A concrete counterexample is J with Gram diag(6,6,8), y=(1/2,1/2,1/2), mu(y+J)=5, h=2, and s=1. The bordered Gram matrix with cross=(3,3,4), last diagonal 6 passes the m=1 test, yet (-1,-1,-1,2) has norm 4. This error can only admit extra candidates; it cannot discard a genuine extension. In the actual det-7722 output, both accepted extensions have s=39/22>3/2, so all |m|>=2 layers automatically have norm >6. In addition, they are not compatible with the shortest-dual flag and their minimum is checked directly. Thus this defect does not invalidate the rank-nine bound. Add `if h*h*s < 6: continue` and rerun the small affected branch. The main `extend_flag.py` implementation checks every m with m^2*s<6 and has no such omission.
4. **Squared versus unsquared first minimum.** The manuscript uses lambda_1(M) to mean the minimum squared norm, contrary to another widespread convention. Define it explicitly or replace it by min(M) throughout. Every displayed formula is correct with squared norms.
5. **E8 rigidity is an imported theorem.** From min(L8)>=6 and det(L8)=3^8 one needs uniqueness of the lattice attaining gamma_8=2 among all Euclidean lattices. Uniqueness merely among even unimodular lattices would not suffice, because L8/sqrt(3) is not known integral a priori. The required stronger theorem is classical and also follows from Viazovska's uniqueness among periodic optimal packings. State exactly the stronger result and cite it.
6. **Root-reflection terminology.** The matrix H/3 in the E7 verifier has some positive off-diagonal entries and is not a simple-root Cartan matrix. Its basis vectors are roots, and reflections in them are genuine integral isometries, which is all the proof needs. Replace “simple root reflections” by “reflections in the displayed root basis.” There is no need to prove that they generate the entire Weyl group: orbits of any certified subgroup safely reduce the extension list, and the output shows that the chosen subgroup suffices here.
7. **Discrete radius terminology.** rho_glue^2 is a maximum over J*/J, not the ordinary continuous covering radius. The definition is correct; retain the qualifier “discriminant” or “glue” whenever reporting it. Code filenames containing `covering_radius` are not themselves claims about the continuous covering radius.

## Detailed reconstruction of the structural proof

### 1. Normalization and determinant

For a rank-r lattice with basis matrix B, G=B^T B and det(L)=det(G)=covol(L)^2. Its minimum m(L)=min_{x in Z^r\{0}} x^T G x is a squared length. Under vector scaling tL, G becomes t^2G, m becomes t^2m and det becomes t^{2r}det. The dual Gram matrix in the dual basis is G^{-1}, so det(L*)=1/det(L). For an integral lattice J, J*/J is finite of order det(J).

A basis change X in GL_r(Z) transforms G to X^T G X, preserving all these invariants. To identify two input forms it is sufficient to exhibit such an X and verify det(X)=+/-1 and the matrix identity exactly. Failure to merge equivalent forms only causes over-enumeration; an incorrect merge is dangerous and must be excluded by explicit maps.

### 2. Primitive hyperplane and saturation

Let y be a shortest nonzero vector in M*. It is primitive: y=kz with |k|>1 and z in M* would contradict minimality. The pairing map phi_y:M->Z is surjective. To see the latter without assuming it, if its image were kZ with k>1 then y/k would lie in M*, contradicting primitivity. Its kernel J=M intersect y^perp is primitive and rank one less. Choose v with <v,y>=1. Then M=J+Zv, and the perpendicular component of v is y/<y,y>, of squared norm 1/<y,y>. Thus

    det(M)=det(J)/<y,y>,  det(J)=det(M)*m(M*).

Every sublattice in the descending flag is even integral and has minimum at least that of M. Primitivity is transitive: if A is primitive in B and B in C, nx in A first forces x in B, then x in A. Hence the one-vector model is applicable at every level, including the final rank-eight-to-nine step.

### 3. Hermite constants and an explicit derivation of Mordell's inequality

Define gamma_r=sup_M m(M)/det(M)^{1/r}, over all positive-definite Euclidean rank-r lattices. The classical exact values used are

    gamma_r^r = 1, 4/3, 2, 4, 8, 64/3, 64, 256  (r=1,...,8).

They imply det(M)>=(6/gamma_r)^r whenever m(M)>=6. Applying the same inequality to M* and then the hyperplane identity gives

    det(J) <= gamma_r det(M)^{(r-1)/r}.

Mordell's inequality can be derived within this note rather than imported unexplained. Normalize an arbitrary rank-n lattice M to det(M)=1. For its shortest-dual section J,

    m(M) <= m(J) <= gamma_{n-1} det(J)^{1/(n-1)}
                     <= gamma_{n-1} gamma_n^{1/(n-1)}.

Taking the supremum over M and dividing by gamma_n^{1/(n-1)} gives, for n>=3,

    gamma_n^{(n-2)/(n-1)} <= gamma_{n-1},
    gamma_n <= gamma_{n-1}^{(n-1)/(n-2)}.

For n=9 this gives gamma_9<=2^{8/7}. There is no use of a proposed exact rank-nine Hermite constant, no dependence on a recent rank-nine packing preprint, and no circular use of the desired integral determinant theorem.

### 4. Determinant congruences

Reduction modulo 2 of an even symmetric Gram matrix is alternating and therefore has even rank. In odd dimension its determinant is even. In dimension 2m, singular reduction has nullity at least two, so at least two Smith factors are even and the determinant is divisible by four. In the nonsingular case, split off a 2x2 block with odd off-diagonal entry over Z/4Z. Its determinant is -1 mod4. Orthogonal elimination preserves evenness of diagonal entries; iteration gives det(G)=(-1)^m mod4. Thus even-rank determinants are 0 or (-1)^{r/2} mod4.

Consequently, a rank-nine counterexample has det(L9)<=21868, not merely <=21869.

### 5. Exact windows

The lower Hermite values for r=1,...,8 are exactly

    6, 27, 108, 324, 972, 2187, 4374, 6561.

After the E8 equality case is excluded, the first congruence-allowed rank-eight determinant above 6561 is 6564.

The upper recursion was rechecked with exact integer powers. Let U9=21868. The rank-eight endpoint follows from

    15908^63 <= 2^72 * 21868^56 < 15909^63.

For r<=8, if c_r=gamma_r^r, determine the integer floor a of gamma_r U_r^{(r-1)/r} by

    a^r <= c_r U_r^{r-1} < (a+1)^r.

The raw floors in ranks 7,6,5,4,3,2,1 are 9493,4647,1894,634,178,39,7. Congruences reduce them to 9492,4647,1894,633,178,39,6. The final windows in the recovered text are therefore correct:

|r|Lower|Upper|Congruence|
|---|---:|---:|---|
|8|6564|15908|0 or 1 mod4|
|7|4374|9492|0 mod2|
|6|2187|4647|0 or 3 mod4|
|5|972|1894|0 mod2|
|4|324|633|0 or 1 mod4|
|3|108|178|0 mod2|
|2|27|39|0 or 3 mod4|
|1|6|6|0 mod2|

These are windows for a specially selected shortest-dual flag of a hypothetical rank-nine counterexample. They are not bounds on all even lattices in those ranks without the displayed upper cutoffs. In ranks at most seven, any even minimum-six lattice satisfying the corresponding upper cutoff has a descending shortest-dual flag in the earlier windows; hence a complete enumeration does also cover all such bounded low-rank lattices. This does not imply a classification in rank nine. The exclusion of the rank-eight endpoint6561 is special to continuation into a strict rank-nine counterexample.

### 6. The E8 equality case

If det(L8)=6561 and min(L8)>=6, then L8/sqrt(3) has determinant1 and minimum>=2, hence attains gamma_8=2. The classical rigidity theorem gives L8 congruent to sqrt(3)E8. Its discriminant group is naturally E8/3E8: the class of z in E8 corresponds to z/sqrt(3) modulo sqrt(3)E8. The squared norm in the scaled dual class is one third of the minimum squared norm in z+3E8.

The reported exact class distribution is (minimum,count)=(0,1),(2,240),(4,2160),(6,2240),(8,1920), totaling6561 classes. Thus rho_glue^2=8/3. The one-vector bound below gives det(L9)>=6561*(6-8/3)=21870. The equality case is therefore excluded under the strict counterexample assumption.

### 7. Discriminant classes and one-vector extensions

Assume J is even integral, min(J)>=6, with Gram matrix G. Let p in Z^r be the cross-pairing column of a new basis vector v, and let n=<v,v>. In the orthogonal decomposition v=y+z, y has basis coordinates G^{-1}p, and

    mu=<y,y>=p^T G^{-1}p,
    s=<z,z>=n-mu,
    H=[[G,p],[p^T,n]],
    det(H)=det(G)*s.

Replacing v by v+x, x in J, is a unimodular change of the extended basis and changes y only inside its class a in J*/J. Thus one may choose y to be a shortest class representative. The class norm modulo2 is well-defined because

    <y+x,y+x>-<y,y>=2<y,x>+<x,x> in 2Z.

The extension is positive definite iff s>0, and even iff n=s+mu is even. Every vector outside J is x+mv with m nonzero. Its least squared norm for fixed m is

    m^2*s + mu_J(ma).

Therefore min(H)>=6 iff these expressions are >=6 for all m!=0, with the parent hypothesis controlling m=0. Negative m are redundant since mu_J(-a)=mu_J(a). Terms with m^2s>=6 are automatic. If a has order h, an alternative correct finite criterion is:

    h^2*s>=6 and m^2*s+mu_J(ma)>=6 for 1<=m<=floor(h/2).

For nonzero residues, replace m modulo h by a representative of least absolute value, using mu(-a)=mu(a). For the zero residue, the least nonzero coefficient is h, which explains the additional h-layer test.

The discriminant radius bound is obtained just from m=1:

    s >= 6-mu_J(a) >= 6-rho_glue(J)^2,
    det(H) >= det(J)*(6-rho_glue(J)^2).

Only an upper bound on all class minima is needed to prove this determinant lower bound. Exact maxima provide convenient sharp numerical certificates, but unnecessarily stronger claims about continuous covering radii are not required.

### 8. Why one witness per discriminant class suffices

The class fingerprint is G^{-1}p mod Z^r; equivalently adj(G)p mod det(G). This map identifies precisely the quotient G^{-1}Z^r/Z^r, of order det(G). Enumerating the complete dual ellipsoid of squared radius B and finding det(G) distinct fingerprints proves that every class was encountered. If every class has a representative of norm<=B, any hypothetical shorter representative also lies in that ellipsoid; hence the least recorded norm in each class is exact.

Given a class minimum mu and determinant window [a,b], all possible even n lie in the finite interval [mu+a/det(G),mu+b/det(G)]. A different shortest representative in the same class changes only the basis of the same extension for a fixed s. Thus one shortest witness per class loses no isometry class of extension.

The algorithm's emergency cutoff `bound>20` is safe provided it raises an error (as it does): it does not silently return an incomplete table. The exact ellipsoid enumeration and positive isometry identities are the trusted finite interfaces, to be independently audited by the code agent.

### 9. Shortest-normal condition and lifting

The perpendicular dual vector y0=z/s has squared norm1/s and pairs to1 with v and to0 with J. Thus J is a shortest-dual hyperplane of K iff min(K*)=1/s. The implementation enumerates all dual vectors up to the inclusive exact threshold1/s; equality ties must be retained, as they are in the main code.

Let u be shortest in J*, of squared norm lambda. Choose an integer k nearest to <u,v> and put c=k-<u,v>, so |c|<=1/2. The vector u+c*y0 pairs integrally with J and with v, hence belongs to K*. It is nonzero because u is nonzero and perpendicular to y0. Consequently

    1/s <= ||u+c*y0||^2 = lambda+c^2/s <= lambda+1/(4s),

and s>=3/(4lambda). Applied to L7 contained in L8, with min(L7*)=d6/d7, this gives d8>=3d7^2/(4d6). The inequality is only a necessary condition; passing it does not certify the shortest-normal property.

An isometry of the parent transports its entire already chosen lower flag, so deduplicating a parent by abstract lattice isometry cannot lose an extension needed for this argument. The value d6/d7 is intrinsic once the shortest-dual flag condition is imposed.

### 10. Binary seed check

For J=[6], representatives of the six discriminant classes have pairing k in {0,+1,-1,+2,-2,3}. A shortest representative has mu=k^2/6. The new diagonal n is even, at least6, and det=6n-k^2 lies in27..39. At n=6 all six classes occur, giving four isometry types with determinants27,32,35,36. At n=8 only k=3 gives det39. No n>=10 can lie in the interval. This gives exactly seven labelled forms and five types, matching the first finite level without relying on the released program.

### 11. Independent rank-seven arithmetic and all branches

A new rational Gaussian determinant computation over all138 parents and2235 children gave31 distinct pairs, and exactly2139 children have 3d7^2/(4d6)>15908. The surviving96 forms split as follows:

|d6|d7|Lifting floor for d8|Multiplicity|
|---:|---:|---:|---:|
|2187|4374|6561|2|
|2187|6318|13689|54|
|2835|7722|552123/35|32|
|4096|8192|12288|1|
|3240|8100|30375/2|1|
|3267|7986|14641|6|

The claimed reduction to six abstract rank-seven classes requires exactly the96 positive GL7 maps; no negative isometry oracle is needed. The six determinants are distinct, so six linked representatives are automatically pairwise nonisometric.

The branch implications, conditional only on the exact finite output claimed in the files, are arithmetically correct:

* sqrt(3)E7: four rank-eight types with (det,rho_glue^2,floor)=(12393,58/17,32076),(14580,9/2,21870),(15309,32/7,21870),(15309,68/21,42282). All exclude a strict rank-nine counterexample. The two determinant15309 types are nonisometric because their discriminant radii differ.
* H6318:12 labelled unrestricted extensions, split2 at12393 and10 at13689. The first pair violates the lifting floor13689, but keeping it is safe over-enumeration. The respective rank-nine bounds32076 and36504 close both types. Nothing requires asserting that every extension at13689 passes the shortest-normal test.
* H7722: the lifting floor is552123/35, which is strictly greater than13689. Its two unrestricted extensions both have determinant13689. Therefore neither can occur in the chosen flag; there is no flag continuation. Calling either one “admissible” without specifying unrestricted extension is misleading. Their common discrete radius10/3 and floor36504 are redundant checks only.
* H8192=2E7*: rho_glue^2=7/2 forces d8>=20480>15908.
* H8100: rho_glue^2=15/4 forces d8>=18225>15908.
* H7986: rho_glue^2=25/6 forces d8>=14641. Its two extensions are actually tested by the full shortest-normal criterion, not only the lifting inequality. They are opposite classes of one det14641 type; rho_glue^2=36/11 gives d9>=39930.

Hence every possible flag is impossible under d9<21870. The displayed K9 gives attainment after its exact determinant, positive definiteness, and minimum are checked separately. The abstract optimum is therefore21870 if the finite verifications succeed.

### 12. Orthogonal complements and precise packing scope

For primitive K in an integral unimodular Lambda, restriction Lambda=Lambda* -> K* is onto: any integer functional on K extends to Lambda because K is primitive as an abelian subgroup. Its kernel is the primitive orthogonal complement L. Thus

    Lambda/(K direct-sum L) is isomorphic to K*/K,
    [Lambda:K direct-sum L]=det(K),
    det(K)det(L)=[Lambda:K direct-sum L]^2,

which implies det(L)=det(K). For rank(K)=9 inside a rank48 minimum6 ambient lattice, L has rank39 and inherits minimum at least6. At ambient packing radius sqrt(6)/2=sqrt(3/2), the center density is

    (3/2)^(39/2)/sqrt(det(K)) <= 2^-20*3^16/sqrt(5).

This bounds that inherited-radius construction. It does not establish the global best sphere packing in39 dimensions, optimality after arbitrary radius changes if a complement has greater minimum, cluster optimality, uniqueness of the rank-nine optimizer, or a classification of ambient embeddings. The claim that the source construction attains the bound additionally relies on the source's actual saturated embedding, which should be checked by the source/scope auditor.

## Primary source support checked during this audit

No confidential source title, manuscript content, private lattice number or new theorem was sent as a search query. The only external lookups concerned standard Hermite/E8 theory.

* H. F. Blichfeldt, *The minimum values of positive quadratic forms in six, seven and eight variables*, Mathematische Zeitschrift39 (1935),1–15, DOI https://doi.org/10.1007/BF01201341. Publisher metadata was verified at https://link.springer.com/article/10.1007/BF01201341 . This is the classical primary reference for the low-dimensional extremal bounds. Full text was not accessible through that publisher page; do not say this audit reread Blichfeldt's entire proof.
* M. Viazovska, *The sphere packing problem in dimension8*, Annals of Mathematics185 (2017),991–1015, DOI https://doi.org/10.4007/annals.2017.185.3.7; accessible author manuscript https://arxiv.org/html/1603.04246v2 . The statement immediately following Theorem1 gives uniqueness of E8 among periodic optimal packings, using the argument of Cohn–Elkies Section8; this directly supplies the lattice equality rigidity needed here.
* N. M. Vetchinkin's classical uniqueness theorem is a natural historical reference, but no precise full-text URL was successfully retrieved in this audit. Prefer the verified Viazovska reference for a clickable primary source rather than inventing a locator.

## Recommended status language

“The theoretical reduction has passed a new independent audit, with the listed corrections. The bound is a computer-assisted theorem whose finite content is the complete exact enumeration and its independently replayed certificates. The audit does not constitute a Lean/Coq formalization, an external referee report, or a novelty search.”

Use the phrase “independently replayed” only for parts actually rerun in the present audit; list remaining checks as archived evidence if a new full regeneration is still running. Checksums establish file identity, never mathematical completeness by themselves.

## Final review of the expanded English monograph

The completed `output/rank9_audit_theory_EN.txt` was reviewed through its bibliography and appendices. The corrections above are explicitly incorporated, including the distinction between an arbitrary positive-definite extension and an integral extension. The manuscript now takes s in Q_{>0}, states integrality iff s+mu_J(a) is integral, and states even integrality/minimum only after imposing the parity and layer conditions. The integer-power endpoint equivalence is restricted to nonnegative integers.

All new mathematical sections were checked. In particular:

* the 64-tuple sharpness proof for K9 is valid: the residue norm is8 modulo6, the only possible smaller norm is2, the coordinate Cauchy bounds capture every norm-two vector in the class, and the64 tuples have the stated norm distribution;
* the explicit H8100, H7986, and J14641 matrices were parsed from the new document and match the exact certificate JSON targets;
* the primitive-complement restriction map and index-square determinant identity are valid;
* the radius and density normalization give3^16/(2^20*sqrt(5));
* the text attributes the ambient embedding attainment to the source, and explicitly records that those separate source embedding certificates were not rerun;
* it distinguishes inherited-radius determinant improvement from arbitrary-radius or cluster improvements;
* the report distinguishes the completed same-code full regeneration from independent checks of smaller arithmetic and search components, without describing the latter as a wholly independent implementation of the rank-seven search.

The added original first paragraph of Source Section7 was compared with the recovered text and agrees. The Bacher and Wen–Chang arXiv titles, authors and identifiers were separately checked against their primary arXiv records. No further mathematical correction was requested after the final English review. This final sign-off concerns the mathematical text; PDF visual layout and the complete program replay are separate audit tasks.
