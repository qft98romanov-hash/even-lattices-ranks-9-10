#!/usr/bin/env python3
"""Independent SymPy/Fraction checks of the displayed lattices.

No archived verifier is imported. SymPy supplies determinants, LDL factors,
Smith forms, inverses and finite-field ranks. The complete ellipsoid enumerator
below is a new implementation using deliberately conservative integer intervals
and exact rejection; it does not use a floating-point square root.

This verifies explicit examples and structural data. It does not prove the
global determinant lower bounds or exhaust the space of all input lattices.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from itertools import product
from math import gcd, isqrt
from pathlib import Path
import hashlib
import json
import platform
import sys
import time

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent


def require(condition: bool, description: str) -> None:
    """Checks remain active even if someone invokes Python with -O."""
    if not condition:
        raise ArithmeticError(description)


def fraction(value) -> Fraction:
    value = sp.Rational(value)
    return Fraction(int(value.p), int(value.q))


def ceiling_square_root(value: Fraction) -> int:
    """Return ceil(sqrt(value)) using integer arithmetic only."""
    require(value >= 0, 'Square-root argument must be nonnegative')
    root = isqrt(value.numerator // value.denominator)
    return root if root * root * value.denominator == value.numerator else root + 1


def evaluate(matrix, coordinates) -> Fraction:
    return sum((matrix[i][j] * coordinates[i] * coordinates[j]
                for i in range(len(coordinates)) for j in range(len(coordinates))), Fraction(0))


def enumerate_ellipsoid(matrix: sp.Matrix, bound: Fraction):
    """Enumerate every integral coordinate vector x with x^T matrix x <= bound.

    SymPy's exact decomposition A=L D L^T gives
      x^T A x = sum_k D[k,k] * (x[k] + sum_{j>k} L[j,k]*x[j])^2.
    Once coordinates above k are fixed, the residual budget bounds x[k].
    We take an integer interval slightly larger than the true one, then test
    every choice by an exact rational inequality. Thus no endpoint is lost
    because of rounded square roots. Zero and both signs are retained.
    """
    require(matrix == matrix.T, 'Enumeration matrix is not symmetric')
    lower, diagonal_matrix = matrix.LDLdecomposition(hermitian=False)
    require(lower * diagonal_matrix * lower.T == matrix, 'LDL identity failed')
    dimension = matrix.rows
    diagonal = [fraction(diagonal_matrix[i, i]) for i in range(dimension)]
    require(all(d > 0 for d in diagonal), 'Enumeration matrix is not positive definite')
    upper = [[fraction(lower[j, i]) for j in range(dimension)] for i in range(dimension)]
    exact_matrix = [[fraction(matrix[i, j]) for j in range(dimension)]
                    for i in range(dimension)]
    coordinates = [0] * dimension
    results = []
    nodes = 0

    def descend(index: int, budget: Fraction) -> None:
        nonlocal nodes
        nodes += 1
        if index < 0:
            direct = evaluate(exact_matrix, coordinates)
            require(direct == bound - budget and direct <= bound, 'Leaf norm mismatch')
            results.append((tuple(coordinates), direct))
            return
        offset = sum((upper[index][j] * coordinates[j]
                      for j in range(index + 1, dimension)), Fraction(0))
        center = -offset
        radius = ceiling_square_root(budget / diagonal[index])
        floor_center = center.numerator // center.denominator
        # These endpoints enclose [center-sqrt(B/d), center+sqrt(B/d)].
        for value in range(floor_center - radius, floor_center + radius + 2):
            cost = diagonal[index] * (Fraction(value) + offset) ** 2
            if cost <= budget:
                coordinates[index] = value
                descend(index - 1, budget - cost)

    descend(dimension - 1, Fraction(bound))
    results.sort(key=lambda item: (item[1], item[0]))
    vectors = {vector for vector, _ in results}
    require(len(vectors) == len(results), 'Duplicate enumeration output')
    require(all(tuple(-v for v in vector) in vectors for vector in vectors),
            'Enumeration is not invariant under sign')
    return results, {'nodes': nodes, 'ldl_diagonal': [str(x) for x in diagonal]}


def validate_enumerator() -> list:
    """Compare to exhaustive coordinate boxes on three small nontrivial cases.

    Cauchy-Schwarz gives x_i^2 <= bound*(A^-1)[i,i], hence the box search
    is complete independently of the LDL recursion.
    """
    cases = [
        (sp.Matrix([[4, 3], [3, 4]]), Fraction(13, 2)),
        (sp.Matrix([[2, -1, 1], [-1, 3, 0], [1, 0, 3]]), Fraction(8)),
        (sp.Matrix([[sp.Rational(2, 3), sp.Rational(-1, 3)],
                    [sp.Rational(-1, 3), sp.Rational(5, 6)]]), Fraction(11, 3)),
    ]
    output = []
    for matrix, bound in cases:
        enumerated, _ = enumerate_ellipsoid(matrix, bound)
        inverse = matrix.inv()
        limits = [ceiling_square_root(bound * fraction(inverse[i, i]))
                  for i in range(matrix.rows)]
        raw = [[fraction(v) for v in row] for row in matrix.tolist()]
        boxed = {(point, evaluate(raw, point))
                 for point in product(*(range(-limit, limit + 1) for limit in limits))
                 if evaluate(raw, point) <= bound}
        require(set(enumerated) == boxed, 'Independent box/enumerator comparison failed')
        output.append({'dimension': matrix.rows, 'bound': str(bound),
                       'vectors': len(boxed), 'coordinate_limits': limits})
    return output


def modular_rank(matrix: sp.Matrix, prime: int) -> int:
    return int(DomainMatrix.from_Matrix(matrix).convert_to(sp.GF(prime)).rank())


def shell_counts(vectors) -> dict:
    return dict(sorted(Counter(str(norm) for _, norm in vectors).items(),
                       key=lambda item: Fraction(item[0])))


def vector_record(vectors) -> list:
    return [{'coordinates': list(vector), 'squared_norm': str(norm)}
            for vector, norm in vectors]


def check_lattice(name: str, values: list, expected: dict):
    started = time.perf_counter()
    matrix = sp.Matrix(values)
    require(matrix == matrix.T, f'{name}: symmetry')
    require(all(v.q == 1 for v in matrix), f'{name}: integral Gram entries')
    require(all(matrix[i, i] % 2 == 0 for i in range(matrix.rows)), f'{name}: even diagonal')
    determinant = int(matrix.det(method='bareiss'))
    leading_minors = [int(matrix[:k, :k].det(method='bareiss'))
                      for k in range(1, matrix.rows + 1)]
    require(all(x > 0 for x in leading_minors), f'{name}: Sylvester positivity')
    smith = smith_normal_form(matrix, domain=sp.ZZ)
    smith_diagonal = [abs(int(smith[i, i])) for i in range(matrix.rows)]
    ranks = {str(prime): modular_rank(matrix, prime) for prime in (3, 5)}
    vectors, stats = enumerate_ellipsoid(matrix, Fraction(10))
    counts = shell_counts(vectors)
    nonzero_norms = [norm for _, norm in vectors if norm]
    minimum = min(nonzero_norms)

    # Compare expected answers only after their independent recomputation.
    require(determinant == expected['determinant'], f'{name}: determinant mismatch')
    require(minimum == expected['minimum'], f'{name}: minimum mismatch')
    for norm, count in expected['theta_shells'].items():
        require(counts.get(norm, 0) == count, f'{name}: norm-{norm} count mismatch')
    for prime in (3, 5):
        key = f'rank_mod_{prime}'
        if key in expected:
            require(ranks[str(prime)] == expected[key], f'{name}: rank modulo {prime}')
    if 'smith_diagonal' in expected:
        require(smith_diagonal == expected['smith_diagonal'], f'{name}: Smith form mismatch')

    report = {'rank': matrix.rows, 'positive_definite': True, 'integral': True, 'even': True,
              'determinant': determinant, 'leading_principal_minors': leading_minors,
              'smith_diagonal': smith_diagonal,
              'discriminant_group_invariant_factors': [v for v in smith_diagonal if v > 1],
              'rank_mod_prime': ranks, 'minimum_squared_norm': str(minimum),
              'complete_enumeration_bound': '10', 'shell_counts': counts,
              'enumeration': stats}
    complete = {'primal_through_10': vector_record(vectors)}

    if matrix.rows == 10:
        inverse = matrix.inv()
        require(matrix * inverse == sp.eye(10), f'{name}: inverse identity')
        dual, dual_stats = enumerate_ellipsoid(inverse, Fraction(2, 5))
        dual_norms = [norm for _, norm in dual if norm]
        require(min(dual_norms) == Fraction(expected['dual_minimum']), f'{name}: dual minimum')
        normals = [vector for vector, norm in dual if norm]
        require(len(normals) == expected['dual_minimal_vectors'], f'{name}: dual shell count')
        require(sp.Matrix(normals).rank() == 2, f'{name}: dual span rank')
        require(all(not any(vector[:8]) for vector in normals), f'{name}: dual normals on G8')
        primitive_kernels = []
        for normal in normals:
            require(gcd(*normal) == 1, f'{name}: dual normal is not primitive')
            if next(x for x in normal if x) < 0:
                continue
            a, b = normal[-2:]
            # gcd(a,b)=1 proves that these rows span the entire integral kernel.
            require(gcd(a, b) == 1, f'{name}: nonprimitive final normal pair')
            basis = [list(sp.eye(10).row(i)) for i in range(8)] + [[0] * 8 + [b, -a]]
            basis_matrix = sp.Matrix(basis)
            require(basis_matrix * sp.Matrix(normal) == sp.zeros(9, 1), f'{name}: kernel')
            gram = basis_matrix * matrix * basis_matrix.T
            kernel_vectors, kernel_stats = enumerate_ellipsoid(gram, Fraction(6))
            require(int(gram.det()) == 21870, f'{name}: kernel determinant')
            require(shell_counts(kernel_vectors) == {'0': 1, '6': 258}, f'{name}: kernel shell')
            primitive_kernels.append({'primitive_pairing_normal': list(normal),
                                      'basis_rows': [[int(v) for v in row] for row in basis],
                                      'gram': [[int(v) for v in row] for row in gram.tolist()],
                                      'determinant': 21870, 'minimum_squared_norm': 6,
                                      'minimal_vectors': 258, 'enumeration': kernel_stats})
        require(len(primitive_kernels) == 3, f'{name}: number of shortest-normal kernels')
        report['dual'] = {'determinant': str(fraction(inverse.det())),
                          'minimum_squared_norm': str(min(dual_norms)),
                          'minimal_vectors': len(normals), 'span_rank': 2,
                          'vanish_on_first_eight_basis_vectors': True,
                          'enumeration': dual_stats}
        report['primitive_kernels_of_shortest_dual_pairs'] = primitive_kernels
        complete['dual_through_2_over_5'] = vector_record(dual)
    else:
        positive = [v for v, norm in vectors if norm == minimum
                    and next(entry for entry in v if entry) > 0]
        products = sp.Matrix([[v[i] * v[j] for i in range(9) for j in range(i, 9)]
                              for v in positive])
        _, pivots = products.T.rref()
        require(len(pivots) == 45, 'K9: perfection span rank is not 45')
        minor = products[list(pivots), :]
        minor_determinant = int(minor.det(method='bareiss'))
        require(minor_determinant != 0, 'K9: perfection minor is singular')
        report['perfection'] = {'antipodal_pairs': len(positive), 'span_rank': 45,
                                'selected_pair_indices': list(pivots),
                                'selected_minor_determinant': minor_determinant,
                                'selected_vectors': [list(positive[i]) for i in pivots]}

    report['elapsed_seconds'] = round(time.perf_counter() - started, 6)
    return report, complete


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=HERE / 'data/lattices.json')
    parser.add_argument('--output', type=Path, default=HERE / 'results/exact.json')
    args = parser.parse_args()
    started = time.perf_counter()
    data = json.loads(args.input.read_text(encoding='utf-8'))
    report = {'status': 'RUNNING', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
              'python': platform.python_version(), 'sympy': sp.__version__,
              'input_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
              'implementation': 'SymPy plus new Fraction enumeration; no original verifier imports',
              'scope': 'Explicit lattice properties, short vectors, duals and three primitive kernels. '
                       'Not a global determinant bound or exhaustive equality-classification proof.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        report['independent_box_tests'] = validate_enumerator()
        report['lattices'] = {}
        vector_output = {}
        for name in ['K9', 'K10', 'K10_alt']:
            result, vectors = check_lattice(name, data['matrices'][name], data['expected'][name])
            report['lattices'][name] = result
            vector_output[name] = vectors
            print(name, 'PASS', 'det =', result['determinant'],
                  'shells =', result['shell_counts'], flush=True)
        require(report['lattices']['K10']['rank_mod_prime']['3'] !=
                report['lattices']['K10_alt']['rank_mod_prime']['3'],
                'The two rank10 types were not distinguished modulo 3')
        report['rank10_nonisometry_certificate'] = 'Distinct Gram ranks over F_3: 4 and 3'
        vector_path = args.output.with_name('exact_vectors.json')
        vector_path.write_text(json.dumps(vector_output, separators=(',', ':')) + '\n', encoding='utf-8')
        report['vectors_file'] = vector_path.name
        report['vectors_sha256'] = hashlib.sha256(vector_path.read_bytes()).hexdigest()
        report['status'] = 'PASS'
    except Exception as error:
        report['status'] = 'FAIL'
        report['error'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        report['elapsed_seconds'] = round(time.perf_counter() - started, 6)
        args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('INDEPENDENT_SYMPY_FRACTION_CHECKS_PASS', flush=True)
    print(args.output)
    return 0


if __name__ == '__main__':
    sys.exit(main())
