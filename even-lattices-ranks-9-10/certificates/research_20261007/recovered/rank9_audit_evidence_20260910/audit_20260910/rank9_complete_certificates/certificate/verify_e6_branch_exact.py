#!/usr/bin/env python3
"""Exact certificate for the rank-9 flag branch containing sqrt(3) E6.

This complements ``verify_e7_branch_exact.py``.  It classifies all admissible
rank-seven children of sqrt(3) E6 in the determinant window 2188..9492, then
all rank-eight children in the window 6564..15908.  Exact integral isometries
reduce the latter to five Gram matrices.  Exact dual-coset enumeration proves
that every rank-nine continuation of minimum at least 6 has determinant at
least 21870.

Only integer/rational arithmetic is used.  The Fincke--Pohst enumerator is the
small independently checkable helper ``../rank9_exact_ldl.py``; it uses an
exact Fraction LDL^T decomposition and exact isqrt endpoints.
"""

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rank9_exact_ldl import enumerate_vectors, quadratic_value  # noqa: E402


def det_bareiss(matrix):
    a = [list(row) for row in matrix]
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


def discriminant_data(gram, search_bound):
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

    def fingerprint(z):
        return tuple(
            sum(adjugate[i][j] * z[j] for j in range(len(gram))) % determinant
            for i in range(len(gram))
        )

    minima = {}
    witnesses = {}
    point_count = 0
    for z in enumerate_vectors(adjugate, F(search_bound) * determinant):
        point_count += 1
        numerator = quadratic_value(adjugate, z)
        c = fingerprint(z)
        if c not in minima or numerator < minima[c]:
            minima[c] = numerator
            witnesses[c] = z
    assert len(minima) == determinant, (len(minima), determinant, search_bound)
    minima = {c: q / determinant for c, q in minima.items()}
    return determinant, fingerprint, minima, witnesses, point_count


def extend(gram, cross, last):
    return [gram[i] + [cross[i]] for i in range(len(gram))] + [cross[:] + [last]]


def dot(gram, x, y):
    return sum(x[i] * gram[i][j] * y[j] for i in range(len(gram)) for j in range(len(gram)))


def minimum_vectors(gram, norm):
    return [z for z in enumerate_vectors(gram, norm) if any(z) and quadratic_value(gram, z) == norm]


def find_isometry(source, target):
    """Find exact U with U source U^T=target and det(U)=+-1.

    Rows of U are selected from the complete exact lists of source vectors of
    the required target diagonal norms.  Pairing tests are exact integers.  A
    returned U is therefore a compact, directly verified isometry witness.
    """
    assert det_bareiss(source) == det_bareiss(target)
    n = len(source)
    pools = {q: minimum_vectors(source, q) for q in set(target[i][i] for i in range(n))}
    rows = []

    def recurse(k):
        if k == n:
            if abs(det_bareiss(rows)) == 1:
                return tuple(tuple(x for x in row) for row in rows)
            return None
        for v in pools[target[k][k]]:
            if all(dot(source, v, rows[j]) == target[k][j] for j in range(k)):
                rows.append(v)
                result = recurse(k + 1)
                if result is not None:
                    return result
                rows.pop()
        return None

    result = recurse(0)
    assert result is not None
    assert abs(det_bareiss(result)) == 1
    assert all(
        dot(source, result[i], result[j]) == target[i][j]
        for i in range(n)
        for j in range(n)
    )
    return result


def classify_one_vector_extensions(gram, search_bound, det_lo, det_hi, t_max=8):
    determinant, fingerprint, minima, witnesses, points = discriminant_data(gram, search_bound)
    zero = fingerprint((0,) * len(gram))

    def multiple(c, m):
        return fingerprint(tuple(m * x for x in witnesses[c]))

    def order(c):
        for h in range(1, determinant + 1):
            if multiple(c, h) == zero:
                return h
        raise AssertionError("class order not found")

    allowed = []
    for c, q in minima.items():
        h = order(c)
        q_mod_2 = q % 2
        for t in range(1, t_max + 1):
            s = 2 * t - q_mod_2
            child_det = determinant * s
            if not (det_lo <= child_det <= det_hi):
                continue
            assert child_det.denominator == 1
            layers = tuple((m, m * m * s + minima[multiple(c, m)]) for m in range(1, h + 1))
            if all(norm >= 6 for _, norm in layers):
                last = q + s
                assert last.denominator == 1 and int(last) % 2 == 0
                cross = list(witnesses[c])
                child = extend(gram, cross, int(last))
                assert det_bareiss(child) == int(child_det)
                allowed.append(
                    {
                        "det": int(child_det),
                        "class": c,
                        "order": h,
                        "q": q,
                        "s": s,
                        "cross": cross,
                        "last": int(last),
                        "layers": layers,
                        "gram": child,
                    }
                )
    return determinant, fingerprint, minima, witnesses, points, allowed


