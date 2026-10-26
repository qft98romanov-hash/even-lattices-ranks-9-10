"""Exact certificate excluding the saturated-flag branch L6 = sqrt(3) E6.

The statement certified here is the following.

Let

    L6 < L7 < L8 < L9

be primitive one-rank extensions of even integral lattices of minimum at
least 6, with L6 isometric to sqrt(3) E6 and with the determinant windows
used in the rank-9 hyperplane/HKZ reduction:

    4374 <= det(L7) <= 9492,
    6564 <= det(L8) <= 15908.

Then det(L9) >= 21870.  In particular this branch cannot improve the
rank-9 section of determinant 21870.

All ellipsoid membership tests use Fraction arithmetic and exact integer
square roots (rank9_exact_ldl.py).  Isometries are certified by explicit
unimodular basis maps (exact_lattice.py).  No floating-point comparison or
external lattice package is used.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from exact_lattice import (  # noqa: E402
    deduplicate_isometry,
    determinant,
    enumerate_vectors as enumerate_lattice_vectors,
    isometry,
)
from rank9_exact_ldl import enumerate_vectors, quadratic_value  # noqa: E402


Matrix = list[list[int]]
Vector = tuple[int, ...]
Fingerprint = tuple[int, ...]


E6: Matrix = [
    [6, -3, -3, -3, -3, -3],
    [-3, 6, 3, 3, 3, 3],
    [-3, 3, 6, 0, 3, 0],
    [-3, 3, 0, 6, 3, 3],
    [-3, 3, 3, 3, 6, 3],
    [-3, 3, 0, 3, 3, 6],
]


E7: Matrix = [
    [6, -3, -3, -3, -3, -3, -3],
    [-3, 6, 3, 3, 3, 3, 3],
    [-3, 3, 6, 0, 3, 0, 0],
    [-3, 3, 0, 6, 3, 3, 3],
    [-3, 3, 3, 3, 6, 3, 3],
    [-3, 3, 0, 3, 3, 6, 3],
    [-3, 3, 0, 3, 3, 3, 6],
]


def extend(g: Matrix, cross: Iterable[int], last: int) -> Matrix:
    cross = list(map(int, cross))
    assert len(cross) == len(g)
    return [list(g[i]) + [cross[i]] for i in range(len(g))] + [cross + [last]]


def inverse_fraction(a: Matrix) -> list[list[Fraction]]:
    n = len(a)
    aug = [
        [Fraction(a[i][j]) for j in range(n)]
        + [Fraction(int(i == j)) for j in range(n)]
        for i in range(n)
    ]
    for j in range(n):
        pivot_row = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[pivot_row] = aug[pivot_row], aug[j]
        pivot = aug[j][j]
        aug[j] = [x / pivot for x in aug[j]]
        for i in range(n):
            if i != j and aug[i][j]:
                multiple = aug[i][j]
                aug[i] = [aug[i][k] - multiple * aug[j][k] for k in range(2 * n)]
    return [row[n:] for row in aug]


def adjugate(a: Matrix) -> tuple[int, Matrix]:
    det = determinant(a)
    inv = inverse_fraction(a)
    adj: Matrix = []
    for row in inv:
        out = []
        for value in row:
            scaled = det * value
            assert scaled.denominator == 1
            out.append(scaled.numerator)
        adj.append(out)
    # Independent exact multiplication check A*adj(A)=det(A) I.
    n = len(a)
    assert all(
        sum(a[i][k] * adj[k][j] for k in range(n)) == det * int(i == j)
        for i in range(n)
        for j in range(n)
    )
    return det, adj


def fingerprint(adj: Matrix, det: int, z: Iterable[int]) -> Fingerprint:
    z = tuple(z)
    return tuple(
        sum(adj[i][j] * z[j] for j in range(len(z))) % det
        for i in range(len(z))
    )


@dataclass
class CosetTable:
    gram: Matrix
    det: int
    adj: Matrix
    minima_num: dict[Fingerprint, int]
    witnesses: dict[Fingerprint, Vector]
    point_count: int
    radius: Fraction
    digest: str

    def fp(self, z: Iterable[int]) -> Fingerprint:
        return fingerprint(self.adj, self.det, z)

    def mu(self, c: Fingerprint) -> Fraction:
        return Fraction(self.minima_num[c], self.det)


def coset_table(gram: Matrix, radius: Fraction) -> CosetTable:
    """Enumerate every dual discriminant class up through ``radius``.

    Once exactly det(G) fingerprints have appeared, the least enumerated
    norm in every fingerprint is its true coset minimum: a hypothetical
    smaller representative would also lie inside the enumerated ellipsoid.
    """

    det, adj = adjugate(gram)
    minima: dict[Fingerprint, int] = {}
    witnesses: dict[Fingerprint, Vector] = {}
    count = 0
    bound = radius * det
    assert bound.denominator == 1
    for z in enumerate_vectors(adj, bound):
        count += 1
        numerator = quadratic_value(adj, z)
        assert numerator.denominator == 1
        numerator = numerator.numerator
        c = fingerprint(adj, det, z)
        if c not in minima or numerator < minima[c]:
            minima[c] = numerator
            witnesses[c] = z
    assert len(minima) == det, (len(minima), det)
    actual_radius = Fraction(max(minima.values()), det)
    assert actual_radius == radius, (actual_radius, radius)

    digest_state = hashlib.sha256()
    for c in sorted(minima):
        digest_state.update(json.dumps([c, minima[c]], separators=(",", ":")).encode())
        digest_state.update(b"\n")
    return CosetTable(
        gram=gram,
        det=det,
        adj=adj,
        minima_num=minima,
        witnesses=witnesses,
        point_count=count,
        radius=actual_radius,
        digest=digest_state.hexdigest(),
    )


@dataclass(frozen=True)
class Extension:
    c: Fingerprint
    witness: Vector
    q: Fraction
    height: Fraction
    last: int
    det: int


def extension_candidates(
    table: CosetTable,
    det_lo: int,
    det_hi: int,
    allowed_residues: set[int],
    modulus: int,
) -> list[Extension]:
    """All even primitive one-vector extensions in a determinant window.

    If a is a discriminant class, use its shortest representative y and an
    orthogonal vector of square s.  Replacing an arbitrary representative by
    y is an integral basis change.  Thus every extension has a presentation

        [[G,z],[z^T,t]],  t even,  s=t-mu(a),  det(new)=det(G)*s.

    The exact layer test is m^2*s+mu(m*a)>=6.  It is enough to inspect m
    while m^2*s<6, since all omitted terms are automatically at least 6.
    """

    answer: list[Extension] = []
    zero = (0,) * len(table.gram)
    assert zero in table.minima_num and table.minima_num[zero] == 0
    for c in sorted(table.minima_num):
        q = table.mu(c)
        z = table.witnesses[c]
        # The determinant windows here force t<=10; 20 is a harmless exact
        # over-bound and is asserted retrospectively below.
        for last in range(2, 22, 2):
            height = Fraction(last) - q
            if height <= 0:
                continue
            new_det = table.det * height
            if new_det.denominator != 1:
                continue
            new_det_int = new_det.numerator
            if not det_lo <= new_det_int <= det_hi:
                continue
            if new_det_int % modulus not in allowed_residues:
                continue
            good = True
            m = 1
            while m * m * height < 6:
                mc = table.fp(m * x for x in z)
                if m * m * height + table.mu(mc) < 6:
                    good = False
                    break
                m += 1
            if good:
                assert last <= 10
                answer.append(
                    Extension(
                        c=c,
                        witness=z,
                        q=q,
                        height=height,
                        last=last,
                        det=new_det_int,
                    )
                )
    return answer


def reflection_covector(gram: Matrix, i: int, z: Vector) -> Vector:
    """Action on covector coordinates of reflection in basis root i."""

    assert gram[i][i] == 6
    assert all(value % 3 == 0 for value in gram[i])
    return tuple(z[j] - z[i] * (gram[i][j] // 3) for j in range(len(z)))


def extension_orbits(
    table: CosetTable,
    extensions: list[Extension],
    *,
    add_central_inversion: bool,
) -> list[set[tuple[Fingerprint, int]]]:
    """Orbits under basis-root reflections (and optionally -I)."""

    by_state = {(x.c, x.last): x for x in extensions}
    assert len(by_state) == len(extensions)
    unseen = set(by_state)
    orbits: list[set[tuple[Fingerprint, int]]] = []
    while unseen:
        seed = next(iter(unseen))
        orbit = {seed}
        stack = [seed]
        while stack:
            c, last = stack.pop()
            z = table.witnesses[c]
            images = [
                reflection_covector(table.gram, i, z)
                for i in range(len(table.gram))
            ]
            if add_central_inversion:
                images.append(tuple(-x for x in z))
            for image in images:
                state = (table.fp(image), last)
                assert state in by_state
                if state not in orbit:
                    orbit.add(state)
                    stack.append(state)
        unseen -= orbit
        orbits.append(orbit)
    return orbits


def gram_of_extension(parent: Matrix, extension: Extension) -> Matrix:
    return extend(parent, extension.witness, extension.last)


def assert_minimum_six(gram: Matrix) -> None:
    # There is a displayed basis vector of norm 6 in every form below.
    assert any(gram[i][i] == 6 for i in range(len(gram)))
    assert not enumerate_lattice_vectors(gram, 5, include_zero=False)


def target_rank8_forms() -> list[tuple[str, Matrix, Fraction, int]]:
    """Five standard representatives, their glue radii and lower bounds."""

    cases = [
        (
            "J12393",
            [2, -3, -2, -3, -3, -3],
            6,
            [1, 0, -1, 0, 0, 0, -3],
            6,
            Fraction(58, 17),
            32076,
        ),
        (
            "J13689",
            [2, -3, -2, -3, -3, -3],
            6,
            [1, 2, 2, 0, 0, 0, -3],
            6,
            Fraction(10, 3),
            36504,
        ),
        (
            "J14580",
            [3, -3, -2, -3, -3, -3],
            6,
            [0, 0, -1, 0, 0, 0, -3],
            6,
            Fraction(9, 2),
            21870,
        ),
        (
            "J15309a",
            [2, -3, -1, -3, -3, -3],
            6,
            [-2, 0, 1, 0, 0, 0, -3],
            6,
            Fraction(32, 7),
            21870,
        ),
        (
            "J15309b",
            [3, -3, -3, -3, -3, -3],
            8,
            [-3, 0, 3, 0, 0, 0, -3],
            6,
            Fraction(68, 21),
            42282,
        ),
    ]
    result = []
    for name, c1, t1, c2, t2, radius, lower in cases:
        h = extend(E6, c1, t1)
        result.append((name, extend(h, c2, t2), radius, lower))
    return result


def main() -> None:
    print("EXACT CERTIFICATE: L6 = sqrt(3) E6 branch")
    assert determinant(E6) == 2187
    assert_minimum_six(E6)

    # Step 1: all L6 -> L7 extensions.  Reflections in the six simple roots
    # generate W(E6), and adjoining -I gives the full Aut(E6) (the diagram
    # involution is -w0).  Hence these are full isometry orbits over E6.
    e6_table = coset_table(E6, Fraction(4))
    e7_extensions = extension_candidates(e6_table, 4374, 9492, {0}, 2)
    assert len(e7_extensions) == 1360
    e7_orbits = extension_orbits(
        e6_table, e7_extensions, add_central_inversion=True
    )
    assert len(e7_orbits) == 8
    e7_orbit_summary = sorted(
        (
            next(iter(orbit))[1],
            next(
                x.det
                for x in e7_extensions
                if (x.c, x.last) == next(iter(orbit))
            ),
            len(orbit),
        )
        for orbit in e7_orbits
    )
    assert e7_orbit_summary == [
        (6, 4374, 2),
        (6, 6318, 54),
        (6, 7290, 144),
        (6, 7776, 432),
        (6, 8748, 240),
        (6, 9234, 54),
        (6, 9234, 432),
        (8, 8748, 2),
    ]

    l7_specs = [
        ("H4374", [3, -3, -3, -3, -3, -3], 6, Fraction(9, 2), 1375),
        ("H6318", [2, -3, -2, -3, -3, -3], 6, Fraction(105, 26), 12),
        ("H7290", [3, -3, -2, -3, -3, -3], 6, Fraction(43, 10), 4),
        ("H7776", [2, -3, -1, -3, -3, -3], 6, Fraction(33, 8), 4),
        ("H8748a", [0, 0, -1, 2, -1, -1], 6, Fraction(17, 4), 4),
        ("H8748b", [3, -3, -3, -3, -3, -3], 8, Fraction(5), 2),
        ("H9234a", [0, 2, 1, -1, 0, 0], 6, Fraction(84, 19), 2),
        ("H9234b", [0, 0, 0, 0, -2, 0], 6, Fraction(177, 38), 2),
    ]
    orbit_index: dict[tuple[Fingerprint, int], int] = {}
    for i, orbit in enumerate(e7_orbits):
        for state in orbit:
            orbit_index[state] = i
    chosen_orbits = []
    l7_forms: dict[str, Matrix] = {}
    for name, cross, last, _radius, _count in l7_specs:
        state = (e6_table.fp(cross), last)
        assert state in orbit_index
        chosen_orbits.append(orbit_index[state])
        form = extend(E6, cross, last)
        assert_minimum_six(form)
        l7_forms[name] = form
    assert len(set(chosen_orbits)) == 8

    # The first representative is sqrt(3) E7.  Record/verify an explicit
    # isometry to a simple-root presentation so that its Weyl group can be
    # used for a four-orbit reduction of the 1375 raw L8 extensions.
    h4374_to_e7 = [
        [0, -1, -1, -1, -1, 0, 1],
        [0, 0, 0, 1, 0, -1, 0],
        [0, -1, -1, -1, -1, 1, 0],
        [0, -1, 0, -1, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, -1, -1, 0, 0],
        [1, -1, -1, -1, -1, 0, 1],
    ]
    # isometry() convention is X^T * target * X = source.
    assert determinant(h4374_to_e7) in (-1, 1)
    assert all(
        sum(
            h4374_to_e7[k][i] * E7[k][ell] * h4374_to_e7[ell][j]
            for k in range(7)
            for ell in range(7)
        )
        == l7_forms["H4374"][i][j]
        for i in range(7)
        for j in range(7)
    )

    # Step 2: enumerate all L7 -> L8 extensions.  The H4374/E7 case is
    # reduced by the full Weyl group; all other cases are small enough that
    # every raw discriminant class is retained before exact isometry dedup.
    rank8_children: list[Matrix] = []
    l7_summaries = []

    e7_table = coset_table(E7, Fraction(9, 2))
    e7_to_8 = extension_candidates(e7_table, 6564, 15908, {0, 1}, 4)
    assert len(e7_to_8) == 1375
    e7_to_8_orbits = extension_orbits(
        e7_table, e7_to_8, add_central_inversion=False
    )
    assert sorted(len(orbit) for orbit in e7_to_8_orbits) == [1, 126, 576, 672]
    e7_ext_by_state = {(x.c, x.last): x for x in e7_to_8}
    for orbit in e7_to_8_orbits:
        rank8_children.append(
            gram_of_extension(E7, e7_ext_by_state[next(iter(orbit))])
        )
    l7_summaries.append(("H4374", len(e7_to_8), len(e7_to_8_orbits)))

    for name, _cross, _last, radius, expected_count in l7_specs[1:]:
        table = coset_table(l7_forms[name], radius)
        candidates = extension_candidates(table, 6564, 15908, {0, 1}, 4)
        assert len(candidates) == expected_count, (name, len(candidates))
        rank8_children.extend(
            gram_of_extension(l7_forms[name], extension)
            for extension in candidates
        )
        l7_summaries.append((name, len(candidates), len(candidates)))

    # 4 E7 orbit representatives plus every raw candidate from the other
    # seven cases.  Exact exhaustive basis imaging collapses them to five
    # isometry classes.  Adding the five named standard forms proves both
    # coverage and pairwise nonisometry of the named list.
    assert len(rank8_children) == 34
    targets = target_rank8_forms()
    target_grams = [gram for _name, gram, _radius, _lower in targets]
    combined = rank8_children + target_grams
    representatives, classes, maps = deduplicate_isometry(combined)
    assert len(representatives) == 5
    assert sorted(determinant(g) for g in representatives) == [
        12393,
        13689,
        14580,
        15309,
        15309,
    ]
    target_classes = classes[-5:]
    assert len(set(target_classes)) == 5
    assert set(classes[:34]) <= set(target_classes)
    for source, rep_index, basis_map in zip(combined, classes, maps):
        assert basis_map is not None
        rep = representatives[rep_index]
        n = len(source)
        assert determinant(basis_map) in (-1, 1)
        assert all(
            sum(
                basis_map[k][i] * rep[k][ell] * basis_map[ell][j]
                for k in range(n)
                for ell in range(n)
            )
            == source[i][j]
            for i in range(n)
            for j in range(n)
        )

    # Step 3: exact glue covering radii of the five rank-8 classes.  For any
    # further one-vector extension, s+mu(a)>=6 gives
    # det(L9)>=det(L8)*(6-rho_glue(L8)^2).
    rank8_summaries = []
    for name, gram, expected_radius, expected_lower in targets:
        assert_minimum_six(gram)
        table = coset_table(gram, expected_radius)
        lower = table.det * (6 - table.radius)
        assert lower.denominator == 1
        assert lower.numerator == expected_lower
        assert lower >= 21870
        rank8_summaries.append(
            {
                "name": name,
                "det": table.det,
                "points": table.point_count,
                "cosets": len(table.minima_num),
                "rho2": str(table.radius),
                "rank9_lower": lower.numerator,
                "sha256": table.digest,
            }
        )

    print("E6_COSETS", e6_table.point_count, len(e6_table.minima_num), e6_table.digest)
    print("L7_ORBITS", e7_orbit_summary)
    print("L7_TO_L8", l7_summaries)
    print("RANK8_CLASSES", [item["name"] for item in rank8_summaries])
    for item in rank8_summaries:
        print("RANK8", json.dumps(item, sort_keys=True))
    print("CONCLUSION det(L9) >= 21870: VERIFIED")


if __name__ == "__main__":
    main()
