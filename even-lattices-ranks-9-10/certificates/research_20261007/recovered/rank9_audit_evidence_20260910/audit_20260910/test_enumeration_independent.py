"""Independent box-enumeration audit; archived files are read-only inputs."""
from fractions import Fraction as F
from itertools import product
from math import isqrt
from random import Random
from pathlib import Path
import sys, json

CERT=Path(__file__).parent/'rank9_complete_certificates'/'certificate'
sys.path.insert(0,str(CERT))
from exact_lattice import enumerate_vectors, _integer_interval, determinant, ldl
from extend_flag import discriminant_minima, extend_parent

def det_rec(a):
    if not a: return F(1)
    return sum((-1)**j*a[0][j]*det_rec([r[:j]+r[j+1:] for r in a[1:]]) for j in range(len(a)))

def inv_adj(a):
    d=det_rec(a); n=len(a)
    return [[(-1)**(i+j)*det_rec([r[:i]+r[i+1:] for k,r in enumerate(a) if k!=j])/d for j in range(n)] for i in range(n)]

def q(a,x):
    return sum(x[i]*a[i][j]*x[j] for i in range(len(x)) for j in range(len(x)))

def brute(a,bound,zero=True):
    ia=inv_adj(a)
    limits=[isqrt((bound*ia[i][i]).numerator//(bound*ia[i][i]).denominator) for i in range(len(a))]
    out=[]
    for x in product(*(range(-b,b+1) for b in limits)):
        if (zero or any(x)) and q(a,x)<=bound: out.append((x,q(a,x)))
    return sorted(out,key=lambda z:(z[1],z[0]))

def key(ig,p):
    vals=[sum(r[j]*p[j] for j in range(len(p))) for r in ig]
    return tuple(v-v.numerator//v.denominator for v in vals)

def classes_box(g,bound):
    ig=inv_adj(g); mins={}; witness={}
    for p,mu in brute(ig,F(bound)):
        k=key(ig,p)
        if k not in mins or mu<mins[k]: mins[k]=mu; witness[k]=p
    assert len(mins)==det_rec(g)
    return ig,mins,witness

def extensions_box(g,lo,hi,mod,res):
    ig,mins,wi=classes_box(g,6); d=det_rec(g); out=[]
    for k,mu in mins.items():
        p=wi[k]
        # An independent deliberately larger range, followed by exact tests.
        for n in range(0,40,2):
            s=F(n)-mu
            if not (lo<=d*s<=hi) or int(d*s)%mod not in res: continue
            h=[list(row)+[p[i]] for i,row in enumerate(g)]+[list(p)+[n]]
            if brute(h,F(5),zero=False): continue
            ih=inv_adj(h)
            small=brute(ih,1/s,zero=False)
            if not small or small[0][1]!=1/s: continue
            out.append(h)
    return out

def main():
    rnd=Random(20260910)
    for _ in range(10000):
        c=F(rnd.randrange(-300,301),rnd.randrange(1,50))
        rr=F(rnd.randrange(0,1000),rnd.randrange(1,50))
        left=c.numerator//c.denominator-35
        right=c.numerator//c.denominator+36
        want=[z for z in range(left,right) if (F(z)-c)**2<=rr]
        assert list(_integer_interval(c,rr))==want
    for base in [10**100,-10**100]:
        for frac in [F(0),F(1,3),F(2,3)]:
            c=base+frac
            for rr in [F(0),F(1,9),F(4,9),F(999999,1000000),F(1),F(1000001,1000000)]:
                want=[base+j for j in range(-3,4) if (F(base+j)-c)**2<=rr]
                assert list(_integer_interval(c,rr))==want
    print('INTEGER_INTERVAL 10000 random + 36 huge-centre boundary cases PASS')
    count=0
    for n,num in [(1,20),(2,35),(3,35),(4,10)]:
        for _ in range(num):
            b=[[rnd.randrange(-2,3) for j in range(n)] for i in range(n)]
            scale=F(rnd.randrange(1,5),rnd.randrange(1,6))
            a=[[scale*(sum(b[k][i]*b[k][j] for k in range(n))+int(i==j)) for j in range(n)] for i in range(n)]
            bound=F(rnd.randrange(0,8),rnd.randrange(1,4))
            assert enumerate_vectors(a,bound)==brute(a,bound)
            count+=1
    print('RATIONAL_ELLIPSOIDS',count,'independent adjugate/Cauchy box comparisons PASS')
    for n in range(1,7):
        for _ in range(10):
            a=[[rnd.randrange(-5,6) for j in range(n)] for i in range(n)]
            assert determinant(a)==det_rec(a)
    print('BAREISS_DETERMINANTS 60 arbitrary integer matrices PASS')
    for g in [[[6]],[[6,3],[3,6]],[[6,2],[2,6]],[[6,1],[1,6]],[[6,0],[0,6]],[[6,3],[3,8]]]:
        gi,m,w=classes_box(g,6)
        gi2,m2,w2,b=discriminant_minima(g)
        assert gi==gi2 and m==m2
        for k,p in w2.items(): assert key(gi,p)==k and q(gi,p)==m[k]
    print('DISCRIMINANT_CLASS_MINIMA ranks 1 and all five rank2 parents PASS')
    seed=[[6]]
    raw,_=extend_parent(seed,27,39,4,{0,3})
    want=extensions_box(seed,27,39,4,{0,3})
    assert raw==want
    print('INDEPENDENT_EXTENSION_GENERATOR rank1->rank2',len(raw),'raw PASS')
    parents=json.loads((CERT/'rank2_exact_classes_regen.json').read_text())['representatives']
    total=0
    for g in parents:
        got,_=extend_parent(g,108,178,2,{0})
        want=extensions_box(g,108,178,2,{0})
        assert got==want
        total+=len(got)
    print('INDEPENDENT_EXTENSION_GENERATOR rank2->rank3',total,'raw PASS')
    print('ALL_INDEPENDENT_ENUMERATION_KERNEL_TESTS_PASS')

if __name__=='__main__': main()
