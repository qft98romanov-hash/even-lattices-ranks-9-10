#!/usr/bin/env python3
"""Compare complete PARI vector sets to the independent exact enumerator."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
exact = json.loads((HERE / 'results/exact_vectors.json').read_text())
pari = {}
for line in (HERE / 'results/pari.log').read_text().splitlines():
    if line.startswith('VECTORS '):
        _, name, literal = line.split(' ', 2)
        representatives = json.loads(literal)
        points = {tuple(x) for x in representatives}
        if len(points) != len(representatives):
            raise ArithmeticError('Duplicate PARI representative')
        opposite = {tuple(-t for t in x) for x in points}
        if points & opposite:
            raise ArithmeticError('PARI list does not contain just one sign per pair')
        pari[name] = points | opposite
reports = {}
for name in ('K9', 'K10', 'K10_alt'):
    records = exact[name]['primal_through_10']
    points = {tuple(x['coordinates']) for x in records if x['squared_norm'] != '0'}
    if pari[name] != points:
        raise ArithmeticError(f'{name}: PARI/exact vector sets differ')
    reports[name] = {'matching_nonzero_vectors_through_10': len(points)}
result = {'status': 'PASS', 'lattices': reports,
          'scope': 'Equality of complete returned coordinate sets; exact completeness supplied by the separate rational enumerator.'}
(HERE / 'results/pari_vector_comparison.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
print('PARI_EXACT_VECTOR_COMPARISON_PASS')
