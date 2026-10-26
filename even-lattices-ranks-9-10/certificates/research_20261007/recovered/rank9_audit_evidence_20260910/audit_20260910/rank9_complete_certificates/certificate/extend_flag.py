"""Exact one-step extension for the shortest-dual saturated-flag search.

Given a rank-r even integral parent G, this enumerates all one-vector Gram
matrices H in a prescribed determinant interval for which

* min(H) >= 6, and
* the dual vector perpendicular to G is a shortest nonzero vector of H^*.

The enumeration is by all classes in G^*/G.  Completeness of the class table
is certified by seeing exactly det(G) distinct fractional fingerprints.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from exact_lattice import deduplicate_isometry, determinant, enumerate_vectors


def inverse(a):
    n = len(a)
    m = [
        [Fraction(a[i][j]) for j in range(n)]
        + [Fraction(int(i == j)) for j in range(n)]
        for i in range(n)
    ]
    for j in range(n):
        pivot = next(i for i in range(j, n) if m[i][j])
        m[j], m[pivot] = m[pivot], m[j]
        scale = m[j][j]
        m[j] = [x / scale for x in m[j]]
        for i in range(n):
            if i != j and m[i][j]:
                scale = m[i][j]
                m[i] = [m[i][k] - scale * m[j][k] for k in range(2 * n)]
    return [row[n:] for row in m]


def matvec(a, x):
    return [sum(a[i][j] * x[j] for j in range(len(x))) for i in range(len(a))]


def dot(x, y):
    return sum(xi * yi for xi, yi in zip(x, y))


def fractional_part(x: Fraction) -> Fraction:
    return x - (x.numerator // x.denominator)


def class_key(inv_g, p):
    return tuple(fractional_part(x) for x in matvec(inv_g, p))


def discriminant_minima(g, *, verbose=False):
    """Return exact minima and one witness for every class of G^*/G."""
    inv_g = inverse(g)
    expected = determinant(g)
    if expected <= 0:
        raise ValueError("parent is not positive definite")
    bound = 0
    best = {}
    witness = {}
    while len(best) < expected:
        bound += 1
        points = enumerate_vectors(inv_g, bound, include_zero=True)
        for p, mu in points:
            key = class_key(inv_g, p)
            if key not in best or mu < best[key]:
                best[key] = Fraction(mu)
                witness[key] = p
        if verbose:
            print("  discr bound", bound, "classes", len(best), "/", expected)
        if bound > 20:
            raise RuntimeError("unexpectedly large covering-radius search")
    assert len(best) == expected
    # Since every point of norm <= bound was enumerated and every class has
    # appeared, these are the exact class minima, not merely upper bounds.
    return inv_g, best, witness, Fraction(bound)


def dual_minimum(inv_g):
    """Exact first minimum of the dual Gram matrix inv_g."""
    bound = 1
    while True:
        points = enumerate_vectors(inv_g, bound, include_zero=False)
        if points:
            return min(Fraction(q) for _, q in points)
        bound += 1


def ceil_fraction(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


def child_minimum_ok(inv_g, minima, p, s):
    m = 1
    while Fraction(m * m) * s < 6:
        key = class_key(inv_g, tuple(m * x for x in p))
        if Fraction(m * m) * s + minima[key] < 6:
            return False
        m += 1
    return True


def append_gram(g, p, diagonal):
    return [list(g[i]) + [int(p[i])] for i in range(len(g))] + [list(map(int, p)) + [diagonal]]


def normal_is_dual_shortest(child, s):
    inv_child = inverse(child)
    target = Fraction(1, 1) / s
    points = enumerate_vectors(inv_child, target, include_zero=False)
    assert points, "the perpendicular dual vector must occur"
    return min(Fraction(q) for _, q in points) == target


def extend_parent(g, det_low, det_high, modulus, residues, *, verbose=False):
    d = determinant(g)
    inv_g_pre = inverse(g)
    lambda_dual = dual_minimum(inv_g_pre)
    # Let y be the perpendicular dual vector of a putative child, y^2=1/s.
    # A shortest u in G^* lifts to a child-dual vector of norm at most
    # lambda_dual+1/(4s), by choosing the last integral pairing nearest to
    # its required real value.  If y is shortest, then
    #   1/s <= lambda_dual+1/(4s), hence s >= 3/(4 lambda_dual).
    # Since s=det(child)/d, this gives a cheap class-independent exact prune.
    required_s = Fraction(3, 4) / lambda_dual
    if Fraction(det_high, d) < required_s:
        return [], {
            "parent_det": d,
            "dual_minimum": str(lambda_dual),
            "global_required_s": str(required_s),
            "global_s_upper": str(Fraction(det_high, d)),
            "globally_pruned": True,
            "discriminant_classes": 0,
            "cover_search_bound": "not-run",
            "tested": {},
        }
    inv_g, minima, witnesses, cover_bound = discriminant_minima(g, verbose=verbose)
    children = []
    tested = Counter()
    for key, mu in minima.items():
        p = witnesses[key]
        lower_n = mu + Fraction(det_low, d)
        upper_n = mu + Fraction(det_high, d)
        n = ceil_fraction(lower_n)
        if n % 2:
            n += 1
        while Fraction(n) <= upper_n:
            s = Fraction(n) - mu
            det_child = d * s
            assert det_child.denominator == 1
            det_child = det_child.numerator
            tested["even_diagonal"] += 1
            if det_low <= det_child <= det_high and det_child % modulus in residues:
                tested["det_congruence"] += 1
                if child_minimum_ok(inv_g, minima, p, s):
                    tested["minimum"] += 1
                    child = append_gram(g, p, n)
                    assert determinant(child) == det_child
                    if normal_is_dual_shortest(child, s):
                        tested["dual_shortest"] += 1
                        children.append(child)
            n += 2
    return children, {
        "parent_det": d,
        "dual_minimum": str(lambda_dual),
        "global_required_s": str(required_s),
        "global_s_upper": str(Fraction(det_high, d)),
        "globally_pruned": False,
        "discriminant_classes": len(minima),
        "cover_search_bound": str(cover_bound),
        "tested": dict(tested),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="JSON containing a representatives array")
    parser.add_argument("output", type=Path)
    parser.add_argument("--low", type=int, required=True)
    parser.add_argument("--high", type=int, required=True)
    parser.add_argument("--modulus", type=int, default=2)
    parser.add_argument("--residues", default="0", help="comma-separated allowed residues")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    parents = data["representatives"]
    residues = {int(x) % args.modulus for x in args.residues.split(",")}
    raw = []
    stats = []
    for i, parent in enumerate(parents):
        print("PARENT", i, "/", len(parents), "rank", len(parent), "det", determinant(parent), flush=True)
        children, parent_stats = extend_parent(
            parent, args.low, args.high, args.modulus, residues, verbose=args.verbose
        )
        parent_stats["raw_children"] = len(children)
        stats.append(parent_stats)
        raw.extend(children)
        print("  RAW_CHILDREN", len(children), "TOTAL", len(raw), flush=True)
    raw_checkpoint = args.output.with_suffix(args.output.suffix + ".raw")
    raw_checkpoint.write_text(json.dumps({"representatives": raw}), encoding="utf-8")
    print("RAW_CHECKPOINT", raw_checkpoint, flush=True)
    print("DEDUPLICATING", len(raw), flush=True)
    reps, classes, maps = deduplicate_isometry(raw)
    multiplicities = Counter(classes)
    payload = {
        "rank": len(reps[0]) if reps else len(parents[0]) + 1,
        "determinant_window": [args.low, args.high],
        "determinant_modulus": args.modulus,
        "determinant_residues": sorted(residues),
        "parent_count": len(parents),
        "raw_count": len(raw),
        "class_count": len(reps),
        "determinant_counts": dict(sorted(Counter(determinant(g) for g in reps).items())),
        "representatives": reps,
        "raw_to_class": classes,
        "class_multiplicities": [multiplicities[i] for i in range(len(reps))],
        "isometry_maps": maps,
        "parent_stats": stats,
    }
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("CLASSES", len(reps))
    print("DET_COUNTS", payload["determinant_counts"])
    print("OUTPUT", args.output)


if __name__ == "__main__":
    main()
