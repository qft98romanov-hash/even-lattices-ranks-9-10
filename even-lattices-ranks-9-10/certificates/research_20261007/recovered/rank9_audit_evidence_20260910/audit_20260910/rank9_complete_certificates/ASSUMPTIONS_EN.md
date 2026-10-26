# Mathematical assumptions and scope

The certificate package separates the human mathematical reduction from the
finite exact computation.

## Inputs not reproved by the programs

The derivation of the determinant windows uses the following standard
lattice-theoretic facts:

1. a shortest nonzero vector of a dual lattice is primitive, and its
   orthogonal kernel is a saturated hyperplane section;
2. the determinant identity
   `det(L_{r-1}) = det(L_r) * ||y||^2` for this primitive dual normal;
3. the classical exact Hermite constants in dimensions at most eight and
   the equality case in dimension eight;
4. Mordell's inequality, in particular
   `gamma_9 <= gamma_8^(8/7) = 2^(8/7)`;
5. the determinant congruences for even integral lattices;
6. the exact discriminant-class criterion for a primitive one-vector
   extension.

The source preprint and the accompanying English/Russian proof manuscripts
give the mathematical derivations. The programs certify the exhaustive
finite searches and every numerical or isometry claim used after that
reduction.

## What the package proves

Subject to the standard facts above, the package proves for every abstract
positive-definite even integral rank-nine lattice of minimum at least six
that its determinant is at least 21870. It separately verifies an explicit
Gram matrix attaining 21870.

Because the statement is about all abstract lattices, it also rules out any
ambient-lattice section with smaller determinant. No assumption about an
embedding in `P_48p`, `P_48q`, or `P_48n` is needed for the lower bound.

## What the package does not prove

- uniqueness of the determinant-21870 optimizer;
- a complete isometry classification in rank nine;
- the analogous determinant problem in rank ten;
- classification of embeddings in a 48-dimensional ambient lattice;
- optimality of antipodal or more general cluster packings.

