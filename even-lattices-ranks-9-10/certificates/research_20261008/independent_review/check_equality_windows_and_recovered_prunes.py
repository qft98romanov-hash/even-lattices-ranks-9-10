#!/usr/bin/env python3
"""Independent exact endpoint and reuse audit for rank-ten equality.

This is an arithmetic/coverage audit, not an extension-generation certificate.
The full equality theorem additionally requires exhaustive new boundary searches.
"""
from fractions import Fraction as Q
from pathlib import Path
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'research_20261007'/'rank10'/'early_flags'

def rootfloor(q,k):
    lo,hi=0,1
    while hi**k<=q:hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**k<=q:lo=mid
        else:hi=mid
    assert lo**k<=q<(lo+1)**k
    return lo

def read(path):return json.loads(path.read_text())
def hashfile(path):return sha256(path.read_bytes()).hexdigest()

def windows(top):
    U={10:top};raw={9:rootfloor(Q(2**45*top**36),40)}
    U[9]=raw[9]-raw[9]%2
    gamma={9:Q(512),8:Q(256),7:Q(64),6:Q(64,3),5:Q(8),4:Q(4),3:Q(2),2:Q(4,3)}
    for rank in range(9,1,-1):
        r=rank-1;raw[r]=rootfloor(gamma[rank]*U[rank]**r,rank)
        u=raw[r]
        if r%2:u-=u%2
        else:
            while u%4 not in {0,(-1)**(r//2)%4}:u-=1
        U[r]=u
    return U,raw

strict,_=windows(54672)
equality,raw=windows(54675)
assert strict=={1:6,2:44,3:210,4:789,5:2492,6:6459,7:13938,8:24673,9:40054,10:54672}
assert equality=={1:6,2:44,3:210,4:789,5:2492,6:6460,7:13940,8:24676,9:40056,10:54675}
new_endpoints={r:[v for v in range(strict[r]+1,equality[r]+1)if v%(2 if r%2 else 4)in({0}if r%2 else{0,(-1)**(r//2)%4})]for r in range(1,10)}
assert new_endpoints=={1:[],2:[],3:[],4:[],5:[],6:[6460],7:[13940],8:[24676],9:[40056]}

old_raw_prunes=[];old_parent_prunes=[];hashes={}
for rank in (7,8,9):
    path=BASE/f'rank{rank}_lifting_prunes.json';hashes[str(path.relative_to(HERE.parents[1]))]=hashfile(path)
    rec=read(path)['prunes'];recovered=[]
    for row in rec:
        pi,ci,dprev,d,lhs,rhs=row
        assert lhs==3*d*d and rhs==4*dprev*strict[rank+1]and lhs>rhs
        if lhs<=4*dprev*equality[rank+1]:
            recovered.append({'parent_index':pi,'child_index':ci,'parent_determinant':dprev,'child_determinant':d,'necessary_next_determinant':str(Q(lhs,4*dprev)),'old_lhs':lhs,'old_rhs':rhs,'new_rhs':4*dprev*equality[rank+1]})
    old_raw_prunes.append({'rank':rank,'old_prunes':len(rec),'recovered_count':len(recovered),'recovered':recovered})
    path=BASE/f'rank{rank}_parents'/'exact_prunes.json';hashes[str(path.relative_to(HERE.parents[1]))]=hashfile(path)
    rec=read(path)['prunes'];recovered=[]
    for row in rec:
        d,dprev=(row['d6'],row['d5'])if rank==7 else(row['det'],row['preceding_det'])
        assert row['left']==3*d*d and row['right']==4*dprev*strict[rank]and row['left']>row['right']
        if row['left']<=4*dprev*equality[rank]:recovered.append(row)
    old_parent_prunes.append({'child_rank':rank,'old_prunes':len(rec),'recovered_count':len(recovered),'recovered':recovered})
assert [x['recovered_count']for x in old_raw_prunes]==[4,0,0]
assert [x['recovered_count']for x in old_parent_prunes]==[0,0,0]
recovered=old_raw_prunes[0]['recovered']
assert [(r['parent_index'],r['child_index'],r['parent_determinant'],r['child_determinant'])for r in recovered]==[(3297,k,4131,11658)for k in range(606,610)]
assert all(r['necessary_next_determinant']=='3775249/153'for r in recovered)
assert Q(3775249,153)>24673 and Q(3775249,153)<24676
assert [v for v in range(24674,24677)if v%4 in {0,1}]==[24676]

out={'status':'PASS','scope':__doc__,'strict_upper_windows':strict,'equality_upper_windows':equality,'equality_raw_floors':raw,'new_admissible_endpoints':new_endpoints,'old_raw_prune_audits':old_raw_prunes,'old_parent_prune_audits':old_parent_prunes,'recovered_rank7_only_possible_child_determinant':24676,'source_sha256':hashes,'theorem_status':'Arithmetic component of the completed equality proof; the separate finite-module checker and old audited prefix supply the required exhaustive coverage. This file alone is not an equality classification.'}
HERE.joinpath('equality_windows_and_recovered_prunes.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
print('EQUALITY_WINDOWS_AND_ALL_OLD_PRUNE_REUSE_AUDIT_PASS')
