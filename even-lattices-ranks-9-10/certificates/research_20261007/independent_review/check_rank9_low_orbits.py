"""Independent E8 residue orbits and lifted rank-nine isometries.

Uses its own rational ellipsoid enumeration and only the eight basis-root
reflections. No original lattice-enumeration or reflection code is imported.
"""
import json,math
from collections import deque,Counter
from fractions import Fraction as F
from pathlib import Path

def mv(a,v):return[sum(x*y for x,y in zip(row,v))for row in a]
def tr(a):return[list(r)for r in zip(*a)]
def mm(a,b):return[[sum(x*y for x,y in zip(row,col))for col in zip(*b)]for row in a]
def border(g,p):return[row+[p[i]]for i,row in enumerate(g)]+[p+[6]]
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'rank10/rank9_low_spectrum.json').read_text())
G=[row[:8]for row in data['examples'][0]['gram'][:8]]
C=[[v//3 for v in row]for row in G]
assert[[3*v for v in row]for row in C]==G and all(C[i][i]==2 for i in range(8))
L=[[F(i==j)for j in range(8)]for i in range(8)];D=[]
for i in range(8):
 d=F(C[i][i])-sum(L[i][h]**2*D[h]for h in range(i));assert d>0;D.append(d)
 for k in range(i+1,8):L[k][i]=(F(C[k][i])-sum(L[k][h]*L[i][h]*D[h]for h in range(i)))/d
assert math.prod(D)==1
x=[0]*8;mins={};reps={};vectors=0
def rec(k,left):
 global vectors
 if k<0:
  norm=8-left;key=tuple(v%3 for v in x);vectors+=1
  if key not in mins or norm<mins[key]:mins[key]=norm;reps[key]=x[:]
  return
 center=-sum(L[h][k]*x[h]for h in range(k+1,8));den=center.denominator;num=center.numerator;r2=left/D[k]
 rad=math.isqrt(r2.numerator*den*den//r2.denominator)
 for v in range(-((-(num-rad))//den),(num+rad)//den+1):x[k]=v;rec(k-1,left-D[k]*(v-center)**2)
rec(7,F(8))
assert len(mins)==6561 and Counter(mins.values())=={0:1,2:240,4:2160,6:2240,8:1920}
reflections=[]
for i in range(8):
 R=[[int(h==k)-int(h==i)*C[i][k]for k in range(8)]for h in range(8)]
 assert mm(mm(tr(R),G),R)==G
 reflections.append(R)
rows=[]
for norm,expected in [(8,1920),(6,2240),(4,2160)]:
 domain={c for c,q in mins.items()if q==norm};assert len(domain)==expected
 start=min(domain);seen={start};queue=deque([start]);edges=0
 while queue:
  c=queue.popleft();w0=reps[c]
  for R in reflections:
   nxt=tuple(v%3 for v in mv(R,w0));assert nxt in domain
   if nxt in seen:continue
   seen.add(nxt);queue.append(nxt);w1=reps[nxt]
   numer=[u-v for u,v in zip(mv(R,w1),w0)];assert all(v%3==0 for v in numer)
   t=[v//3 for v in numer]
   U=[row+[t[i]]for i,row in enumerate(R)]+[[0]*8+[1]]
   assert mm(mm(tr(U),border(G,mv(C,w0))),U)==border(G,mv(C,w1))
   edges+=1
 assert seen==domain and edges==expected-1
 rows.append({'class_norm':norm,'classes':expected,'orbit_count':1,'lifted_integral_isometries_checked':edges,'determinant':int(6561*(6-F(norm,3)))})
out={'status':'PASS','independent_vectors':vectors,'basis_root_reflections':8,'orbits':rows,'total_lifted_isometries':sum(r['lifted_integral_isometries_checked']for r in rows)}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print('THREE_E8_ORBITS_AND_6317_EXPLICIT_EXTENSION_ISOMETRIES_PASS')
