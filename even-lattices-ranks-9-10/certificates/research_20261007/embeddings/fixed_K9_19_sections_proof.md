# Classification of optimal rank-10 supersections of the fixed printed K9

Status: full independent Python replay PASS, all 281 fibers and actual vectors agree with the completed C++ enumeration. Independent coverage, mate-negation, primitive-minor, and ambient-sublattice deduplication audit PASS. Final certificate: `all_fixed_K9_extensions_verified.json`. Python replay time: 397.17 seconds in the shared session; this is not a benchmark.

## Precise statement

Let Lambda be the lattice with the printed P48p Gram matrix, and let K be the particular primitive rank-9 sublattice given by the printed T9. There are **exactly 19 distinct primitive rank-10 sublattices S of Lambda** such that

    K is contained in S,  det S = 54675,  min S >= 6.

All 19 are isometric to the original printed K10. None is isometric to the alternative A10. Each has determinant minimal among rank-10 sections containing K, because each contains its primitive sqrt(3)E8 section and the sharp bound for that subclass is 54675.

The number 19 counts concrete ambient sublattices, not automorphism-group orbits. This statement concerns the particular printed K, not all embeddings of an abstract K9 in P48p. If the ambient minimum-6 theorem is used, the condition min S>=6 is automatic. The equality classification independently guarantees minimum 6 for the enumerated intrinsic Gram matrices.

## Complete candidate set

Write G8=3C with C an even unimodular E8 Gram matrix and K=[[G8,p],[p^t,6]]. Set w=C^{-1}p and a=w mod3. The ninth basis vector has E8 component w/3 and perpendicular component z1 of squared norm 10/3.

For any optimal rank-10 supersection S, projection perpendicular to the fixed E8 yields a hexagonal lattice P of determinant25/3 and minimum10/3. Take an acute hexagonal basis z1,z2; both squared norms are10/3 and their inner product is5/3. The E8 discriminant classes a,b,a-b must all have minimum8/3, because z1,z2,z1-z2 are projected minimal vectors.

Exact enumeration of E8/3E8 gives

    class norms: 0,2,4,6,8
    counts:      1,240,2160,2240,1920.

For the fixed a, precisely561 classes b have both b and a-b among the1920 deepest classes. The involution b->a-b preserves this set. It has a single fixed point b=-a, and280 two-element orbits. Hence281 unoriented candidate targets suffice.

Choose any norm-8 integer vector v representing b. Put

    q=Cv,
    t=(p^t v+5)/3,
    r_b=(q,t).

The number t is an integer, since a-b is deep. A closest lift of z2 can be shifted by an element of E8 so that its E8 component is exactly v/3. This preserves its norm6 and gives exactly the full K pairing column r_b. Therefore every optimal supersection appears in one of these281 fibers

    T9 G u = r_b,    u^t G u = 6,    u in Z^48.

Exact inversion gives r_b^t K^{-1} r_b=7/2. The corresponding561 oriented discriminant classes are distinct. The fixed point gives the unique order-2 class; the other560 have order6. An independent generator in the rank-10 work produced the same561 adjugate fingerprints, and this equality of sets was checked exactly.

## Exact finite enumeration

All fibers use the same full integral kernel B of T9G and its positive-definite rank-39 Gram matrix. Each target has an integral lift u0. Its perpendicular residual problem is an exact rational ellipsoid of radius squared5/2. The independently verified integer enclosure is the one proved in `embedding_findings.md`, Section2.3.

The full run gives

    281 target fibers;
    171472428 recursion nodes;
    19 leaves;
    19 norm-6 solutions;
    262 empty fibers and19 singleton fibers.

Every branch is tested with integer arithmetic. All561 class candidates and all281 fibers are covered; there is no probabilistic sampling and no floating-point pruning. The Python replay independently recomputes all rational prerequisites, including coefficient bounds and rounding bounds, and compares every fiber's node count and its actual solution list with the C++ result.

The order-2 alternative fiber is empty. Every nonempty fiber belongs to the order-6 family, hence to the original K10 isometry type by the separately proved E8-containing equality classification.

## Why this counts sublattices rather than generators

First, the two acute choices z2 and z1-z2 in a fixed hexagonal plane exchange b with a-b. Taking one representative of each pair removes this systematic duplication. For a chosen order-6 class, a fixed ambient supersection has only one generator with the prescribed full K pairing column. If two quotient generators differed by sign, equality of their K projections would require twice the dual projection to belong to K, contradicting order6. Generators of the same sign differ by an element of K; identical K projection forces that difference to be zero.

Second, the certificate verifies a stronger direct ambient criterion. For each of the19 solutions u, form T10=[T9;u]. Its Smith form is [I10|0]. Thus its row lattice is saturated and equals the full ambient lattice in its real span.

Let d=det K=21870 and r=T9Gu. Define the integer ambient-coordinate vector

    N(u)=d u - T9^t adj(K) r.

Then N(u)/d is the component of u perpendicular to the fixed K and has squared norm5/2. Two resulting rank-10 spans coincide if and only if N(u)=+N(u') or N(u)=-N(u'), since the normals have equal nonzero length. The exact certificate checks that all19 normal vectors are distinct modulo sign. Thus the19 sections have different real spans and are different ambient sublattices. Saturation rules out different primitive row lattices with the same span.

The verified output supplies all19 new ambient vectors, their rank-10 Gram matrices, primitive Smith forms, and normal numerators. A complete ambient automorphism-orbit classification of these19 sections is a further problem and is not claimed.

## Files

- `prepare_all_fixed_K9_extensions.py`: construction of the complete561/281 candidate set and exact input bounds.
- `all_fixed_K9_extension_inputs.json`: common kernel data and281 exact targets.
- `search_all_fixed_K9_extensions.cpp`: exact C++ enumeration; fixed-width overflow bounds are checked by the input generator.
- `search_all_fixed_K9_extensions.log`: completed C++ transcript.
- `verify_all_fixed_K9_extensions.py`: independent arbitrary-precision Python replay, source checks, full coverage, exact vector matching, primitive-lattice checks and deduplication.
- `all_fixed_K9_extensions_verified.json`: final catalogue and verification summary, written only after all checks pass.
- `independent_deep_class_crosscheck.json`: equality with the separately generated rank-10 discriminant-class list.

The exact Python scripts use the standard library and the already audited adjacent `rank10/exact_lattice.py` for E8 short-vector enumeration.
