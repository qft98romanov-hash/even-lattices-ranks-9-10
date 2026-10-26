#!/usr/bin/env python3
"""Independent Python-integer enumeration of the rigorously enclosing fiber.
Default: exclude the prescribed opposite-projection A10 extension.
--control: enumerate the original published K10 extension fiber.
Both modes recompute all rational prerequisites, without trusting float search.
"""
import json,sys,time,math
from pathlib import Path
from fractions import Fraction as F
from verify_ambient_embeddings import mm,tr,det,inv
ROOT=Path(__file__).resolve().parent
control='--control' in sys.argv
prefix='K10_control_exact_cvp' if control else 'A10_exact_cvp'
j=json.loads((ROOT/(prefix+'_input.json')).read_text());m=json.loads((ROOT/'printed_matrices.json').read_text());G=m['P48p_G'];T=m['P48p_T9'];A=mm(T,G);K=mm(A,tr(T));n=j['rank'];B=j['basis_B'];w=j['lift_w0'];C=j['gram_C'];g=j['linear_g'];wn=j['constant_norm'];target=j['target_pairings']
assert mm(A,tr(B))==[[0]*n for _ in T]
assert mm(A,[[x]for x in w])==[[x]for x in target]
assert C==mm(mm(B,G),tr(B)) and det(C)==det(K)==21870
assert g==[r[0]for r in mm(mm(B,G),[[x]for x in w])]
assert wn==mm(mm([w],G),[[x]for x in w])[0][0]
if control:assert target==[r[0]for r in mm(A,[[x]for x in m['P48p_T10'][-1]])]
else:assert target==[-K[i][-1]for i in range(8)]+[-1]
Ci=inv(C);co=[-sum(Ci[i][k]*g[k]for k in range(n))for i in range(n)]
assert F(wn)-sum(F(g[i])*Ci[i][k]*g[k]for i in range(n)for k in range(n))==F(7,2)
L=[[F(x)for x in r]for r in j['exact_L']];D=[F(x)for x in j['exact_D']];y=[F(x)for x in j['exact_y']]
assert all(D[i]>0 and L[i][i]==1 and all(L[i][k]==0 for k in range(i+1,n))for i in range(n))
assert mm(mm(L,[[D[i]if i==k else 0 for k in range(n)]for i in range(n)]),tr(L))==C
assert y==[sum(co[k]*L[k][i]for k in range(i,n))for i in range(n)]
S=j['scale'];df=j['lower_D_scaled'];yr=j['round_y'];lr=j['round_L'];E=j['center_error_scaled'];bounds=j['coefficient_bounds']
for i in range(n):
 assert bounds[i]>=abs(co[i]) and (F(bounds[i])-abs(co[i]))**2>=F(5,2)*Ci[i][i]
 assert 0<F(df[i],S)<=D[i]
 assert abs(F(yr[i],S)-y[i])<=F(1,2*S)
 assert F(E[i],S)>=F(1+sum(bounds[i+1:]),2*S)
 for h in range(n):assert abs(F(lr[h][i],S)-L[h][i])<=F(1,2*S)
# Full kernel follows from primitive T, unimodular ambient, and exact det(C)=det(K).
# Reverify primitiveness of T and ambient unimodularity instead of relying on JSON.
from verify_ambient_embeddings import snf
st,_,_=snf(T);assert [st[i][i]for i in range(9)]==[1]*9
assert det(G)==1
nodes=leaves=0;solutions=[];x=[0]*n;started=time.monotonic()
def rec(k,rem):
 global nodes,leaves
 nodes+=1
 if k<0:
  leaves+=1
  val=wn+2*sum(a*b for a,b in zip(x,g))+sum(x[i]*C[i][h]*x[h]for i in range(n)for h in range(n))
  if val==6:solutions.append(x[:])
  return
 c=yr[k]-sum(x[h]*lr[h][k]for h in range(k+1,n));rad=math.isqrt(rem//df[k])+E[k]
 lo=max(-bounds[k],-(-(c-rad)//S));hi=min(bounds[k],(c+rad)//S)
 for v in range(lo,hi+1):
  z=max(0,abs(S*v-c)-E[k]);term=z*z*df[k]
  if term<=rem:x[k]=v;rec(k-1,rem-term)
rec(n-1,5*S**3//2)
if control:
 assert len(solutions)==1
 sol=solutions[0];ambient=[w[h]+sum(sol[i]*B[i][h]for i in range(n))for h in range(48)]
 assert ambient==m['P48p_T10'][-1]
else:assert not solutions
out={'result':'CERTIFIED_UNIQUE_PUBLISHED_FIBER' if control else 'CERTIFIED_EMPTY_ALTERNATIVE_MARKED_FIBER','nodes':nodes,'leaves':leaves,'norm6_witnesses':len(solutions),'coordinate_solutions':solutions,'elapsed_seconds':time.monotonic()-started,'arithmetic':'Python unbounded integers and fractions; math.isqrt; no floating-point pruning'}
(ROOT/(prefix+'_verified_result.json')).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
