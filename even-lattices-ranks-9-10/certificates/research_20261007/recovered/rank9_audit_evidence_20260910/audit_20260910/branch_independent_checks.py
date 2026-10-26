"""Independent bounded checks for the 2026-09-10 branch audit.

The archived certificate files are imported without being modified.  Random
small exact ellipsoids are compared with complete Cartesian-product search,
whose coordinate bounds follow from Q^{-1}.  The rank-nine example is checked
using the Leibniz determinant formula and a second archived vector enumerator.
"""
from fractions import Fraction as F
from itertools import product, permutations
from math import isqrt
from pathlib import Path
from random import Random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'rank9_complete_certificates' / 'certificate'))
import rank9_exact_ldl as helper
import exact_lattice as general
from verify_rank9_extremal_example_exact import K9
from verify_e7_branch_exact import H
from verify_e6_branch_exact import E6, H6318, J12393, J13689, J14580, J15309a, J15309b
from verify_rank7_topdown import C_E7, DESCENDANTS

def inverse_q(q):
    n = len(q)
    a = [[F(x) for x in q[i]] + [F(i == j) for j in range(n)] for i in range(n)]
    for i in range(n):
        k = next(k for k in range(i, n) if a[k][i])
        a[i], a[k] = a[k], a[i]
        pivot = a[i][i]
        a[i] = [x / pivot for x in a[i]]
        for j in range(n):
            if j != i:
                scale = a[j][i]
                a[j] = [x - scale * y for x, y in zip(a[j], a[i])]
    return [row[n:] for row in a]

def leibniz_det(q):
    n = len(q)
    result = 0
    for p in permutations(range(n)):
        term = 1
        for i, j in enumerate(p):
            term *= q[i][j]
            if not term:
                break
        if term:
            sign = (-1) ** sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
            result += sign * term
    return result

def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]

def brute(q, b, c):
    qi = inverse_q(q)
    boxes = []
    for i, ci in enumerate(c):
        radius2 = b * qi[i][i]
        radius = isqrt(radius2.numerator // radius2.denominator)
        if radius * radius < radius2:
            radius += 1
        floor = ci.numerator // ci.denominator
        boxes.append(range(floor - radius, floor + radius + 2))
    answer = set()
    for z in product(*boxes):
        centered = [F(a) - v for a, v in zip(z, c)]
        if helper.quadratic_value(q, centered) <= b:
            answer.add(z)
    return answer

def main():
    rng = Random(20260910)
    checks = 0
    for n in range(1, 5):
        for k in range(12):
            a = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
            q = [[F(sum(a[r][i] * a[r][j] for r in range(n)) + (i == j),
                    1 + k % 3) for j in range(n)] for i in range(n)]
            b = F(1 + k % 6, 1 + k % 2)
            c = [F(rng.randint(-3, 3), 1 + k % 3) for _ in range(n)]
            expected = brute(q, b, c)
            actual_list = list(helper.enumerate_vectors(q, b, c))
            assert set(actual_list) == expected
            assert len(actual_list) == len(expected)
            zero_expected = brute(q, b, [F(0)] * n)
            assert {x for x, _ in general.enumerate_vectors(q, b)} == zero_expected
            checks += 1
    # A highly sheared form and exact-boundary off-centre cases.
    for q, b, c in [
        ([[1, 17], [17, 290]], F(6), [F(0), F(0)]),
        ([[2, 1], [1, 2]], F(1, 2), [F(1, 2), F(0)]),
        ([[F(1, 100)]], F(1), [F(-1, 3)]),
    ]:
        actual = list(helper.enumerate_vectors(q, b, c))
        assert set(actual) == brute(q, b, c)
        assert len(actual) == len(set(actual))
        checks += 1
    print('CARTESIAN_ELLIPSOID_COMPARISONS', checks, 'PASS')

    assert leibniz_det(K9) == 21870
    assert all(leibniz_det([row[:i] for row in K9[:i]]) > 0 for i in range(1, 10))
    pts = list(helper.enumerate_vectors(K9, 6))
    norms = [helper.quadratic_value(K9, z) for z in pts if any(z)]
    assert len(norms) == 258 and set(norms) == {F(6)}
    assert set(pts) == {z for z, _ in general.enumerate_vectors(K9, 6)}
    print('K9_LEIBNIZ_DETERMINANT_AND_TWO_ENUMERATORS det=21870 min=6 kissing=258 PASS')

    # Root-reflection matrices on pairing coordinates preserve the dual form.
    for q in (E6, H):
        n = len(q)
        qi = inverse_q(q)
        for i in range(n):
            t = [[F(j == k) for k in range(n)] for j in range(n)]
            for j in range(n):
                t[j][i] -= F(q[i][j], 3)
            assert leibniz_det(t) == -1
            assert multiply(list(zip(*t)), multiply(qi, t)) == qi
    print('E6_E7_REFLECTIONS_EXACT_DUAL_ISOMETRIES PASS')

    # Direct minimum checks remove any reliance on existence-only shell tests.
    named = [('H6318', H6318), ('J12393', J12393), ('J13689', J13689),
             ('J14580', J14580), ('J15309a', J15309a), ('J15309b', J15309b)]
    for name, gram in named:
        assert not any(any(z) for z in helper.enumerate_vectors(gram, 5))
        assert min(gram[i][i] for i in range(len(gram))) == 6
        print('DIRECT_MINIMUM', name, '6 PASS')

    # Check the concrete omitted m=h zero-coset case in the topdown helper.
    radii = {7722: F(93, 22), 8208: F(297, 76),
             9018: F(1377, 334), 9342: F(1449, 346)}
    for d, radius in radii.items():
        assert 4 * (6 - radius) >= 6
    assert F(3 * 7722 ** 2, 4 * 2835) == F(552123, 35)
    assert 13689 < F(552123, 35) <= 15908
    g8192 = [[4 * x for x in row] for row in inverse_q(C_E7)]
    assert leibniz_det(g8192) == 8192
    print('TOPDOWN_ZERO_CLASS_LAYERS_AND_7722_FLAG_BOUND PASS')
    print('ALL_INDEPENDENT_BRANCH_CHECKS_PASS')

if __name__ == '__main__':
    main()
