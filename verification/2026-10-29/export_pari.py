#!/usr/bin/env python3
"""Export exact Gram matrices to PARI/GP literals; no mathematical verification."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'data/lattices.json').read_text())
lines = ['\\\\ Generated from data/lattices.json by export_pari.py.']
for name in ('K9', 'K10', 'K10_alt', 'E8'):
    rows = data['matrices'][name]
    literal = '[' + ';'.join(','.join(map(str, row)) for row in rows) + ']'
    lines.append(f'{name} = {literal};')
(ROOT / 'data/pari_inputs.gp').write_text('\n'.join(lines) + '\n')
print('Wrote data/pari_inputs.gp')
