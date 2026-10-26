"""Independent exact arithmetic replay of the arbitrary-determinant E8-fiber bound.

No imports from the proposed cluster verifier. Geometric deductions are audited
in all_e8_rank9_cluster_review.md; no finite search certifies those deductions.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json

assert Q(6561,21870)==Q(3,10)
counts={r:sum(comb(8+j,j)for j in range(r+1))for r in (2,3,4,8)}
assert counts=={2:55,3:220,4:715,8:24310}

# g(beta)^2=(beta-c)*(1-beta/6)^39. Its derivative has the sign
# of 6+39c-40beta throughout c<beta<6. The critical point is unique.
def square_max(c):
    beta=(6+39*c)/40
    assert c<beta<6
    return beta,(beta-c)*(1-beta/6)**39

b0,g0=square_max(Q(0));b1,g1=square_max(Q(2,3))
assert b0==Q(3,20)and b1==Q(4,5)
results={'one_projection':Q(40,3)*g0,
         'all_singleton_fibers_small_diameter':81*Q(8,9)**39,
         'multiple_fibers_small_diameter':Q(4000,3)*g1}
assert results['one_projection']==2*Q(39,40)**39
assert results['multiple_fibers_small_diameter']==Q(1600,9)*Q(13,15)**39

# For integers t>=2,u>=1,M>=2, (M+1)(t+u-2)-[t+(M-1)u]
# equals M(t-2)+2(u-1), so the fiber size inequality holds identically.
# Coefficients of t,u,constant on both sides are checked symbolically.
for M in range(2,10):
    assert (M+1-1,(M+1)-(M-1),-2*(M+1))==(M,2,-2*M-2)

# Each row supplies endpoint majorants for the square roots, followed by
# exact rational comparison of the resulting squared density ratio with 1.
heavy=[(Q(4,3),Q(3,2),Q(3,4),Q(9,4)),
       (Q(3,2),Q(2),Q(3,2),Q(8,3))]
for left,right,a,b in heavy:
    assert Q(10,3)*(right-Q(4,3))<a*a
    assert Q(10,3)*right<b*b
    B=55+46*a+9*b
    results[f'heavy_{left}_to_{right}']=B*B*(1-left/6)**39
large=[(Q(2),Q(8,3),3,220),(Q(8,3),Q(3),Q(13,4),715),
       (Q(3),Q(6),Q(9,2),24310)]
for left,right,a,M in large:
    assert Q(10,3)*right<a*a
    B=M*(1+a)
    results[f'large_{left}_to_{right}']=B*B*(1-left/6)**39
assert len(results)==8
assert all(0<v<1 for v in results.values())
out={'status':'PASS','exact_squared_bounds':{k:str(v)for k,v in results.items()},
     'maximum_of_case_bounds_squared':str(max(results.values())),
     'scope':'All finite clusters in duals of all rank-nine even minimum-six lattices containing sqrt(3)E8, arbitrary determinant; guaranteed antipode radius only.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
