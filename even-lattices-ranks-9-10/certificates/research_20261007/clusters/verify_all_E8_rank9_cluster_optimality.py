#!/usr/bin/env python3
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
assert F(6561,21870)==F(3,10)
assert [comb(9+r,r) for r in [2,3,4,8]]==[55,220,715,24310]
assert F(6,40)==F(3,20)
assert (6+39*F(2,3))/40==F(4,5)
checks={
 'one_fiber_global':2*F(39,40)**39,
 'singletons_below_4_over_3':81*F(8,9)**39,
 'multiple_fiber_below_4_over_3':F(1600,9)*F(13,15)**39,
 'heavy_4_over_3_to_3_over_2':F(439,4)**2*F(7,9)**39,
 'heavy_3_over_2_to_2':148**2*F(3,4)**39,
 'diameter_2_to_8_over_3':880**2*F(2,3)**39,
 'diameter_8_over_3_to_3':F(12155,4)**2*F(5,9)**39,
 'diameter_3_to_6':133705**2*F(1,2)**39,
}
for value,upper in [(F(5,9),F(3,4)),(F(5),F(9,4)),(F(20,9),F(3,2)),(F(20,3),F(8,3)),(F(80,9),F(3)),(F(10),F(13,4)),(F(20),F(9,2))]:assert value<upper**2
assert 55+46*F(3,4)+9*F(9,4)==F(439,4)
assert 55+46*F(3,2)+9*F(8,3)==148
assert 715*(1+F(13,4))==F(12155,4)
assert 24310*(1+F(9,2))==133705
for name,v in checks.items():assert 0<v<=81*F(8,9)**39<1,(name,v)
out={'claim':'No cluster over any primitive sqrt(3)E8-containing rank-nine lattice of minimum >=6 improves the bare determinant-21870 packing at the guaranteed radius. Equality only singleton and determinant21870.','exact_squared_bounds':{k:str(v) for k,v in checks.items()},'display_only_unsquared_bounds':{k:float(v)**.5 for k,v in checks.items()},'status':'ALL_EXACT_CHECKS_PASS'}
Path(__file__).with_name('all_E8_rank9_cluster_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
