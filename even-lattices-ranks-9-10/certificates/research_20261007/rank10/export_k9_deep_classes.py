#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from math import gcd,lcm
import json
from exact_lattice import enumerate_vectors,determinant,qform,bilinear
from verify_rank9_extremal_example_exact import K9
from verify_rank10_e8_classification import inverse,mv
C=[[K9[i][j]//3 for j in range(8)]for i in range(8)]
p=[r[-1]for r in K9[:8]];w=tuple(int(x)for x in mv(inverse(C),p));a=tuple(x%3 for x in w)
mins={};witness={}
for v,q in enumerate_vectors(C,8):
    b=tuple(x%3 for x in v)
    if b not in mins or q<mins[b]:mins[b]=q;witness[b]=v
D=determinant(K9);Gi=inverse(K9);adj=[[int(D*x)for x in row]for row in Gi]
deep={b for b,q in mins.items()if q==8};allowed={b for b in deep if tuple((x-y)%3 for x,y in zip(b,a))in deep}
assert len(allowed)==561
rows=[];keys=set();orders=Counter()
for b in sorted(allowed):
    v=witness[b];inner=bilinear(C,w,v);assert (inner+5)%3==0
    r=tuple(mv(C,v))+((inner+5)//3,)
    assert qform(Gi,r)==F(7,2)
    key=tuple(x%D for x in mv(adj,r));assert key not in keys;keys.add(key)
    neg=tuple(-x%D for x in key)
    order=lcm(*(D//gcd(D,x)for x in key));orders[order]+=1
    rows.append({'E8_residue_b':b,'E8_norm8_witness':v,'pairing_column':r,'class_fingerprint_mod_D':key,'order':order,'canonical_mod_sign':key<=neg})
assert orders=={2:1,6:560}
assert sum(x['canonical_mod_sign']for x in rows)==281
out=Path(__file__).with_name('k9_deep_class_pairings.json')
out.write_text(json.dumps({'K9':K9,'determinant':D,'class_minimum':'7/2','count':len(rows),'order_counts':dict(orders),'unoriented_count':281,'classes':rows},indent=2)+'\n')
print('EXACT_K9_DEEP_CLASSES',len(rows),'ORDERS',dict(orders),'MOD_SIGN',281)
