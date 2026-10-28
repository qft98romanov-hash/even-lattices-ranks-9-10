#!/usr/bin/env sage-python
"""SageMath cross-check of explicit Gram matrices; run: sage -python check_sage.py.

Sage's short-vector and equivalence methods below call PARI.  Consequently
their agreement with check_pari.gp is NOT an independent enumeration backend.
Exact arithmetic checks of returned vectors/matrices do not prove that a
floating-point enumeration omitted no vector.  See docs/CAS_GUIDE_EN.md.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import traceback

from sage.all import CartanMatrix, GF, QQ, ZZ, QuadraticForm, lcm, matrix, vector
from sage.env import SAGE_VERSION

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def serial_matrix(M):
    return [[int(x) for x in row] for row in M.rows()]


def enumerate_shells(G, upper):
    # QuadraticForm(A) uses the Hessian A, so Q(v) = v^T A v / 2.
    Q = QuadraticForm(2 * G)
    require(Q.matrix() == 2 * G, "Hessian normalization")
    for i in range(G.nrows()):
        e = vector(ZZ, [int(j == i) for j in range(G.nrows())])
        require(Q(e) == e * G * e, "Unit-vector normalization")
    # Strict upper bound; both signs are requested and must not be doubled.
    shells = Q.short_vector_list_up_to_length(ZZ(upper + 1), up_to_sign_flag=False)
    require(len(shells) == upper + 1, "Unexpected shell-list length")
    for norm, entries in enumerate(shells):
        unique = {tuple(int(x) for x in v) for v in entries}
        require(len(unique) == len(entries), "Duplicate enumerated vector")
        for vv in unique:
            v = vector(ZZ, vv)
            require(v * G * v == norm, "Incorrect vector norm")
            require(tuple(-x for x in vv) in unique, "Missing opposite sign")
    require(len(shells[0]) == 1, "Zero vector convention")
    return Q, shells


def run():
    raw = (ROOT / "data/lattices.json").read_bytes()
    data = json.loads(raw)
    require(data["schema"] == 1, "Unsupported input schema")
    matrices = {name: matrix(ZZ, rows) for name, rows in data["matrices"].items()}
    report = {
        "status": "RUNNING", "sage_version": SAGE_VERSION,
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "enumeration_backend": "Sage QuadraticForm / PARI qfminim",
        "scope": "Explicit lattices only; no global determinant/classification claim",
        "enumeration_completeness_certificate": False, "lattices": {},
    }
    forms = {}
    for name in ("K9", "K10", "K10_alt", "E8"):
        G = matrices[name]
        n = G.nrows()
        expected = data["expected"][name]
        require(G == G.transpose(), name + ": symmetry")
        require(all(G[i, i] % 2 == 0 for i in range(n)), name + ": even")
        require(all(G[:k, :k].det() > 0 for k in range(1, n + 1)), name + ": positivity")
        detG = G.det()
        require(detG == expected["determinant"], name + ": determinant")
        S, U, V = G.smith_form()
        require(U * G * V == S, name + ": Smith certificate")
        require(abs(U.det()) == abs(V.det()) == 1, name + ": Smith unimodularity")
        diagonal = [int(abs(S[i, i])) for i in range(n)]
        if "smith_diagonal" in expected:
            require(diagonal == expected["smith_diagonal"], name + ": Smith invariants")
        bound = 8 if name == "E8" else 10
        Q, shells = enumerate_shells(G, bound)
        forms[name] = Q
        minimum = next(i for i in range(1, len(shells)) if shells[i])
        require(minimum == expected["minimum"], name + ": minimum")
        for norm, count in expected["theta_shells"].items():
            require(len(shells[int(norm)]) == count, name + ": shell " + norm)
        entry = {
            "determinant": int(detG), "minimum": minimum,
            "shells": {str(i): len(s) for i, s in enumerate(shells)},
            "smith_diagonal": diagonal,
            "smith_left_matrix": serial_matrix(U), "smith_right_matrix": serial_matrix(V),
        }
        if name in ("K10", "K10_alt"):
            for p in (3, 5):
                rk = int(G.change_ring(GF(p)).rank())
                require(rk == expected["rank_mod_" + str(p)], name + ": finite-field rank")
                entry["rank_mod_" + str(p)] = rk
            Gi = G.change_ring(QQ).inverse()
            require(Gi.det() == 1 / QQ(detG), name + ": dual determinant")
            scale = lcm([a.denominator() for a in Gi.list()])
            H = matrix(ZZ, scale * Gi)
            dual_min = QQ(expected["dual_minimum"])
            scaled_min = scale * dual_min
            require(scaled_min.denominator() == 1, name + ": dual bound integral")
            _, dual_shells = enumerate_shells(H, int(scaled_min))
            first = next(i for i in range(1, len(dual_shells)) if dual_shells[i])
            require(QQ(first) / scale == dual_min, name + ": dual minimum")
            vectors = dual_shells[first]
            require(len(vectors) == expected["dual_minimal_vectors"], name + ": dual count")
            require(matrix(QQ, vectors).rank() == 2, name + ": dual minimal-vector span")
            entry.update(dual_minimum=str(dual_min), dual_minimal_vectors=len(vectors),
                         dual_coordinates=[list(map(int, v)) for v in vectors],
                         dual_integral_scale=int(scale))
        report["lattices"][name] = entry
        print(name, "determinant", detG, "minimum", minimum, "shells", entry["shells"], flush=True)

    # Exact positive certificate, even though the search is delegated to PARI.
    C = matrix(ZZ, CartanMatrix(["E", 8]))
    E8standard = QuadraticForm(2 * C)
    M = forms["E8"].is_globally_equivalent_to(E8standard, return_matrix=True)
    require(M is not False, "E8 identification failed")
    M = matrix(ZZ, M)
    require(abs(M.det()) == 1, "E8 certificate unimodularity")
    require(M.transpose() * matrices["E8"] * M == C, "E8 isometry certificate")
    report["E8_isometry_matrix"] = serial_matrix(M)
    # Nonisometry also follows independently of qfisom from unequal mod-3 ranks.
    require(not forms["K10"].is_globally_equivalent_to(forms["K10_alt"]), "Rank-ten nonisometry")
    report["rank10_not_isometric"] = True
    report["status"] = "PASS_CROSS_CHECK"
    return report


if __name__ == "__main__":
    target = ROOT / "results/sage_run.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = run()
    except Exception as exc:
        target.write_text(json.dumps({"status": "FAIL", "error": repr(exc)}, indent=2) + "\n")
        traceback.print_exc()
        sys.exit(1)
    target.write_text(json.dumps(result, indent=2) + "\n")
    print("ALL_SAGE_EXPLICIT_CROSS_CHECKS_PASS")
