# Exact ambient-embedding results, 7 October 2026

This is a confidential continuation of the supplied manuscript. No unpublished material was sent to a public search service. These results do not amount to a complete classification of automorphism-group orbits in rank 48.

## 1. Independently checked printed data

The complete integer matrices were extracted from Appendix A of `main (4).pdf`, using `source_extracted.txt`. The final verifier `verify_ambient_embeddings.py` uses only Python integer and rational arithmetic.

Both printed 48-dimensional Gram matrices (labelled P48p and P48m in the source) satisfy symmetry, even diagonal, determinant 1, and positive definiteness, checked with exact LDL decomposition. Identifying the printed matrices with the particular named published lattices, and independently enumerating their complete minimal shells, are separate matters; no new full ambient minimum enumeration is claimed.

For each printed section the verifier checks the Gram matrix, determinant, Smith decomposition with unimodular transformations, primitivity, an explicit full integer basis of the orthogonal complement, its determinant, and the index of the orthogonal direct sum in the ambient. It also constructs an explicit discriminant anti-isometry using integral lifts in the ambient.

| Ambient | Section rank | Section/complement determinant | Nontrivial discriminant invariant factors | Complement rank |
|---|---:|---:|---|---:|
| P48p | 8 | 6561 | 3,3,3,3,3,3,3,3 | 40 |
| P48p | 9 | 21870 | 3,3,3,3,3,3,30 | 39 |
| P48p | 10 | 54675 | 3,3,3,3,15,45 | 38 |
| P48m | 5 | 3072 | 4,16,48 | 43 |
| P48m | 3 | 128 | 2,8,8 | 45 |

For every row, the Smith form of the embedding matrix is `[I | 0]`, and the direct-sum index equals the displayed determinant. Every computed complement basis contains a norm-6 vector. Assuming the ambient minimum-6 theorem, these witnesses prove that the complements have minimum exactly 6. The verifier also checks the printed cluster-lift pairing identities for the last two rows.

The first eight rows of printed T9 are an explicitly verified unimodular change of basis of the printed T8 section. The first nine rows of T10 equal T9. Thus the nested section chain is verified in ambient coordinates, rather than only abstractly.

### Explicit anti-isometry certificate

Use column coordinates in the ambient, let T be the section row matrix, G its ambient Gram matrix, K=TGT^t, and d=det K. A Smith decomposition supplies an integer matrix Q with TGQ=I. Put

    N = d Q - T^t adj(K).

Then TGN=0, and each column of N/d belongs to the dual of the integral complement. The verifier checks

    (N/d)^t G (N/d) = Q^t GQ - K^{-1}.

The matrix Q^tGQ is integral with even diagonal. Hence this induces the opposite finite quadratic form on the complement discriminant group. The full matrices Q,N, complement bases, Gram matrices, and Smith transformations are in `ambient_embedding_certificates.json`.

## 2. A new restricted non-embedding theorem

Let K9 denote the precise printed primitive section of P48p, with the specified ordered basis, and write its Gram matrix as

    K9 = [[G8,p],[p^t,6]],
    p = (-2,1,3,-1,1,0,1,-1)^t,
    G8 = Gram(sqrt(3) E8).

The new alternative rank-10 lattice found in this research run is

    A10 = [[G8,p,-p],[p^t,6,-1],[-p^t,-1,6]].

It has determinant 54675, minimum 6, and is not isometric to the previously printed K10; those intrinsic facts are verified in the separate rank-10 work. The following ambient statement is independently established here:

**Theorem. No isometric copy of A10 in the printed P48p contains the specific printed K9 section.**

This is a statement about this K9 sublattice, not an assertion that A10 has no embedding anywhere in P48p or in another rank-48 ambient.

### 2.1 Exact empty fiber

There is no integer ambient coordinate vector w satisfying

    w^t G w = 6,
    T9 G w = (2,-1,-3,1,-1,0,-1,1,-1)^t = (-p,-1)^t.

This has been checked by exhaustive, rigorously enclosing integer enumeration:

- 611239 recursion nodes;
- 0 leaves;
- 0 norm-6 witnesses.

The Python implementation uses arbitrary-precision integers, exact rational arithmetic, and `math.isqrt`; no floating-point value participates in any pruning step. A separate C++ implementation gives the same counts. The floating search that suggested this result is not the certificate.

As a positive control, the fiber for the original printed K10 has target

    (1,-1,1,0,-1,-2,-2,1,2)^t.

The same exact procedure visits 610015 nodes and finds exactly one leaf and one norm-6 vector. Converting that vector back to ambient coordinates reproduces exactly the last row of the printed T10 matrix.

### 2.2 Why the empty fiber excludes every A10 containing this K9

Suppose an isometric A10 contained the fixed K9. It then contains its fixed primitive K8=sqrt(3)E8. Write V=span(K8)^perp inside the real span of A10, and let P be the projected rank-2 lattice in V.

