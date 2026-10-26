#!/usr/bin/env python3
"""Exact certificates for the new rank-7 top-down branches.

There is deliberately no floating-point arithmetic in this file.  Vector
enumeration uses an exact U^T D U decomposition over Fraction.  If vectors
of the dual quadratic form are enumerated through B and their fingerprints
cover all det(G) elements of G^{-1} Z^n / Z^n, the stored minimum in every
class is the true class minimum: a missing vector has norm > B, whereas
each class already has a representative of norm <= B.

The script verifies the following statements.

* L = 4 E7^* has determinant 8192, minimum 6 and discrete glue radius
  7/2.  Hence every one-vector extension of minimum 6 has determinant at
  least 20480, outside the rank-8 window ending at 15908.
* Four genuine non-E6 rank-7 stages have determinants
  7722, 8208, 9018, 9342.  Their shortest dual vectors all give a
  rank-6 kernel of determinant 2835.  Their exact glue radii are
  93/22, 297/76, 1377/334, 1449/346, respectively.
* Only the determinant-7722 stage has an extension in the rank-8 window;
  the two opposite glue classes give determinant 13689.  The resulting
  lattice is explicitly isometric to the previously known J_13689.
* J_13689 has glue radius 10/3, hence its next determinant is at least
  36504 > 21868.  Thus all four displayed descendants are closed for the
  rank-9 search.
"""

from fractions import Fraction
from math import gcd, isqrt, lcm


def bareiss_det(a):
    """Exact determinant of an integer matrix."""
    m = [list(map(int, row)) for row in a]
    n = len(m)
    if n == 0:
        return 1
    old = 1
    sign = 1
    for k in range(n - 1):
        if m[k][k] == 0:
            p = next((i for i in range(k + 1, n) if m[i][k]), None)
            if p is None:
                return 0
            m[k], m[p] = m[p], m[k]
            sign = -sign
        pivot = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (
                    m[i][j] * pivot - m[i][k] * m[k][j]
                ) // old
        old = pivot
    return sign * m[-1][-1]


def inverse_fraction(a):
    n = len(a)
    m = [
        [Fraction(a[i][j]) for j in range(n)]
        + [Fraction(int(i == j)) for j in range(n)]
        for i in range(n)
    ]
    for j in range(n):
        p = next(i for i in range(j, n) if m[i][j])
        m[j], m[p] = m[p], m[j]
        pivot = m[j][j]
        m[j] = [x / pivot for x in m[j]]
        for i in range(n):
            if i != j and m[i][j]:
                q = m[i][j]
                m[i] = [m[i][k] - q * m[j][k] for k in range(2 * n)]
    return [row[n:] for row in m]


def ldl_upper(q):
    """Return U,d with q = U^T diag(d) U and U upper unitriangular."""
    n = len(q)
    u = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    d = [Fraction(0) for _ in range(n)]
    for i in range(n):
        d[i] = Fraction(q[i][i]) - sum(
            d[k] * u[k][i] * u[k][i] for k in range(i)
        )
        if d[i] <= 0:
            raise AssertionError("matrix is not positive definite")
        for j in range(i + 1, n):
            u[i][j] = (
                Fraction(q[i][j])
                - sum(d[k] * u[k][i] * u[k][j] for k in range(i))
            ) / d[i]
    return u, d


