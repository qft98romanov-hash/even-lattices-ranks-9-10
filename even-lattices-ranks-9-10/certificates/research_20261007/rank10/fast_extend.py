"""Exact one-rank flag extension using adjugate integer arithmetic.
Parent must be positive definite, even integral, and have minimum >=6.
These parent hypotheses come from the preceding certificate stage.
It must itself be a certified shortest-dual flag extension in the
supplied basis. That assertion is independently checked for each parent.
See fast_extension_proof.txt for the integer shortest-normal criterion.
"""
from fractions import Fraction as F
from collections import Counter
from exact_lattice import determinant,enumerate_vectors
from extend_flag import inverse,append_gram

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mv(a,x):return tuple(dot(row,x)for row in a)
def ceilq(x):return -((-x.numerator)//x.denominator)

def extend_parent(g,det_low,det_high,modulus,residues,*,verbose=False):
    n=len(g);d=determinant(g);dprev=determinant([row[:n-1]for row in g[:n-1]])
    dualmin=F(dprev,d);invg=inverse(g)
    small=enumerate_vectors(invg,dualmin,include_zero=False)
    assert small and min(q for _,q in small)==dualmin,'parent basis is not the claimed dual-shortest flag'
    required_s=F(3,4)/dualmin
    if F(det_high,d)<required_s:
        return [],{'parent_det':d,'dual_minimum':str(dualmin),'globally_pruned':True,'discriminant_classes':0,'tested':{}}
    effective_low=max(det_low,ceilq(d*required_s))
    adj=[[int(d*x)for x in row]for row in invg]
    assert all(F(adj[i][j],d)==invg[i][j]for i in range(n)for j in range(n))
    # Parent dual vectors relevant to ANY allowed shortest-normal test.
    duals=[]
    for q,qnorm in enumerate_vectors(invg,F(d,effective_low),include_zero=False):
        if next(x for x in q if x)<0:continue
        aq=mv(adj,q);Q=dot(q,aq)
        assert F(Q,d)==qnorm
        duals.append((Q,aq))
    best={};witness={};bound=3
    while len(best)<d:
        bound+=1
        for p,mu in enumerate_vectors(invg,bound,include_zero=True):
            key=tuple(x%d for x in mv(adj,p));M=mu*d;assert M.denominator==1;M=int(M)
            if key not in best or M<best[key]:best[key]=M;witness[key]=p
        if bound>20:raise RuntimeError('class coverage bound unexpectedly exceeds20')
    assert len(best)==d
    children=[];tested=Counter()
    for key,M in best.items():
        p=witness[key]
        diag=(M+effective_low+d-1)//d
        if diag%2:diag+=1
        while diag*d<=M+det_high:
            D=diag*d-M;tested['even_diagonal']+=1
            assert D>=effective_low
            if D%modulus in residues:
                tested['det_congruence']+=1
                m=1;ok=True
                while m*m*D<6*d:
                    mkey=tuple(m*x%d for x in key)
                    if m*m*D+best[mkey]<6*d:ok=False;break
                    m+=1
                if ok:
                    tested['minimum']+=1
                    for Q,aq in duals:
                        if D*Q>=d*d:continue
                        rem=dot(p,aq)%d;rem=min(rem,d-rem)
                        if D*Q+rem*rem<d*d:ok=False;break
                    if ok:
                        child=append_gram(g,p,diag);assert determinant(child)==D
                        children.append(child);tested['dual_shortest']+=1
            diag+=2
    return children,{'parent_det':d,'dual_minimum':str(dualmin),'global_required_s':str(required_s),'global_s_upper':str(F(det_high,d)),'globally_pruned':False,'discriminant_classes':len(best),'cover_search_bound':str(bound),'effective_low':effective_low,'tested':dict(tested),'kernel':'exact adjugate/lifted-dual'}
