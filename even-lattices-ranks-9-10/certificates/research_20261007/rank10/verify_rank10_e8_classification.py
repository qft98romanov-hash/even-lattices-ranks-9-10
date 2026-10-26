#!/usr/bin/env python3
"""Exact certificate for the E8-containing rank-ten theorem and its TWO equality types.

Run python verify_rank10_e8_classification.py with assertions enabled.
Uses only stdlib and the adjacent exact_lattice.py (archived exact kernel).
This is NOT a proof of global e10(6)=54675; it classifies the subclass
containing sqrt(3) E8. See rank10_e8_theorem.md for the completeness proof.
"""
from collections import Counter, deque
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
from exact_lattice import determinant,ldl,enumerate_vectors,qform,bilinear
from verify_rank9_extremal_example_exact import K9

def inverse(a):
    n=len(a)
    m=[[F(x) for x in row]+[F(i==j)for j in range(n)]for i,row in enumerate(a)]
    for j in range(n):
        i=next(i for i in range(j,n)if m[i][j])
        m[i],m[j]=m[j],m[i]
        v=m[j][j];m[j]=[x/v for x in m[j]]
        for i in range(n):
            if i!=j:
                v=m[i][j];m[i]=[x-v*y for x,y in zip(m[i],m[j])]
    return [row[n:]for row in m]

def mv(a,x):return tuple(sum(ai*xi for ai,xi in zip(row,x))for row in a)

def modrank(a,p):
    a=[[x%p for x in row]for row in a];r=0
    for c in range(len(a[0])):
        i=next((i for i in range(r,len(a))if a[i][c]),None)
        if i is None:continue
        a[r],a[i]=a[i],a[r]
        t=pow(a[r][c],-1,p);a[r]=[x*t%p for x in a[r]]
        for i in range(r+1,len(a)):
            t=a[i][c];a[i]=[(x-t*y)%p for x,y in zip(a[i],a[r])]
        r+=1
    return r

def extend(g,p,n):return [row+[p[i]]for i,row in enumerate(g)]+[p+[n]]

def main():
    G8=[row[:8]for row in K9[:8]]
    C=[[x//3 for x in row]for row in G8]
    assert [[3*x for x in row]for row in C]==G8
    assert determinant(C)==1 and determinant(G8)==6561
    assert all(C[i][i]%2==0 for i in range(8))
    ldl(C)
    points=enumerate_vectors(C,8)
    assert Counter(int(q)for _,q in points)=={0:1,2:240,4:2160,6:6720,8:17520}
    best={}
    for x,q in points:
        key=tuple(t%3 for t in x)
        if key not in best or q<best[key]:best[key]=int(q)
    assert len(best)==6561
    assert Counter(best.values())=={0:1,2:240,4:2160,6:2240,8:1920}
    deep={a for a,q in best.items()if q==8}
    assert max(best.values())==8  # exact glue radius squared =8/3
    roots=[r for r,q in points if q==2 and next(t for t in r if t)>0]
    assert len(roots)==120
    reflections=[]
    for r in roots:
        cr=mv(C,r)
        R=[[int(i==j)-r[i]*cr[j]for j in range(8)]for i in range(8)]
        assert determinant(R)==-1
        assert all(bilinear(C,[R[k][i]for k in range(8)],[R[k][j]for k in range(8)])==C[i][j]for i in range(8)for j in range(8))
        reflections.append((r,cr))
    def reflect(x,rd):
        r,cr=rd;t=sum(xi*ci for xi,ci in zip(x,cr))%3
        return tuple((xi-t*ri)%3 for xi,ri in zip(x,r))
    def orbit(seed,gens,domain):
        seen={seed};queue=deque([seed])
        while queue:
            x=queue.popleft()
            for rd in gens:
                y=reflect(x,rd)
                assert y in domain
                if y not in seen:seen.add(y);queue.append(y)
        return seen
    p=[row[-1]for row in K9[:8]]
    Ci=inverse(C)
    w=mv(Ci,p)
    assert all(x.denominator==1 for x in w)
    a=tuple(int(x)%3 for x in w)
    assert a in deep and orbit(a,reflections,deep)==deep
    stabilizing=[r for r in reflections if reflect(a,r)==a]
    assert len(stabilizing)==36
    allowed={b for b in deep if tuple((bi-ai)%3 for bi,ai in zip(b,a))in deep}
    assert len(allowed)==561
    minus_a=tuple(-ai%3 for ai in a)
    assert minus_a in allowed
    assert orbit(minus_a,stabilizing,allowed)=={minus_a}
    q=[1,-1,1,0,-1,-2,-2,1]
    b=tuple(int(x)%3 for x in mv(Ci,q))
    other=orbit(b,stabilizing,allowed)
    assert len(other)==560 and other==allowed-{minus_a}
    original=extend(K9,q+[2],6)
    alternative=extend(K9,[-x for x in p]+[-1],6)
    # Orthogonal rank-two complements of the displayed E8 in each type.
    wi=[int(x) for x in w]
    vi=[int(x) for x in mv(Ci,q)]
    alt_perp=[[0]*8+[1,1],[-x for x in wi]+[1,-2]]
    orig_perp=[[-x for x in wi]+[3,0],[-x for x in vi]+[0,3]]
    for G,V,target in [(alternative,alt_perp,[[10,-5],[-5,10]]),(original,orig_perp,[[30,15],[15,30]])]:
        assert all(mv(G,v)[i]==0 for v in V for i in range(8))
        assert [[bilinear(G,u,v)for v in V]for u in V]==target
    results=[]
    for name,G,targetrank in [('K10_original',original,4),('K10_alternative',alternative,3)]:
        assert all(G[i][j]==G[j][i]for i in range(10)for j in range(10))
        assert all(G[i][i]%2==0 for i in range(10))
        ldl(G)
        assert determinant(G)==54675
        shell=Counter(int(q)for _,q in enumerate_vectors(G,10,include_zero=False))
        assert set(shell)=={6,8,10} and shell[6]==294 and shell[8]==216
        assert shell[10]==(756 if name=='K10_original' else 762)
        assert modrank(G,3)==targetrank
        assert modrank(G,5)==8
        results.append({'name':name,'gram':G,'determinant':54675,'minimum':6,'rank_mod_3':targetrank,'rank_mod_5':8,'theta_shells':dict(shell)})
    assert F(6561)*F(3,4)*F(10,3)**2==54675
    payload={'scope':'even integral rank10 min>=6 containing sqrt(3)E8; not global e10','class_distribution':dict(Counter(best.values())),'deep_class_count':1920,'admissible_second_class_count':561,'stabilizer_orbits':[560,1],'inequivalent_equality_types':2,'examples':results}
    out=Path(__file__).with_name('rank10_e8_certificate.json')
    out.write_text(json.dumps(payload,indent=2)+'\n')
    print('CLASS_MINIMA',sorted(Counter(best.values()).items()))
    print('DEEP_CLASSES_TRANSITIVE',len(deep))
    print('STABILIZING_REFLECTIONS',len(stabilizing))
    print('ADMISSIBLE_SECOND_CLASSES',len(allowed))
    print('STABILIZER_ORBITS',560,1)
    print('LOWER_BOUND_FOR_E8_CONTAINING_RANK10',54675)
    for item in results:print(item['name'],'det',item['determinant'],'min',item['minimum'],'rank_mod3',item['rank_mod_3'],'shells',item['theta_shells'])
    print('OUTPUT_SHA256',sha256(out.read_bytes()).hexdigest())
    print('RANK10_E8_SUBCLASS_TWO_EQUALITY_TYPES_EXACT_OK')

if __name__=='__main__':main()