def ceil_div(a, b):
    assert b > 0
    return -((-a) // b)


def exact_interval(center, radius_squared):
    """Integers x satisfying (x+center)^2 <= radius_squared."""
    if radius_squared < 0:
        return range(0)
    center = Fraction(center)
    radius_squared = Fraction(radius_squared)
    a, b = center.numerator, center.denominator
    # y = b*x+a is integral and y^2*q <= p*b^2.
    p, q = radius_squared.numerator, radius_squared.denominator
    bound = isqrt((p * b * b) // q)
    lo = ceil_div(-bound - a, b)
    hi = (bound - a) // b
    return range(lo, hi + 1)


def quadratic_value(q, z):
    n = len(q)
    return sum(
        Fraction(z[i]) * Fraction(q[i][j]) * z[j]
        for i in range(n)
        for j in range(n)
    )


def enumerate_vectors(q, bound, visit):
    """Enumerate exactly all z in Z^n with z^T q z <= bound."""
    u, d = ldl_upper(q)
    n = len(q)
    z = [0] * n
    count = 0

    def rec(i, used):
        nonlocal count
        if i < 0:
            value = quadratic_value(q, z)
            assert value <= bound
            count += 1
            visit(tuple(z), value)
            return
        center = sum(u[i][j] * z[j] for j in range(i + 1, n))
        remaining = Fraction(bound) - used
        for x in exact_interval(center, remaining / d[i]):
            z[i] = x
            term = d[i] * (Fraction(x) + center) ** 2
            rec(i - 1, used + term)

    rec(n - 1, Fraction(0))
    return count


def matrix_mul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b)))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def border(g, cross, last):
    n = len(g)
    return [g[i] + [cross[i]] for i in range(n)] + [list(cross) + [last]]


def adjugate(g):
    determinant = bareiss_det(g)
    gi = inverse_fraction(g)
    adj = []
    for row in gi:
        new_row = []
        for x in row:
            y = determinant * x
            assert y.denominator == 1
            new_row.append(y.numerator)
        adj.append(new_row)
    return determinant, adj


def assert_even_positive_minimum_six(g):
    assert g == transpose(g)
    assert all(g[i][i] % 2 == 0 for i in range(len(g)))
    ldl_upper(g)  # exact positive definiteness
    seen_nonzero = []

    def visit(z, value):
        if any(z):
            seen_nonzero.append((z, value))

    enumerate_vectors(g, 5, visit)
    assert not seen_nonzero
    # Every displayed Gram matrix has a diagonal entry 6.
    assert min(g[i][i] for i in range(len(g))) == 6


def shortest_dual_numerator(g, expected):
    """For det D, verify min(G^{-1}) = expected/D."""
    determinant, adj = adjugate(g)
    values = []

    def visit(z, value):
        if any(z):
            values.append(value)

    enumerate_vectors(adj, expected, visit)
    assert values and min(values) == expected
    return Fraction(expected, determinant)


def coset_minima(g, bound_numerator):
    """Exact minima of every class of G^{-1}Z^n/Z^n.

    The dual norm is qnum/det(G).  ``bound_numerator`` is the integral
    numerator through which the dual enumeration is performed.
    """
    determinant, adj = adjugate(g)
    n = len(g)
    best = {}
    witness = {}

    def visit(z, value):
        assert value.denominator == 1
        qnum = value.numerator
        fp = tuple(
            sum(adj[i][j] * z[j] for j in range(n)) % determinant
            for i in range(n)
        )
        if fp not in best or qnum < best[fp]:
            best[fp] = qnum
            witness[fp] = z

    point_count = enumerate_vectors(adj, bound_numerator, visit)
    assert len(best) == determinant, (len(best), determinant)
    radius = Fraction(max(best.values()), determinant)
    return radius, best, witness, point_count


def fingerprint(g, z):
    determinant, adj = adjugate(g)
    return tuple(
        sum(adj[i][j] * z[j] for j in range(len(g))) % determinant
        for i in range(len(g))
    )


