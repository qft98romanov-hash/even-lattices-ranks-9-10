from pathlib import Path
import sys,json,time
from fractions import Fraction as F
from collections import Counter,deque
CERT=Path(__file__).resolve().parents[1]/'recovered/rank9_audit_evidence_20260910/audit_20260910/rank9_complete_certificates/certificate'
sys.path.insert(0,str(CERT))
from exact_lattice import determinant,ldl,enumerate_vectors,qform,bilinear
from verify_rank9_extremal_example_exact import K9
from extend_flag import inverse,matvec
C=[[K9[i][j]//3 for j in range(8)] for i in range(8)]
assert determinant(C)==1
print('ENUM E8',flush=True)
pts=enumerate_vectors(C,8)
mins={};wit={}
for x,q in pts:
    key=tuple(z%3 for z in x)
    if key not in mins or q<mins[key]:mins[key]=q;wit[key]=x
assert len(mins)==6561
D=set(a for a,q in mins.items() if q==8)
roots=[x for x,q in pts if q==2]
print('POINTS',len(pts),'DEEP',len(D),'ROOTS',len(roots),flush=True)
assert len(D)==1920 and len(roots)==240
rdata=[(r,tuple(matvec(C,r))) for r in roots if next(t for t in r if t)!=-1 or False]
# Keep one representative from each +/- root pair.
rdata=[(r,tuple(matvec(C,r))) for r in roots if next(t for t in r if t)>0]
assert len(rdata)==120
p=[row[-1] for row in K9[:-1]]
w=tuple(int(z) for z in matvec(inverse(C),p));a=tuple(z%3 for z in w)
assert mins[a]==8

def reflect(x,rd):
    r,cr=rd
    t=sum(xi*ci for xi,ci in zip(x,cr))%3
    return tuple((xi-t*ri)%3 for xi,ri in zip(x,r))

def orbit(seed,rds,domain):
    found={seed};queue=deque([seed])
    while queue:
        x=queue.popleft()
        for rd in rds:
            y=reflect(x,rd)
            assert y in domain
            if y not in found:found.add(y);queue.append(y)
    return found
first=orbit(a,rdata,D)
print('DEEP_ORBIT',len(first),flush=True)
assert first==D
stab=[rd for rd in rdata if reflect(a,rd)==a]
print('ROOT_STAB',len(stab),flush=True)
N={b for b in D if tuple((x-y)%3 for x,y in zip(b,a)) in D}
print('ADMISSIBLE_B',len(N),flush=True)
orbits=[];remain=set(N)
while remain:
    seed=min(remain);orb=orbit(seed,stab,N);orbits.append((seed,orb));remain-=orb
print('B_ORBITS',[len(orb) for _,orb in orbits],flush=True)
output={'C':C,'w':w,'a':a,'deep_count':len(D),'deep_transitive':len(first),'root_reflections':len(rdata),'root_reflections_stabilizing_a':len(stab),'admissible_b':len(N),'b_orbits':[]}
for seed,orb in orbits:
    u=wit[a];v=wit[seed]
    inner=F(bilinear(C,u,v),3)
    k=inner+F(5,3)
    assert k.denominator==1
    cu=matvec(C,u);cv=matvec(C,v)
    G=[list(row)+[cu[i],cv[i]] for i,row in enumerate([[3*x for x in row]for row in C])]
    G += [cu+[6,int(k)],cv+[int(k),6]]
    assert determinant(G)==54675
    print('CHECK REPRESENTATIVE',seed,len(orb),flush=True)
    ldl(G)
    vv=enumerate_vectors(G,6,include_zero=False)
    assert min(q for _,q in vv)==6
    item={'seed':seed,'size':len(orb),'G':G,'min':6,'minimal_vectors':len(vv)}
    output['b_orbits'].append(item)
print('RESULT',output,flush=True)
(Path(__file__).parent/'e8_optimal_orbits.json').write_text(json.dumps(output,indent=2))
