#!/usr/bin/env python3
"""Exact certificate for the rank-9 branch containing sqrt(3) E7.

The program proves, using only integer/rational arithmetic, that every
rank-eight even integral one-vector extension J of sqrt(3) E7 with

    min(J) >= 6,       6564 <= det(J) <= 15908

is isometric to one of four displayed Gram matrices.  It then computes the
exact glue covering radius of each of the four lattices and proves that every
rank-nine integral one-vector extension K of minimum at least 6 satisfies

    det(K) >= 21870.

There is deliberately no floating-point arithmetic.  Short-vector
enumeration is an exact Fincke--Pohst recursion based on a rational LDL^T
decomposition.  Thus both endpoint decisions and enumeration completeness
are independently checkable from this single file (Python standard library
only).
"""

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import isqrt


def det_bareiss(matrix):
    """Exact determinant of an integer matrix."""
    a = [row[:] for row in matrix]
    n = len(a)
    old = 1
    sign = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next(i for i in range(k + 1, n) if a[i][k] != 0)
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * p - a[i][k] * a[k][j]) // old
        old = p
    return sign * a[-1][-1]


def inverse_fraction(matrix):
    """Exact inverse by Gauss--Jordan elimination over Q."""
    n = len(matrix)
    a = [
        [F(matrix[i][j]) for j in range(n)]
        + [F(int(i == j)) for j in range(n)]
        for i in range(n)
    ]
    for j in range(n):
        pivot = next(i for i in range(j, n) if a[i][j] != 0)
        a[j], a[pivot] = a[pivot], a[j]
        p = a[j][j]
        a[j] = [x / p for x in a[j]]
        for i in range(n):
            if i != j and a[i][j] != 0:
                p = a[i][j]
                a[i] = [a[i][k] - p * a[j][k] for k in range(2 * n)]
    return [row[n:] for row in a]


def ldlt(matrix):
    """Exact A=L D L^T, with L unit lower triangular."""
    n = len(matrix)
    a = [[F(x) for x in row] for row in matrix]
    lower = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    diagonal = [F(0) for _ in range(n)]
    for j in range(n):
        diagonal[j] = a[j][j] - sum(
            lower[j][k] * lower[j][k] * diagonal[k] for k in range(j)
        )
        assert diagonal[j] > 0, "matrix is not positive definite"
        for i in range(j + 1, n):
            lower[i][j] = (
                a[i][j]
                - sum(
                    lower[i][k] * lower[j][k] * diagonal[k]
                    for k in range(j)
                )
            ) / diagonal[j]
    # An exact reconstruction check makes the decomposition part of the
    # certificate rather than a trusted numerical preprocessing step.
    for i in range(n):
        for j in range(n):
            reconstructed = sum(
                lower[i][k] * diagonal[k] * lower[j][k]
                for k in range(min(i, j) + 1)
            )
            assert reconstructed == a[i][j]
    return lower, diagonal


def floor_fraction(x):
    return x.numerator // x.denominator


def ceil_fraction(x):
    return -floor_fraction(-x)


