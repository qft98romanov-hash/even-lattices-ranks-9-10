#!/usr/bin/env python3
"""Complete raw rank7 extension search from certified rank6 prefix.
500 active parents, 3252 exact lifting prunes. Per-parent resumable files.
This does not classify rank7 isometry or finish ranks8-10.
"""
from pathlib import Path
import json,hashlib,time,os,multiprocessing as mp
from extend_flag import extend_parent
from exact_lattice import determinant
HERE=Path(__file__).resolve().parent
OUT=HERE/'early_flags'/'rank7_parents';OUT.mkdir(parents=True,exist_ok=True)
SOURCE=HERE/'early_flags'/'rank6_fast.json'
PARENTS=json.loads(SOURCE.read_text())['representatives']
SOURCE_HASH=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
CODE_HASH=hashlib.sha256((HERE/'extend_flag.py').read_bytes()).hexdigest()

def job(index):
    path=OUT/f'parent_{index:04d}.json'
    if path.exists():
        item=json.loads(path.read_text())
        assert item['input_sha256']==SOURCE_HASH and item['extension_code_sha256']==CODE_HASH
        return index,item['raw_count'],item['seconds'],True
    g=PARENTS[index]
    start=time.monotonic()
    (OUT/f'parent_{index:04d}.running').write_text(json.dumps({'parent':index,'pid':os.getpid(),'started':time.time()}))
    children,stats=extend_parent(g,4374,13938,2,{0})
    sec=time.monotonic()-start
    payload={'parent_index':index,'parent_gram':g,'input_sha256':SOURCE_HASH,'extension_code_sha256':CODE_HASH,'rank7_window':[4374,13938],'statistics':stats,'raw_count':len(children),'seconds':sec,'representatives':children}
    tmp=path.with_suffix(f'.tmp.{os.getpid()}');tmp.write_text(json.dumps(payload)+'\n');tmp.replace(path)
    (OUT/f'parent_{index:04d}.running').unlink()
    return index,len(children),sec,False

def main():
    started=time.monotonic();active=[];pruned=[]
    for i,g in enumerate(PARENTS):
        d=determinant(g);d5=determinant([row[:5]for row in g[:5]])
        if 3*d*d<=4*d5*13938:active.append(i)
        else:pruned.append({'parent_index':i,'d6':d,'d5':d5,'left':3*d*d,'right':4*d5*13938})
    assert len(active)==500 and len(pruned)==3252
    print('START','parents',len(PARENTS),'active',len(active),'pruned',len(pruned),'workers',7,flush=True)
    (OUT/'exact_prunes.json').write_text(json.dumps({'input_sha256':SOURCE_HASH,'prunes':pruned},indent=2)+'\n')
    completed=0;total=0;timings=[]
    with mp.get_context('fork').Pool(7) as pool:
        for index,n,sec,cached in pool.imap_unordered(job,active,chunksize=1):
            completed+=1;total+=n;timings.append({'parent':index,'raw_count':n,'seconds':sec,'cached':cached})
            progress={'completed':completed,'active':len(active),'raw_so_far':total,'elapsed':time.monotonic()-started,'last_parent':index}
            (OUT/'progress.json').write_text(json.dumps(progress)+'\n')
            print('DONE',completed,'/',len(active),'PARENT',index,'RAW',n,'TOTAL',total,'SECONDS',round(progress['elapsed'],1),flush=True)
    files=[OUT/'exact_prunes.json']+[OUT/f'parent_{i:04d}.json'for i in active]
    manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n'for p in files)
    (OUT/'SHA256SUMS.txt').write_text(manifest)
    summary={'input_sha256':SOURCE_HASH,'extension_code_sha256':CODE_HASH,'rank6_representatives':len(PARENTS),'exact_pruned_parents':len(pruned),'fully_enumerated_parents':len(active),'raw_rank7_candidates':total,'wall_seconds':time.monotonic()-started,'timings':timings,'rank7_isometry_deduplication':'NOT YET PERFORMED','ranks8_to10':'NOT YET PERFORMED'}
    (OUT/'complete_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('ALL_RANK7_RAW_PARENTS_COMPLETE',total,'SECONDS',round(summary['wall_seconds'],2),flush=True)
if __name__=='__main__':main()
