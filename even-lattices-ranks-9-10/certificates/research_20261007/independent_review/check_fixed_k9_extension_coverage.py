"""Separate exact coverage and distinctness checks; does not rerun the CVP tree."""
import json,math,random
from pathlib import Path
from fractions import Fraction as F
from collections import Counter

def tr(a):return[list(r)for r in zip(*a)]
def mm(a,b):return[[sum(x*y for x,y in zip(r,c))for c in zip(*b)]for r in a]
def mv(a,v):return[sum(x*y for x,y in zip(r,v))for r in a]
def q(a,v):return sum(x*y for x,y in zip(v,mv(a,v)))
def determinant(a):
 a=[[F(x)for x in r]for r in a];d=F(1);n=len(a)
 for j in range(n):
  k=next((k for k in range(j,n)if a[k][j]),None)
  if k is None:return 0
  if k!=j:a[k],a[j]=a[j],a[k];d=-d
  p=a[j][j];d*=p
  for k in range(j+1,n):
   t=a[k][j]/p
   for h in range(j+1,n):a[k][h]-=t*a[j][h]
   a[k][j]=0
 return d

def inv(a):
 n=len(a);m=[[F(x)for x in r]+[F(i==j)for j in range(n)]for i,r in enumerate(a)]
 for j in range(n):
  k=next(k for k in range(j,n)if m[k][j]);m[k],m[j]=m[j],m[k]
  p=m[j][j];m[j]=[x/p for x in m[j]]
  for k in range(n):
   if k!=j:
    p=m[k][j];m[k]=[x-p*y for x,y in zip(m[k],m[j])]
 return[r[n:]for r in m]

# A gcd-one collection of maximal minors suffices for primitivity, even
# without exhaustive minors or a Smith-normal-form routine.
def primitive_minors(a,seed):
 r=len(a);n=len(a[0]);rr=random.Random(seed);gcd=0;witness=[]
 for unused in range(10000):
  cols=sorted(rr.sample(range(n),r));d=int(determinant([[row[i]for i in cols]for row in a]))
  old=gcd;gcd=math.gcd(gcd,d)
  if gcd!=old:witness.append({'columns':cols,'determinant':d})
  if gcd==1:return witness
 raise AssertionError(('did not find gcd-one minors',gcd))

