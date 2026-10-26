#!/usr/bin/env python3
"""Resumable exact one-rank extension search; completed raw coverage only."""
from pathlib import Path
import argparse,json,hashlib,time,os,multiprocessing as mp
from fractions import Fraction as F
from fast_extend import extend_parent
from exact_lattice import determinant
P=argparse.ArgumentParser();P.add_argument('--input',type=Path,required=True);P.add_argument('--rank',type=int,required=True);P.add_argument('--low',type=int,required=True);P.add_argument('--high',type=int,required=True);P.add_argument('--modulus',type=int,required=True);P.add_argument('--residues',required=True);P.add_argument('--workers',type=int,default=7);P.add_argument('--probe-count',type=int,default=0);P.add_argument('--output-name',default=None)
ARGS=P.parse_args();HERE=Path(__file__).resolve().parent;OUT=HERE/'early_flags'/(ARGS.output_name or f'rank{ARGS.rank}_parents');OUT.mkdir(exist_ok=True,parents=True)
SOURCE=ARGS.input.resolve();PARENTS=json.loads(SOURCE.read_text())['representatives'];SOURCE_HASH=hashlib.sha256(SOURCE.read_bytes()).hexdigest();CODE_HASH=hashlib.sha256((HERE/'fast_extend.py').read_bytes()).hexdigest();OLD_CODE_HASH=hashlib.sha256((HERE/'extend_flag.py').read_bytes()).hexdigest();RES={int(s)for s in ARGS.residues.split(',')}

def job(index):
    path=OUT/f'parent_{index:04d}.json'
    if path.exists():
        item=json.loads(path.read_text());assert item['input_sha256']==SOURCE_HASH and item['extension_code_sha256'] in {CODE_HASH,OLD_CODE_HASH}
        assert item['window']==[ARGS.low,ARGS.high]
        assert item['parent_index']==index and item['parent_gram']==PARENTS[index]
        assert item['modulus']==ARGS.modulus and set(item['residues'])==RES
        return index,item['raw_count'],item['seconds'],True
    g=PARENTS[index];start=time.monotonic()
    (OUT/f'parent_{index:04d}.running').write_text(json.dumps({'parent':index,'pid':os.getpid(),'started':time.time()}))
    children,stats=extend_parent(g,ARGS.low,ARGS.high,ARGS.modulus,RES)
    d=determinant(g);n=len(g);dprev=determinant([row[:n-1]for row in g[:n-1]])
    assert F(stats['dual_minimum'])==F(dprev,d)
    sec=time.monotonic()-start
    payload={'parent_index':index,'parent_gram':g,'input_sha256':SOURCE_HASH,'extension_code_sha256':CODE_HASH,'window':[ARGS.low,ARGS.high],'modulus':ARGS.modulus,'residues':sorted(RES),'statistics':stats,'raw_count':len(children),'seconds':sec,'representatives':children}
    tmp=path.with_suffix(f'.tmp.{os.getpid()}');tmp.write_text(json.dumps(payload)+'\n');tmp.replace(path)
    (OUT/f'parent_{index:04d}.running').unlink()
    return index,len(children),sec,False

def main():
    started=time.monotonic();active=[];pruned=[]
    for i,g in enumerate(PARENTS):
        n=len(g);d=determinant(g);dp=determinant([row[:n-1]for row in g[:n-1]])
        assert n==ARGS.rank-1
        if 3*d*d<=4*dp*ARGS.high:active.append(i)
        else:pruned.append({'parent_index':i,'det':d,'preceding_det':dp,'left':3*d*d,'right':4*dp*ARGS.high})
    (OUT/'exact_prunes.json').write_text(json.dumps({'input_sha256':SOURCE_HASH,'prunes':pruned},indent=2)+'\n')
    todo=active
    if ARGS.probe_count:todo=[active[k*(len(active)-1)//max(1,ARGS.probe_count-1)]for k in range(ARGS.probe_count)];todo=sorted(set(todo))
    print('START_RANK',ARGS.rank,'parents',len(PARENTS),'active',len(active),'todo',len(todo),'workers',ARGS.workers,flush=True)
    completed=0;total=0;timings=[]
    with mp.get_context('fork').Pool(ARGS.workers) as pool:
        for index,n,sec,cached in pool.imap_unordered(job,todo,chunksize=1):
            completed+=1;total+=n;timings.append({'parent':index,'raw_count':n,'seconds':sec,'cached':cached})
            progress={'rank':ARGS.rank,'completed':completed,'todo':len(todo),'active':len(active),'raw_so_far':total,'elapsed':time.monotonic()-started,'last_parent':index}
            (OUT/'progress.json').write_text(json.dumps(progress)+'\n')
            print('DONE',completed,'/',len(todo),'PARENT',index,'RAW',n,'TOTAL',total,'SECONDS',round(progress['elapsed'],1),flush=True)
    summary={'rank':ARGS.rank,'input_sha256':SOURCE_HASH,'extension_code_sha256':CODE_HASH,'accepted_extension_code_sha256':[CODE_HASH,OLD_CODE_HASH],'parent_count':len(PARENTS),'exact_pruned_parents':len(pruned),'fully_enumerated_parents':len(todo),'raw_candidates':total,'wall_seconds':time.monotonic()-started,'timings':timings,'isometry_deduplication':'NOT YET PERFORMED','later_ranks':'NOT YET PERFORMED'}
    if ARGS.probe_count:
        (OUT/'probe_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print('PROBE_COMPLETE',flush=True)
    else:
        files=[OUT/'exact_prunes.json']+[OUT/f'parent_{i:04d}.json'for i in active]
        (OUT/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n'for p in files))
        (OUT/'complete_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        print('ALL_RAW_PARENTS_COMPLETE_RANK',ARGS.rank,'RAW',total,'SECONDS',round(summary['wall_seconds'],2),flush=True)
if __name__=='__main__':main()
