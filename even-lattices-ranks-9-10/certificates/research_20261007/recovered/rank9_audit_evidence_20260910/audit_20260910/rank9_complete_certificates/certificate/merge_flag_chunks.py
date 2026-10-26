#!/usr/bin/env python3
"""Merge disjoint exact saturated-flag chunks without deduplication."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from hashlib import sha256
from pathlib import Path

from exact_lattice import determinant


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("chunks", type=Path, nargs="+")
    args = parser.parse_args()

    pairs = [
        (p, json.loads(p.read_text(encoding="utf-8"))) for p in args.chunks
    ]
    pairs.sort(key=lambda pair: pair[1]["parent_range"])
    chunks = [chunk for _, chunk in pairs]
    common = (
        chunks[0]["input_sha256"], chunks[0]["parent_total"],
        chunks[0]["determinant_window"], chunks[0]["determinant_modulus"],
        chunks[0]["determinant_residues"],
    )
    cursor = 0
    children = []
    child_parent_indices = []
    parent_stats = []
    chunk_manifest = []
    for path, chunk in pairs:
        assert chunk["complete"] is True
        assert (
            chunk["input_sha256"], chunk["parent_total"],
            chunk["determinant_window"], chunk["determinant_modulus"],
            chunk["determinant_residues"],
        ) == common
        start, stop = chunk["parent_range"]
        assert start == cursor
        assert chunk["completed_parents"] == list(range(start, stop))
        cursor = stop
        assert len(chunk["children"]) == chunk["raw_count"]
        children.extend(chunk["children"])
        child_parent_indices.extend(chunk["child_parent_indices"])
        parent_stats.extend(chunk["parent_stats"])
        chunk_manifest.append({
            "file": path.name,
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "range": [start, stop],
            "raw_count": chunk["raw_count"],
        })
    assert cursor == common[1]

    payload = {
        "format": "exact-saturated-flag-merged-v1",
        "input_sha256": common[0],
        "parent_total": common[1],
        "determinant_window": common[2],
        "determinant_modulus": common[3],
        "determinant_residues": common[4],
        "chunks": chunk_manifest,
        "raw_count": len(children),
        "determinant_counts": dict(sorted(Counter(
            determinant(g) for g in children
        ).items())),
        "children": children,
        "child_parent_indices": child_parent_indices,
        "parent_stats": parent_stats,
    }
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("PARENTS", cursor)
    print("RAW", len(children))
    print("DET_COUNTS", payload["determinant_counts"])
    print("OUTPUT_SHA256", sha256(args.output.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
