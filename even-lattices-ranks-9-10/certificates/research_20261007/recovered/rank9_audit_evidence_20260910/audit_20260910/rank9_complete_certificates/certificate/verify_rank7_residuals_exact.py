"""Autonomous exact closure of the residual d7=7986 and d7=8100 branches.

The two rank-seven representatives are selected directly from the complete
merged saturated-flag output.  The companion survivor-linkage certificate
proves that every raw survivor with the same (d6,d7) pair is isometric to the
selected representative.

For d7=8100, the exact discriminant covering radius is 15/4, forcing
det(L8) >= 18225.  For d7=7986, exact extension enumeration gives two
opposite presentations of one rank-eight class of determinant 14641.  Its
exact discriminant covering radius is 36/11, forcing det(L9) >= 39930.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Sequence

from exact_lattice import determinant, enumerate_vectors, isometry, ldl
from extend_flag import (
    class_key,
    discriminant_minima,
    dot,
    extend_parent,
    fractional_part,
    inverse,
    matvec,
    normal_is_dual_shortest,
)


HERE = Path(__file__).resolve().parent
FROZEN = HERE / "rank6_isometry_classes.json"
MERGED = HERE / "rank7_merged.json"
LINKAGE = HERE / "rank7_survivor_linkage_exact.json"
REPORT = HERE / "rank7_residuals_exact.json"
TRANSCRIPT = HERE / "verify_rank7_residuals_exact.transcript"
MANIFEST = HERE / "rank7_residuals_sha256.txt"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def transpose(a: Sequence[Sequence[int]]):
    return [list(row) for row in zip(*a)]


def multiply(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def congruence(x, target):
    return multiply(transpose(x), multiply(target, x))


def minimum_at_least_six(g):
    ldl(g)
    assert not enumerate_vectors(g, 5, include_zero=False)
    assert min(g[i][i] for i in range(len(g))) == 6


def coset_order(key) -> int:
    order = 1
    for value in key:
        denominator = value.denominator
        order = order * denominator // gcd(order, denominator)
    return order


def exact_radius(g):
    inv, minima, witnesses, search_bound = discriminant_minima(g)
    assert len(minima) == determinant(g)
    rho = max(minima.values())
    # Recount exactly through the covering radius itself.  This is a useful
    # presentation-independent diagnostic (and is not an assumption in the
    # completeness proof of the discriminant table).
    point_count = len(enumerate_vectors(inv, rho, include_zero=True))
    assert set(minima) == set(witnesses)
    return rho, point_count, search_bound


def selected_residual(merged, parents, d6, d7):
    rows = []
    for serial, (child, parent_index) in enumerate(
        zip(merged["children"], merged["child_parent_indices"])
    ):
        if determinant(parents[parent_index]) == d6 and determinant(child) == d7:
            rows.append((serial, parent_index, child))
    assert rows
    return rows


def main() -> None:
    lines = []

    def emit(message):
        print(message, flush=True)
        lines.append(message)

    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    merged = json.loads(MERGED.read_text(encoding="utf-8"))
    linkage = json.loads(LINKAGE.read_text(encoding="utf-8"))
    parents = frozen["representatives"]
    assert merged["input_sha256"] == sha256(FROZEN)
    assert linkage["merged_sha256"] == sha256(MERGED)
    assert linkage["frozen_sha256"] == sha256(FROZEN)
    assert linkage["result"] == "PASS"

    rows7986 = selected_residual(merged, parents, 3267, 7986)
    rows8100 = selected_residual(merged, parents, 3240, 8100)
    assert len(rows7986) == 6 and len(rows8100) == 1
    g7986 = rows7986[0][2]
    g8100 = rows8100[0][2]
    minimum_at_least_six(g7986)
    minimum_at_least_six(g8100)

    emit("EXACT RESIDUAL RANK-7 CERTIFICATE")
    emit(f"FROZEN_SHA256 {sha256(FROZEN)}")
    emit(f"MERGED_SHA256 {sha256(MERGED)}")
    emit(f"LINKAGE_SHA256 {sha256(LINKAGE)}")
    emit("FLOATING_POINT_DECISIONS 0")

    rho8100, points8100, bound8100 = exact_radius(g8100)
    assert rho8100 == Fraction(15, 4)
    d8_floor8100 = 8100 * (6 - rho8100)
    assert d8_floor8100 == 18225 > 15908
    emit(
        f"D7_8100 rho={rho8100} points={points8100} "
        f"search_bound={bound8100} rank8_floor={d8_floor8100} CLOSED"
    )

    rho7986, points7986, bound7986 = exact_radius(g7986)
    assert rho7986 == Fraction(25, 6)
    d8_floor7986 = 7986 * (6 - rho7986)
    assert d8_floor7986 == 14641
    emit(
        f"D7_7986 rho={rho7986} points={points7986} "
        f"search_bound={bound7986} rank8_floor={d8_floor7986}"
    )

    children8, extension_stats = extend_parent(g7986, 6564, 15908, 4, {0, 1})
    assert len(children8) == 2
    assert [determinant(g) for g in children8] == [14641, 14641]
    for child in children8:
        minimum_at_least_six(child)
        assert normal_is_dual_shortest(child, Fraction(14641, 7986))

    inv7986 = inverse(g7986)
    keys = []
    extension_data = []
    target8 = children8[0]
    maps = []
    for child in children8:
        p = tuple(row[-1] for row in child[:-1])
        diagonal = child[-1][-1]
        mu = dot(p, matvec(inv7986, p))
        s = Fraction(diagonal) - mu
        key = class_key(inv7986, p)
        keys.append(key)
        assert mu == Fraction(25, 6)
        assert s == Fraction(11, 6)
        assert coset_order(key) == 6
        x = isometry(child, target8)
        assert x is not None
        assert abs(determinant(x)) == 1
        assert congruence(x, target8) == child
        maps.append(x)
        extension_data.append(
            {
                "cross": list(p),
                "diagonal": diagonal,
                "mu": str(mu),
                "s": str(s),
                "coset_key": [str(value) for value in key],
                "coset_order": coset_order(key),
                "X_to_target8": x,
            }
        )
    assert all(fractional_part(a + b) == 0 for a, b in zip(keys[0], keys[1]))
    emit("D7_7986_EXTENSIONS raw=2 opposite_cosets=PASS classes=1 det8=14641")

    rho14641, points14641, bound14641 = exact_radius(target8)
    assert rho14641 == Fraction(36, 11)
    d9_floor = 14641 * (6 - rho14641)
    assert d9_floor == 39930
    emit(
        f"D8_14641 rho={rho14641} points={points14641} "
        f"search_bound={bound14641} rank9_floor={d9_floor} CLOSED"
    )
    emit("ALL_RESIDUAL_RANK7_CERTIFICATES_OK")

    report = {
        "certificate": "exact residual rank-7 closure",
        "frozen_sha256": sha256(FROZEN),
        "merged_sha256": sha256(MERGED),
        "linkage_sha256": sha256(LINKAGE),
        "d8100": {
            "target_gram": g8100,
            "rho": str(rho8100),
            "enumerated_points": points8100,
            "search_bound": str(bound8100),
            "rank8_determinant_floor": int(d8_floor8100),
        },
        "d7986": {
            "target_gram": g7986,
            "rho": str(rho7986),
            "enumerated_points": points7986,
            "search_bound": str(bound7986),
            "rank8_determinant_floor": int(d8_floor7986),
            "extension_stats": extension_stats,
            "extensions": extension_data,
            "opposite_cosets": True,
            "rank8_class_count": 1,
        },
        "d14641": {
            "target_gram": target8,
            "rho": str(rho14641),
            "enumerated_points": points14641,
            "search_bound": str(bound14641),
            "rank9_determinant_floor": int(d9_floor),
        },
        "result": "PASS",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    TRANSCRIPT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    paths = [FROZEN, MERGED, LINKAGE, Path(__file__).resolve(), REPORT,
             TRANSCRIPT, HERE / "exact_lattice.py", HERE / "extend_flag.py"]
    MANIFEST.write_text(
        "\n".join(
            f"{sha256(path)}  {path.name}" for path in sorted(paths, key=lambda p: p.name)
        ) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
