#!/usr/bin/env python3
"""Independent exact linkage audit for the completed equality delta data.

The separate quadratic-module checker supplies exhaustive independent
necessary-condition coverage. This checker compares its exact class sets
with the actual generated matrices and verifies every stored job and merge.
It uses only the previously independent standard-library arithmetic kernel.
"""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
from collections import Counter
import sys,json,time
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
E=ROOT/'research_20261007'/'rank10'/'early_flags';NEW=ROOT/'research_20261008'/'rank10_equality'
sys.path.insert(0,str(ROOT/'research_20261007'/'independent_review'))
from check_rank10_global_chain import det,key,matrix_data,flag,enumerate_short

def read(p):return json.loads(p.read_text())
def digest(p):return sha256(p.read_bytes()).hexdigest()
def parents(name):return read(E/name)['representatives']
def linear(g):return [r[:-1]for r in g[:-1]]
START=time.monotonic();STEPS=[]

def step(name,**v):
    row={'step':name,**v};STEPS.append(row);print(json.dumps(row),flush=True)

proof=read(HERE/'boundaries_by_quadratic_module.json');assert proof['status']=='ALL_EXCLUDED'and proof['unresolved_count']==0
assert proof['parent_target_pairs']==4952
for name,h in proof['source_sha256'].items():assert digest(ROOT/name)==h
window=read(HERE/'equality_windows_and_recovered_prunes.json');assert window['status']=='PASS'
for name,h in window['source_sha256'].items():assert digest(ROOT/name)==h
records={(r['input'],r['parent_index'],r['target']):r for r in proof['records']}
assert len(records)==4952
step('independent_proof_inputs',source_hashes_verified=len(proof['source_sha256'])+len(window['source_sha256']),parent_target_pairs=len(records))

kernel_hash=digest(ROOT/'research_20261007'/'rank10'/'fast_extend.py')
configurations=[
 ('rank6_boundary',parents('rank5.json'),6460,6460,4,[0,3],'rank5.json'),
 ('rank7_boundary',parents('rank6_fast.json'),13940,13940,2,[0],'rank6_fast.json'),
 ('rank7_from_new6',read(NEW/'rank6_boundary.json')['representatives'],4374,13940,2,[0],None),
 ('rank8_boundary',parents('rank7_eligible.json'),24676,24676,4,[0,1],'rank7_eligible.json'),
 ('rank8_from_new7',read(NEW/'new_rank7_parents.json')['representatives'],6564,24676,4,[0,1],None),
 ('rank9_boundary',parents('rank8_eligible.json'),40056,40056,2,[0],'rank8_eligible.json'),
 ('rank9_from_new8',read(NEW/'new_rank8_parents.json')['representatives'],19684,40056,2,[0],None),
]
all_jobs=set();all_new_flags=0
for name,ps,lo,hi,mod,res,source in configurations:
    raw=[];origins=[];fingerprint_matches=0
    for i,g in enumerate(ps):
        f=NEW/'jobs'/f'{name}_{i:04d}.json';all_jobs.add(f.name);obj=read(f)
        assert obj['config']=={'name':name,'index':i,'parent_gram':g,'low':lo,'high':hi,'modulus':mod,'residues':res,'kernel_sha256':kernel_hash}
        d=det(g);dp=det(linear(g));stats=obj['statistics'];children=obj['children']
        assert stats['parent_det']==d and Q(stats['dual_minimum'])==Q(dp,d)
        if stats['globally_pruned']:assert 3*d*d>4*dp*hi and children==[]
        else:assert stats['discriminant_classes']==d and stats['tested'].get('dual_shortest',0)==len(children)
        classset=set()
        for j,h in enumerate(children):
            assert len(h)==len(g)+1 and linear(h)==g
            D,dd,inv,adj=matrix_data(key(h));assert dd==d and lo<=D<=hi and D%mod in res
            minimum,count=enumerate_short([[Q(x)for x in row]for row in h],Q(6));assert minimum==6 and count>0
            D2,dd2,_=flag(h);assert(D2,dd2)==(D,d)
            _,_,_,A=matrix_data(key(g));p=h[-1][:-1]
            c=tuple(sum(A[a][b]*p[b]for b in range(len(g)))%d for a in range(len(g)))
            assert c not in classset;classset.add(c)
            raw.append(h);origins.append([name,i,j]);all_new_flags+=1
        if source:
            r=records[source,i,hi]
            wanted={tuple(c)for c in r.get('surviving_classes',[])}
            assert classset==wanted,(name,i,len(classset),len(wanted))
            fingerprint_matches+=len(classset)
        elif name=='rank7_from_new6':
            assert not children and 3*d*d>4*dp*13940
        elif name=='rank8_from_new7':
            assert not children and d==11658 and dp==4131
            assert Q(3*d*d,4*dp)>24673 and hi==24676
            assert [t for t in range(24674,24677)if t%4 in(0,1)]==[24676]
            wanted=records['rank7_parents/parent_3297.json',606+i,24676]
            assert wanted['method']=='finite_quadratic_module_nonrepresentation'
            assert g==read(E/'rank7_parents'/'parent_3297.json')['representatives'][606+i]
    summary=read(NEW/f'{name}.json')
    assert summary['name']==name and summary['parent_count']==len(ps)and summary['window']==[lo,hi]
    assert summary['raw_count']==len(raw)and summary['representatives']==raw and summary['origins']==origins
    step(name,parents=len(ps),raw_children=len(raw),independently_verified_primal_and_dual_minima=len(raw),exact_fingerprint_matches=fingerprint_matches)
