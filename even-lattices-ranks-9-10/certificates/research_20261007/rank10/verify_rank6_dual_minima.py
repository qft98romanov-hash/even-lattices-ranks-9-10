#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import json
from exact_lattice import determinant,enumerate_vectors
from extend_flag import inverse
here=Path(__file__).parent/'early_flags'
parents=json.loads((here/'rank6_fast.json').read_text())['representatives']
checked=[];active=[]
for i,g in enumerate(parents):
    d=determinant(g);d5=determinant([row[:5]for row in g[:5]])
    target=F(d5,d)
    points=enumerate_vectors(inverse(g),target,include_zero=False)
    assert points and min(q for _,q in points)==target
    checked.append({'parent':i,'d6':d,'d5':d5,'dual_minimum':str(target),'boundary_vectors':len(points)})
    if 3*d*d<=4*d5*13938:active.append(i)
    if i%500==0:print('CHECKED',i,flush=True)
saved=json.loads((here/'rank7_active_parents.json').read_text())['active']
assert active==[r[0]for r in saved]
(here/'rank6_dual_minima_verified.json').write_text(json.dumps({'count':len(checked),'records':checked},indent=2)+'\n')
print('ALL_RANK6_DUAL_MINIMA_EXACT',len(checked),'RANK7_ACTIVE',len(active),'PRUNED',len(checked)-len(active))
