"""Independent elementary checking of equality certificates; no search-code imports."""
import json, math
from collections import deque
from itertools import product
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EQ=ROOT/'equality'
OLD=ROOT/'recovered/rank9_audit_evidence_20260910/audit_20260910/rank9_complete_certificates/certificate'

def determinant(a):
    a=[[F(x) for x in r] for r in a];d=F(1);n=len(a)
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]),None)
        if k is None:return 0
        if k!=j:a[k],a[j]=a[j],a[k];d=-d
        p=a[j][j];d*=p
        for k in range(j+1,n):
            t=a[k][j]/p
            for h in range(j+1,n):a[k][h]-=t*a[j][h]
            a[k][j]=0
    return d

def inv(a):
    n=len(a);m=[[F(x) for x in r]+[F(i==j) for j in range(n)] for i,r in enumerate(a)]
    for j in range(n):
        k=next(k for k in range(j,n) if m[k][j]);m[k],m[j]=m[j],m[k]
        p=m[j][j];m[j]=[x/p for x in m[j]]
        for k in range(n):
            if k!=j:
                p=m[k][j];m[k]=[x-p*y for x,y in zip(m[k],m[j])]
    return [r[n:] for r in m]

def mv(a,v):return [sum(x*y for x,y in zip(r,v)) for r in a]
def tr(a):return [list(r) for r in zip(*a)]
def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def ext(g,p,n):return [r+[p[i]] for i,r in enumerate(g)]+[list(p)+[n]]
def q(g,v):return sum(x*y for x,y in zip(v,mv(g,v)))

def floorroot(n,k):
    lo,hi=0,1
    while hi**k<=n:hi*=2
    while lo+1<hi:
        mid=(lo+hi)//2
        if mid**k<=n:lo=mid
        else:hi=mid
    return lo

