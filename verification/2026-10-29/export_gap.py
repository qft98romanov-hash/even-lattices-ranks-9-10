#!/usr/bin/env python3
"""Export literal GAP input; no lattice algorithms are executed here.

Run this script, then run ``gap -q -b -T check_orbits.g`` from this directory.
GAP performs its own rational enumeration and finite group calculations.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    source = ROOT / "data" / "lattices.json"
    raw = source.read_bytes()
    obj = json.loads(raw)
    g = obj["matrices"]["E8"]
    if len(g) != 8 or any(len(row) != 8 for row in g):
        raise ValueError("An 8 by 8 E8 Gram matrix is required")
    if any(type(x) is not int for row in g for x in row):
        raise ValueError("Only exact integer Gram entries are accepted")
    text = (
        "# Generated from data/lattices.json by export_gap.py.\n"
        "# E8Gram is a Gram matrix for squared norm x*G*x^T.\n"
        f'E8InputSHA256 := "{hashlib.sha256(raw).hexdigest()}";\n'
        f"E8Gram := {json.dumps(g)};\n"
    )
    target = ROOT / "data" / "gap_inputs.g"
    target.write_text(text, encoding="utf-8")
    print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
