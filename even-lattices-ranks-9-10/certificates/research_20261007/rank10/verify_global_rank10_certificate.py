#!/usr/bin/env python3
"""Independent standard-library audit of strict rank-ten search records.

Recomputes windows, all integral covering isometries, parent/child linkage,
every recorded lifting exclusion, and the final obstruction.  Exact short
dual enumeration is independently implemented below and run on all retained
representatives and all final rank-nine records.  This verifies the saved
certificate chain; exhaustive production of extension lists still relies on
the separately audited original/fast extension algorithms and their runs.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt
import hashlib,json,re,time,argparse,multiprocessing as mp,subprocess,sys

R=Path(__file__).resolve().parent; E=R/'early_flags'
REPLAY_JOBS=[]
REPORT={'scope':'Independent exact audit of saved coverage, isometries, flags and prunes; extension-list generation uses separately reviewed generators.','steps':[]}
START=time.monotonic()

def read(p):return json.loads(Path(p).read_text())
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def key(g):return tuple(tuple(row)for row in g)
def det(g):
    a=[list(row)for row in g]; n=len(a)
    if not n:return 1
    prev=1;sgn=1
    for j in range(n-1):
        if not a[j][j]:
            k=next((k for k in range(j+1,n)if a[k][j]),None)
            if k is None:return 0
            a[j],a[k]=a[k],a[j];sgn=-sgn
        pivot=a[j][j]
        for i in range(j+1,n):
            for k in range(j+1,n):
                v=a[i][k]*pivot-a[i][j]*a[j][k];assert v%prev==0
                a[i][k]=v//prev
        prev=pivot
    return sgn*a[-1][-1]

@lru_cache(None)
def matrix_data(g):
    n=len(g)
    assert all(len(row)==n for row in g)
    assert all(isinstance(g[i][j],int)and g[i][j]==g[j][i]for i in range(n)for j in range(n))
    assert all(g[i][i]%2==0 for i in range(n))
    a=[[F(x)for x in row]+[F(i==j)for j in range(n)]for i,row in enumerate(g)]
    for j in range(n):
        assert a[j][j]>0 # SPD successive Schur pivots
        v=a[j][j];a[j]=[x/v for x in a[j]]
        for i in range(n):
            if i!=j:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[j])]
    inv=tuple(tuple(row[n:])for row in a);d=det(g);assert d>0
    adj=tuple(tuple(int(x*d)for x in row)for row in inv)
    assert all(F(adj[i][j],d)==inv[i][j]for i in range(n)for j in range(n))
    dp=det([row[:-1]for row in g[:-1]])
    return d,dp,inv,adj

def enumerate_short(a,bound):
    """Independent exact rational triangular enumeration, inclusive bound."""
    n=len(a);L=[[F(i==j)for j in range(n)]for i in range(n)];D=[]
    for k in range(n):
        dk=a[k][k]-sum(L[k][h]*L[k][h]*D[h]for h in range(k));assert dk>0;D.append(dk)
        for i in range(k+1,n):L[i][k]=(a[i][k]-sum(L[i][h]*L[k][h]*D[h]for h in range(k)))/dk
    x=[0]*n;minimum=None;count=0
    def rec(k,remaining):
        nonlocal minimum,count
        if k<0:
            if any(x):
                norm=bound-remaining;count+=1
                if minimum is None or norm<minimum:minimum=norm
            return
        centre=-sum(L[j][k]*x[j]for j in range(k+1,n))
        a0,b0=centre.numerator,centre.denominator
        z=remaining/D[k];rr=isqrt((z.numerator*b0*b0)//z.denominator)
        lo=-((-(a0-rr))//b0);hi=(a0+rr)//b0
        for v in range(lo,hi+1):
            x[k]=v;cost=D[k]*(v-centre)**2
            assert cost<=remaining
            rec(k-1,remaining-cost)
        x[k]=0
    rec(n-1,F(bound));return minimum,count

FLAG_CACHE={}
def flag(g):
    kg=key(g)
    if kg in FLAG_CACHE:return FLAG_CACHE[kg]
    d,dp,inv,adj=matrix_data(kg);mu=F(dp,d)
    found,count=enumerate_short(inv,mu);assert found==mu,(len(g),d,dp,found)
    FLAG_CACHE[kg]=(d,dp,count)
    return d,dp,count

def step(name,**kw):
    row={'step':name,**kw};REPORT['steps'].append(row);print(json.dumps(row),flush=True)

def check_windows():
    U={10:54672};gam={9:F(512),8:F(256),7:F(64),6:F(64,3),5:F(8),4:F(4),3:F(2),2:F(4,3)}
    rows=read(R/'rank10_windows.json')['windows']
    for row in rows:
        rank=row['rank'];n=rank+1
        rhs=F(2**45*U[10]**36)if n==10 else gam[n]*U[n]**(n-1)
        power=40 if n==10 else n;raw=row['raw']
        assert F(raw**power)<=rhs<F((raw+1)**power)
        modulus=2 if rank%2 else 4;res={0}if rank%2 else{0,(-1)**(rank//2)%4}
        u=raw
        while u%modulus not in res:u-=1
        assert row['upper']==u and F(row['rhs'])==rhs and row['power']==power
        U[rank]=u
    assert U=={1:6,2:44,3:210,4:789,5:2492,6:6459,7:13938,8:24673,9:40054,10:54672}
    # Classical Hermite lower determinants before the E8/gap exclusions.
    lower={rank:(F(6**rank)/gam[rank]) for rank in range(2,9)}
    assert lower=={2:F(27),3:F(108),4:F(324),5:F(972),6:F(2187),7:F(4374),8:F(6561)}
    step('exact_windows',upper_by_rank=U,classical_lower_by_rank={r:str(x)for r,x in lower.items()},special_lowers={'rank8':6564,'rank9_generic_lower':19684,'rank9_low_interval':[19684,24450],'rank9_high_interval':[24452,40054]})

def check_cover(raw,dedup,name):
    reps=dedup['representatives'];ids=dedup['raw_to_class'];maps=dedup['isometry_maps']
    assert len(raw)==len(ids)==len(maps)==dedup['raw_count']
    assert len(reps)==dedup['class_count'] and set(ids)==set(range(len(reps)))
    rawset={key(g)for g in raw}
    assert all(key(g)in rawset for g in reps),'representatives must retain actual raw flag bases'
    for g,j,T in zip(raw,ids,maps):
        H=reps[j];n=len(g);assert abs(det(T))==1
        HT=[[sum(H[a][z]*T[z][b]for z in range(n))for b in range(n)]for a in range(n)]
        result=[[sum(T[z][a]*HT[z][b]for z in range(n))for b in range(n)]for a in range(n)]
        assert result==g
    for g in reps:flag(g)
    step(name,raw_count=len(raw),representative_count=len(reps),all_maps_verified=True,all_representative_dual_minima_independently_verified=True)
    return reps

def child_record(g,parent,lo,hi,mod,res):
    n=len(parent);assert len(g)==n+1 and all(len(row)==n+1 for row in g)
    assert [row[:n]for row in g[:n]]==parent
    assert all(g[i][-1]==g[-1][i]and isinstance(g[i][-1],int)for i in range(n))and g[-1][-1]%2==0
    d,dp,inv,A=matrix_data(key(parent));p=g[-1][:-1]
    D=g[-1][-1]*d-sum(p[i]*A[i][j]*p[j]for i in range(n)for j in range(n))
    assert lo<=D<=hi and D%mod in res
    return D,d

def check_low():
    parents=read(R/'rank1_seed.json')['representatives'];assert parents==[[[6]]];flag(parents[0])
    cases=[(2,27,44,4,{0,3}),(3,108,210,2,{0}),(4,324,789,4,{0,1}),(5,972,2492,2,{0}),(6,2187,6459,4,{0,3})]
    for rank,lo,hi,mod,res in cases:
        raw=read(E/f'rank{rank}.json.raw')['representatives']
        out=read(E/(f'rank{rank}.json'if rank<6 else 'rank6_fast.json'))
        text=(E/f'rank{rank}.log').read_text();pats=re.findall(r'PARENT (\d+) / (\d+) rank (\d+) det (\d+)\s+RAW_CHILDREN (\d+) TOTAL (\d+)',text)
        assert len(pats)==len(parents),(rank,len(pats),len(parents))
        offset=0
        for i,(si,sn,srank,sd,sc,st)in enumerate(pats):
            count=int(sc);assert(int(si),int(sn),int(srank),int(sd))==(i,len(parents),rank-1,det(parents[i]))
            add_replay(f'early_r{rank}_p{i}',parents[i],lo,hi,mod,res,raw[offset:offset+count])
            for g in raw[offset:offset+count]:child_record(g,parents[i],lo,hi,mod,res)
            offset+=count;assert offset==int(st)
            if rank<6:
                s=out['parent_stats'][i];assert s['parent_det']==int(sd)and s['raw_children']==count
                assert F(s['dual_minimum'])==F(matrix_data(key(parents[i]))[1],int(sd))
                if s['globally_pruned']:assert 3*int(sd)**2>4*matrix_data(key(parents[i]))[1]*hi and count==0
                else:assert s['discriminant_classes']==int(sd)
        assert offset==len(raw)and 'RAW_CHECKPOINT'in text
        parents=check_cover(raw,out,f'rank{rank}_coverage_and_isometries')
    stored=read(E/'rank6_dual_minima_verified.json');assert stored['count']==len(parents)
    for i,row in enumerate(stored['records']):
        d,dp,normals=flag(parents[i]);assert row['parent']==i and row['d6']==d and row['d5']==dp and F(row['dual_minimum'])==F(dp,d)
    return parents

def check_high(rank,parentfile,lo,hi,mod,res,next_high):
    parents=read(parentfile)['representatives'];src=E/f'rank{rank}_parents';summary=read(src/'complete_summary.json');sourcehash=digest(parentfile)
    assert summary['input_sha256']==sourcehash
    manifest={}
    for line in(src/'SHA256SUMS.txt').read_text().splitlines():
        h,name=line.split('  ');assert name not in manifest;manifest[name]=h;assert digest(src/name)==h
    prune_data=read(src/'exact_prunes.json');assert prune_data['input_sha256']==sourcehash
    covered=set();pruned_parent=prune_data['prunes']
    for row in pruned_parent:
        i=row['parent_index'];assert i not in covered;covered.add(i);d,dp,_=flag(parents[i])
        left,right=3*d*d,4*dp*hi;assert left>right and row['left']==left and row['right']==right
        if rank==7:assert row['d6']==d and row['d5']==dp
        else:assert row['det']==d and row['preceding_det']==dp
    accepted={digest(R/'extend_flag.py'),digest(R/'fast_extend.py')}
    eligible=[];origins=[];prunes=[];all_raw_count=0;final_bounds=[];filenames={'exact_prunes.json'}
    for f in sorted(src.glob('parent_*.json')):
        item=read(f);i=item['parent_index'];assert i not in covered and 0<=i<len(parents);covered.add(i);filenames.add(f.name)
        assert f.name==f'parent_{i:04d}.json'and item['parent_gram']==parents[i]and item['input_sha256']==sourcehash
        assert item['extension_code_sha256']in accepted
        if rank==7:assert item['rank7_window']==[lo,hi]
        else:assert item['window']==[lo,hi]and item['modulus']==mod and set(item['residues'])==res
        raw=item['representatives'];assert len(raw)==item['raw_count'];d,dp,_=flag(parents[i]);stats=item['statistics']
        add_replay(f'rank{rank}_p{i}',parents[i],lo,hi,mod,res,raw)
        assert stats['parent_det']==d and F(stats['dual_minimum'])==F(dp,d)
        assert not stats['globally_pruned']and stats['discriminant_classes']==d
        assert stats['tested'].get('dual_shortest',0)==len(raw)
        for j,g in enumerate(raw):
            D,dcheck=child_record(g,parents[i],lo,hi,mod,res);assert dcheck==d;all_raw_count+=1
            if rank==9:
                gd,gdp,_=flag(g);assert gd==D and gdp==d
                final_bounds.append(F(3*D*D,4*d))
            if 3*D*D<=4*d*next_high:
                eligible.append(g);origins.append([i,j,d,D])
            else:prunes.append([i,j,d,D,3*D*D,4*d*next_high])
    assert set(manifest)==filenames
    assert covered==set(range(len(parents)))
    assert len(pruned_parent)==summary['exact_pruned_parents']
    assert len(filenames)-1==summary['fully_enumerated_parents']
    assert all_raw_count==summary['raw_rank7_candidates'if rank==7 else'raw_candidates']
    assert eligible==read(E/f'rank{rank}_eligible.json.raw')['representatives']
    assert origins==read(E/f'rank{rank}_eligible_origins.json')['origins']
    savedprunes=read(E/f'rank{rank}_lifting_prunes.json');assert prunes==savedprunes['prunes']
    assert savedprunes['upper_rank8'if rank==7 else'next_upper']==next_high
    step(f'rank{rank}_complete_records',parents=len(parents),parent_prunes=len(pruned_parent),enumerated_parents=len(filenames)-1,raw=all_raw_count,next_prunes=len(prunes),eligible=len(eligible),all_linkage_hashes_and_prunes_verified=True)
    if rank<9:
        return check_cover(eligible,read(E/f'rank{rank}_eligible.json'),f'rank{rank}_eligible_cover')
    assert not eligible and len(prunes)==3819
    least=min(final_bounds);assert least==F(12966723,212)and least>54672
    step('final_obstruction',all_rank9_dual_minima_independently_reenumerated=True,rank9_candidates=len(final_bounds),least_next_determinant_bound=str(least),strict_target_upper=54672,remaining_candidates=0)

def list_digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def add_replay(name,g,lo,hi,mod,res,children):
    REPLAY_JOBS.append({'name':name,'parent':g,'low':lo,'high':hi,'modulus':mod,'residues':sorted(res),'count':len(children),'sha256':list_digest(children)})

def check_low_rank9():
    assert F(6**9,512)==19683 and 19683%2==1
    source=E/'rank8_eligible.json';parents=read(source)['representatives'];src=E/'rank9_low_parents';summary=read(src/'complete_summary.json');sh=digest(source)
    assert summary['input_sha256']==sh
    names={}
    for line in(src/'SHA256SUMS.txt').read_text().splitlines():
        h,n=line.split('  ');assert n not in names and digest(src/n)==h;names[n]=h
    pr=read(src/'exact_prunes.json');assert pr['input_sha256']==sh
    covered=set();files={'exact_prunes.json'}
    for row in pr['prunes']:
        i=row['parent_index'];assert i not in covered;covered.add(i)
        d,dp,_=flag(parents[i]);assert row['det']==d and row['preceding_det']==dp
        assert row['left']==3*d*d and row['right']==4*dp*24450 and row['left']>row['right']
    accepted={digest(R/'extend_flag.py'),digest(R/'fast_extend.py')};active=0
    for f in sorted(src.glob('parent_*.json')):
        item=read(f);i=item['parent_index'];assert i not in covered;covered.add(i);files.add(f.name);active+=1
        assert f.name==f'parent_{i:04d}.json' and item['parent_gram']==parents[i] and item['input_sha256']==sh
        assert item['extension_code_sha256']in accepted and item['window']==[19684,24450]
        assert item['modulus']==2 and set(item['residues'])=={0}
        assert item['raw_count']==0 and item['representatives']==[]
        d,dp,_=flag(parents[i]);st=item['statistics'];assert st['parent_det']==d and F(st['dual_minimum'])==F(dp,d)
        assert st['discriminant_classes']==d and not st['globally_pruned'] and st['tested'].get('dual_shortest',0)==0
        add_replay(f'rank9_low_p{i}',parents[i],19684,24450,2,{0},[])
    assert covered==set(range(47)) and set(names)==files and active==2 and len(pr['prunes'])==45
    assert summary['fully_enumerated_parents']==2 and summary['exact_pruned_parents']==45 and summary['raw_candidates']==0
    step('rank9_low_complete_without_old_rank9_theorems',interval=[19684,24450],parents=47,prunes=45,fully_enumerated=2,raw=0)

def replay_job(i):
    from fast_extend import extend_parent
    j=REPLAY_JOBS[i];t=time.monotonic()
    children,stats=extend_parent(j['parent'],j['low'],j['high'],j['modulus'],set(j['residues']))
    h=list_digest(children)
    assert len(children)==j['count'] and h==j['sha256'],(j['name'],len(children),j['count'],h,j['sha256'])
    out={'job':j['name'],'raw_count':len(children),'ordered_children_sha256':h,'seconds':time.monotonic()-t}
    (R/'global_replay_records'/f"{j['name']}.json").write_text(json.dumps(out)+'\n')
    return out

def main():
    assert sys.flags.optimize==0,'assertions must be enabled'
    parser=argparse.ArgumentParser();parser.add_argument('--replay',action='store_true');parser.add_argument('--workers',type=int,default=7);args=parser.parse_args()
    check_windows();check_low()
    check_high(7,E/'rank6_fast.json',4374,13938,2,{0},24673)
    check_high(8,E/'rank7_eligible.json',6564,24673,4,{0,1},40054)
    check_low_rank9()
    check_high(9,E/'rank8_eligible.json',24452,40054,2,{0},54672)
    # Exact finite E8 input, two explicit K10 witnesses, and their minimum-six checks.
    subprocess.run([sys.executable,str(R/'verify_rank10_e8_classification.py')],check=True)
    REPORT['status']='PASS_STATIC_CERTIFICATE_CHAIN';REPORT['elapsed_seconds']=time.monotonic()-START
    REPORT['independently_enumerated_dual_minima_unique_matrices']=len(FLAG_CACHE)
    REPORT['reviewed_code_hashes']={p.name:digest(p)for p in[R/'exact_lattice.py',R/'extend_flag.py',R/'fast_extend.py']}
    REPORT['mathematical_dependencies']=['external gamma9<=2 and proved Mordell inequality','classical Hermite constants through rank8 and unique Hermite equality E8 in rank8','proved E8-containing rank10 determinant bound54675 with exact E8 class data','complete exact flag-extension generation; NO old rank9 determinant theorem or gap theorem is used']
    REPORT['full_generator_replay_performed']=False
    if args.replay:
        (R/'global_replay_records').mkdir(exist_ok=True)
        (R/'global_replay_jobs.json').write_text(json.dumps(REPLAY_JOBS)+'\n')
        done=0;total_raw=0;rt=time.monotonic()
        with mp.get_context('fork').Pool(args.workers) as pool:
            for result in pool.imap_unordered(replay_job,range(len(REPLAY_JOBS)),chunksize=1):
                done+=1;total_raw+=result['raw_count']
                if done%25==0 or done==len(REPLAY_JOBS):
                    progress={'done':done,'total':len(REPLAY_JOBS),'raw_checked':total_raw,'elapsed':time.monotonic()-rt}
                    (R/'global_replay_progress.json').write_text(json.dumps(progress)+'\n')
                    print('EXACT_REPLAY',json.dumps(progress),flush=True)
        REPORT['full_generator_replay_performed']=True;REPORT['replay_jobs']=done;REPORT['replay_raw_candidates']=total_raw;REPORT['replay_seconds']=time.monotonic()-rt
        REPORT['status']='PASS_FULL_EXACT_REPLAY'
    REPORT['elapsed_seconds']=time.monotonic()-START
    (R/'global_rank10_certificate_verified.json').write_text(json.dumps(REPORT,indent=2)+'\n')
    print('GLOBAL_RANK10_CERTIFICATE_PASS',REPORT['status'],'e10=54675 UNDER gamma9<=2',flush=True)
if __name__=='__main__':main()