# Exact integer-power window derivation. gamma_r^r for r <= 8.
gamma={2:F(4,3),3:F(2),4:F(4),5:F(8),6:F(64,3),7:F(64),8:F(256)}
upper={9:21870}
raw8=floorroot(2**72*21870**56,63)
assert raw8==15910
upper[8]=max(x for x in range(raw8+1) if x%4 in (0,1))
raw={8:raw8}
for r in range(8,1,-1):
    a=gamma[r]*upper[r]**(r-1)
    z=floorroot(a.numerator//a.denominator,r)
    raw[r-1]=z
    if (r-1)%2:z-=z%2
    else:
        residues=(0,(-1)**((r-1)//2)%4)
        while z%4 not in residues:z-=1
    upper[r-1]=z
assert upper=={9:21870,8:15909,7:9494,6:4648,5:1894,4:633,3:178,2:39,1:6}
print('WINDOWS',upper,'raw',raw)

# Recompute the necessary lifting filter at the enlarged equality endpoint;
# then independently check every archived isometry for the surviving records.
rank6=json.loads((OLD/'rank6_isometry_classes.json').read_text())['representatives']
rank7=json.loads((OLD/'rank7_merged.json').read_text())
linkage=json.loads((OLD/'rank7_survivor_linkage_exact.json').read_text())
rank6det=[int(determinant(g))for g in rank6]
survivors={};pair_counts={}
for serial,(g,pi) in enumerate(zip(rank7['children'],rank7['child_parent_indices'])):
    assert [r[:6]for r in g[:6]]==rank6[pi]
    d6=rank6det[pi];d7=int(determinant(g))
    if 3*d7*d7<=4*d6*upper[8]:
        survivors[serial]=(d6,d7)
        pair_counts[d6,d7]=pair_counts.get((d6,d7),0)+1
assert len(rank7['children'])==len(rank7['child_parent_indices'])==2235
assert pair_counts=={(2187,4374):2,(2187,6318):54,(2835,7722):32,(4096,8192):1,(3240,8100):1,(3267,7986):6}
covered=set()
for group in linkage['groups']:
    target=group['target_gram']
    assert int(determinant(target))==group['d7']
    for item in group['maps']:
        serial=item['merged_serial'];u=item['X']
        assert serial in survivors and serial not in covered;covered.add(serial)
        assert survivors[serial]==(group['d6'],group['d7'])
        assert item['parent_index']==rank7['child_parent_indices'][serial]
        assert abs(determinant(u))==1
        assert mm(mm(tr(u),target),u)==rank7['children'][serial]
assert covered==set(survivors) and len(covered)==96
print('LIFTING_2235_TO_96_AT_15909_AND_ALL_96_LINKAGE_MAPS_PASS',pair_counts)

# Independent polynomial-content obstruction for boundary determinants.
boundary=[]
for filename,target in [('rank5_isometry_classes.json',4648),('rank6_isometry_classes.json',9494)]:
    forms=json.loads((OLD/filename).read_text())['representatives']; left=[]
    for i,g in enumerate(forms):
        d=determinant(g);a=inv(g);n=len(g)
        adj=[[int(x*d) for x in r] for r in a]
        assert mm(g,adj)==[[int(d)*(i==j)for j in range(n)]for i in range(n)]
        content=math.gcd(int(2*d),*[adj[j][j] for j in range(n)],*[2*adj[j][k]for j in range(n)for k in range(j)])
        if target%content==0:left.append([i,int(d),content])
    boundary.append({'input':filename,'target':target,'parents':len(forms),'content_obstruction_excludes':len(forms)-len(left),'not_excluded_by_content':left})
print('BOUNDARY_CONTENT',boundary)

# Independent boundary exclusion: finite quadratic module BFS, with no norm
# enumeration. For p in Z^n, c=adj(G)p mod d and q=p^T adj(G)p mod 2d.
# Since G is even, q depends only on c. Under p -> p+e_i,
# q -> q+2*c_i+adj(G)_ii mod 2d. A child's even diagonal implies
# target = -q mod 2d. Alternatively, an explicit short dual vector proves
# the elementary lifting obstruction without computing the dual minimum.
def boundary_exclude(g,target):
    n=len(g);d=int(determinant(g));a=inv(g)
    adj=[[int(d*x)for x in r]for r in a]
    best=None
    for p in product((-1,0,1),repeat=n):
        if not any(p):continue
        qp=q(adj,p)
        if 4*target*qp<3*d*d:
            return {'method':'explicit_dual_vector','parent_det':d,'target':target,'pairing_vector':p,'dual_norm':str(F(qp,d))}
    zero=(0,)*n;values={zero:0};queue=deque([zero])
    while queue:
        c=queue.popleft();value=values[c]
        for j in range(n):
            cc=tuple((c[i]+adj[i][j])%d for i in range(n))
            vv=(value+2*c[j]+adj[j][j])%(2*d)
            if cc in values:assert values[cc]==vv
            else:values[cc]=vv;queue.append(cc)
    assert len(values)==d
    assert (-target)%(2*d) not in values.values()
    return {'method':'quadratic_module_nonrepresentation','parent_det':d,'target':target,'class_count':d,'represented_norm_residues':sorted(set(values.values()))}

indep_boundary=[]
for filename,target in [('rank5_isometry_classes.json',4648),('rank6_isometry_classes.json',9494)]:
    for i,g in enumerate(json.loads((OLD/filename).read_text())['representatives']):
        rr=boundary_exclude(g,target);rr.update({'parent_file':filename,'parent_index':i});indep_boundary.append(rr)
for i,row in enumerate(json.loads((EQ/'boundary8_results.json').read_text())):
    rr=boundary_exclude(row['gram'],15909);rr.update({'parent_label':row['label'],'parent_index':i});indep_boundary.append(rr)
assert len(indep_boundary)==262
print('ALL_262_BOUNDARY_PARENTS_INDEPENDENTLY_EXCLUDED',dict((s,sum(r['method']==s for r in indep_boundary))for s in ('explicit_dual_vector','quadratic_module_nonrepresentation')))
(ROOT/'independent_review/equality_boundary_independent.json').write_text(json.dumps(indep_boundary,indent=2))

rows=json.loads((EQ/'equality_candidates.json').read_text())
assert [(r['name'],r['count'])for r in rows]==[('E8',1920),('J14580',1),('J15309a',2)]
for row in rows:
    g=row['gram'];d=int(determinant(g));a=inv(g)
    assert d==row['det'] and len(row['candidates'])==row['count']
    for c in row['candidates']:
        p=c['cross'];n=c['last'];v=mv(a,p)
        assert n%2==0 and n-q(a,p)==F(21870,d)
        assert c['gram']==ext(g,p,n)
        assert tuple(int(d*x)%d for x in v)==tuple(c['class'])
print('ALL_1923_CANDIDATE_GRAMS_AND_SCHUR_COMPLEMENTS_PASS')

orbit=json.loads((EQ/'e8_orbit_certificate.json').read_text())
g=orbit['gram'];n=len(g);d=int(determinant(g));a=inv(g)
adj=[[int(d*x)for x in r]for r in a]
def fp(p):return tuple(x%d for x in mv(adj,p))
tree=orbit['tree'];refs=orbit['generators'];rootp=orbit['root_cross'];k9=ext(g,rootp,6)
assert len(tree)==1920 and orbit['class_count']==1920
assert tree[0]['witness']==rootp and tree[0]['class']==list(fp(rootp))
for r in refs:
    assert mm(mm(tr(r),g),r)==g and determinant(r)==-1
    assert mm(r,r)==[[i==j for j in range(n)]for i in range(n)]
classes=set()
for i,node in enumerate(tree):
    p=node['witness'];cl=tuple(node['class'])
    assert fp(p)==cl and cl not in classes;classes.add(cl)
    assert q(a,p)==F(8,3)
    if i:
        j=node['parent'];assert 0<=j<i
        r=refs[node['generator']];p0=tree[j]['witness']
        assert fp(mv(tr(r),p0))==cl
        delta=[x-y for x,y in zip(mv(tr(r),p),p0)]
        t=mv(a,delta);assert all(x.denominator==1 for x in t);t=[int(x)for x in t]
        u=[r[h]+[t[h]]for h in range(n)]+[[0]*n+[1]]
        assert mm(mm(tr(u),ext(g,p0,6)),u)==ext(g,p,6)
assert classes=={tuple(c['class'])for c in rows[0]['candidates']}
print('E8_ALL_1920_CLASSES_CONNECTED; ALL_1919_LIFTED_EXTENSION_ISOMETRIES_PASS')

maps=json.loads((EQ/'equality_isometries.json').read_text())
for row in maps:
    u=row['to_K9'];assert abs(determinant(u))==1
    assert mm(mm(tr(u),k9),u)==row['gram']
    cand=next(r for r in rows if r['name']==row['parent'])['candidates'][row['index']]
    assert cand['gram']==row['gram']
assert {(x['parent'],x['index']) for x in maps}=={('E8',0),('J14580',0),('J15309a',0),('J15309a',1)}
print('ALL_FOUR_EXPLICIT_K9_ISOMETRIES_PASS')
output={'windows':upper,'raw_windows':raw,'lifting_raw_records':2235,'lifting_survivors':96,'lifting_linkage_maps_checked':96,'boundary_content':boundary,'boundary_parents_independently_excluded':262,'candidate_count':1923,'e8_orbit_count':1920,'lifted_isometries_checked':1919,'explicit_isometries_checked':4,'status':'PASS'}
Path(__file__).with_suffix('.json').write_text(json.dumps(output,indent=2))