ROOT=Path(__file__).resolve().parents[1];P=ROOT/'embeddings'
j=json.loads((P/'all_fixed_K9_extension_inputs.json').read_text())
m=json.loads((P/'printed_matrices.json').read_text())
G=m['P48p_G'];T=m['P48p_T9'];A=mm(T,G);K=mm(A,tr(T))
assert determinant(K)==21870
C=[[x//3 for x in row[:8]]for row in K[:8]]
assert[[3*x for x in row]for row in C]==[row[:8]for row in K[:8]]
assert determinant(C)==1
ci=inv(C);ki=inv(K);p=[row[8]for row in K[:8]];a=tuple(int(x)%3 for x in mv(ci,p))

# Own rational LDL ellipsoid enumeration in rank eight, including the origin.
H=[[F(v)for v in row]for row in C]
L=[[F(i==h)for h in range(8)]for i in range(8)];D=[]
for i in range(8):
 d=H[i][i]-sum(L[i][h]**2*D[h]for h in range(i));assert d>0;D.append(d)
 for k in range(i+1,8):L[k][i]=(H[k][i]-sum(L[k][h]*L[i][h]*D[h]for h in range(i)))/d
x=[0]*8;best={};bestrep={};vectors=0

def rec(k,left):
 global vectors
 if k<0:
  value=F(8)-left;key=tuple(z%3 for z in x);vectors+=1
  if key not in best or value<best[key]:best[key]=value;bestrep[key]=x[:]
  return
 center=-sum(L[h][k]*x[h]for h in range(k+1,8));rad2=left/D[k]
 den=center.denominator;num=center.numerator
 rr=math.isqrt(rad2.numerator*den*den//rad2.denominator)
 lo=-((-(num-rr))//den);hi=(num+rr)//den
 for v in range(lo,hi+1):x[k]=v;rec(k-1,left-D[k]*(v-center)**2)
rec(7,F(8))
assert len(best)==6561
assert Counter(best.values())=={0:1,2:240,4:2160,6:2240,8:1920}
deep={b for b,v in best.items()if v==8}
def mate(b):return tuple((x-y)%3 for x,y in zip(a,b))
allowed={b for b in deep if mate(b)in deep};assert len(allowed)==561
assert len([b for b in allowed if mate(b)==b])==1
covered=set();keys=set()
for case in j['cases']:
 b=tuple(case['class_E8']);c=tuple(case['mate_E8'])
 assert b in allowed and c==mate(b)and not({b,c}&covered);covered|={b,c}
 target=case['target'];v=mv(ci,target[:8])
 assert all(z.denominator==1 for z in v)
 assert tuple(int(z)%3 for z in v)==b and q(C,v)==8
 assert 3*target[8]==sum(x*y for x,y in zip(p,v))+5
 z=mv(ki,target);assert sum(x*y for x,y in zip(target,z))==F(7,2)
 key=tuple(t%1 for t in z);neg=tuple(-t%1 for t in key)
 # Reconstruct a target for the mate using our independently chosen shortest
 # representative and verify that its K9-dual class is exactly the negative.
 vm=bestrep[c];last=F(sum(x*y for x,y in zip(p,vm))+5,3)
 assert last.denominator==1
 tm=mv(C,vm)+[int(last)];zm=mv(ki,tm)
 assert sum(x*y for x,y in zip(tm,zm))==F(7,2)
 assert tuple(t%1 for t in zm)==neg
 assert key not in keys and neg not in keys;keys|={key,neg}
 assert case['order']==math.lcm(*(t.denominator for t in key))
assert covered==allowed and len(keys)==561 and len(j['cases'])==281

# Reconstruct all integer ambient vectors from the C++ log and check them.
# Enumeration exhaustiveness is audited elsewhere; this verifies each reported
# witness, a separate primitivity certificate, and lattice distinction.
B=j['basis_B'];normalkeys=set();solutions=[];stats={}
for line in(P/'search_all_fixed_K9_extensions.log').read_text().splitlines():
 z=line.split()
 if z[0]=='CASE':stats[int(z[1])]=(int(z[3]),int(z[5]),int(z[7]))
 if z[0]!='EXACT_NORM6_WITNESS':continue
 caseid=int(z[1]);coeff=[int(t)for t in z[2:]];case=j['cases'][caseid]
 w=[x+y for x,y in zip(case['lift_w0'],mv(tr(B),coeff))];target=case['target']
 assert mv(A,w)==target and q(G,w)==6
 TT=T+[w];gram=mm(mm(TT,G),tr(TT));assert determinant(gram)==54675
 minors=primitive_minors(TT,caseid)
 proj=mv(tr(T),mv(ki,target));normal=[x-y for x,y in zip(w,proj)]
 assert mv(A,normal)==[0]*9 and q(G,normal)==F(5,2)
 nn=[21870*x for x in normal];assert all(t.denominator==1 for t in nn)
 key=tuple(int(t)for t in nn);neg=tuple(-t for t in key)
 assert key not in normalkeys and neg not in normalkeys;normalkeys|={key,neg}
 assert case['order']==6
 solutions.append({'case_id':caseid,'normal_numerator':list(key),'gcd_one_maximal_minor_witnesses':minors})
assert len(stats)==281 and len(solutions)==19 and len(normalkeys)==38
assert tuple(sum(s[i]for s in stats.values())for i in range(3))==(171472428,19,19)
out={'status':'PASS','independent_e8_vectors':vectors,'e8_classes':6561,'admissible_classes':561,'involution_orbits':281,'reported_norm6_vectors_checked':19,'distinct_unoriented_normals':19,'primitive_rank10_lattices':19,'solutions':solutions,'scope':'Coverage and witness/dedup audit; full CVP tree not rerun here.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print('E8_CLASS_COVERAGE_561_TO_281_AND_19_DISTINCT_PRIMITIVE_AMBIENT_SUPERSECTIONS_PASS')
