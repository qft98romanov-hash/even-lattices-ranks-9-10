#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json
# Critical points of sqrt(beta)*(1-beta/6)^19 and beta*(1-beta/6)^19.
assert F(6,39)==F(2,13)
assert F(6,20)==F(3,10)
# Exact constants in the geometric comparisons.
assert F(3,2)**2*3 < F(8,3)**2
assert 2<F(8,3)
assert F(22,7)<F(16,5)  # Classical pi<22/7 implies needed majorant.
assert F(5,6)*F(16,5)==F(8,3)
assert F(5,1)**2/F(3)*4/F(10,3)==10
assert (6+38*F(2,3))/39==F(94,117)
assert F(94,117)-F(2,3)==F(16,117)
assert 1-F(94,117)/6==F(304,351)
values={'collinear_squared':F(20,13)*F(38,39)**38,'noncollinear_squared':F(16,3)*F(19,20)**38,'mixed_all_collinear_small_diameter_squared':1620*F(16,117)*F(304,351)**38,'mixed_singletons_small_diameter_squared':81*F(8,9)**38}
assert all(0<v<1 for v in values.values())
out={'scope':'All determinants, rank10 containing sqrt(3)E8: nontrivial one-projection clusters; also beta<4/3 clusters whose every non-singleton fiber is collinear. Does not cover general mixed fibers.','exact_ratio_bounds_squared':{k:str(v) for k,v in values.items()},'display_only_ratio_bounds':{k:float(v)**.5 for k,v in values.items()},'status':'ALL_EXACT_CHECKS_PASS'}
Path(__file__).with_name('rank10_single_projection_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