The exact discriminant-class bound for K8 is

    max_{a in K8*/K8} mu(a) = 8/3.

Every nonzero projected vector z has a lift whose K8 component has squared norm at most 8/3. Since A10 has minimum 6, ||z||^2 >= 10/3. Also

    det P = det(A10)/det(K8) = 54675/6561 = 25/3.

The two-dimensional Hermite bound is therefore an equality, so P is a scaled hexagonal lattice. The projection z1 of the ninth printed K9 basis vector has squared norm 10/3, hence is shortest. Choose a hexagonal basis z1,z2 with norms 10/3 and inner product 5/3. Choose a closest lift w of z2. Its K8 class has minimum exactly 8/3, and w has norm 6.

Because K8 is primitive and z1,z2 form a basis of the projected lattice, the fixed K8 basis followed by the ninth vector and w is a full integral basis of A10. Let q be its integral pairing column with the fixed K8 basis. The Gram matrix of A10 reduced modulo 3 has rank 3; this follows directly from the displayed matrix. If q and p were linearly independent modulo 3, the block matrix

    [[0,p,q],[p^t,0,c],[q^t,c,0]]

would have rank 4. Therefore q is proportional to p modulo 3. The zero multiple is impossible because it would be the zero discriminant class, whereas its class minimum is 8/3. The multiple +1 is impossible: the inner product of the K8 components is congruent to 8/3 modulo integers, while (z1,z2)=5/3, so the total would be congruent to 13/3 and would not be integral. Consequently q=-p modulo 3.

Since G8/3 is unimodular, congruence modulo 3 identifies the K8 discriminant class. Subtracting a vector of K8 from w therefore makes its K8 component exactly the negative of the ninth vector's K8 component. Its squared norm remains 8/3+10/3=6, and its inner product with the ninth vector becomes

    -8/3 + 5/3 = -1.

This produces exactly the forbidden fiber (-p,-1). Contradiction.

No uniqueness theorem for the K8 section inside K9, and no complete classification of all K9 embeddings, is required for this argument.

### 2.3 Completeness of the integer enumeration

Set A=T9G and b=(-p,-1). An integer right inverse Q gives a particular solution w0=Qb. The verified rows of B form the full integer kernel of A. Therefore all possible w are exactly

    w = w0 + B^t x,    x in Z^39.

Put C=BGB^t, g=BGw0, c=-C^{-1}g. Exact computations give

    w0^t G w0 - g^t C^{-1}g = 7/2.

Thus w has norm at most 6 if and only if

    (x-c)^t C (x-c) <= 5/2.

An exact LDL decomposition C=L diag(D_i)L^t rewrites the left side as

    sum_i D_i (x_i + sum_{j>i} L_{ji} x_j - y_i)^2,
    y = L^t c.

For each i, the Cauchy inequality bounds every feasible coefficient by

    |x_i| <= B_i,
    (B_i-|c_i|)^2 >= (5/2)(C^{-1})_{ii},  B_i >= |c_i|.

All these inequalities are checked with rational arithmetic. The largest B_i is 28 for the excluded fiber.

Take S=2^24. Round each S L_{ji} and S y_i to an integer with error at most 1/2, and let d_i=floor(S D_i)>0. For a partially chosen tail x_j, j>i, let

    C_i = round(S y_i) - sum_{j>i} x_j round(S L_{ji}),
    E_i = ceil((1+sum_{j>i} B_j)/2).

The exact center is within E_i/S of C_i/S. Consequently the exact i-th squared contribution is bounded below by

    d_i max(0, |S x_i-C_i|-E_i)^2 / S^3.

Every actual feasible vector must therefore satisfy the relaxed integer inequality

    sum_i d_i max(0, |S x_i-C_i|-E_i)^2 <= 5 S^3/2.

