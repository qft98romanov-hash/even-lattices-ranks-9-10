#!/usr/bin/env python3
"""Static exact audit of the regenerated saturated flag through rank six.

This verifier checks every one of the 3699 saved raw extensions, every saved
raw-to-class unimodular map, all determinant windows/congruences, minimum six,
the inherited parent block, and the shortest-dual-normal condition.  It is
independent of representative ordering and uses no floating-point decision.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from exact_lattice import determinant, enumerate_vectors, ldl
from extend_flag import normal_is_dual_shortest


HERE = Path(__file__).resolve().parent
TRANSCRIPT = HERE / "verify_lower_flag_chain_exact.transcript"
MANIFEST = HERE / "lower_flag_chain_exact.sha256"

STEPS = (
    ("rank1_seed.json", "rank2_exact_classes_regen.json", 27, 39, 4, {0, 3}, 7, 5),
    ("rank2_exact_classes_regen.json", "rank3_exact_classes_regen.json", 108, 178, 2, {0}, 52, 14),
    ("rank3_exact_classes_regen.json", "rank4_exact_classes_regen.json", 324, 633, 4, {0, 1}, 279, 47),
    ("rank4_exact_classes_regen.json", "rank5_isometry_classes_regen.json", 972, 1894, 2, {0}, 1456, 118),
    ("rank5_isometry_classes_regen.json", "rank6_isometry_classes_regen.json", 2187, 4647, 4, {0, 3}, 1905, 138),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def congruence(x, gram):
    return multiply(transpose(x), multiply(gram, x))


def main() -> None:
    lines = [
        "EXACT STATIC AUDIT OF REGENERATED LOWER FLAG",
        "ARITHMETIC integer+rational; floating-point decisions 0",
    ]
    all_inputs: set[Path] = {Path(__file__).resolve(), HERE / "exact_lattice.py", HERE / "extend_flag.py"}
    total_raw = 0
    counts = [1]

    for parent_name, child_name, low, high, modulus, residues, raw_expected, class_expected in STEPS:
        parent_path = HERE / parent_name
        child_path = HERE / child_name
        raw_path = child_path.with_suffix(child_path.suffix + ".raw")
        all_inputs.update((parent_path, child_path, raw_path))

        parent_data = json.loads(parent_path.read_text(encoding="utf-8"))
        child_data = json.loads(child_path.read_text(encoding="utf-8"))
        raw_data = json.loads(raw_path.read_text(encoding="utf-8"))
        parents = parent_data["representatives"]
        reps = child_data["representatives"]
        raw = raw_data["representatives"]

        assert child_data["determinant_window"] == [low, high]
        assert child_data["determinant_modulus"] == modulus
        assert set(child_data["determinant_residues"]) == residues
        assert child_data["parent_count"] == len(parents)
        assert child_data["raw_count"] == len(raw) == raw_expected
        assert child_data["class_count"] == len(reps) == class_expected
        classes = child_data["raw_to_class"]
        maps = child_data["isometry_maps"]
        assert len(classes) == len(maps) == len(raw)
        assert Counter(classes) == Counter({i: n for i, n in enumerate(child_data["class_multiplicities"])})
        assert set(classes) == set(range(len(reps)))

        cursor = 0
        stats = child_data["parent_stats"]
        assert len(stats) == len(parents)
        for parent, parent_stats in zip(parents, stats):
            assert parent_stats["parent_det"] == determinant(parent)
            stop = cursor + parent_stats["raw_children"]
            for child in raw[cursor:stop]:
                rank = len(child)
                assert rank == len(parent) + 1
                assert child == transpose(child)
                assert all(isinstance(value, int) for row in child for value in row)
                assert all(child[i][i] % 2 == 0 for i in range(rank))
                assert [row[:-1] for row in child[:-1]] == parent
                ldl(child)
                assert not enumerate_vectors(child, 5, include_zero=False)
                d_parent = determinant(parent)
                d_child = determinant(child)
                assert low <= d_child <= high and d_child % modulus in residues
                assert normal_is_dual_shortest(child, Fraction(d_child, d_parent))
            cursor = stop
        assert cursor == len(raw)

        for form, class_index, x in zip(raw, classes, maps):
            rep = reps[class_index]
            assert abs(determinant(x)) == 1
            assert congruence(x, rep) == form

        total_raw += len(raw)
        counts.append(len(reps))
        lines.append(
            f"RANK {len(reps[0])} RAW {len(raw)} CLASSES {len(reps)} "
            f"WINDOW [{low},{high}] MAPS {len(maps)} PASS"
        )

    assert total_raw == 3699
    assert counts == [1, 5, 14, 47, 118, 138]
    lines.extend(
        [
            "TOTAL_RAW 3699",
            "CLASS_COUNTS 1,5,14,47,118,138",
            "ALL_LOWER_FLAG_RAW_FORMS_AND_GL_MAPS_EXACT_OK",
        ]
    )
    text = "\n".join(lines) + "\n"
    print(text, end="")
    TRANSCRIPT.write_text(text, encoding="utf-8")
    all_inputs.add(TRANSCRIPT)
    MANIFEST.write_text(
        "\n".join(
            f"{sha256(path)}  {path.name}" for path in sorted(all_inputs, key=lambda p: p.name)
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
