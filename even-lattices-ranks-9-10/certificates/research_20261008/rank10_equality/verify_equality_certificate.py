#!/usr/bin/env python3
"""Verify delta coverage at det54675; --replay regenerates every list afresh.
Default also verifies the complete strict base certificate without mutating it.
--skip-base is suitable only when the strict certificate was checked separately.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib,sys,time,multiprocessing as mp
R=Path(__file__).resolve().parent; OLD=R.parents[1]/'research_20261007'/'rank10'
sys.path.insert(0,str(OLD))
import verify_global_rank10_certificate as base
from exact_lattice import determinant
from fast_extend import extend_parent
from process_delta import lifting

def read(p):return json.loads(Path(p).read_text())
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):Path(p).write_text(json.dumps(d,indent=2)+'\n')
def readparents(n):return read(OLD/'early_flags'/n)['representatives']
JOBS=[];COUNTS={}
def windows():
 U={10:54675};gam={9:F(512),8:F(256),7:F(64),6:F(64,3),5:F(8),4:F(4),3:F(2),2:F(4,3)};details=[]
 for n in range(10,1,-1):
  rhs=F(2**45*U[10]**36)if n==10 else gam[n]*U[n]**(n-1);power=40 if n==10 else n
  lo=0;hi=1
  while hi**power<=rhs:hi*=2
  while hi-lo>1:
   mid=(lo+hi)//2
   if mid**power<=rhs:lo=mid
   else:hi=mid
  raw=lo;r=n-1;mod=2 if r%2 else 4;res={0}if r%2 else{0,(-1)**(r//2)%4}
  while lo%mod not in res:lo-=1
  U[r]=lo;details.append({'rank':r,'raw':raw,'upper':lo,'power':power,'rhs':str(rhs)})
 assert U=={1:6,2:44,3:210,4:789,5:2492,6:6460,7:13940,8:24676,9:40056,10:54675}
 return U,details

def check_batch(name,parents,lo,hi,mod,res):
 assembled=[];origins=[];pruned=0;active=0
 for i,g in enumerate(parents):
  f=R/'jobs'/f'{name}_{i:04d}.json';x=read(f);c=x['config'];st=x['statistics'];children=x['children']
  assert c=={'name':name,'index':i,'parent_gram':g,'low':lo,'high':hi,'modulus':mod,'residues':res,'kernel_sha256':digest(OLD/'fast_extend.py')}
  d,dp,_=base.flag(g);assert st['parent_det']==d and F(st['dual_minimum'])==F(dp,d)
  if 3*d*d>4*dp*hi:
   pruned+=1;assert st['globally_pruned'] and not children and st['discriminant_classes']==0
  else:
   active+=1;assert not st['globally_pruned'] and st['discriminant_classes']==d
   assert st['effective_low']==max(lo,-((-3*d*d)//(4*dp)))
   assert st['tested'].get('dual_shortest',0)==len(children)
  for j,h in enumerate(children):
   D,PD=base.child_record(h,g,lo,hi,mod,set(res));assert PD==d
   dd,ddp,_=base.flag(h);assert (dd,ddp)==(D,d)
   minimum,number=base.enumerate_short([[F(v)for v in row]for row in h],F(6));assert minimum==6
  JOBS.append((name,i,g,lo,hi,mod,res,children));assembled.extend(children);origins.extend([[name,i,j]for j in range(len(children))])
 data=read(R/(name+'.json'));assert data['representatives']==assembled and data['origins']==origins
 assert data['raw_count']==len(assembled) and data['parent_count']==len(parents) and data['window']==[lo,hi]
 COUNTS[name]={'parents':len(parents),'pruned_parents':pruned,'enumerated_parents':active,'raw':len(assembled)}
 print('BATCH_PASS',name,COUNTS[name],flush=True);return assembled

def process(rank,newnames):
 oldU,newU={7:(24673,24676),8:(40054,40056),9:(54672,54675)}[rank]
 eligible=[];origins=[];revived=[];pruned=[];oldraw=0;oldprunes=0;newraw=0;datafiles=[]
 for f in sorted((OLD/'early_flags'/f'rank{rank}_parents').glob('parent_*.json')):
  data=read(f)
  for j,g in enumerate(data['representatives']):
   oldraw+=1;v=lifting(g,newU)
   if v[2]>4*v[1]*oldU:
    oldprunes+=1
    if v[2]<=v[3]:eligible.append(g);origins.append(['old',f.name,j]);revived.append([f.name,j,*v])
 for name in newnames:
  f=R/(name+'.json');datafiles.append([f.name,digest(f)])
  for j,g in enumerate(read(f)['representatives']):
   newraw+=1;v=lifting(g,newU)
   if v[2]<=v[3]:eligible.append(g);origins.append([name,j])
   else:pruned.append([name,j,*v])
 expected={'rank':rank,'old_next_upper':oldU,'new_next_upper':newU,'old_raw':oldraw,'old_prunes':oldprunes,'old_revived':revived,'new_raw':newraw,'new_pruned':pruned,'new_eligible_count':len(eligible),'representatives':eligible,'origins':origins,'new_datafiles':datafiles,'deduplication':'NONE; duplicate raw matrices retained safely'}
 assert read(R/f'new_rank{rank}_parents.json')==expected
 print('DELTA_COVER_PASS',rank,'revived',len(revived),'newraw',newraw,'pruned',len(pruned),'eligible',len(eligible),flush=True)
 return eligible,expected

def replay_job(i):
 name,index,g,lo,hi,mod,res,oldchildren=JOBS[i];t=time.monotonic()
 children,statistics=extend_parent(g,lo,hi,mod,set(res)) # NEVER uses cached job output
 assert children==oldchildren,(name,index,len(children),len(oldchildren))
 obj={'name':name,'index':index,'count':len(children),'ordered_children_sha256':hashlib.sha256(json.dumps(children,separators=(',',':')).encode()).hexdigest(),'seconds':time.monotonic()-t}
 save(R/'replay_records'/f'{name}_{index:04d}.json',obj);return obj

def main():
 assert sys.flags.optimize==0,'Do not disable Python assertions'
 p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');p.add_argument('--workers',type=int,default=5);p.add_argument('--skip-base',action='store_true');a=p.parse_args();start=time.monotonic()
 manifest=read(R/'base_dependency_hashes.json')
 for rel,h in manifest.items():assert digest(OLD/rel)==h,rel
 U,details=windows()
 if not a.skip_base:
  base.check_windows();base.check_low()
  base.check_high(7,base.E/'rank6_fast.json',4374,13938,2,{0},24673)
  base.check_high(8,base.E/'rank7_eligible.json',6564,24673,4,{0,1},40054)
  base.check_low_rank9();base.check_high(9,base.E/'rank8_eligible.json',24452,40054,2,{0},54672)
 r6=check_batch('rank6_boundary',readparents('rank5.json'),6460,6460,4,[0,3])
 r7boundary=check_batch('rank7_boundary',readparents('rank6_fast.json'),13940,13940,2,[0])
 new7from6=check_batch('rank7_from_new6',r6,4374,13940,2,[0])
 new7,step7=process(7,['rank7_boundary','rank7_from_new6'])
 r8boundary=check_batch('rank8_boundary',readparents('rank7_eligible.json'),24676,24676,4,[0,1])
 r8fromnew=check_batch('rank8_from_new7',new7,6564,24676,4,[0,1])
 new8,step8=process(8,['rank8_boundary','rank8_from_new7'])
 r9boundary=check_batch('rank9_boundary',readparents('rank8_eligible.json'),40056,40056,2,[0])
 r9fromnew=check_batch('rank9_from_new8',new8,19684,40056,2,[0])
 new9,step9=process(9,['rank9_boundary','rank9_from_new8'])
 assert len(r6)==58 and len(r7boundary)==20 and len(new7from6)==0 and len(new7)==4
 assert not r8boundary and not r8fromnew and not new8 and not r9boundary and not r9fromnew and not new9
 # Every original rank9 terminal prune remains strict at the new target.
 vals=[]
 for f in sorted((OLD/'early_flags'/'rank9_parents').glob('parent_*.json')):
  for g in read(f)['representatives']:
   d,dp,left,right=lifting(g,54675);assert left>right;vals.append(F(left,4*dp))
 assert len(vals)==3819 and min(vals)==F(12966723,212)>54675
 report={'status':'PASS_STATIC_EQUALITY_CERTIFICATE','theorem':'Under gamma9<=2, every even integral rank10 lattice of minimum>=6 and determinant54675 contains sqrt3E8; exactly two isometry types by archived E8 classification.','base_checked_this_run':not a.skip_base,'base_dependency_files':len(manifest),'windows':details,'batches':COUNTS,'revived_rank7':step7['old_revived'],'old_rank9_count':len(vals),'old_terminal_least_bound':str(min(vals)),'non_E8_equality_survivors':0,'full_replay_performed':False}
 if a.replay:
  (R/'replay_records').mkdir(exist_ok=True);rt=time.monotonic();done=0;raw=0
  with mp.get_context('fork').Pool(a.workers)as pool:
   for x in pool.imap_unordered(replay_job,range(len(JOBS)),chunksize=1):
    done+=1;raw+=x['count']
    if done%250==0 or done==len(JOBS):print('REPLAY',done,len(JOBS),'raw',raw,'seconds',round(time.monotonic()-rt,2),flush=True)
  report.update(status='PASS_FULL_EQUALITY_REPLAY',full_replay_performed=True,replay_jobs=done,replay_raw_candidates=raw,replay_seconds=time.monotonic()-rt)
 report['seconds']=time.monotonic()-start
 save(R/'equality_certificate_verified.json',report)
 if a.replay:save(R/'equality_full_replay_record.json',report)
 print('GLOBAL_RANK10_EQUALITY_TWO_TYPES_PASS',report['status'],'UNDER gamma9<=2',flush=True)
if __name__=='__main__':main()
