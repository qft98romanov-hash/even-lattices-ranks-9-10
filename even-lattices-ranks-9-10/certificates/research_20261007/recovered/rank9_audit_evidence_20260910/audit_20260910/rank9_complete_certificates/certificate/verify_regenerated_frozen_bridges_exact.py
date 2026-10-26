"""Exact bridges from regenerated lower-flag classes to frozen classes.

This verifier is deliberately independent of representative ordering.  For
each rank and each frozen representative set used by the rank-9 computation,
it finds an explicit unimodular integer matrix X satisfying

    X^T F X = R,

where R is a freshly regenerated representative and F is a frozen one.  It
then checks that the matching is a bijection.  All vector enumeration and
isometry decisions are exact; see ``exact_lattice.py``.

The script does not modify any input JSON.  It writes three certificate
outputs next to itself:

* regenerated_frozen_bridges_exact.json
* verify_regenerated_frozen_bridges_exact.transcript
* regenerated_frozen_bridges_sha256.txt
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Sequence

from exact_lattice import determinant, isometry, short_signature


HERE = Path(__file__).resolve().parent
REPORT = HERE / "regenerated_frozen_bridges_exact.json"
TRANSCRIPT = HERE / "verify_regenerated_frozen_bridges_exact.transcript"
MANIFEST = HERE / "regenerated_frozen_bridges_sha256.txt"


# A rank can have more than one frozen set because early stages of the
# historical computation used independently deduplicated representatives.
DATASETS = (
    (1, "rank1_seed.json", "rank1_seed.json"),
    (2, "rank2_exact_classes_regen.json", "rank2_exact_classes.json"),
    (2, "rank2_exact_classes_regen.json", "rank2_seed_classes.json"),
    (3, "rank3_exact_classes_regen.json", "rank3_exact_classes.json"),
    (4, "rank4_exact_classes_regen.json", "rank4_exact_classes.json"),
    (4, "rank4_exact_classes_regen.json", "rank4_isometry_classes.json"),
    (5, "rank5_isometry_classes_regen.json", "rank5_isometry_classes.json"),
    (6, "rank6_isometry_classes_regen.json", "rank6_isometry_classes.json"),
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def transpose(a: Sequence[Sequence[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*a)]


def multiply(
    a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]
) -> list[list[int]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def congruence(x, frozen):
    return multiply(transpose(x), multiply(frozen, x))


def load_representatives(filename: str, rank: int):
    path = HERE / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    reps = data["representatives"]
    assert data.get("rank", rank) == rank, filename
    assert data.get("class_count", len(reps)) == len(reps), filename
    assert reps, filename
    assert all(len(g) == rank and all(len(row) == rank for row in g) for g in reps)
    return path, data, reps


def exact_bijection(rank: int, regenerated, frozen):
    assert len(regenerated) == len(frozen)
    # Norm 6 is a common, exact, isometry-invariant shell cutoff throughout
    # this minimum-six search.  It is only a sound prefilter; every surviving
    # comparison is decided by the exhaustive exact isometry routine.
    frozen_buckets = defaultdict(list)
    for j, form in enumerate(frozen):
        key = (determinant(form), short_signature(form, 6))
        frozen_buckets[key].append(j)

    bridges = []
    used = set()
    isometry_calls = 0
    for i, form in enumerate(regenerated):
        key = (determinant(form), short_signature(form, 6))
        candidates = frozen_buckets.get(key, [])
        matches = []
        for j in candidates:
            isometry_calls += 1
            x = isometry(form, frozen[j])
            if x is not None:
                assert abs(determinant(x)) == 1, (rank, i, j)
                assert congruence(x, frozen[j]) == form, (rank, i, j)
                matches.append((j, x))
        # Exact uniqueness also proves that the frozen list contains no two
        # representatives from the same isometry class.
        assert len(matches) == 1, (rank, i, [j for j, _ in matches], candidates)
        j, x = matches[0]
        assert j not in used, (rank, i, j)
        used.add(j)
        bridges.append(
            {
                "regenerated_index": i,
                "frozen_index": j,
                "determinant": determinant(form),
                "X": x,
            }
        )
    assert used == set(range(len(frozen))), (rank, len(used), len(frozen))
    return bridges, isometry_calls


def main() -> None:
    lines: list[str] = []

    def emit(message: str) -> None:
        print(message, flush=True)
        lines.append(message)

    input_names = sorted({name for _, regen, frozen in DATASETS for name in (regen, frozen)})
    report = {
        "certificate": "exact regenerated-to-frozen GL_n(Z) bridges",
        "identity_convention": "X^T * frozen * X = regenerated",
        "arithmetic": "integer and rational only; no floating-point decisions",
        "inputs_sha256": {name: sha256(HERE / name) for name in input_names},
        "comparisons": [],
    }

    emit("EXACT REGENERATED/FROZEN LOWER-FLAG BRIDGE VERIFIER")
    emit("CONVENTION X^T * FROZEN * X = REGENERATED")
    emit("FLOATING_POINT_DECISIONS 0")
    for rank, regen_name, frozen_name in DATASETS:
        _, regen_data, regenerated = load_representatives(regen_name, rank)
        _, frozen_data, frozen = load_representatives(frozen_name, rank)
        assert len(regenerated) == len(frozen)
        bridges, calls = exact_bijection(rank, regenerated, frozen)
        comparison = {
            "rank": rank,
            "regenerated_file": regen_name,
            "frozen_file": frozen_name,
            "class_count": len(bridges),
            "regenerated_raw_count": regen_data.get("raw_count"),
            "frozen_raw_count": frozen_data.get("raw_count"),
            "exact_isometry_calls": calls,
            "bridges": bridges,
        }
        report["comparisons"].append(comparison)
        emit(
            f"RANK {rank} REGEN {regen_name} FROZEN {frozen_name} "
            f"CLASSES {len(bridges)} EXACT_GL_BRIDGES {len(bridges)} "
            f"ISOMETRY_CALLS {calls} BIJECTION PASS"
        )

    # Pin the expected complete-chain counts independently of JSON metadata.
    primary_counts = {
        comparison["rank"]: comparison["class_count"]
        for comparison in report["comparisons"]
        if comparison["frozen_file"]
        in {
            "rank1_seed.json",
            "rank2_exact_classes.json",
            "rank3_exact_classes.json",
            "rank4_exact_classes.json",
            "rank5_isometry_classes.json",
            "rank6_isometry_classes.json",
        }
    }
    assert primary_counts == {1: 1, 2: 5, 3: 14, 4: 47, 5: 118, 6: 138}
    report["primary_class_counts"] = primary_counts
    report["result"] = "PASS"
    emit("PRIMARY_CLASS_COUNTS 1,5,14,47,118,138")
    emit("ALL_REGENERATED_FROZEN_EXACT_BRIDGES_OK")

    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    TRANSCRIPT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest_paths = [
        HERE / name for name in input_names
    ] + [
        Path(__file__).resolve(),
        REPORT,
        TRANSCRIPT,
        HERE / "exact_lattice.py",
        HERE / "extend_flag.py",
    ]
    manifest_lines = [
        f"{sha256(path)}  {path.name}" for path in sorted(set(manifest_paths), key=lambda p: p.name)
    ]
    MANIFEST.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