E6 = [
    [6, -3, -3, -3, -3, -3],
    [-3, 6, 3, 3, 3, 3],
    [-3, 3, 6, 0, 3, 0],
    [-3, 3, 0, 6, 3, 3],
    [-3, 3, 3, 3, 6, 3],
    [-3, 3, 0, 3, 3, 6],
]


RANK7 = [
    ("H4374=sqrt(3)E7", [3, -3, -3, -3, -3, -3], 6, 4374, F(9, 2)),
    ("H6318", [2, -3, -2, -3, -3, -3], 6, 6318, F(9, 2)),
    ("H7290", [3, -3, -2, -3, -3, -3], 6, 7290, F(9, 2)),
    ("H7776", [2, -3, -1, -3, -3, -3], 6, 7776, F(9, 2)),
    ("H8748a", [0, 0, -1, 2, -1, -1], 6, 8748, F(9, 2)),
    ("H8748b", [3, -3, -3, -3, -3, -3], 8, 8748, F(5)),
    ("H9234a", [0, 2, 1, -1, 0, 0], 6, 9234, F(9, 2)),
    ("H9234b", [0, 0, 0, 0, -2, 0], 6, 9234, F(5)),
]


# Four targets coincide with those in the sqrt(3)E7 certificate.  J13689 is
# the one genuinely new rank-eight type arising through H6318.
E7 = [
    [6, -3, -3, -3, -3, -3, -3],
    [-3, 6, 3, 3, 3, 3, 3],
    [-3, 3, 6, 0, 3, 0, 0],
    [-3, 3, 0, 6, 3, 3, 3],
    [-3, 3, 3, 3, 6, 3, 3],
    [-3, 3, 0, 3, 3, 6, 3],
    [-3, 3, 0, 3, 3, 3, 6],
]
J12393 = extend(E7, [1, -3, 0, -3, -3, -3, -3], 6)
H6318 = extend(E6, RANK7[1][1], RANK7[1][2])
J13689 = extend(H6318, [1, 2, 2, 0, 0, 0, -3], 6)
J14580 = extend(E7, [2, -3, -1, -3, -3, -3, -3], 6)
J15309a = extend(E7, [0, 2, 2, -1, -1, -1, -1], 6)
J15309b = extend(E7, [0, -3, 0, -3, -3, -3, -3], 8)


RANK8_TARGETS = {
    12393: [("J12393", J12393, F(58, 17), F(7, 2))],
    13689: [("J13689", J13689, F(10, 3), F(7, 2))],
    14580: [("J14580", J14580, F(9, 2), F(9, 2))],
    15309: [
        ("J15309a", J15309a, F(32, 7), F(5)),
        ("J15309b", J15309b, F(68, 21), F(7, 2)),
    ],
}