The recursion enumerates this entire relaxation, clipping only by the proven coordinate bounds. Given remaining integer budget R, its candidate interval is exactly enclosed using

    |S x_i-C_i| <= E_i + isqrt(R // d_i).

The excluded fiber has no leaves even in this relaxation, proving that it has no actual solution. Integer rounding only enlarges the enumerated set; it cannot discard a genuine solution.

The verifier recomputes all algebraic prerequisites, the kernel determinant, the primitive Smith form, the exact LDL factorization, the coordinate bounds, and every rounding bound. The rounded data are not trusted without those checks. The basis B was found with a heuristic reduction, but its full-kernel property is subsequently certified exactly; no correctness claim relies on that heuristic.

## 2.4 Complete local classification: exactly 19 optimal supersections

The targeted negative computation was extended to the entire finite equality family. **The specific printed K9 in P48p is contained in exactly 19 distinct primitive rank-10 sections of determinant 54675 and minimum at least 6. All 19 are isometric to the original K10; the alternative A10 occurs zero times.** These are the determinant-minimizing supersections of this fixed K9, by the sharp E8-containing bound. The count19 refers to concrete ambient sublattices, not automorphism-group orbits.

All561 admissible E8 discriminant classes were paired under b->a-b, giving281 targets. Exact enumeration found262 empty fibers and19 singleton fibers, totaling171472428 nodes and19 leaves. A full independent Python arbitrary-precision replay took397.17 seconds and matched every C++ fiber count and actual solution vector. The main certificate is `all_fixed_K9_extensions_verified.json`.

Each resulting embedding has Smith form[I10|0]. Exact residual normal numerators modulo sign distinguish all19 ambient real spans, and hence all19 primitive sublattices. An independent audit also verified primitivity by gcd-one maximal minors, without using the Smith routine. The candidate set was independently reconstructed and matched a separately generated561-class discriminant list; the mate involution was explicitly checked to be class negation.

The complete proof, including why a target-pair enumeration counts sublattices rather than merely new basis vectors, is in `fixed_K9_19_sections_proof.md`. The general classification of all K9 embeddings and the automorphism-group orbit classification remain open. This local theorem does not use the global rank-nine determinant lower-bound search.

## 3. Automatic primitivity

Let M be an even integral ambient of minimum at least 6, and let J be an isometric copy of a rank-r lattice K inside M. Its saturation Jbar in M remains even integral of minimum at least 6. If the saturation index is t then

    det Jbar = det K / t^2.

Therefore det K < 4 e_r(6) forces t=1. In particular, every embedding of a rank-9 determinant minimizer with determinant 21870 is automatically primitive, assuming the audited e9(6)=21870 theorem.

One unconditional-in-this-branch consequence of that theorem and the Mordell bounds is

    gamma_10 <= 2^(9/7),
    21870 <= gamma_10 (det L10)^(9/10),
    det L10 >= (21870/2^(9/7))^(10/9).

The exact integer comparison is

    2^90 * 24661^63 < 21870^70 <= 2^90 * 24662^63.

Since an even rank-10 determinant is 0 or 3 modulo 4, this implies det L10>=24663. This bound is only a byproduct and may be weaker than other rank-10 results in the run. It already suffices to show that every embedding of either determinant-54675 rank-10 lattice in an even minimum-6 ambient is primitive, because 54675/4<24663.

## 4. What an actual complete embedding classification requires

For any primitive embedding K into an even unimodular M, with L=K^perp intersect M, the discriminant forms satisfy q_L is isomorphic to -q_K. The overlattice M of K orthogonal-sum L is the graph of a discriminant anti-isometry phi:A_K->A_L.

Conversely, any such graph defines an even unimodular overlattice with K and L primitive. To obtain embeddings in a specified positive-definite ambient M, one must also test that the resulting overlattice is isometric to that particular M. Minimum 6 must be imposed on the glued lattice, not only on the two components.

Up to ambient isometry and reparametrization of the source K, the classification is therefore a union over complement classes L of

    O(L) \ {anti-isometries phi with glued lattice isometric to M} / O(K).

This is a finite reduction, not a completed orbit enumeration. For labelled embeddings of a fixed source, the quotient by O(K) is omitted. Indefinite-lattice uniqueness results do not automatically apply to these positive-definite rank-48 lattices.

The supplied PDF prints ambient certificates for P48p and P48m. The other ambient instances P48q and P48n are referenced in the manuscript's repository but are not included in the local printed data used here. No exhaustive minimal-shell or automorphism-group orbit search was performed in any ambient, and no complete complement classification in ranks 38 or 39 was obtained.

## 5. Reproduction and file roles

Required Python modules are standard-library only for all exact verification. From this directory (with the original extracted source at the relative location expected by the ambient verifier), run:

    python verify_ambient_embeddings.py
    python prepare_A10_exact_cvp.py
    python prepare_A10_exact_cvp.py --control
    python verify_A10_extension_exact.py
    python verify_A10_extension_exact.py --control

The last two commands can also run directly from the existing exact JSON files, and independently recompute their rational prerequisites. `printed_matrices.json` contains the source integer matrices. `A10_integer_fiber_basis.json` contains only the integral basis and lift needed to regenerate the exact fiber inputs. `A10_exact_cvp_verified_result.json` and `K10_control_exact_cvp_verified_result.json` record the independently reproduced outcomes.

Optional C++ reproduction uses `search_A10_exact_cvp.cpp`, compiled without disabling assertions, and the corresponding `*_input.txt` files. The Python arbitrary-precision verifier is the main portable certificate and avoids any fixed-width overflow assumption.

Files named `search_alternative_*`, the original floating `search_cvp.cpp`, and `A10_cvp_search_data.json` record exploratory work. They are not needed for certification and should not be confused with the exact verifiers.