assert all_new_flags==78
assert {p.name for p in(NEW/'jobs').glob('*.json')}==all_jobs
assert len(all_jobs)==5010

for rank,oldU,newU in [(7,24673,24676),(8,40054,40056),(9,54672,54675)]:
    oldprunes=read(E/f'rank{rank}_lifting_prunes.json')['prunes']
    revived=[];eligible=[];origins=[]
    for pi,ci,dp,d,left,right in oldprunes:
        assert left==3*d*d and right==4*dp*oldU and left>right
        if left<=4*dp*newU:
            fname=f'parent_{pi:04d}.json';g=read(E/f'rank{rank}_parents'/fname)['representatives'][ci]
            assert det(g)==d and det(linear(g))==dp
            eligible.append(g);origins.append(['old',fname,ci]);revived.append([fname,ci,d,dp,left,4*dp*newU])
    newpruned=[];newcount=0;datafiles=[]
    for name in [f'rank{rank}_boundary',f'rank{rank}_from_new{rank-1}']:
        p=NEW/(name+'.json');summary=read(p);datafiles.append([p.name,digest(p)])
        for i,g in enumerate(summary['representatives']):
            newcount+=1;d=det(g);dp=det(linear(g));left=3*d*d;right=4*dp*newU
            if left<=right:eligible.append(g);origins.append([name,i])
            else:newpruned.append([name,i,d,dp,left,right])
    out=read(NEW/f'new_rank{rank}_parents.json')
    assert out['rank']==rank and out['old_next_upper']==oldU and out['new_next_upper']==newU
    oldraw=sum(len(read(p)['representatives'])for p in(E/f'rank{rank}_parents').glob('parent_*.json'))
    assert out['old_raw']==oldraw and out['old_prunes']==len(oldprunes)and out['old_revived']==revived
    assert out['new_raw']==newcount and out['new_pruned']==newpruned
    assert out['new_eligible_count']==len(eligible)and out['representatives']==eligible and out['origins']==origins
    assert out['new_datafiles']==datafiles
    assert len(eligible)==(4 if rank==7 else 0)
    step(f'rank{rank}_complete_merge',old_raw=oldraw,old_prunes=len(oldprunes),revived=len(revived),new_raw=newcount,new_pruned=len(newpruned),new_eligible=len(eligible))

terminal=read(E/'rank9_lifting_prunes.json')['prunes'];assert len(terminal)==3819
ratios=[]
for pi,ci,d8,d9,lhs,rhs in terminal:
    assert lhs==3*d9*d9 and rhs==4*d8*54672
    assert lhs>4*d8*54675
    ratios.append(Q(lhs,4*d8))
assert min(ratios)==Q(12966723,212)
step('old_terminal_obstruction_at_equality',rank9_records=len(terminal),least_required_next_determinant=str(min(ratios)),equality_target=54675)

out={'status':'PASS','scope':__doc__,'mathematical_conclusion':'Global rank-ten determinant54675 equality has exactly two isometry types, under gamma9<=2, the old audited complete prefix, and the E8 two-type classification.','jobs_checked':len(all_jobs),'new_raw_grams_checked':all_new_flags,'steps':STEPS,'elapsed_seconds':time.monotonic()-START}
HERE.joinpath('delta_chain_independent_verified.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k!='steps'},indent=2))
print('GLOBAL_RANK10_EQUALITY_DELTA_LINKAGE_AND_INDEPENDENT_CLASS_MATCH_PASS')
