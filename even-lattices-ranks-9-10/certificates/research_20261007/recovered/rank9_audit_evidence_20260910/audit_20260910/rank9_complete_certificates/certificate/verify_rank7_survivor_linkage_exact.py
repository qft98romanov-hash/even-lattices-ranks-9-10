"""Exact GL_7(Z) linkage of all rank-7 lifting survivors.

From the merged rank-6 -> rank-7 saturated-flag output, retain precisely the
children for which the necessary next-lift inequality does not already force

    det(L_8) >= 3 det(L_7)^2 / (4 det(L_6)) > 15908.

There must be 96 such raw forms in six determinant-pair groups.  Every form
is linked by an explicit unimodular integer matrix X to the displayed target
of its group, in the convention X^T TARGET X = RAW.  Thus the 96 raw forms
represent exactly six isometry classes.

No input file is modified.  Exact vector/isometry routines use no floating
point decisions.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Sequence

from exact_lattice import determinant, enumerate_vectors, isometry, ldl
from extend_flag import inverse


HERE = Path(__file__).resolve().parent
FROZEN = HERE / "rank6_isometry_classes.json"
MERGED = HERE / "rank7_merged.json"
REPORT = HERE / "rank7_survivor_linkage_exact.json"
TRANSCRIPT = HERE / "verify_rank7_survivor_linkage_exact.transcript"
MANIFEST = HERE / "rank7_survivor_linkage_sha256.txt"

L8_UPPER = 15908

EXPECTED = {
    (2187, 4374): (2, "sqrt3_E7"),
    (2187, 6318): (54, "H6318"),
    (2835, 7722): (32, "D7722"),
    (4096, 8192): (1, "four_E7_dual"),
    (3240, 8100): (1, "R8100"),
    (3267, 7986): (6, "R7986"),
}


E6 = [
    [6, -3, -3, -3, -3, -3],
    [-3, 6, 3, 3, 3, 3],
    [-3, 3, 6, 0, 3, 0],
    [-3, 3, 0, 6, 3, 3],
    [-3, 3, 3, 3, 6, 3],
    [-3, 3, 0, 3, 3, 6],
]

SQRT3_E7 = [
    [6, -3, -3, -3, -3, -3, -3],
    [-3, 6, 3, 3, 3, 3, 3],
    [-3, 3, 6, 0, 3, 0, 0],
    [-3, 3, 0, 6, 3, 3, 3],
    [-3, 3, 3, 3, 6, 3, 3],
    [-3, 3, 0, 3, 3, 6, 3],
    [-3, 3, 0, 3, 3, 3, 6],
]

C_E7 = [
    [2, 0, -1, 0, 0, 0, 0],
    [0, 2, 0, -1, 0, 0, 0],
    [-1, 0, 2, -1, 0, 0, 0],
    [0, -1, -1, 2, -1, 0, 0],
    [0, 0, 0, -1, 2, -1, 0],
    [0, 0, 0, 0, -1, 2, -1],
    [0, 0, 0, 0, 0, -1, 2],
]


def border(g, cross, last):
    return [list(g[i]) + [int(cross[i])] for i in range(len(g))] + [
        list(map(int, cross)) + [int(last)]
    ]


H6318 = border(E6, [2, -3, -2, -3, -3, -3], 6)
D7722 = [row[:] for row in H6318]
D7722[3][1] -= 2
D7722[1][3] -= 2


def four_e7_dual():
    result = []
    for row in inverse(C_E7):
        converted = []
        for value in row:
            value *= 4
            assert value.denominator == 1
            converted.append(value.numerator)
        result.append(converted)
    return result


STANDARD_TARGETS = {
    (2187, 4374): SQRT3_E7,
    (2187, 6318): H6318,
    (2835, 7722): D7722,
    (4096, 8192): four_e7_dual(),
}


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


def main() -> None:
    lines = []

    def emit(message):
        print(message, flush=True)
        lines.append(message)

    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    merged = json.loads(MERGED.read_text(encoding="utf-8"))
    parents = frozen["representatives"]
    children = merged["children"]
    parent_indices = merged["child_parent_indices"]
    assert merged["format"] == "exact-saturated-flag-merged-v1"
    assert merged["input_sha256"] == sha256(FROZEN)
    assert len(parents) == 138
    assert len(children) == len(parent_indices) == merged["raw_count"] == 2235

    groups = defaultdict(list)
    excluded = 0
    for serial, (raw, parent_index) in enumerate(zip(children, parent_indices)):
        d6 = determinant(parents[parent_index])
        d7 = determinant(raw)
        lower = Fraction(3 * d7 * d7, 4 * d6)
        if lower > L8_UPPER:
            excluded += 1
        else:
            groups[(d6, d7)].append((serial, parent_index, raw, lower))
    assert excluded == 2139
    assert set(groups) == set(EXPECTED)
    assert {pair: len(rows) for pair, rows in groups.items()} == {
        pair: count_label[0] for pair, count_label in EXPECTED.items()
    }
    assert sum(map(len, groups.values())) == 96

    emit("EXACT RANK-7 LIFTING-SURVIVOR LINKAGE")
    emit(f"FROZEN_SHA256 {sha256(FROZEN)}")
    emit(f"MERGED_SHA256 {sha256(MERGED)}")
    emit("RAW_TOTAL 2235 LIFTING_EXCLUDED 2139 SURVIVORS 96 GROUPS 6")
    emit("CONVENTION X^T * TARGET * X = RAW")
    emit("FLOATING_POINT_DECISIONS 0")

    report_groups = []
    total_maps = 0
    for pair in EXPECTED:
        expected_count, label = EXPECTED[pair]
        rows = groups[pair]
        target = STANDARD_TARGETS.get(pair, rows[0][2])
        assert determinant(target) == pair[1]
        minimum_at_least_six(target)
        maps = []
        for serial, parent_index, raw, lower in rows:
            x = isometry(raw, target)
            assert x is not None, (pair, serial)
            assert abs(determinant(x)) == 1, (pair, serial)
            assert congruence(x, target) == raw, (pair, serial)
            maps.append(
                {
                    "merged_serial": serial,
                    "parent_index": parent_index,
                    "lifting_lower_bound": str(lower),
                    "X": x,
                }
            )
        assert len(maps) == expected_count
        total_maps += len(maps)
        report_groups.append(
            {
                "d6": pair[0],
                "d7": pair[1],
                "label": label,
                "raw_count": len(rows),
                "target_gram": target,
                "maps": maps,
            }
        )
        emit(
            f"PAIR d6={pair[0]} d7={pair[1]} LABEL={label} "
            f"RAW={len(rows)} EXACT_GL7_MAPS={len(maps)} ONE_CLASS PASS"
        )
    assert total_maps == 96
    emit("ALL_96_SURVIVORS_LINKED_TO_6_EXACT_CLASSES")

    report = {
        "certificate": "rank-7 lifting-survivor exact isometry linkage",
        "frozen_sha256": sha256(FROZEN),
        "merged_sha256": sha256(MERGED),
        "lifting_rule": "3*d7^2/(4*d6) <= 15908",
        "raw_total": len(children),
        "lifting_excluded": excluded,
        "survivor_raw_count": total_maps,
        "survivor_class_count": len(report_groups),
        "identity_convention": "X^T * target_gram * X = raw_child",
        "groups": report_groups,
        "result": "PASS",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    TRANSCRIPT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    paths = [FROZEN, MERGED, Path(__file__).resolve(), REPORT, TRANSCRIPT,
             HERE / "exact_lattice.py", HERE / "extend_flag.py"]
    MANIFEST.write_text(
        "\n".join(
            f"{sha256(path)}  {path.name}" for path in sorted(paths, key=lambda p: p.name)
        ) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
