"""Independent exact arithmetic for the strict rank-ten flag windows."""
from fractions import Fraction as Q
from pathlib import Path
import json

def floorroot(q,k):
 lo=0;hi=1
 while hi**k<=q:hi*=2
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**k<=q:lo=mid
  else:hi=mid
 assert lo**k<=q<(lo+1)**k
 return lo

upper={10:54672};raw={9:floorroot(Q(2**45*54672**36),40)}
upper[9]=raw[9]-raw[9]%2
gamma_powers={2:Q(4,3),3:Q(2),4:Q(4),5:Q(8),6:Q(64,3),7:Q(64),8:Q(256),9:Q(512)}
for rank in range(9,1,-1):
 lowrank=rank-1
 raw[lowrank]=floorroot(gamma_powers[rank]*upper[rank]**lowrank,rank)
 v=raw[lowrank]
 if lowrank%2:v-=v%2
 else:
  while v%4 not in (0,(-1)**(lowrank//2)%4):v-=1
 upper[lowrank]=v
assert upper=={1:6,2:44,3:210,4:789,5:2492,6:6459,7:13938,8:24673,9:40054,10:54672}
lower={1:6}
for rank in range(2,10):
 q=Q(6**rank)/gamma_powers[rank]
 v=-(-q.numerator//q.denominator)
 if rank%2:v+=v%2
 else:
  while v%4 not in (0,(-1)**(rank//2)%4):v+=1
 lower[rank]=v
assert lower=={1:6,2:27,3:108,4:324,5:972,6:2187,7:4374,8:6561,9:19684}
assert 54675%4==3 and max(x for x in range(54675)if x%4 in (0,3))==54672
assert 6561%4==1 and min(x for x in range(6562,6570)if x%4 in(0,1))==6564

root=Path(__file__).resolve().parents[1]
final=json.loads((root/'rank10/early_flags/rank9_lifting_prunes.json').read_text())
ratios=[]
for pi,ci,d8,d9,lhs,rhs in final['prunes']:
 assert lhs==3*d9*d9 and rhs==4*d8*54672 and lhs>rhs
 ratios.append(Q(lhs,4*d8))
assert len(ratios)==3819 and min(ratios)==Q(12966723,212)>54672
out={'status':'PASS','strict_upper_windows':upper,'raw_floors':raw,'hermite_lower_windows':lower,
     'restricted_lower_rank8':6564,'previous_gap_based_lower_rank9':24452,
     'final_lifting_records':len(ratios),'minimum_required_rank10_determinant':str(min(ratios)),
     'external_input':'gamma9<=2, together with Mordell gamma10<=gamma9^(9/8)',
     'scope':'Exact windows and final lifting arithmetic; not a replay of all parent extension searches.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
