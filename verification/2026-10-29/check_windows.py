#!/usr/bin/env python3
"""Independent arithmetic and HNF certificate audit for the equality boundary.

This program imports no archived verifier.  SymPy supplies determinant,
inverse, integer-root, and column-Hermite-normal-form arithmetic.  Its finite
module representatives differ from the archived breadth-first traversal.
Archived shorter-dual vectors are treated only as proposed witnesses: every
required norm and inequality is evaluated again with exact integers.

This is NOT an independent regeneration of the entire strict-search prefix.
Completeness of that prefix and the external Hermite bounds remain inputs.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import gcd, prod
from pathlib import Path
import json
import platform
import time

import sympy
from sympy import Matrix, integer_nthroot
from sympy.matrices.normalforms import hermite_normal_form

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def source_root():
    for root in HERE.parents:
        for candidate in (root / 'even-lattices-ranks-9-10' / 'certificates',
                          root / 'certificates'):
            if (candidate / 'research_20261008').is_dir():
                return candidate
    raise FileNotFoundError('Cannot find the preserved certificate directory')


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def admissible(value, rank):
    return value % 2 == 0 if rank % 2 else value % 4 in (0, (-1)**(rank//2) % 4)


def root_floor(value, degree):
    value = F(value)
    result = int(integer_nthroot(value.numerator // value.denominator, degree)[0])
    require(F(result**degree) <= value < F((result+1)**degree), 'Invalid integer root')
    return result


def upper_windows(top):
    # Gamma[r] is gamma_r**r, not gamma_r itself.
    gamma = {2: F(4, 3), 3: F(2), 4: F(4), 5: F(8),
             6: F(64, 3), 7: F(64), 8: F(256), 9: F(512)}
    result, raw = {10: top}, {}
    for parent_rank in range(9, 0, -1):
        child_rank = parent_rank + 1
        if child_rank == 10:
            value, degree = F(2**45 * top**36), 40
        else:
            value = gamma[child_rank] * result[child_rank]**parent_rank
            degree = child_rank
        raw[parent_rank] = root_floor(value, degree)
        bound = raw[parent_rank]
        while not admissible(bound, parent_rank):
            bound -= 1
        result[parent_rank] = bound
    return result, raw


def arithmetic_audit(evidence):
    base = evidence / 'research_20261007' / 'rank10' / 'early_flags'
    strict_top = 54675 - 1
    while not admissible(strict_top, 10):
        strict_top -= 1
    strict, strict_raw = upper_windows(strict_top)
    equality, equality_raw = upper_windows(54675)
    expected = [6, 44, 210, 789, 2492, 6460, 13940, 24676, 40056, 54675]
    require([equality[r] for r in range(1, 11)] == expected, 'Equality windows disagree')
    endpoints = {r: [d for d in range(strict[r]+1, equality[r]+1) if admissible(d, r)]
                 for r in range(1, 10)}
    require(endpoints == {1: [], 2: [], 3: [], 4: [], 5: [],
                          6: [6460], 7: [13940], 8: [24676], 9: [40056]},
            'Unexpected new endpoints')
    gamma = {1: F(1), 2: F(4, 3), 3: F(2), 4: F(4), 5: F(8),
             6: F(64, 3), 7: F(64), 8: F(256), 9: F(512)}
    hermite_lower = {r: F(6**r) / gamma[r] for r in range(1, 10)}
    low = {}
    for r, q in hermite_lower.items():
        d = -(-q.numerator // q.denominator)
        if r == 8:  # The E8-free branch excludes the unique Hermite equality case.
            d += 1
        while not admissible(d, r):
            d += 1
        low[r] = d
    require([low[r] for r in range(1, 10)] ==
            [6, 27, 108, 324, 972, 2187, 4374, 6564, 19684], 'Lower-window error')

    raw_audits, parent_audits, terminal_bounds = [], [], []
    for r in (7, 8, 9):
        records = load(base / f'rank{r}_lifting_prunes.json')['prunes']
        revived = []
        for parent_index, child_index, dp, d, lhs, rhs in records:
            require(lhs == 3*d*d and rhs == 4*dp*strict[r+1] and lhs > rhs,
                    'Invalid archived raw lifting inequality')
            if lhs <= 4*dp*equality[r+1]:
                revived.append({'parent_index': parent_index, 'child_index': child_index,
                                'previous_determinant': dp, 'determinant': d,
                                'next_lower_bound': str(F(3*d*d, 4*dp))})
            if r == 9:
                terminal_bounds.append(F(3*d*d, 4*dp))
        raw_audits.append({'rank': r, 'checked': len(records), 'revived': revived})
        records = load(base / f'rank{r}_parents' / 'exact_prunes.json')['prunes']
        revived = []
        for row in records:
            d, dp = (row['d6'], row['d5']) if r == 7 else (row['det'], row['preceding_det'])
            require(row['left'] == 3*d*d and row['right'] == 4*dp*strict[r]
                    and row['left'] > row['right'], 'Invalid whole-parent prune')
            if 3*d*d <= 4*dp*equality[r]:
                revived.append(row['parent_index'])
        parent_audits.append({'child_rank': r, 'checked': len(records), 'revived': revived})
    require([len(r['revived']) for r in raw_audits] == [4, 0, 0], 'Revived raw cases differ')
    require(not any(r['revived'] for r in parent_audits), 'A whole-parent prune revives')
    recovered = raw_audits[0]['revived']
    require([(r['parent_index'], r['child_index']) for r in recovered] ==
            [(3297, j) for j in range(606, 610)], 'Recovered case identities differ')
    records = load(base / 'rank7_parents' / 'parent_3297.json')['representatives']
    for row in recovered:
        g = Matrix(records[row['child_index']])
        require(int(g.det()) == 11658 and int(g[:-1, :-1].det()) == 4131,
                'Recovered matrix determinant mismatch')
        bound = F(3*11658**2, 4*4131)
        candidates = [d for d in range(-(-bound.numerator//bound.denominator), equality[8]+1)
                      if admissible(d, 8)]
        require(candidates == [24676], 'Recovered branch has an unhandled endpoint')
    require(len(terminal_bounds) == 3819 and min(terminal_bounds) == F(12966723, 212)
            and min(terminal_bounds) > equality[10], 'An old terminal record can continue')
    return {'strict_upper': strict, 'equality_upper': equality, 'strict_raw_floors': strict_raw,
            'equality_raw_floors': equality_raw, 'new_endpoints': endpoints,
            'hermite_lower_before_E8_and_parity': {r: str(x) for r, x in hermite_lower.items()},
            'E8_free_lower': low, 'raw_prunes': raw_audits, 'whole_parent_prunes': parent_audits,
            'terminal_candidates': len(terminal_bounds),
            'minimum_terminal_continuation_bound': str(min(terminal_bounds))}


def boundary_audit(evidence):
    """Cover every new endpoint using HNF classes and verified witness integers.

    For upper triangular column HNF H of G, the box
    0 <= p_i < H_ii represents Z^r/G Z^r exactly once.  The quotient and
    determinant identities are verified before using this representation.
    """
    base = evidence / 'research_20261007' / 'rank10' / 'early_flags'
    witness_path = evidence / 'research_20261008' / 'independent_review' / 'boundaries_by_quadratic_module.json'
    witness_data = load(witness_path)['records']
    witness_lookup = {(r['input'], r['parent_index'], r['target']): r.get('witness_counts', {})
                      for r in witness_data}
    families = [('rank5.json', 6460), ('rank6_fast.json', 13940),
                ('rank7_eligible.json', 24676), ('rank8_eligible.json', 40056)]
    jobs = []
    for name, target in families:
        for index, gram in enumerate(load(base/name)['representatives']):
            jobs.append((name, index, gram, target))
    revived_name = 'rank7_parents/parent_3297.json'
    revived = load(base/revived_name)['representatives']
    for j in range(606, 610):
        jobs.append((revived_name, j, revived[j], 24676))
    require(len(jobs) == 4952, 'Unexpected boundary family size')
    records, methods = [], Counter()
    next_upper = {6460: 13940, 13940: 24676, 24676: 40056, 40056: 54675}
    start = time.monotonic()
    for job_index, (name, index, gram, target) in enumerate(jobs):
        g = Matrix(gram)
        require(g == g.T and all(int(g[i, i]) % 2 == 0 for i in range(g.rows)), 'Not even symmetric')
        d = int(g.det(method='domain-ge'))
        dp = int(g[:-1, :-1].det(method='domain-ge'))
        require(d > 0 and dp > 0, 'Nonpositive determinant')
        record = {'input': name, 'parent_index': index, 'parent_determinant': d,
                  'preceding_determinant': dp, 'target': target}
        if 3*d*d > 4*dp*target:
            record.update(method='parent_lifting', lhs=3*d*d, rhs=4*dp*target)
        elif 3*target*target > 4*d*next_upper[target]:
            # This is a universal obstruction to continuing any such child.
            record.update(method='next_lifting', lhs=3*target*target,
                          rhs=4*d*next_upper[target], next_upper=next_upper[target])
        else:
            inverse = g.inv(method='DM')
            adj = inverse*d
            require(all(x.q == 1 for x in adj) and g*adj == Matrix.eye(g.rows)*d,
                    'Invalid adjugate')
            a = [[int(adj[i, j]) for j in range(g.cols)] for i in range(g.rows)]
            content = gcd(2*d, *[a[i][i] for i in range(g.rows)],
                          *[2*a[i][j] for i in range(g.rows) for j in range(i)])
            if target % content:
                record.update(method='quadratic_content', content=content)
            else:
                h = hermite_normal_form(g)
                diagonal = [int(h[i, i]) for i in range(g.rows)]
                require(all(x > 0 for x in diagonal) and prod(diagonal) == d,
                        'Wrong Hermite fundamental box volume')
                require(all(h[i, j] == 0 for i in range(g.rows) for j in range(i)),
                        'HNF is not upper triangular')
                transform = inverse*h
                require(all(x.q == 1 for x in transform) and abs(transform.det()) == 1,
                        'HNF does not generate the same integer column lattice')
                active = [i for i in range(g.rows) if diagonal[i] != 1]
                coefficients = [(u, v, (1 if u == v else 2)*a[i][j])
                                for u, i in enumerate(active)
                                for v, j in enumerate(active) if v >= u]
                witnesses = []
                for proposed in witness_lookup.get((name, index, target), {}):
                    q = ast.literal_eval(proposed)
                    require(isinstance(q, tuple) and len(q) == g.rows
                            and all(isinstance(v, int) for v in q) and any(q),
                            'Malformed shorter-dual witness')
                    aq = [sum(a[i][j]*q[j] for j in range(g.rows)) for i in range(g.rows)]
                    norm_numerator = sum(q[i]*aq[i] for i in range(g.rows))
                    require(norm_numerator > 0, 'Nonpositive proposed witness norm')
                    witnesses.append((q, aq, norm_numerator))
                compatible = 0
                witness_usage = Counter()
                all_classes = 0
                for p in product(*(range(diagonal[i]) for i in active)):
                    all_classes += 1
                    norm_numerator = sum(c*p[u]*p[v] for u, v, c in coefficients)
                    if (norm_numerator+target) % (2*d):
                        continue
                    compatible += 1
                    for wi, (q, aq, qnorm) in enumerate(witnesses):
                        residue = sum(p[u]*aq[i] for u, i in enumerate(active)) % d
                        distance = min(residue, d-residue)
                        if target*qnorm+distance*distance < d*d:
                            witness_usage[wi] += 1
                            break
                    else:
                        raise RuntimeError(f'Unexcluded HNF class: {name} #{index}, T={target}, p={p}')
                require(all_classes == d, 'Incomplete HNF fundamental box')
                record.update(method='HNF_nonrepresentation' if compatible == 0 else 'HNF_verified_dual_witnesses',
                              HNF_diagonal=diagonal, enumerated_classes=all_classes,
                              compatible_classes=compatible,
                              witnesses=[{'q': list(witnesses[i][0]), 'classes_excluded': count}
                                         for i, count in sorted(witness_usage.items())])
        methods[record['method']] += 1
        records.append(record)
        if (job_index+1) % 250 == 0 or job_index+1 == len(jobs):
            print(f'BOUNDARY_HNF {job_index+1}/{len(jobs)} seconds={time.monotonic()-start:.3f}', flush=True)
    return {'pairs_checked': len(records), 'method_counts': dict(methods),
            'elapsed_seconds': time.monotonic()-start, 'records': records,
            'witness_source_sha256': sha256(witness_path.read_bytes()).hexdigest(),
            'scope': 'Independent HNF congruence and witness checking; archived parent lists remain inputs.'}


def geometric_audit():
    uniform9_squared = 81*F(8, 9)**39
    rank9 = {'one_fiber': 2*F(39, 40)**39,
             'several_singletons': uniform9_squared,
             'small_diameter_nonsingleton': F(1600, 9)*F(13, 15)**39,
             'four_thirds_to_three_halves': F(439, 4)**2*F(7, 9)**39,
             'three_halves_to_two': 148**2*F(3, 4)**39,
             'two_to_eight_thirds': 880**2*F(2, 3)**39,
             'eight_thirds_to_three': F(12155, 4)**2*F(5, 9)**39,
             'three_to_six': 133705**2*F(1, 2)**39}
    require(all(0 < value <= uniform9_squared < 1 for value in rank9.values()),
            'Rank-nine geometric upper bound fails')
    rows = [(F(2, 5), 3), (F(2, 3), 9), (F(23, 30), 11), (F(29, 30), 27),
            (F(6, 5), 36), (F(4, 3), 82), (F(8, 5), 109), (F(49, 30), 385),
            (F(2), 1540), (F(8, 3), 54675)]
    uniform10 = 9*F(8, 9)**19
    rank10 = [{'left': str(left), 'cardinality': n,
               'bound_exact': str(n*(1-left/6)**19)} for left, n in rows]
    require(all(F(r['bound_exact']) <= uniform10 < 1 for r in rank10),
            'Rank-ten endpoint bound fails')

    # Exhaustive maximum cliques in the tiny translated triangular-lattice balls.
    f = lambda u, v: u*u-u*v+v*v
    anticodes = []
    for threshold in (1, 3, 4):
        points = [(u, v) for u in range(-3, 4) for v in range(-3, 4) if f(u, v) <= threshold]
        points.remove((0, 0))
        neighbours = []
        for i, (u, v) in enumerate(points):
            neighbours.append(sum(1 << j for j, (x, y) in enumerate(points)
                                  if j != i and f(u-x, v-y) <= threshold))
        best = []
        def extend(clique, candidates):
            nonlocal best
            if len(clique)+candidates.bit_count() <= len(best):
                return
            if not candidates:
                if len(clique) > len(best):
                    best = clique[:]
                return
            while candidates:
                bit = candidates & -candidates
                candidates ^= bit
                v = bit.bit_length()-1
                extend(clique+[v], candidates & neighbours[v])
                if len(clique)+candidates.bit_count() <= len(best):
                    break
        extend([], (1 << len(points))-1)
        anticodes.append({'unscaled_norm_threshold': threshold, 'ball_size': len(points)+1,
                          'maximum_cardinality': len(best)+1,
                          'witness': [(0, 0)]+[points[i] for i in best]})
    require([r['ball_size'] for r in anticodes] == [7, 13, 19]
            and [r['maximum_cardinality'] for r in anticodes] == [3, 4, 7],
            'Triangular anticode maximum differs')
    roots = [(u, v) for u in range(-2, 3) for v in range(-2, 3) if f(u, v) == 1]
    pairbounds = [F(1, 10)*max(f(u+x, v+y), f(u-x, v-y))
                  for u, v in roots for x, y in roots]
    require(len(pairbounds) == 36 and min(pairbounds) == F(3, 10), 'Two-fiber midpoint bound fails')
    return {'rank9_upper_bounds_squared': {key: str(v) for key, v in rank9.items()},
            'rank9_uniform_squared': str(uniform9_squared), 'rank10_rows': rank10,
            'rank10_uniform': str(uniform10), 'rank10_uniform_decimal': float(uniform10),
            'triangular_anticodes': anticodes, 'minimal_root_pairs_checked': len(pairbounds),
            'two_fiber_vertical_lower_bound': str(min(pairbounds)),
            'scope': 'Exact endpoint arithmetic and finite fiber anticodes; geometric reductions are reviewed in accompanying note.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE/'results'/'windows.json')
    args = parser.parse_args()
    start = time.monotonic()
    evidence = source_root()
    source_files = [evidence/'research_20261007'/'rank10'/'early_flags'/name for name in
                    ('rank5.json', 'rank6_fast.json', 'rank7_eligible.json', 'rank8_eligible.json',
                     'rank7_parents/parent_3297.json', 'rank7_lifting_prunes.json',
                     'rank8_lifting_prunes.json', 'rank9_lifting_prunes.json',
                     'rank7_parents/exact_prunes.json', 'rank8_parents/exact_prunes.json',
                     'rank9_parents/exact_prunes.json')]
    report = {'started_utc': datetime.now(timezone.utc).isoformat(),
              'python': platform.python_version(), 'sympy': sympy.__version__,
              'assumptions': ['Classical Hermite constants through rank eight and unique E8 extremizer',
                              'External bound gamma_9 <= 2 and Mordell inequality',
                              'Complete strict-search prefix and certified representative coverage'],
              'source_sha256': {str(p.relative_to(evidence)): sha256(p.read_bytes()).hexdigest()
                                for p in source_files}}
    report['window_and_reuse_audit'] = arithmetic_audit(evidence)
    print('WINDOWS_AND_PRUNE_REUSE_PASS', flush=True)
    report['geometric_arithmetic'] = geometric_audit()
    print('CLUSTER_ENDPOINTS_AND_FIBER_ANTICODES_PASS', flush=True)
    report['independent_HNF_boundary_check'] = boundary_audit(evidence)
    report['elapsed_seconds'] = time.monotonic()-start
    report['status'] = 'PASS'
    report['scope'] = ('New independent arithmetic, HNF finite-module certificate checks, and finite fiber checks; '
                       'not formal verification, external review, or a new generation of the full strict-search prefix.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('INDEPENDENT_WINDOWS_HNF_AND_CLUSTER_CHECK_PASS', flush=True)
    print('REPORT', args.output, flush=True)


if __name__ == '__main__':
    main()
