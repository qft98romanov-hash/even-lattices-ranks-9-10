#!/usr/bin/env python3
"""Exact standalone certificate for the ``sqrt(3) E8`` rank-eight branch.

Let E8 be written in the simple-root basis with Gram matrix C below and put

    L = sqrt(3) E8,       Gram(L) = 3 C.

Since E8 is unimodular, L*/L is canonically E8/3E8.  The squared norm of
the dual vector represented by y in E8 is q_C(y)/3.  This program enumerates
*exactly* every y in Z^8 with q_C(y) <= 8, proves that their residues modulo
3 cover all 3^8 classes, and records the exact minimum in every class.
Consequently the discrete glue covering radius is

    rho(L)^2 = max_[y] min_x q_C(y+3x)/3 = 8/3.

For a one-vector extension K of minimum at least 6, orthogonal projection
onto the new one-dimensional complement then gives

    det(K)/det(L) >= 6-rho(L)^2 = 10/3,
    det(K) >= 3^8 * 10/3 = 21870.

There is no floating-point arithmetic and no non-standard dependency.  The
complete ellipsoid enumeration uses an exact rational LDL decomposition and
exact integer endpoints.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from math import isqrt
from pathlib import Path


F = Fraction


def bareiss_det(a):
    """Exact determinant over the integers."""
    m = [list(map(int, row)) for row in a]
    n = len(m)
    old = 1
    sign = 1
    for k in range(n - 1):
        if m[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if m[i][k]), None)
            if pivot is None:
                return 0
            m[k], m[pivot] = m[pivot], m[k]
            sign = -sign
        p = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = m[i][j] * p - m[i][k] * m[k][j]
                assert numerator % old == 0
                m[i][j] = numerator // old
        old = p
    return sign * m[-1][-1]


def ldl_lower(a):
    """Return exact A=L diag(D) L^T with L lower unitriangular."""
    n = len(a)
    ell = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    dia = [F(0) for _ in range(n)]
    for j in range(n):
        dia[j] = F(a[j][j]) - sum(
            ell[j][k] * ell[j][k] * dia[k] for k in range(j)
        )
        assert dia[j] > 0
        for i in range(j + 1, n):
            ell[i][j] = (
                F(a[i][j])
                - sum(ell[i][k] * ell[j][k] * dia[k] for k in range(j))
            ) / dia[j]
    for i in range(n):
        for j in range(n):
            assert sum(
                ell[i][k] * dia[k] * ell[j][k]
                for k in range(min(i, j) + 1)
            ) == a[i][j]
    return ell, dia


def ceil_div(a, b):
    assert b > 0
    return -((-a) // b)


def integer_interval(centre, radius_squared):
    """All z in Z satisfying (z-centre)^2 <= radius_squared, exactly."""
    centre = F(centre)
    radius_squared = F(radius_squared)
    if radius_squared < 0:
        return range(0)
    a, b = centre.numerator, centre.denominator
    rhs_floor = (
        b * b * radius_squared.numerator // radius_squared.denominator
    )
    radius_numerator = isqrt(rhs_floor)
    return range(
        ceil_div(a - radius_numerator, b),
        (a + radius_numerator) // b + 1,
    )


def qform(a, x):
    return sum(
        F(x[i]) * a[i][j] * x[j]
        for i in range(len(a))
        for j in range(len(a))
    )


def enumerate_vectors(a, bound, visit):
    """Visit all x in Z^n with x^T A x <= bound, exactly once."""
    ell, dia = ldl_lower(a)
    n = len(a)
    x = [0] * n
    count = 0

    def rec(k, used):
        nonlocal count
        if k < 0:
            value = qform(a, x)
            assert value == used and value <= bound
            count += 1
            visit(tuple(x), value)
            return
        remaining = F(bound) - used
        if remaining < 0:
            return
        shift = sum(ell[i][k] * x[i] for i in range(k + 1, n))
        for value in integer_interval(-shift, remaining / dia[k]):
            term = dia[k] * (F(value) + shift) ** 2
            if term <= remaining:
                x[k] = value
                rec(k - 1, used + term)
        x[k] = 0

    rec(n - 1, F(0))
    return count


# Bourbaki-type simple-root basis.  The trivalent vertex has arm lengths
# 1, 2 and 4; its determinant is one, as checked below.
C_E8 = [
    [2, 0, -1, 0, 0, 0, 0, 0],
    [0, 2, 0, -1, 0, 0, 0, 0],
    [-1, 0, 2, -1, 0, 0, 0, 0],
    [0, -1, -1, 2, -1, 0, 0, 0],
    [0, 0, 0, -1, 2, -1, 0, 0],
    [0, 0, 0, 0, -1, 2, -1, 0],
    [0, 0, 0, 0, 0, -1, 2, -1],
    [0, 0, 0, 0, 0, 0, -1, 2],
]


def main():
    print("EXACT CERTIFICATE: sqrt(3) E8 GLUE COVERING RADIUS")
    print("arithmetic = integers and fractions only")
    assert C_E8 == [list(row) for row in zip(*C_E8)]
    assert bareiss_det(C_E8) == 1
    ldl_lower(C_E8)
    print("det(E8) =", bareiss_det(C_E8))

    best = {}
    shell_counts = Counter()

    def visit(x, value):
        assert value.denominator == 1
        q = value.numerator
        shell_counts[q] += 1
        residue = tuple(t % 3 for t in x)
        if residue not in best or q < best[residue]:
            best[residue] = q

    point_count = enumerate_vectors(C_E8, 8, visit)
    assert point_count == sum(shell_counts.values())
    assert shell_counts == Counter({0: 1, 2: 240, 4: 2160, 6: 6720, 8: 17520})
    assert len(best) == 3 ** 8 == 6561
    assert max(best.values()) == 8

    distribution = Counter(best.values())
    # Pin the entire finite certificate more strongly than only its maximum.
    expected_distribution = Counter({0: 1, 2: 240, 4: 2160, 6: 2240, 8: 1920})
    assert distribution == expected_distribution

    radius_squared = F(max(best.values()), 3)
    determinant_l = bareiss_det([[3 * x for x in row] for row in C_E8])
    assert determinant_l == 3 ** 8 == 6561
    assert radius_squared == F(8, 3)
    schur_lower_bound = F(6) - radius_squared
    determinant_lower_bound = determinant_l * schur_lower_bound
    assert schur_lower_bound == F(10, 3)
    assert determinant_lower_bound == 21870

    canonical_table = "\n".join(
        f"{','.join(map(str, residue))}:{best[residue]}"
        for residue in sorted(best)
    ).encode("ascii")
    table_sha = sha256(canonical_table).hexdigest()

    print("vectors q_E8 <= 8 =", point_count)
    print("theta shells =", sorted(shell_counts.items()))
    print("covered residues modulo 3 =", len(best))
    print("class-minimum distribution =", sorted(distribution.items()))
    print("canonical class-minimum table sha256 =", table_sha)
    print("rho(sqrt(3) E8)^2 =", radius_squared)
    print("det(sqrt(3) E8) =", determinant_l)
    print("rank-9 Schur lower bound =", schur_lower_bound)
    print("rank-9 determinant lower bound =", determinant_lower_bound)
    print("SQRT3_E8_COVERING_RADIUS_EXACT_OK")


if __name__ == "__main__":
    main()
