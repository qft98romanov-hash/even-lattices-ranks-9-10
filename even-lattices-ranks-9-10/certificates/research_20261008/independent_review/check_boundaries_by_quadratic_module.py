#!/usr/bin/env python3
"""Independent necessary-condition audit: finite discriminant module and lifted duals.

No original extension or vector-generation code is imported. The independent
rational vector enumerator is the previously audited data-chain implementation.
Every ruled-out parent is excluded without computing discriminant-class minima.
A class surviving those necessary conditions is tested against the lifting
bound for the next flag rank; the audited endpoint families are all excluded.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import deque,Counter
from math import gcd
import sys,json,time,argparse
from concurrent.futures import ProcessPoolExecutor
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'research_20261007'/'independent_review'))
from check_rank10_global_chain import matrix_data,key,enumerate_short,det
E=ROOT/'research_20261007'/'rank10'/'early_flags'

def job(args):
    name,index,g,target=args;n=len(g);d=det(g);dp=det([r[:-1]for r in g[:-1]])
    out={'input':name,'parent_index':index,'parent_determinant':d,'target':target}
    if 3*d*d>4*dp*target:
        out.update(method='last_dual_vector',dual_norm=str(Q(dp,d)));return out
    _,_,inv,A=matrix_data(key(g))
    assert all(sum(g[i][k]*A[k][j]for k in range(n))==d*(i==j)for i in range(n)for j in range(n))
    content=gcd(2*d,*[A[i][i]for i in range(n)],*[2*A[i][j]for i in range(n)for j in range(i)])
    if target%content:
        out.update(method='quadratic_polynomial_content',content=content);return out
    duals=[]
    def short(q,norm):
        if not any(q)or next(x for x in q if x)<0:return
        m=norm*d;assert m.denominator==1
        if target*m<d*d:duals.append((q,int(m)))
    enumerate_short(inv,Q(d,target),short)
    values={(0,)*n:0};queue=deque([(0,)*n]);cols=[tuple(A[i][j]for i in range(n))for j in range(n)]
    while queue:
        c=queue.popleft();val=values[c]
        for j in range(n):
            cc=tuple((x+y)%d for x,y in zip(c,cols[j]));vv=(val+2*c[j]+A[j][j])%(2*d)
            if cc in values:assert values[cc]==vv
            else:values[cc]=vv;queue.append(cc)
    assert len(values)==d
    targetres=(-target)%(2*d);normclasses=[c for c,v in values.items()if v==targetres]
    if not normclasses:
        out.update(method='finite_quadratic_module_nonrepresentation',class_count=d,represented_norm_residues=sorted(set(values.values())));return out
    survivors=[];witness_counts=Counter()
    for c in normclasses:
        for qi,(q,m)in enumerate(duals):
            rem=sum(x*y for x,y in zip(c,q))%d;rem=min(rem,d-rem)
            if target*m+rem*rem<d*d:witness_counts[qi]+=1;break
        else:survivors.append(c)
    out.update(class_count=d,compatible_norm_classes=len(normclasses),tested_dual_sign_pairs=len(duals),surviving_class_count=len(survivors))
    if not survivors:
        out.update(method='all_classes_have_explicit_shorter_dual',witness_counts={str(duals[i][0]):v for i,v in witness_counts.items()})
    else:
        next_upper={6:13940,7:24676,8:40056,9:54675}[n+1]
        lhs,rhs=3*target*target,4*d*next_upper
        if lhs>rhs:
            out.update(method='surviving_classes_fail_next_lifting',surviving_classes=survivors,next_rank_upper=next_upper,next_lifting_lhs=lhs,next_lifting_rhs=rhs)
        else:out.update(method='unresolved_by_necessary_conditions',surviving_classes=survivors)
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=2);a=p.parse_args()
    jobs=[]
    for name,target in [('rank5.json',6460),('rank6_fast.json',13940),('rank7_eligible.json',24676),('rank8_eligible.json',40056)]:
        for i,g in enumerate(json.loads((E/name).read_text())['representatives']):jobs.append((name,i,g,target))
    revived=json.loads((E/'rank7_parents'/'parent_3297.json').read_text())['representatives']
    for i in range(606,610):jobs.append(('rank7_parents/parent_3297.json',i,revived[i],24676))
    start=time.monotonic();rows=[]
    with ProcessPoolExecutor(max_workers=a.workers)as pool:
        for row in pool.map(job,jobs):
            rows.append(row)
            if len(rows)%250==0:print('DONE',len(rows),'OF',len(jobs),'elapsed',round(time.monotonic()-start,2),flush=True)
    counts=Counter(r['method']for r in rows);unresolved=[r for r in rows if r['method']=='unresolved_by_necessary_conditions']
    assert not unresolved, 'Boundary equality exclusion incomplete'
    assert len(rows)==4952
    assert sum(r.get('surviving_class_count',0)for r in rows if r['target']==6460)==58
    assert sum(r.get('surviving_class_count',0)for r in rows if r['target']==13940)==20
    assert all(r.get('surviving_class_count',0)==0 for r in rows if r['target']in(24676,40056))
    from hashlib import sha256
    sources={str((E/name).relative_to(ROOT)):sha256((E/name).read_bytes()).hexdigest()for name in ('rank5.json','rank6_fast.json','rank7_eligible.json','rank8_eligible.json','rank7_parents/parent_3297.json')}
    sources[str((ROOT/'research_20261007/independent_review/check_rank10_global_chain.py').relative_to(ROOT))]=sha256((ROOT/'research_20261007/independent_review/check_rank10_global_chain.py').read_bytes()).hexdigest()
    out={'status':'ALL_EXCLUDED'if not unresolved else'PARTIAL_CHECK','source_sha256':sources,'scope':__doc__,'parent_target_pairs':len(rows),'method_counts':dict(counts),'unresolved_count':len(unresolved),'elapsed_seconds':time.monotonic()-start,'records':rows}
    HERE.joinpath('boundaries_by_quadratic_module.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items()if k!='records'},indent=2));print('ALL_4952_EQUALITY_BOUNDARY_PARENT_TARGET_PAIRS_INDEPENDENTLY_EXCLUDED')
if __name__=='__main__':main()
