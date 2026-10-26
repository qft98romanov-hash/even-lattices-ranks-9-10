#!/usr/bin/env python3
"""Resume-safe chunk driver for the exact saturated-flag extension engine.

The mathematical work is performed by ``extend_flag.extend_parent``.  This
driver assigns a disjoint interval of parent representatives to one process
and checkpoints after every completed parent.  It never modifies the frozen
input classification.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from hashlib import sha256
from pathlib import Path

from exact_lattice import determinant
from extend_flag import extend_parent


def canonical_json_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def write_checkpoint(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--stop", type=int, required=True)
    parser.add_argument("--low", type=int, default=4374)
    parser.add_argument("--high", type=int, default=9492)
    parser.add_argument("--modulus", type=int, default=2)
    parser.add_argument("--residues", default="0")
    args = parser.parse_args()

    source = json.loads(args.input.read_text(encoding="utf-8"))
    parents = source["representatives"]
    assert 0 <= args.start <= args.stop <= len(parents)
    residues = {int(x) % args.modulus for x in args.residues.split(",")}

    payload = {
        "format": "exact-saturated-flag-chunk-v1",
        "input": args.input.name,
        "input_sha256": canonical_json_sha(args.input),
        "parent_total": len(parents),
        "parent_range": [args.start, args.stop],
        "determinant_window": [args.low, args.high],
        "determinant_modulus": args.modulus,
        "determinant_residues": sorted(residues),
        "completed_parents": [],
        "children": [],
        "child_parent_indices": [],
        "parent_stats": [],
    }

    # A matching existing checkpoint may be resumed.  A mismatching one is
    # rejected instead of silently mixing computations.
    if args.output.exists():
        old = json.loads(args.output.read_text(encoding="utf-8"))
        for key in (
            "format", "input_sha256", "parent_total", "parent_range",
            "determinant_window", "determinant_modulus",
            "determinant_residues",
        ):
            assert old[key] == payload[key], (key, old[key], payload[key])
        payload = old

    completed = set(payload["completed_parents"])
    expected_prefix = list(range(args.start, args.start + len(completed)))
    assert payload["completed_parents"] == expected_prefix

    for parent_index in range(args.start, args.stop):
        if parent_index in completed:
            continue
        parent = parents[parent_index]
        print(
            "PARENT", parent_index, "/", len(parents),
            "rank", len(parent), "det", determinant(parent),
            flush=True,
        )
        children, stats = extend_parent(
            parent, args.low, args.high, args.modulus, residues
        )
        stats["parent_index"] = parent_index
        stats["raw_children"] = len(children)
        payload["children"].extend(children)
        payload["child_parent_indices"].extend([parent_index] * len(children))
        payload["parent_stats"].append(stats)
        payload["completed_parents"].append(parent_index)
        payload["raw_count"] = len(payload["children"])
        payload["determinant_counts"] = dict(sorted(Counter(
            determinant(g) for g in payload["children"]
        ).items()))
        write_checkpoint(args.output, payload)
        print("  RAW_CHILDREN", len(children), "TOTAL", payload["raw_count"], flush=True)

    assert payload["completed_parents"] == list(range(args.start, args.stop))
    assert len(payload["children"]) == len(payload["child_parent_indices"])
    payload["complete"] = True
    payload["raw_count"] = len(payload["children"])
    write_checkpoint(args.output, payload)
    print("CHUNK_COMPLETE", args.start, args.stop, "RAW", payload["raw_count"])
    print("OUTPUT_SHA256", canonical_json_sha(args.output))


if __name__ == "__main__":
    main()
