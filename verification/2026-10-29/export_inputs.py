#!/usr/bin/env python3
"""Export literal input matrices without importing archived verifier code."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[1]
ARCHIVE = REPOSITORY / 'even-lattices-ranks-9-10' / 'certificates'


def main() -> None:
    rank9_path = ARCHIVE / 'research_20261007/rank10/verify_rank9_extremal_example_exact.py'
    rank10_path = ARCHIVE / 'research_20261007/rank10/rank10_e8_certificate.json'
    tree = ast.parse(rank9_path.read_text(encoding='utf-8'))
    values = [ast.literal_eval(node.value) for node in tree.body
              if isinstance(node, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == 'K9' for t in node.targets)]
    if len(values) != 1:
        raise ValueError('Expected exactly one literal assignment of K9')
    k9 = values[0]
    source10 = json.loads(rank10_path.read_text(encoding='utf-8'))
    by_name = {entry['name']: entry for entry in source10['examples']}
    k10 = by_name['K10_original']['gram']
    alternative = by_name['K10_alternative']['gram']
    if [row[:9] for row in k10[:9]] != k9:
        raise ValueError('The original K10 prefix is not the independently recorded K9')
    g8 = [row[:8] for row in k9[:8]]
    if any(value % 3 for row in g8 for value in row):
        raise ValueError('The displayed scaled E8 block is not divisible by 3')
    expected = {'K9': {'determinant': 21870, 'minimum': 6, 'theta_shells': {'6': 258}}}
    for key, source_name in [('K10', 'K10_original'), ('K10_alt', 'K10_alternative')]:
        entry = by_name[source_name]
        expected[key] = {field: entry[field] for field in
                         ['determinant', 'minimum', 'rank_mod_3', 'rank_mod_5', 'theta_shells']}
        expected[key]['dual_minimum'] = '2/5'
        expected[key]['dual_minimal_vectors'] = 6
    expected['K10']['smith_diagonal'] = [1, 1, 1, 1, 3, 3, 3, 3, 15, 45]
    expected['K10_alt']['smith_diagonal'] = [1, 1, 1, 3, 3, 3, 3, 3, 15, 15]
    expected['E8'] = {'determinant': 1, 'minimum': 2,
                      'theta_shells': {'2': 240, '4': 2160, '6': 6720, '8': 17520},
                      'mod3_class_minimum_distribution': {'0': 1, '2': 240, '4': 2160,
                                                          '6': 2240, '8': 1920}}
    result = {
        'schema': 1,
        'convention': 'Matrices are Gram matrices. Squared norm is x^T G x.',
        'matrices': {'K9': k9, 'K10': k10, 'K10_alt': alternative, 'G8': g8,
                     'E8': [[value // 3 for value in row] for row in g8]},
        'expected': expected,
        'provenance': [{'path': path.relative_to(REPOSITORY).as_posix(),
                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                       for path in [rank9_path, rank10_path]],
        'expected_value_provenance': {
            'rank9': 'Recorded claim; source matrix is read as an AST literal, not executed.',
            'rank10_shells': 'Copied as expected answers from the archived rank10 certificate.',
            'smith_and_dual': 'Expected values stated in the manuscript; recomputed independently.',
            'E8': 'Expected E8 shell and mod-3-class counts; not used to generate candidates.'},
    }
    destination = HERE / 'data' / 'lattices.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(destination)
    print('INPUT_EXPORT_PASS')


if __name__ == '__main__':
    main()
