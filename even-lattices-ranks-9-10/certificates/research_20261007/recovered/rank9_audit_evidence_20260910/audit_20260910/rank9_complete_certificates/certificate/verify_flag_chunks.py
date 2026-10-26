#!/usr/bin/env python3
"""Independent exact audit of merged rank-6 to rank-7 flag output.

By default this verifies the immutable saved output.  ``--rerun`` additionally
re-executes the complete discriminant-class generator for every parent and
compares the exact ordered Gram-matrix list, thereby certifying generator
completeness as well as output validity.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

from exact_lattice import determinant, enumerate_vectors, ldl
from extend_flag import extend_parent, inverse, normal_is_dual_shortest


def matrix_minimum_at_least_six(g):
    # Completeness of the exact ellipsoid enumeration proves there is no
    # nonzero vector of norm <=5.  An extension basis vector has norm an even
    # diagonal n >=6, and every generated form has an inherited norm-6 vector.
    points = enumerate_vectors(g, 5, include_zero=False)
    assert not points
    assert min(g[i][i] for i in range(len(g))) == 6


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("merged", type=Path)
    parser.add_argument("--rerun", action="store_true")
    args = parser.parse_args()

    frozen = json.loads(args.input.read_text(encoding="utf-8"))
    merged = json.loads(args.merged.read_text(encoding="utf-8"))
    parents = frozen["representatives"]

    assert merged["format"] == "exact-saturated-flag-merged-v1"
    assert merged["input_sha256"] == sha256(args.input.read_bytes()).hexdigest()
    assert merged["parent_total"] == len(parents) == 138
    assert merged["determinant_window"] == [4374, 9492]
    assert merged["determinant_modulus"] == 2
    assert merged["determinant_residues"] == [0]
    children = merged["children"]
    indices = merged["child_parent_indices"]
    assert len(children) == len(indices) == merged["raw_count"]

    grouped = defaultdict(list)
    dual_boundary_count = 0
    determinant_pairs = Counter()
    for serial, (child, parent_index) in enumerate(zip(children, indices)):
        parent = parents[parent_index]
        n = len(parent)
        assert len(child) == n + 1 == 7
        assert child == [list(row) for row in zip(*child)]
        assert [row[:n] for row in child[:n]] == parent
        assert all(child[i][i] % 2 == 0 for i in range(n + 1))
        ldl(child)  # exact positive definiteness
        matrix_minimum_at_least_six(child)
        d6 = determinant(parent)
        d7 = determinant(child)
        assert 4374 <= d7 <= 9492 and d7 % 2 == 0
        s = Fraction(d7, d6)
        assert normal_is_dual_shortest(child, s)
        # Count the exact boundary shell realizing lambda_1(L7*)=1/s.
        inv_child = inverse(child)
        boundary = enumerate_vectors(inv_child, Fraction(1, s), include_zero=False)
        assert boundary and min(q for _, q in boundary) == Fraction(1, s)
        dual_boundary_count += sum(q == Fraction(1, s) for _, q in boundary)
        determinant_pairs[(d6, d7)] += 1
        grouped[parent_index].append(child)

    assert Counter(map(determinant, children)) == {
        int(k): v for k, v in merged["determinant_counts"].items()
    }
    assert len(merged["parent_stats"]) == len(parents)
    for i, stats in enumerate(merged["parent_stats"]):
        assert stats["parent_index"] == i
        assert stats["raw_children"] == len(grouped[i])

    if args.rerun:
        for i, parent in enumerate(parents):
            regenerated, stats = extend_parent(parent, 4374, 9492, 2, {0})
            assert regenerated == grouped[i], (i, len(regenerated), len(grouped[i]))
            assert stats["parent_det"] == merged["parent_stats"][i]["parent_det"]
            print("RERUN_PARENT", i, "RAW", len(regenerated), flush=True)

    active = sorted((i, len(grouped[i])) for i in grouped if grouped[i])
    print("EXACT STATIC AUDIT OF RANK6->RANK7 FLAG")
    print("input sha256 =", sha256(args.input.read_bytes()).hexdigest())
    print("merged sha256 =", sha256(args.merged.read_bytes()).hexdigest())
    print("parents =", len(parents))
    print("raw children =", len(children))
    print("active parents =", active)
    print("distinct (d6,d7) pairs =", len(determinant_pairs))
    print("distinct d7 values =", len({d7 for _, d7 in determinant_pairs}))
    print("dual boundary vectors =", dual_boundary_count)
    print("generator rerun =", args.rerun)
    print("RANK6_TO_RANK7_CHUNKS_EXACT_OK")


if __name__ == "__main__":
    main()
