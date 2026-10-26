#!/usr/bin/env python3
"""Independent small exact checks for the 2026-09-10 rank-nine audit.

No archived module is imported.  This is a transparent arithmetic check,
not a replacement for the large exhaustive determinant-window enumeration.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json


def inverse_and_det(matrix):
    n = len(matrix)
    a = [[F(x) for x in row] + [F(i == j) for j in range(n)]
         for i, row in enumerate(matrix)]
    determinant = F(1)
    for j in range(n):
        k = next(i for i in range(j, n) if a[i][j])
        if j != k:
            a[j], a[k] = a[k], a[j]
            determinant = -determinant
        pivot = a[j][j]
        determinant *= pivot
        a[j] = [v / pivot for v in a[j]]
        for i in range(n):
            if i != j:
                multiplier = a[i][j]
                a[i] = [u - multiplier * v for u, v in zip(a[i], a[j])]
    inv = [row[n:] for row in a]
    assert all(sum(matrix[i][k] * inv[k][j] for k in range(n)) == (i == j)
               for i in range(n) for j in range(n))
    return inv, determinant


def qform(g, x):
    return sum(x[i] * g[i][j] * x[j]
               for i in range(len(x)) for j in range(len(x)))


def floor_root(rational, degree):
    value = F(rational)
    left, right = 0, 1
    while right ** degree <= value:
        right *= 2
    while right - left > 1:
        middle = (left + right) // 2
        if middle ** degree <= value:
            left = middle
        else:
            right = middle
    assert left ** degree <= value < (left + 1) ** degree
    return left


def allowed_det(d, rank):
    if rank % 2:
        return d % 2 == 0
    return d % 4 in {0, (-1) ** (rank // 2) % 4}


def main():
    powers = {1: F(1), 2: F(4, 3), 3: F(2), 4: F(4),
              5: F(8), 6: F(64, 3), 7: F(64), 8: F(256)}
    upper = {9: 21868}
    # (2^(8/7)*D^(8/9))^63 = 2^72*D^56.
    raw = floor_root(2 ** 72 * upper[9] ** 56, 63)
    upper[8] = raw
    while not allowed_det(upper[8], 8):
        upper[8] -= 1
    raw_upper = {8: raw}
    for rank in range(8, 1, -1):
        raw = floor_root(powers[rank] * upper[rank] ** (rank - 1), rank)
        raw_upper[rank - 1] = raw
        upper[rank - 1] = raw
        while not allowed_det(upper[rank - 1], rank - 1):
            upper[rank - 1] -= 1
    assert [upper[i] for i in range(1, 9)] == [6, 39, 178, 633, 1894, 4647, 9492, 15908]
    lower = {r: F(6 ** r) / powers[r] for r in range(1, 9)}
    assert [lower[i] for i in range(1, 9)] == [6, 27, 108, 324, 972, 2187, 4374, 6561]
    print("HERMITE_WINDOW_ARITHMETIC_PASS")
    print("unrounded_integer_floors", json.dumps(raw_upper, sort_keys=True))
    print("congruence_adjusted_upper", json.dumps(upper, sort_keys=True))
    pairs = [(2187, 4374), (2187, 6318), (2835, 7722),
             (4096, 8192), (3240, 8100), (3267, 7986)]
    print("lifting_bounds", [str(F(3*d7*d7, 4*d6)) for d6, d7 in pairs])

    c = [
        [2,-1,-1,-1,-1,-1,-1,1],
        [-1,2,1,1,1,1,1,0],
        [-1,1,2,0,1,0,0,-1],
        [-1,1,0,2,1,1,1,0],
        [-1,1,1,1,2,1,1,-1],
        [-1,1,0,1,1,2,1,0],
        [-1,1,0,1,1,1,2,0],
        [1,0,-1,0,-1,0,0,2],
    ]
    ci, det = inverse_and_det(c)
    assert det == 1
    for r in range(1, 9):
        _, minor = inverse_and_det([row[:r] for row in c[:r]])
        assert minor > 0
    diagonal = [ci[i][i] for i in range(8)]
    assert diagonal == [4, 2, 4, 2, 4, 2, 2, 2]
    p = [-2, 1, 3, -1, 1, 0, 1, -1]
    w = [sum(ci[i][j] * p[j] for j in range(8)) for i in range(8)]
    assert w == [-1, -1, 2, -1, 0, 0, 1, 1]
    assert qform(c, w) == 8
    # Every possible root has coordinate square <= 2*(C^-1)_ii,
    # hence absolute coordinate <= 2. Impose its residue modulo 3.
    choices = [tuple(z for z in range(-2, 3) if (z - w[i]) % 3 == 0)
               for i in range(8)]
    distribution = Counter(qform(c, r) for r in product(*choices))
    assert sum(distribution.values()) == 64
    assert min(distribution) == 8
    print("K9_ROOT_RESIDUE_64_TEST_PASS")
    print("64_point_norm_distribution", sorted(distribution.items()))
    # q_C(w+3x) = 8 mod 6, so the sole possible smaller positive norm
    # is 2. It has just been excluded. The class minimum is exactly 8.
    mu, s = F(8, 3), F(10, 3)
    assert 3 ** 8 * s == 21870 and mu + s == 6
    assert 4*s > 6
    print("K9_SCHUR_MINIMUM_SIX_AND_DETERMINANT_21870_PASS")

    # Counterexample to using only centered residues without m=ord(a).
    parent = [[6, 0, 0], [0, 6, 0], [0, 0, 8]]
    cross = [3, 3, 4]
    bordered = [row + [cross[i]] for i, row in enumerate(parent)] + [cross + [6]]
    assert qform(bordered, [-1, -1, -1, 2]) == 4
    assert F(1, 4) * (6 + 6 + 8) == 5
    assert 1 + 5 == 6 and 2*2*1 < 6
    print("CENTERED_RESIDUE_SHORTCUT_COUNTEREXAMPLE_VERIFIED")
    print("ALL_THEORY_AND_64_POINT_SHARPNESS_CHECKS_PASS")


if __name__ == "__main__":
    main()
