#!/usr/bin/env python3
"""Exact witnesses/orbits for corollaries of the completed global prefix.
The absence statements use the audited global prefix and gamma9<=2.
"""
from pathlib import Path
from collections import deque,Counter
import json
from exact_lattice import determinant,ldl,enumerate_vectors
from verify_rank9_extremal_example_exact import K9
from verify_rank10_e8_classification import mv
here=Path(__file__).parent
C=[[K9[i][j]//3 for j in range(8)]for i in range(8)]
pts=enumerate_vectors(C,8);mins={};wit={}
for v,q in pts:
 a=tuple(x%3 for x in v)
 if a not in mins or q<mins[a]:mins[a]=int(q);wit[a]=v
assert len(mins)==6561
roots=[r for r,q in pts if q==2 and next(x for x in r if x)>0]
reflection=[(r,mv(C,r))for r in roots]
def orbit(a,domain):
 seen={a};queue=deque([a])
 while queue:
  x=queue.popleft()
  for r,cr in reflection:
   b=sum(xi*ci for xi,ci in zip(x,cr))%3
   y=tuple((xi-b*ri)%3 for xi,ri in zip(x,r))
   assert y in domain
   if y not in seen:seen.add(y);queue.append(y)
 return seen
rows=[]
for q,target_det,count in [(8,21870,258),(6,26244,246),(4,30618,242)]:
 domain={a for a,v in mins.items()if v==q};a=min(domain)
 assert orbit(a,domain)==domain
 w=wit[a];p=list(mv(C,w));G=[list(row[:8])+[p[i]]for i,row in enumerate(K9[:8])]+[p+[6]]
 assert determinant(G)==target_det;ldl(G)
 vv=enumerate_vectors(G,6,include_zero=False);assert min(v for _,v in vv)==6 and len(vv)==count
 rows.append({'determinant':target_det,'class_norm_unscaled':q,'class_orbit_size':len(domain),'gram':G,'minimum':6,'minimal_vector_count':count})
example=None
for path in sorted((here/'early_flags'/'rank9_parents').glob('parent_*.json')):
 for g in json.loads(path.read_text())['representatives']:
  if determinant(g)==32076:example=g;break
 if example is not None:break
assert example is not None
ldl(example);vv=enumerate_vectors(example,6,include_zero=False)
assert min(q for _,q in vv)==6 and 32076%(2*3**7)!=0
payload={'assumption':'gamma9<=2 plus completed new global-prefix certificate','rank9_determinants_below_32076':[21870,26244,30618],'one_isometry_class_at_each_of_these_three_determinants':True,'examples':rows,'smallest_rank9_determinant_without_sqrt3E8':32076,'no_E8_example':{'gram':example,'determinant':32076,'minimum':6,'minimal_vector_count':len(vv),'nondivisibility_mod_4374':32076%(2*3**7)}}
(here/'rank9_low_spectrum.json').write_text(json.dumps(payload,indent=2)+'\n')
print('RANK9_LOW_SPECTRUM',[(r['determinant'],r['class_orbit_size'],r['minimal_vector_count'])for r in rows])
print('SMALLEST_NO_E8_RANK9',32076,'KISSING',len(vv),'MOD4374',32076%4374)
print('RANK9_LOW_SPECTRUM_EXACT_WITNESSES_AND_ORBITS_PASS')
