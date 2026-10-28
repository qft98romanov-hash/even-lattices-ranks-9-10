#!/usr/bin/env python3
"""Adversarial finite tests of the new ellipsoid enumerator.

The reference search uses an independently bounded integer coordinate box,
not the enumerator's LDL recursion or its square-root helper. This is a
software check on small forms, not a proof of the global lattice theorems.
"""
from __future__ import annotations

from fractions import Fraction
import importlib.util
import itertools
import json
from pathlib import Path
import random
import sys

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('independent_exact', ROOT / 'check_exact.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def reference_check(matrix, bound):
    """Cauchy-Schwarz gives x_i^2 <= bound*(matrix^-1)[i,i]."""
    inverse = matrix.inv()
    limits = []
    for i in range(matrix.rows):
        limit = 0
        while limit * limit <= bound * inverse[i, i]:
            limit += 1
        limits.append(limit)
    expected = set()
    for point in itertools.product(*(range(-n, n + 1) for n in limits)):
        norm = sum(matrix[i, j] * point[i] * point[j]
                   for i in range(matrix.rows) for j in range(matrix.rows))
        if norm <= bound:
            expected.add((point, Fraction(int(norm.p), int(norm.q))))
    found, _ = checker.enumerate_ellipsoid(matrix, Fraction(int(bound.p), int(bound.q)))
    if set(found) != expected:
        raise ArithmeticError(f'Enumeration mismatch: {matrix}, {bound}')
    return {'n': matrix.rows,
            'matrix': [[str(value) for value in row] for row in matrix.tolist()],
            'bound': str(bound), 'points': len(found),
            'boundary_points': sum(norm == bound for _, norm in expected),
            'box_limits': limits}


def main():
    seed = 20261029
    rng = random.Random(seed)
    cases = []
    for n in (1, 2, 3):
        for j in range(8):
            basis = sp.Matrix(n, n, [rng.randint(-2, 2) for _ in range(n * n)])
            matrix = (basis.T * basis + sp.eye(n)) / rng.choice([1, 2, 3, 5])
            vector = sp.Matrix([rng.randint(-1, 1) for _ in range(n)])
            bound = ((vector.T * matrix * vector)[0] if j % 2 else
                     sp.Rational(rng.randint(0, 15), rng.choice([1, 2, 3])))
            cases.append(reference_check(matrix, bound))
    for matrix, bound in [
        (sp.Matrix([[1, 5], [5, 26]]), sp.Rational(1)),
        (sp.eye(2) / 49, sp.Rational(2, 49)),
        (sp.eye(2), sp.Rational(0)),
    ]:
        cases.append(reference_check(matrix, bound))
    report = {'status': 'PASS', 'random_seed': seed, 'case_count': len(cases),
              'scope': 'Adversarial unit validation of exact ellipsoid enumeration only, '
                       'not a global lattice theorem', 'cases': cases}
    destination = ROOT / 'results/checker_review/enumerator_adversarial.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('PASS', len(cases), 'complete brute-force comparisons; boundary points',
          sum(case['boundary_points'] for case in cases))
    print(destination)


if __name__ == '__main__':
    main()