def class_order(c, modulus):
    ans = 1
    for x in c:
        ans = lcm(ans, modulus // gcd(modulus, x))
    return ans


def allowed_one_vector_extensions(g, best, witness, upper=15908):
    """All even min-6 one-vector extensions in the determinant window."""
    determinant = bareiss_det(g)
    radius = Fraction(max(best.values()), determinant)
    answer = []
    for c, qnum in best.items():
        mu = Fraction(qnum, determinant)
        # The new basis vector itself has even norm >= 6.  The determinant
        # upper bound and mu <= radius give a finite exact list.
        largest_last = int(Fraction(upper, determinant) + radius)
        for last in range(6, largest_last + 1, 2):
            s = Fraction(last) - mu
            new_det = determinant * s
            if s <= 0 or new_det.denominator != 1:
                continue
            new_det = new_det.numerator
            if not (6564 <= new_det <= upper):
                continue
            if new_det % 4 not in (0, 1):
                continue
            h = class_order(c, determinant)
            # The least nonzero layer whose class is zero is m=h.  Its
            # minimum is h^2*s, and it is not represented by the centered
            # nonzero residue range below.  Check it explicitly so this
            # routine is correct without an application-specific lower
            # bound on s.
            if h * h * s < 6:
                continue
            ok = True
            # For m outside this centered residue range, replace m by its
            # representative r with |r| <= h/2.  The class minimum is
            # unchanged up to sign and m^2 >= r^2.  For r=0, the separately
            # checked layer h has the least norm among nonzero multiples.
            for m in range(1, h // 2 + 1):
                mc = tuple((m * x) % determinant for x in c)
                layer = m * m * s + Fraction(best[mc], determinant)
                if layer < 6:
                    ok = False
                    break
            if ok:
                answer.append(
                    (new_det, c, mu, s, last, witness[c], h)
                )
    return answer


# E7 Cartan matrix (determinant 2), with branch at node 4.
C_E7 = [
    [2, 0, -1, 0, 0, 0, 0],
    [0, 2, 0, -1, 0, 0, 0],
    [-1, 0, 2, -1, 0, 0, 0],
    [0, -1, -1, 2, -1, 0, 0],
    [0, 0, 0, -1, 2, -1, 0],
    [0, 0, 0, 0, -1, 2, -1],
    [0, 0, 0, 0, 0, -1, 2],
]


def four_e7_dual_gram():
    ci = inverse_fraction(C_E7)
    g = []
    for row in ci:
        new_row = []
        for x in row:
            y = 4 * x
            assert y.denominator == 1
            new_row.append(y.numerator)
        g.append(new_row)
    return g


# A convenient Gram matrix for sqrt(3) E6.
E6 = [
    [6, -3, -3, -3, -3, -3],
    [-3, 6, 3, 3, 3, 3],
    [-3, 3, 6, 0, 3, 0],
    [-3, 3, 0, 6, 3, 3],
    [-3, 3, 3, 3, 6, 3],
    [-3, 3, 0, 3, 3, 6],
]

H6318 = border(E6, [2, -3, -2, -3, -3, -3], 6)


def mutated_h6318(i, j, delta):
    g = [row[:] for row in H6318]
    g[i][j] += delta
    g[j][i] += delta
    return g


DESCENDANTS = {
    7722: mutated_h6318(3, 1, -2),
    8208: mutated_h6318(3, 1, -1),
    9018: mutated_h6318(3, 0, +1),
    9342: mutated_h6318(2, 1, -2),
}

EXPECTED_RADII = {
    7722: Fraction(93, 22),
    8208: Fraction(297, 76),
    9018: Fraction(1377, 334),
    9342: Fraction(1449, 346),
}


def main():
    print("[1] L = 4 E7^*")
    g8192 = four_e7_dual_gram()
    assert bareiss_det(g8192) == 8192
    assert_even_positive_minimum_six(g8192)
    rho, best, _, points = coset_minima(
        g8192, int(8192 * Fraction(7, 2))
    )
    assert rho == Fraction(7, 2)
    floor = 8192 * (6 - rho)
    assert floor == 20480 > 15908
    print(f"    det=8192, rho_glue^2={rho}, points={points}, floor={floor}")

    print("[2] Four rank-7 descendants with d6=2835")
    saved = {}
    for determinant, g in DESCENDANTS.items():
        assert bareiss_det(g) == determinant
        assert_even_positive_minimum_six(g)
        dual_min = shortest_dual_numerator(g, 2835)
        assert dual_min == Fraction(2835, determinant)
        expected_rho = EXPECTED_RADII[determinant]
        bound = determinant * expected_rho
        assert bound.denominator == 1
        rho, best, witness, points = coset_minima(g, bound.numerator)
        assert rho == expected_rho
        glue_floor = determinant * (6 - rho)
        assert glue_floor.denominator == 1
        saved[determinant] = (g, best, witness)
        print(
            f"    det={determinant}, dual_min={dual_min}, "
            f"rho_glue^2={rho}, points={points}, floor={glue_floor}"
        )
        if determinant != 7722:
            assert glue_floor > 15908

    print("[3] Exact extension list for det 7722")
    g7722, best7722, witness7722 = saved[7722]
    extensions = allowed_one_vector_extensions(
        g7722, best7722, witness7722
    )
    assert len(extensions) == 2
    assert {x[0] for x in extensions} == {13689}
    assert {x[2] for x in extensions} == {Fraction(93, 22)}
    assert {x[3] for x in extensions} == {Fraction(39, 22)}

    # This assertion is intentionally explicit.  The earlier version of the
    # certificate counted two admissible classes but only *reported* that
    # they were opposite.  Fingerprints are elements of
    #     adj(G) Z^7 / det(G) Z^7  ~=  G^{-1} Z^7 / Z^7,
    # so coordinatewise negation modulo det(G) is the exact group inverse.
    d7722 = bareiss_det(g7722)
    c_plus, c_minus = extensions[0][1], extensions[1][1]
    assert c_plus != c_minus
    assert all((x + y) % d7722 == 0 for x, y in zip(c_plus, c_minus))

    # Also certify directly that the two corresponding rank-eight Gram
    # matrices are GL_8(Z)-isometric.  If b_+, b_- are their pairing columns,
    # opposite fingerprints imply k=G^{-1}(b_+ + b_-) is integral.  Replacing
    # the new vector v by -v+k gives the other extension.
    b_plus, b_minus = extensions[0][5], extensions[1][5]
    last_plus, last_minus = extensions[0][4], extensions[1][4]
    assert last_plus == last_minus
    g7722_inverse = inverse_fraction(g7722)
    k_fraction = [
        sum(
            g7722_inverse[i][j] * (b_plus[j] + b_minus[j])
            for j in range(7)
        )
        for i in range(7)
    ]
    assert all(x.denominator == 1 for x in k_fraction)
    k = [x.numerator for x in k_fraction]
    opposite_change = [
        [int(i == j) for j in range(8)]
        for i in range(8)
    ]
    for i in range(7):
        opposite_change[i][7] = k[i]
    opposite_change[7][7] = -1
    extension_plus = border(g7722, b_plus, last_plus)
    extension_minus = border(g7722, b_minus, last_minus)
    assert bareiss_det(opposite_change) == -1
    assert (
        matrix_mul(
            transpose(opposite_change),
            matrix_mul(extension_plus, opposite_change),
        )
        == extension_minus
    )
    assert bareiss_det(extension_plus) == bareiss_det(extension_minus) == 13689
    print(
        "    OPPOSITE_CLASS_ASSERT: c_plus+c_minus=0 in A_L; "
        "det(T)=-1 and T^T J_plus T=J_minus"
    )
    print("    the only determinant is 13689")

    print("[4] Explicit merger with the old J_13689")
    new_cross = [1, 0, 2, 0, 0, 0, -3]
    c = fingerprint(g7722, new_cross)
    assert best7722[c] == 7722 * Fraction(93, 22)
    assert any(x[1] == c for x in extensions)
    new_j = border(g7722, new_cross, 6)
    old_j = border(H6318, [1, 2, 2, 0, 0, 0, -3], 6)
    assert bareiss_det(new_j) == bareiss_det(old_j) == 13689
    assert_even_positive_minimum_six(new_j)
    assert_even_positive_minimum_six(old_j)

    u = [
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, -1, -1],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, -1, 0, 0, -1, 0],
    ]
    assert bareiss_det(u) == -1
    assert matrix_mul(matrix_mul(u, old_j), transpose(u)) == new_j
    print("    det(U)=-1 and U J_old U^T = J_new")

    print("[5] Exact glue closure of J_13689")
    rho_j, _, _, points_j = coset_minima(
        old_j, int(13689 * Fraction(10, 3))
    )
    assert rho_j == Fraction(10, 3)
    rank9_floor = 13689 * (6 - rho_j)
    assert rank9_floor == 36504 > 21868
    print(
        f"    rho_glue^2={rho_j}, points={points_j}, "
        f"rank-9 floor={rank9_floor}"
    )
    print("ALL EXACT CHECKS PASSED")


if __name__ == "__main__":
    main()
