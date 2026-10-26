#!/usr/bin/env python3
"""Exact delta certificate extending the strict rank-ten flag search to equality.
Only newly admitted determinant intervals and newly revived lifting survivors
are searched. The strict-search outputs are dependencies, never overwritten.
"""
from pathlib import Path
import sys,json,hashlib,time,multiprocessing as mp,argparse
R=Path(__file__).resolve().parent
OLD=R.parents[1]/'research_20261007'/'rank10'
sys.path.insert(0,str(OLD))
from fast_extend import extend_parent
from exact_lattice import determinant

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def key(g):return tuple(map(tuple,g))
def read(p):return json.loads(Path(p).read_text())
def save(p,d):Path(p).write_text(json.dumps(d)+'\n')
def parents(name):return read(OLD/'early_flags'/name)['representatives']
def job(spec):
 name,i,g,lo,hi,mod,res=spec;out=R/'jobs'/f'{name}_{i:04d}.json';out.parent.mkdir(exist_ok=True)
 config={'name':name,'index':i,'parent_gram':g,'low':lo,'high':hi,'modulus':mod,'residues':res,'kernel_sha256':digest(OLD/'fast_extend.py')}
 if out.exists():
  obj=read(out);assert obj['config']==config;return name,i,len(obj['children']),obj['seconds'],True
 t=time.monotonic();children,stats=extend_parent(g,lo,hi,mod,set(res))
 save(out,{'config':config,'children':children,'statistics':stats,'seconds':time.monotonic()-t})
 return name,i,len(children),time.monotonic()-t,False

def batch(name,ps,lo,hi,mod,res,workers):
 specs=[(name,i,g,lo,hi,mod,res)for i,g in enumerate(ps)]
 print('START',name,len(ps),lo,hi,flush=True);s=time.monotonic();n=0
 with mp.get_context('fork').Pool(workers)as pool:
  for k,x in enumerate(pool.imap_unordered(job,specs,chunksize=1)):
   n+=x[2]
   if (k+1)%25==0 or k+1==len(specs):print('PROGRESS',name,k+1,len(specs),'children',n,'seconds',round(time.monotonic()-s,2),flush=True)
 children=[];origins=[]
 for i in range(len(ps)):
  obj=read(R/'jobs'/f'{name}_{i:04d}.json')
  children.extend(obj['children']);origins.extend([[name,i,j]for j in range(len(obj['children']))])
 out={'name':name,'parent_count':len(ps),'window':[lo,hi],'raw_count':len(children),'representatives':children,'origins':origins,'seconds':time.monotonic()-s}
 save(R/f'{name}.json',out);return children

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--workers',type=int,default=5);ap.add_argument('--stage',choices=['initial','r8','r9'],default='initial');a=ap.parse_args()
 if a.stage=='initial':
  r6=batch('rank6_boundary',parents('rank5.json'),6460,6460,4,[0,3],a.workers)
  r7=batch('rank7_boundary',parents('rank6_fast.json'),13940,13940,2,[0],a.workers)
  if r6:batch('rank7_from_new6',r6,4374,13940,2,[0],a.workers)
 elif a.stage=='r8':
  batch('rank8_boundary',parents('rank7_eligible.json'),24676,24676,4,[0,1],a.workers)
  batch('rank8_from_new7',read(R/'new_rank7_parents.json')['representatives'],6564,24676,4,[0,1],a.workers)
 elif a.stage=='r9':
  batch('rank9_boundary',parents('rank8_eligible.json'),40056,40056,2,[0],a.workers)
  batch('rank9_from_new8',read(R/'new_rank8_parents.json')['representatives'],19684,40056,2,[0],a.workers)
if __name__=='__main__':main()