def ceil_sqrt_fraction(x):
    """Exact ceiling of sqrt(x), x >= 0 rational."""
    assert x >= 0
    k = isqrt(x.numerator // x.denominator)
    if F(k * k) < x:
        k += 1
    assert F((k - 1) * (k - 1)) < x <= F(k * k) if k else x == 0
    return k


def enumerate_short(matrix, bound, visit):
    """Visit every z in Z^n with z^T matrix z <= bound, exactly.

    If matrix=L D L^T, then

      z^T matrix z = sum_i D_i (z_i + sum_{j>i} L_{j,i} z_j)^2.

    At recursion level i all z_j, j>i, are fixed.  Candidate endpoints are
    obtained from a rational centre and an exact integer ceiling of a rational
    square root, followed by the exact quadratic test.  The initially used
    interval is a (possibly one-integer-too-large) superset, never a subset.
    """
    bound = F(bound)
    lower, diagonal = ldlt(matrix)
    n = len(matrix)
    z = [0] * n
    count = 0

    def recurse(i, remaining):
        nonlocal count
        if i < 0:
            count += 1
            visit(tuple(z), bound - remaining)
            return
        tail = sum(lower[j][i] * z[j] for j in range(i + 1, n))
        radius_squared = remaining / diagonal[i]
        radius_ceiling = ceil_sqrt_fraction(radius_squared)
        centre = -tail
        lo = floor_fraction(centre) - radius_ceiling
        hi = ceil_fraction(centre) + radius_ceiling
        for value in range(lo, hi + 1):
            term = diagonal[i] * (F(value) + tail) ** 2
            if term <= remaining:
                z[i] = value
                recurse(i - 1, remaining - term)

    recurse(n - 1, bound)
    return count


def discriminant_data(gram, search_bound):
    """Return exact minima and witnesses in every class of L*/L."""
    determinant = det_bareiss(gram)
    inverse = inverse_fraction(gram)
    adjugate = [
        [int(determinant * inverse[i][j]) for j in range(len(gram))]
        for i in range(len(gram))
    ]
    assert all(
        F(adjugate[i][j], determinant) == inverse[i][j]
        for i in range(len(gram))
        for j in range(len(gram))
    )

    # The dual vector with pairing column z is G^{-1}z.  Its norm numerator
    # is z^T adj(G) z, and its class is adj(G)z modulo det(G).
    def fingerprint(z):
        return tuple(
            sum(adjugate[i][j] * z[j] for j in range(len(gram))) % determinant
            for i in range(len(gram))
        )

    minima = {}
    witnesses = {}

    def visit(z, numerator):
        # enumerate_short runs on adj(G); divide the recorded norm by det(G).
        c = fingerprint(z)
        if c not in minima or numerator < minima[c]:
            minima[c] = numerator
            witnesses[c] = z

    point_count = enumerate_short(adjugate, F(search_bound) * determinant, visit)
    assert len(minima) == determinant, (
        "the chosen search bound does not cover all discriminant classes",
        len(minima),
        determinant,
    )
    # Once every class has a representative within the searched ball, the
    # recorded minima are exact: every hypothetical shorter representative
    # lies in the same exhaustively enumerated ball.
    minima = {c: q / determinant for c, q in minima.items()}
    return determinant, adjugate, fingerprint, minima, witnesses, point_count


def quadratic(gram, z):
    return sum(z[i] * gram[i][j] * z[j] for i in range(len(z)) for j in range(len(z)))


def minimum_at_most_six(gram):
    values = []
    enumerate_short(gram, 6, lambda z, q: values.append((z, q)) if any(z) else None)
    return min(q for _, q in values), sum(q == 6 for _, q in values)


# This is 3 times an E7 root Gram matrix (the basis used in the working
# computation).  Its determinant is 2*3^7=4374 and its minimum is 6.
H = [
    [6, -3, -3, -3, -3, -3, -3],
    [-3, 6, 3, 3, 3, 3, 3],
    [-3, 3, 6, 0, 3, 0, 0],
    [-3, 3, 0, 6, 3, 3, 3],
    [-3, 3, 3, 3, 6, 3, 3],
    [-3, 3, 0, 3, 3, 6, 3],
    [-3, 3, 0, 3, 3, 3, 6],
]


EXPECTED = [
    ("J12393", [1, -3, 0, -3, -3, -3, -3], 6, 12393, F(58, 17), F(7, 2)),
    ("J14580", [2, -3, -1, -3, -3, -3, -3], 6, 14580, F(9, 2), F(9, 2)),
    ("J15309a", [0, 2, 2, -1, -1, -1, -1], 6, 15309, F(32, 7), F(5)),
    ("J15309b", [0, -3, 0, -3, -3, -3, -3], 8, 15309, F(68, 21), F(7, 2)),
]


def extend(gram, cross, last):
    return [gram[i] + [cross[i]] for i in range(len(gram))] + [cross[:] + [last]]


def main():
    print("EXACT CERTIFICATE: sqrt(3) E7 BRANCH")
    print("arithmetic = integers and fractions only")
    print("det(H) =", det_bareiss(H))
    h_min, h_kissing = minimum_at_most_six(H)
    assert h_min == 6
    print("min(H) =", h_min, "; oriented minimal vectors =", h_kissing)

    # Radius 9/2 is necessary: the unique deepest discriminant class has
    # minimum 9/2.  Exact enumeration finds every one of the 4374 classes.
    d_h, _, fingerprint, mu, witness, point_count = discriminant_data(H, F(9, 2))
    assert d_h == 4374
    assert max(mu.values()) == F(9, 2)
    print("dual enumeration for H: points =", point_count, "; classes =", len(mu))
    print("glue-radius(H) =", max(mu.values()))
    print("coset-minimum distribution:")
    print(" ", sorted(Counter(mu.values()).items()))

    # Simple root reflections act on a pairing column z by
    # z'_j=z_j-z_i C_ij, where C=H/3.  They generate W(E7); adding -1 is
    # harmless (and in fact redundant).  These exact permutations are used
    # only to identify isometric extension matrices, never to omit a class.
    cartan = [[x // 3 for x in row] for row in H]

    def reflected(z, i):
        return tuple(z[j] - z[i] * cartan[i][j] for j in range(7))

    generators = [lambda z, i=i: reflected(z, i) for i in range(7)]
    generators.append(lambda z: tuple(-x for x in z))
    unseen = set(mu)
    orbits = []
    orbit_index = {}
    while unseen:
        seed = next(iter(unseen))
        orbit = {seed}
        stack = [seed]
        while stack:
            c = stack.pop()
            z = witness[c]
            for action in generators:
                image = fingerprint(action(z))
                assert mu[image] == mu[c]
                if image not in orbit:
                    orbit.add(image)
                    stack.append(image)
        index = len(orbits)
        for c in orbit:
            orbit_index[c] = index
        unseen -= orbit
        orbits.append(orbit)
    assert len(orbits) == 12
    print("W(E7)-orbit data (size, coset minimum):")
    print(" ", sorted((len(o), mu[next(iter(o))]) for o in orbits))

    # Exhaust all possible saturated one-vector extensions in the determinant
    # window.  For c of order h and orthogonal square s, the least norm in the
    # m-th layer is m^2 s + mu(m c).  Checking 1<=m<=h is sufficient: for
    # m>=h the tested inequality h^2 s>=6 makes all later layers automatic.
    zero = fingerprint((0,) * 7)

    def multiple(c, m):
        return fingerprint(tuple(m * x for x in witness[c]))

    def order(c):
        for h in range(1, d_h + 1):
            if multiple(c, h) == zero:
                return h
        raise AssertionError("class order not found")

    allowed = []
    for c, q in mu.items():
        h = order(c)
        q_mod_2 = q % 2
        # The determinant bound itself implies s<4, so t=1,...,4 in
        # s=2t-q(c) is more than sufficient.
        for t in range(1, 5):
            s = 2 * t - q_mod_2
            determinant = d_h * s
            if not (6564 <= determinant <= 15908):
                continue
            assert determinant.denominator == 1
            layers = [(m, m * m * s + mu[multiple(c, m)]) for m in range(1, h + 1)]
            if all(norm >= 6 for _, norm in layers):
                last = q + s
                assert last.denominator == 1 and int(last) % 2 == 0
                allowed.append(
                    (int(determinant), orbit_index[c], c, h, q, s, int(last), layers)
                )

    print("allowed labelled classes =", len(allowed))
    print("by determinant =", sorted(Counter(x[0] for x in allowed).items()))
    print("by (determinant, order) =", sorted(Counter((x[0], x[3]) for x in allowed).items()))

    expected_type_keys = set()
    matrices = []
    for name, cross, last, expected_det, expected_rho, search_bound in EXPECTED:
        c = fingerprint(tuple(cross))
        match = [x for x in allowed if x[0] == expected_det and x[1] == orbit_index[c]]
        assert match, (name, "expected orbit was not found")
        expected_type_keys.add((expected_det, orbit_index[c], match[0][5]))
        gram = extend(H, cross, last)
        assert det_bareiss(gram) == expected_det
        assert quadratic(gram, (0,) * 7 + (1,)) == last
        j_min, j_kissing = minimum_at_most_six(gram)
        assert j_min == 6
        matrices.append((name, gram, expected_det, expected_rho, search_bound, j_kissing))

    actual_type_keys = {(x[0], x[1], x[5]) for x in allowed}
    assert actual_type_keys == expected_type_keys
    assert len(actual_type_keys) == 4
    print("number of isometry types =", len(actual_type_keys))

    global_lower = None
    transcript = []
    for name, gram, determinant, expected_rho, search_bound, kissing in matrices:
        d, _, _, minima, _, points = discriminant_data(gram, search_bound)
        assert d == determinant
        rho = max(minima.values())
        assert rho == expected_rho
        lower = determinant * (6 - rho)
        assert lower.denominator == 1
        global_lower = int(lower) if global_lower is None else min(global_lower, int(lower))
        item = (name, determinant, kissing, points, rho, int(lower))
        transcript.append(item)
        print(
            name,
            ": det =", determinant,
            "; oriented minimal vectors =", kissing,
            "; dual points =", points,
            "; classes =", len(minima),
            "; glue-radius =", rho,
            "; rank-9 determinant lower bound =", int(lower),
        )

    assert global_lower == 21870
    assert all(item[-1] >= 21870 for item in transcript)
    print("CONCLUSION: every rank-9 continuation in this branch has det >= 21870")
    print("therefore no candidate with det < 21870 exists in the sqrt(3) E7 branch")

    # A compact deterministic digest makes it easy to compare independent
    # runs without treating the digest itself as mathematical evidence.
    digest_material = repr(
        (
            sorted(Counter(mu.values()).items()),
            sorted((len(o), mu[next(iter(o))]) for o in orbits),
            sorted(Counter((x[0], x[3]) for x in allowed).items()),
            transcript,
        )
    ).encode()
    print("transcript-sha256 =", sha256(digest_material).hexdigest())


if __name__ == "__main__":
    main()
