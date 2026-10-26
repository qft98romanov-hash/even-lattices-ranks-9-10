# Independent review: exclusion of the alternative rank-ten lattice through the fixed printed K9

Status: PASS. This review concerns the particular integer ambient matrix printed as P48p and the particular printed rank-nine embedding T9. It does not classify all embeddings of K9, nor exclude A10 from every embedding into P48p.

Reviewed files:

- ../embeddings/verify_A10_extension_exact.py
- ../embeddings/A10_exact_cvp_input.json
- ../embeddings/K10_control_exact_cvp_input.json
- ../embeddings/printed_matrices.json
- ../embeddings/verify_ambient_embeddings.py
- ../embeddings/embedding_findings.md, sections2.1–2.3

The default and positive-control Python verifiers were actually executed. The results were:

| Mode | Nodes | Leaves | Norm-six witnesses |
|---|---:|---:|---:|
| Alternative extension |611239|0|0|
| Original K10 control |610015|1|1|

The control witness equals the final row of the printed T10 embedding matrix in ambient coordinates. The independent replay logs are A10_cvp_independent_replay.log and K10_cvp_independent_replay.log. I also checked directly that T9 G T9^t equals the fixed abstract K9 matrix used by the rank-ten classification, and that the printed G is symmetric, even, and positive definite by exact rational LDL. This is a code/proof review and replay of the same finite search, not an independently written complete enumeration implementation.

## 1. The full integer fiber, not a proper sublattice

Let Lambda be the integer lattice with Gram G, and K the fixed primitive section. The verifier checks detG=1, a Smith form of T9 with all nine nonzero invariant factors1, A B^t=0, det(B G B^t)=detK=21870, and a particular integral solution w0 of A w=b.

Here is why those checks certify completeness of B. Since K is primitive as an abelian subgroup of the unimodular Lambda, every integer linear functional on K extends to Lambda and is represented by a vector of Lambda. Thus the pairing map Lambda→K* is onto. Its kernel is N=K-perp∩Lambda, and Lambda/(K⊕N) is K*/K. The index is detK. Comparing Gram determinants gives detN=detK. The39 independent rows of B lie in N and have Gram determinant detK, so their index in N has square1. They therefore generate the full kernel. Every ambient integer solution of the nine pairing equations is exactly w0+B^t x with x∈Z^39.

No heuristic property of the reduced basis is used in this argument.

## 2. Exact completion of the square

The verifier recomputes C=B G B^t, g=B G w0, and wn=w0^t G w0, and checks the positive rational LDL factorization of C. With c=−C^(-1)g it verifies

wn−g^t C^(-1)g=7/2.

Consequently the full norm≤6 problem is the exact ellipsoid

(x−c)^t C(x−c)≤5/2.

The individual coordinate bound follows from the Cauchy inequality in the C inner product:

|x_i−c_i|²≤(5/2)(C^(-1))_ii.

The supplied integers B_i are accepted only after the verifier checks B_i≥|c_i| and (B_i−|c_i|)²≥(5/2)(C^(-1))_ii. These conditions imply |x_i|≤B_i for every feasible vector.

## 3. The rounded recursion only enlarges the ellipsoid

Write C=L diag(D_i)L^t, y=L^t c. The true i-th contribution is

D_i [x_i+sum_{h>i}x_h L_hi−y_i]².

The script checks every rounding error, rather than trusting the prepared JSON. With scale S=2^24, d_i=floor(SD_i)>0, rounded center numerator C_i, and error allowance E_i, one has

|S[x_i+sum_{h>i}x_h L_hi−y_i]−(Sx_i−C_i)|≤E_i.

This uses only the already proven coordinate bounds and the individual rounding errors≤1/2. Therefore

d_i max(0,|Sx_i−C_i|−E_i)²
 ≤ S³ D_i [x_i+sum_{h>i}x_h L_hi−y_i]².

Summing proves that every true feasible vector lies in the integer relaxation with budget5S³/2. The recursive candidate interval uses

|Sx_i−C_i|≤E_i+floor(sqrt(R/d_i)),

computed exactly as E_i+isqrt(R//d_i). Its lower integer endpoint is a ceiling and its upper endpoint a floor; inspection of Python's signed floor division confirms the code implements these correctly, including negative centers. Clipping by ±B_i is legitimate. The recursion neither caps points nor stops early.

All arithmetic in the portable verifier uses Python arbitrary-precision integers and Fraction, with math.isqrt. There is no fixed-width overflow condition and no floating-point pruning. The default search has zero leaves even in this larger relaxation, so it excludes every true vector of norm at most6 in the specified fiber. The control evaluates the full exact norm at its leaf and reconstructs the displayed original extension vector.

## 4. Why one empty fiber excludes every alternative copy through this K9

Suppose an isometric copy of A10 contained the fixed printed K9. It also contains the fixed J=sqrt3E8. This J is primitive: a nontrivial saturation class would have a nonzero representative of norm≤8/3, contradicting minA10=6.

The projected rank-two lattice P has determinant25/3 and minimum≥10/3. Binary Hermite equality makes it hexagonal. The ninth K9 basis vector has a projection z1 of squared norm10/3, hence z1 is a shortest primitive vector in P. Choose an acute hexagonal basis(z1,z2). Lifting z2 and adjusting by J yields a vector w of norm6, because its class must have minimum8/3. Primitivity of J and the fact that(z1,z2) is a basis imply that the fixed J basis, the ninth K9 vector, and w form a full integral basis of A10. This legitimizes use of the intrinsic Gram rank modulo3.

Let p and q be the pairing columns of the ninth vector and w with J. The top-left8-by8 Gram block vanishes modulo3. If p,q were independent, the full Gram block would have rank4 modulo3. But A10 has intrinsic Gram rank3 modulo3. Thus q is a scalar multiple of p. The scalar0 gives the zero J-discriminant class and contradicts class minimum8/3. The scalar+1 makes the full pairing congruent to8/3+5/3=13/3 modulo integers, contradicting integrality. Hence q≡−p modulo3.

Since J has Gram3C with C unimodular, this congruence says the two horizontal projection classes are negatives. Subtracting a vector of J from w makes its horizontal component exactly the negative of the ninth vector's component. The norm remains8/3+10/3=6, and the pairing with the ninth vector is−8/3+5/3=−1. Thus w belongs to the forbidden ambient fiber with target(−p,−1). This contradicts the exact empty-fiber certificate.

The resulting theorem is genuinely stronger than exclusion of one marked extension: no copy of the alternative A10 can contain the fixed printed K9, regardless of how the rest of that copy was initially presented. It remains restricted to this K9 embedding. No assertion concerning other K9 automorphism orbits or all ambient embeddings follows.
