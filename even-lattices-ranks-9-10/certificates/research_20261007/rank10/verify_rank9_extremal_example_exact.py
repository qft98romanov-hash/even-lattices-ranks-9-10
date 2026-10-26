#!/usr/bin/env python3
"""Exact certificate for the extremal rank-nine example K_9.

The script uses only integer/rational arithmetic.  It verifies that the
displayed Gram matrix is symmetric, even, positive definite, has determinant
21870, and has minimum exactly 6.  Together with the exhaustive lower-bound
certificate, this proves sharpness.
"""

from hashlib import sha256
from pathlib import Path

from exact_lattice import determinant, enumerate_vectors, ldl, qform


K9 = [
    [ 6, -3, -3, -3, -3, -3, -3,  3, -2],
    [-3,  6,  3,  3,  3,  3,  3,  0,  1],
    [-3,  3,  6,  0,  3,  0,  0, -3,  3],
    [-3,  3,  0,  6,  3,  3,  3,  0, -1],
    [-3,  3,  3,  3,  6,  3,  3, -3,  1],
    [-3,  3,  0,  3,  3,  6,  3,  0,  0],
    [-3,  3,  0,  3,  3,  3,  6,  0,  1],
    [ 3,  0, -3,  0, -3,  0,  0,  6, -1],
    [-2,  1,  3, -1,  1,  0,  1, -1,  6],
]


def main() -> None:
    assert len(K9) == 9 and all(len(row) == 9 for row in K9)
    assert all(K9[i][j] == K9[j][i] for i in range(9) for j in range(9))
    assert all(K9[i][i] % 2 == 0 for i in range(9))

    # Exact rational LDL^T; ldl raises if a pivot is non-positive.
    _lower, diagonal = ldl(K9)
    assert all(x > 0 for x in diagonal)

    det = determinant(K9)
    assert det == 21870

    below = enumerate_vectors(K9, 5, include_zero=False)
    assert below == []
    through_six = enumerate_vectors(K9, 6, include_zero=False)
    minimal = [(x, q) for x, q in through_six if q == 6]
    assert minimal
    assert all(qform(K9, x) == q == 6 for x, q in minimal)

    canonical = repr(K9).encode("ascii")
    print("EXACT CERTIFICATE: EXTREMAL RANK-NINE EXAMPLE")
    print("arithmetic = integers and fractions only")
    print("rank =", len(K9))
    print("even = yes")
    print("positive definite = yes")
    print("det(K9) =", det)
    print("nonzero vectors of norm <= 5 =", len(below))
    print("oriented vectors of norm 6 =", len(minimal))
    print("min(K9) = 6")
    print("canonical Gram sha256 =", sha256(canonical).hexdigest())
    print("RANK9_EXTREMAL_EXAMPLE_EXACT_OK")


if __name__ == "__main__":
    main()
