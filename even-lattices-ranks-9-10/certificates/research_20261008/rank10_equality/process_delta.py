#!/usr/bin/env python3
"""Assemble all new raw cases and revived old lifting exclusions, exactly."""
from pathlib import Path
import json,sys,argparse,hashlib
from fractions import Fraction as F
R=Path(__file__).resolve().parent; OLD=R.parents[1]/'research_20261007'/'rank10'
sys.path.insert(0,str(OLD))
from exact_lattice import determinant

def read(p):return json.loads(Path(p).read_text())
def save(p,d):Path(p).write_text(json.dumps(d)+'\n')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def lifting(g,U):
 d=determinant(g);dp=determinant([row[:-1]for row in g[:-1]]);return [d,dp,3*d*d,4*dp*U]
def main():
 p=argparse.ArgumentParser();p.add_argument('--rank',type=int,required=True);a=p.parse_args();rank=a.rank
 assert rank in(7,8,9)
 oldU,newU={7:(24673,24676),8:(40054,40056),9:(54672,54675)}[rank]
 src=OLD/'early_flags'/f'rank{rank}_parents';eligible=[];origins=[];oldprunes=0;revived=[];oldraw=0
 for f in sorted(src.glob('parent_*.json')):
  x=read(f)
  for j,g in enumerate(x['representatives']):
   oldraw+=1;v=lifting(g,newU)
   if v[2]>4*v[1]*oldU:
    oldprunes+=1
    if v[2]<=v[3]:eligible.append(g);origins.append(['old',f.name,j]);revived.append([f.name,j,*v])
 newraw=0;newpruned=[];datafiles=[]
 for name in [f'rank{rank}_boundary',f'rank{rank}_from_new{rank-1}']:
  f=R/(name+'.json')
  if not f.exists():continue
  d=read(f);datafiles.append([f.name,digest(f)])
  for i,g in enumerate(d['representatives']):
   newraw+=1;v=lifting(g,newU)
   if v[2]<=v[3]:eligible.append(g);origins.append([name,i])
   else:newpruned.append([name,i,*v])
 out={'rank':rank,'old_next_upper':oldU,'new_next_upper':newU,'old_raw':oldraw,'old_prunes':oldprunes,'old_revived':revived,'new_raw':newraw,'new_pruned':newpruned,'new_eligible_count':len(eligible),'representatives':eligible,'origins':origins,'new_datafiles':datafiles,'deduplication':'NONE; duplicate raw matrices retained safely'}
 save(R/f'new_rank{rank}_parents.json',out)
 print('RANK',rank,'OLDRAW',oldraw,'REVIVED',len(revived),'NEWRAW',newraw,'NEWPRUNED',len(newpruned),'NEWELIGIBLE',len(eligible),flush=True)
 if rank==9:
  print('TERMINAL',len(eligible),'SURVIVORS',flush=True)
if __name__=='__main__':main()
