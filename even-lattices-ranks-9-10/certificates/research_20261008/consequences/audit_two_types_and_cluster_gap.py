#!/usr/bin/env python3
"""Independent exact E8-pair orbit and quantitative cluster audit.

Uses its own rational LDL recursion and matrix arithmetic, never imports the
original lattice kernel or equality verifier. Input is the displayed pair
of ten-dimensional Gram matrices. Does not establish global E8 containment.
"""
from collections import Counter, deque
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'research_20261007/rank10/rank10_e8_certificate.json'
data = json.loads(SOURCE.read_text())
G0, G1 = [x['gram'] for x in data['examples']]
C = [[v // 3 for v in row[:8]] for row in G0[:8]]
assert all(3*C[i][j] == G0[i][j] for i in range(8) for j in range(8))

def mv(A, x): return [sum(a*b for a,b in zip(row,x)) for row in A]
def tr(A): return [list(row) for row in zip(*A)]
def mm(A, B): return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def dot(x,y): return sum(a*b for a,b in zip(x,y))
def inv(A):
    n=len(A); B=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if B[i][j])
        B[j],B[pivot]=B[pivot],B[j]
        d=B[j][j];B[j]=[v/d for v in B[j]]
        for i in range(n):
            if i!=j:
                q=B[i][j];B[i]=[x-q*y for x,y in zip(B[i],B[j])]
    return [row[n:] for row in B]
def gram(u,v):
    p=mv(C,u);q=mv(C,v);cross=F(dot(u,q)+5,3)
    assert cross.denominator==1
    return [[3*C[i][j] for j in range(8)]+[p[i],q[i]] for i in range(8)]+[p+[6,int(cross)],q+[int(cross),6]]
def modrank(A,p):
    B=[[v%p for v in row] for row in A];n=len(B);r=0
    for j in range(len(B[0])):
        piv=next((i for i in range(r,n) if B[i][j]),None)
        if piv is None: continue
        B[r],B[piv]=B[piv],B[r]
        for i in range(r+1,n):
            x,y=B[r][j],B[i][j]
            B[i]=[(x*a-y*b)%p for a,b in zip(B[i],B[r])]
        r+=1
    return r

def enumerate_exact(A,bound):
    """Separate dimension-general rational ellipsoid enumeration."""
    n=len(A);B=[[F(i==j) for j in range(n)] for i in range(n)];diagonal=[]
    for i in range(n):
        d=F(A[i][i])-sum(B[i][h]**2*diagonal[h] for h in range(i))
        assert d>0;diagonal.append(d)
        for k in range(i+1,n):
            B[k][i]=(F(A[k][i])-sum(B[k][h]*B[i][h]*diagonal[h] for h in range(i)))/d
    current=[0]*n;answer=[]
    def visit(k,left):
        if k<0:
            answer.append((current[:],bound-left));return
        center=-sum(B[h][k]*current[h] for h in range(k+1,n))
        den=center.denominator;num=center.numerator;r2=left/diagonal[k]
        rad=math.isqrt(r2.numerator*den*den//r2.denominator)
        for v in range(-((-(num-rad))//den),(num+rad)//den+1):
            current[k]=v;visit(k-1,left-diagonal[k]*(v-center)**2)
    visit(n-1,F(bound))
    return answer,math.prod(diagonal)

# Complete independent ellipsoid enumeration: all E8 vectors of norm <=8.
L=[[F(i==j) for j in range(8)] for i in range(8)];D=[]
for i in range(8):
    d=F(C[i][i])-sum(L[i][h]**2*D[h] for h in range(i))
    assert d>0;D.append(d)
    for k in range(i+1,8):
        L[k][i]=(F(C[k][i])-sum(L[k][h]*L[i][h]*D[h] for h in range(i)))/d
assert math.prod(D)==1 and all(C[i][i]==2 for i in range(8))
x=[0]*8;mins={};reps={};roots=[];shells=Counter()
def rec(k,left):
    if k<0:
        norm=8-left;key=tuple(v%3 for v in x);shells[int(norm)]+=1
        if norm==2: roots.append(x[:])
        if key not in mins or norm<mins[key]: mins[key]=norm;reps[key]=x[:]
        return
    center=-sum(L[h][k]*x[h] for h in range(k+1,8))
    den=center.denominator;num=center.numerator;r2=left/D[k]
    rad=math.isqrt(r2.numerator*den*den//r2.denominator)
    low=-((-(num-rad))//den);high=(num+rad)//den
    for v in range(low,high+1):
        x[k]=v;rec(k-1,left-D[k]*(v-center)**2)
rec(7,F(8))
assert shells=={0:1,2:240,4:2160,6:6720,8:17520}
assert len(mins)==6561 and Counter(mins.values())=={0:1,2:240,4:2160,6:2240,8:1920}
deep={a for a,q in mins.items() if q==8}
Ci=inv(C);w=mv(Ci,[G0[i][8] for i in range(8)]);v0=mv(Ci,[G0[i][9] for i in range(8)])
assert all(z.denominator==1 for z in w+v0)
w=list(map(int,w));v0=list(map(int,v0))
assert dot(w,mv(C,w))==dot(v0,mv(C,v0))==8
assert gram(w,v0)==G0 and gram(w,[-t for t in w])==G1
a=tuple(t%3 for t in w);b0=tuple(t%3 for t in v0);minus_a=tuple(-t%3 for t in a)
reps[b0]=v0

reflections=[]
for root in roots:
    if next(t for t in root if t)<0: continue
    cr=mv(C,root)
    R=[[int(i==j)-root[i]*cr[j] for j in range(8)] for i in range(8)]
    assert mm(mm(tr(R),C),R)==C
    assert mm(R,R)==[[int(i==j) for j in range(8)] for i in range(8)]
    # det(I-r(Cr)^t)=1-r^tCr=-1, so R is integral unimodular.
    assert dot(root,cr)==2
    reflections.append(R)
assert len(reflections)==120
basis_reflections=[]
for i in range(8):
    R=[[int(h==k)-int(h==i)*C[i][k] for k in range(8)] for h in range(8)]
    assert mm(mm(tr(R),C),R)==C
    basis_reflections.append(R)

def key(A,x): return tuple(v%3 for v in mv(A,x))
seen={a};queue=deque([a])
while queue:
    t=queue.popleft()
    for R in basis_reflections:
        nxt=key(R,t);assert nxt in deep
        if nxt not in seen: seen.add(nxt);queue.append(nxt)
assert seen==deep
allowed={b for b in deep if tuple((x-y)%3 for x,y in zip(a,b)) in deep}
stabilizer=[R for R in reflections if key(R,a)==a]
assert len(allowed)==561 and len(stabilizer)==36 and minus_a in allowed
assert all(key(R,minus_a)==minus_a for R in stabilizer)

# Verify every tree edge by a full integral 10x10 Gram congruence.
seen={b0};queue=deque([b0]);edges=[]
while queue:
    b=queue.popleft();v=reps[b]
    for index,R in enumerate(stabilizer):
        nxt=key(R,b);assert nxt in allowed
        if nxt in seen: continue
        vp=reps[nxt]
        numer1=[p-q for p,q in zip(mv(R,w),w)]
        numer2=[p-q for p,q in zip(mv(R,v),vp)]
        assert all(t%3==0 for t in numer1+numer2)
        shift1=[t//3 for t in numer1];shift2=[t//3 for t in numer2]
        U=[row+[shift1[i],shift2[i]] for i,row in enumerate(R)]+[[0]*8+[1,0],[0]*8+[0,1]]
        # Its determinant is det R=-1 by the block triangular form.
        assert mm(mm(tr(U),gram(w,vp)),U)==gram(w,v)
        seen.add(nxt);queue.append(nxt)
        edges.append({'source_class':b,'target_class':nxt,'stabilizing_reflection':index,'map':U})
assert seen==allowed-{minus_a} and len(seen)==560 and len(edges)==559
assert modrank(G0,3)==4 and modrank(G1,3)==3

# Direct dual enumeration, independent of the projection argument. Every
# shortest dual vector has integral pairing column a; its physical norm is
# a^t G^{-1} a. All six columns vanish on the displayed E8 sublattice.
dual_records=[]
for name,G in [('original',G0),('alternative',G1)]:
    Gi=inv(G);points,detinv=enumerate_exact(Gi,F(2,5))
    assert detinv==F(1,54675)
    assert Counter(q for x,q in points)=={F(0):1,F(2,5):6}
    normals=[x for x,q in points if q]
    assert all(x[:8]==[0]*8 and math.gcd(*x)==1 for x in normals)
    expected={(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1)}
    assert {tuple(x[-2:]) for x in normals}==expected
    kernels=[]
    for normal in normals:
        if next(v for v in normal if v)<0:continue
        aa,bb=normal[-2:]
        # gcd(aa,bb)=1, so the full primitive kernel basis is J followed
        # by bb*e9-aa*e10. This spans every integer solution aa*x9+bb*x10=0.
        basis=[[int(i==j) for i in range(10)] for j in range(8)]+[[0]*8+[bb,-aa]]
        H=mm(mm(basis,G),tr(basis));short,dH=enumerate_exact(H,F(6))
        assert dH==21870 and Counter(q for x,q in short)=={F(0):1,F(6):258}
        kernels.append({'primitive_dual_pairing':normal,'basis_rows':basis,'gram':H,'determinant':int(dH),'minimum':6,'norm6_vectors':258})
    assert len(kernels)==3
    dual_records.append({'type':name,'dual_minimum':'2/5','dual_minimal_vectors_in_dual_basis':normals,'dual_minimum_span_rank':2,'primitive_rank9_subsections':kernels})

# Exact uniform bound from the previously proved geometric interval table.
rows=[(F(2,5),3),(F(2,3),9),(F(23,30),11),(F(29,30),27),(F(6,5),36),(F(4,3),82),(F(8,5),109),(F(49,30),385),(F(2),1540),(F(8,3),54675)]
uniform=9*F(8,9)**19
assert uniform<1
comparisons=[]
for left,B in rows:
    bound=B*(1-left/6)**19
    assert bound<=uniform
    comparisons.append({'left_endpoint':str(left),'cardinality_bound':B,'density_bound':str(bound),'at_most_uniform':True})

output={'status':'PASS','scope':'E8-containing equality classification and cluster table; global E8 containment is a separate input','input_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'independent_shell_counts':dict(shells),'deep_classes':1920,'transitivity_generators':8,'allowed_second_classes':561,'stabilizing_root_reflections':36,'second_class_orbits':[560,1],'explicit_integral_10x10_isometries':559,'rank_mod3':[4,3],'intrinsic_structure':dual_records,'uniform_cluster_factor_exact':str(uniform),'uniform_cluster_factor_decimal':float(uniform),'uniform_loss_decimal':float(1-uniform),'endpoint_comparisons':comparisons,'orbit_edges':edges}
Path(__file__).with_suffix('.json').write_text(json.dumps(output,indent=2)+'\n')
print('INDEPENDENT_TWO_TYPES_AND_UNIFORM_CLUSTER_GAP_PASS')
print('559 explicit lifted rank10 isometries; orbit sizes 560 and 1; Gram ranks mod3 4 and 3')
print('Each dual: min=2/5, exactly six minima; three primitive rank9 kernels, determinant21870 and minimum6')
print('Uniform nontrivial-cluster ratio <=',uniform,'=',float(uniform))