def main():
    print("EXACT CERTIFICATE: sqrt(3) E6 BRANCH")
    print("arithmetic = integers and fractions only")
    assert det_bareiss(E6) == 2187
    roots_e6 = minimum_vectors(E6, 6)
    assert roots_e6 and all(quadratic_value(E6, z) == 6 for z in roots_e6)
    print("det(sqrt(3)E6) = 2187; oriented minimal vectors =", len(roots_e6))

    # First level: classify rank-seven children modulo the Weyl group W(E6).
    d6, fp6, mu6, wit6, points6, allowed7 = classify_one_vector_extensions(
        E6, 4, 2188, 9492
    )
    assert d6 == 2187 and max(mu6.values()) == 4
    cartan = [[x // 3 for x in row] for row in E6]

    def reflected(z, i):
        return tuple(z[j] - z[i] * cartan[i][j] for j in range(6))

    generators = [lambda z, i=i: reflected(z, i) for i in range(6)]
    generators.append(lambda z: tuple(-x for x in z))
    unseen = set(mu6)
    orbits = []
    orbit_index = {}
    while unseen:
        seed = next(iter(unseen))
        orbit = {seed}
        stack = [seed]
        while stack:
            c = stack.pop()
            z = wit6[c]
            for action in generators:
                image = fp6(action(z))
                assert mu6[image] == mu6[c]
                if image not in orbit:
                    orbit.add(image)
                    stack.append(image)
        index = len(orbits)
        for c in orbit:
            orbit_index[c] = index
        unseen -= orbit
        orbits.append(orbit)
    assert len(orbits) == 12

    expected7_keys = set()
    rank7_grams = []
    for name, cross, last, determinant, search_bound in RANK7:
        c = fp6(tuple(cross))
        matches = [x for x in allowed7 if x["det"] == determinant and orbit_index[x["class"]] == orbit_index[c]]
        assert matches
        expected7_keys.add((determinant, orbit_index[c], matches[0]["s"]))
        gram = extend(E6, cross, last)
        assert det_bareiss(gram) == determinant
        assert minimum_vectors(gram, 6)
        rank7_grams.append((name, gram, search_bound))
    actual7_keys = {(x["det"], orbit_index[x["class"]], x["s"]) for x in allowed7}
    assert actual7_keys == expected7_keys and len(actual7_keys) == 8

    # Do not merely identify H4374 by determinant/root data: certify the
    # claimed isometry with the canonical E7 matrix used by the companion
    # certificate.  In the convention below U^T E7 U = H4374.
    u_e7 = [
        [0, -1, -1, -1, -1, 0, 1],
        [0, 0, 0, 1, 0, -1, 0],
        [0, -1, -1, -1, -1, 1, 0],
        [0, -1, 0, -1, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, -1, -1, 0, 0],
        [1, -1, -1, -1, -1, 0, 1],
    ]
    h4374_from_e6 = rank7_grams[0][1]
    assert abs(det_bareiss(u_e7)) == 1
    assert all(
        sum(
            u_e7[a][i] * E7[a][b] * u_e7[b][j]
            for a in range(7)
            for b in range(7)
        )
        == h4374_from_e6[i][j]
        for i in range(7)
        for j in range(7)
    )
    print("rank-7 dual points =", points6, "; labelled extensions =", len(allowed7))
    print("rank-7 isometry types = 8:", [x[0] for x in RANK7])
    print("rank-7 labelled counts by determinant =", sorted(Counter(x["det"] for x in allowed7).items()))

    # Second level.  H4374 is exactly the E7 subtree certified separately;
    # we nevertheless include its four target types below.  The remaining
    # seven parents contain only 30 labelled admissible classes.  For every
    # one we construct and exactly verify an integral unimodular isometry to
    # one of the five target matrices.
    all_children = []
    per_parent = []
    for name, gram, search_bound in rank7_grams[1:]:
        determinant, _, minima, _, points, children = classify_one_vector_extensions(
            gram, search_bound, 6564, 15908
        )
        all_children.extend((name, x) for x in children)
        per_parent.append(
            (name, determinant, points, max(minima.values()), len(children), Counter(x["det"] for x in children))
        )
    assert len(all_children) == 30
    print("non-E7 rank-8 labelled children =", len(all_children))
    for row in per_parent:
        print(" parent", row)

    isometry_digest_material = []
    type_hits = Counter()
    for parent_name, child in all_children:
        candidates = RANK8_TARGETS[child["det"]]
        # The two determinant-15309 types have different kissing numbers,
        # which is itself exactly enumerated and avoids a failed isometry
        # backtrack.  All other determinant values have a unique target.
        source_kissing = len(minimum_vectors(child["gram"], 6))
        routed = [
            target
            for target in candidates
            if len(minimum_vectors(target[1], 6)) == source_kissing
        ]
        assert len(routed) == 1
        target_name, target_gram, _, _ = routed[0]
        isometry = find_isometry(child["gram"], target_gram)
        type_hits[target_name] += 1
        isometry_digest_material.append((parent_name, child["det"], child["cross"], child["last"], target_name, isometry))

    # Every genuinely new target is hit.  The H4374/E7 subtree supplies
    # J15309b; it need not reappear among the other seven rank-seven parents.
    assert set(type_hits) == {"J12393", "J13689", "J14580", "J15309a"}
    print("exact unimodular isometry targets for the 30 children =", sorted(type_hits.items()))
    print("complete rank-8 type list = J12393, J13689, J14580, J15309a, J15309b")

    # Exact glue radii and the determinant obstruction for rank nine.
    transcript = []
    for determinant in sorted(RANK8_TARGETS):
        for name, gram, expected_rho, search_bound in RANK8_TARGETS[determinant]:
            d, _, minima, _, points = discriminant_data(gram, search_bound)
            assert d == determinant
            rho = max(minima.values())
            assert rho == expected_rho
            lower = determinant * (6 - rho)
            assert lower.denominator == 1
            transcript.append((name, determinant, points, rho, int(lower)))
            print(
                name,
                ": det =", determinant,
                "; dual points =", points,
                "; glue-radius =", rho,
                "; rank-9 determinant lower bound =", int(lower),
            )
    assert min(x[-1] for x in transcript) == 21870
    assert next(x for x in transcript if x[0] == "J13689")[-2:] == (F(10, 3), 36504)
    print("CONCLUSION: every rank-9 continuation in the sqrt(3)E6 branch has det >= 21870")

    digest = sha256(repr((sorted(type_hits.items()), isometry_digest_material, transcript)).encode()).hexdigest()
    print("isometry-and-radius-sha256 =", digest)


if __name__ == "__main__":
    main()
