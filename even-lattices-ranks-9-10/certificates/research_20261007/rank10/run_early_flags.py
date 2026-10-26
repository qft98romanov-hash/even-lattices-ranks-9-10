#!/usr/bin/env python3
"""Reproduce the completed low-rank prefix of the global rank-ten search.
This is NOT the completed rank-ten search. Bounds use gamma9<=2.
All candidate identifications are separately verified by integral maps.
"""
from pathlib import Path
import subprocess,sys,json,argparse
here=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=here/'early_flags_regenerated');parser.add_argument('--through-rank',type=int,default=6,choices=[2,3,4,5,6]);args=parser.parse_args()
out=args.output_dir.resolve();out.mkdir(exist_ok=True,parents=True)
parent=here/'rank1_seed.json';summary=[]
for rank,lo,hi,mod,residues in [(2,27,44,4,'0,3'),(3,108,210,2,'0'),(4,324,789,4,'0,1'),(5,972,2492,2,'0'),(6,2187,6459,4,'0,3')]:
    if rank>args.through_rank:break
    target=out/f'rank{rank}.json'
    with (out/f'rank{rank}_generation.log').open('w') as log:
        subprocess.run([sys.executable,'-u',str(here/'extend_flag.py'),str(parent),str(target),'--low',str(lo),'--high',str(hi),'--modulus',str(mod),'--residues',residues,'--raw-only'],stdout=log,stderr=subprocess.STDOUT,check=True)
    with (out/f'rank{rank}_dedup.log').open('w') as log:
        subprocess.run([sys.executable,'-u',str(here/'fast_deduplicate.py'),str(target)+'.raw',str(target)],stdout=log,stderr=subprocess.STDOUT,check=True)
    with (out/f'rank{rank}_maps.log').open('w') as log:
        subprocess.run([sys.executable,str(here/'verify_fast_dedup_maps.py'),str(target)+'.raw',str(target)],stdout=log,stderr=subprocess.STDOUT,check=True)
    data=json.loads(target.read_text());summary.append({'rank':rank,'raw_count':data['raw_count'],'class_count':data['class_count']})
    print('COMPLETED',summary[-1],flush=True)
    parent=target
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print('LOW_RANK_PREFIX_COMPLETE; RANKS7_TO10_NOT_COMPLETED')
