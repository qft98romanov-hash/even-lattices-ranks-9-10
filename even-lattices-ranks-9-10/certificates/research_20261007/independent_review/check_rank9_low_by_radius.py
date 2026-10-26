"""Independent exclusion of all 47 low rank-nine parent cases.

45 have explicit dual-vector lifting witnesses. The other two are excluded
by independently covering every dual discriminant class with norm <=4.
No original extension or vector-enumeration code is imported.
"""
import json,math
from fractions import Fraction as F
from pathlib import Path

def inverse_and_det(a):
 n=len(a);m=[[F(x)for x in row]+[F(i==j)for j in range(n)]for i,row in enumerate(a)];det=F(1)
 for j in range(n):
  k=next(k for k in range(j,n)if m[k][j])
  if k!=j:m[k],m[j]=m[j],m[k];det=-det
  p=m[j][j];det*=p;m[j]=[x/p for x in m[j]]
  for k in range(n):
   if k!=j:
    p=m[k][j];m[k]=[x-p*y for x,y in zip(m[k],m[j])]
 return[r[n:]for r in m],det

def classes_in_ball(a,d,cap):
 n=len(a);L=[[F(i==j)for j in range(n)]for i in range(n)];D=[]
 for i in range(n):
  q=a[i][i]-sum(L[i][h]**2*D[h]for h in range(i));assert q>0;D.append(q)
  for k in range(i+1,n):L[k][i]=(a[k][i]-sum(L[k][h]*L[i][h]*D[h]for h in range(i)))/q
 adj=[[int(d*x)for x in row]for row in a]
 assert all(F(adj[i][j],d)==a[i][j]for i in range(n)for j in range(n))
 x=[0]*n;seen=set();vectors=0
 def rec(k,left):
  nonlocal vectors
  if k<0:
   seen.add(tuple(sum(v*z for v,z in zip(row,x))%d for row in adj));vectors+=1;return
  center=-sum(L[h][k]*x[h]for h in range(k+1,n));den=center.denominator;num=center.numerator
  r2=left/D[k];r=math.isqrt(r2.numerator*den*den//r2.denominator)
  for v in range(-((-(num-r))//den),(num+r)//den+1):x[k]=v;rec(k-1,left-D[k]*(v-center)**2)
 rec(n-1,F(cap));return len(seen),vectors

root=Path(__file__).resolve().parents[1]
parents=json.loads((root/'rank10/early_flags/rank8_eligible.json').read_text())['representatives']
assert len(parents)==47
out=[]
for i,g in enumerate(parents):
 inv,d=inverse_and_det(g);assert d.denominator==1;d=int(d)
 # The last coordinate unit vector is an explicit nonzero dual vector;
 # its norm supplies a valid lifting obstruction without proving shortestness.
 dualnorm=inv[-1][-1]
 if F(24450,d)*dualnorm<F(3,4):
  out.append({'parent_index':i,'determinant':d,'method':'explicit_dual_lifting','dual_norm':str(dualnorm)})
 else:
  count,vectors=classes_in_ball(inv,d,4)
  assert count==d and 2*d>24450
  out.append({'parent_index':i,'determinant':d,'method':'independent_radius_4_cover','vectors_enumerated':vectors,'classes_covered':count,'rank9_determinant_lower_bound':2*d})
assert sum(r['method']=='explicit_dual_lifting'for r in out)==45
assert {r['parent_index']for r in out if r['method']=='independent_radius_4_cover'}=={20,44}
result={'status':'PASS','target_rank9_window':[19684,24450],'parents':47,'explicit_dual_prunes':45,'independent_discriminant_cover_prunes':2,'records':out}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print('ALL_47_LOW_RANK9_PARENTS_EXCLUDED_INDEPENDENTLY_BY_DUAL_WITNESSES_OR_RADIUS4')
