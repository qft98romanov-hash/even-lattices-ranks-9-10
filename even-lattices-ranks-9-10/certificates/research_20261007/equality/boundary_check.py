exec(open(__file__.replace('boundary_check.py','explore.py')).read().split('D=21870')[0])
from extend_flag import extend_parent
out={}
for rank,filename,target,mod,residues in [(6,'rank5_isometry_classes.json',4648,4,{0,3}),(7,'rank6_isometry_classes.json',9494,2,{0})]:
 parents=json.loads((BASE/filename).read_text())['representatives'];allc=[];stats=[];t=time.time()
 for i,g in enumerate(parents):
  children,st=extend_parent(g,target,target,mod,residues)
  allc.extend(children);stats.append(st)
  print('rank',rank,'parent',i,'children',len(children),'cumulative',len(allc),flush=True)
 out[str(rank)]={'target':target,'parent_count':len(parents),'children':allc,'stats':stats}
 Path(__file__).with_name('boundary_results.json').write_text(json.dumps(out,indent=2))
 print('BOUNDARY',rank,'children',len(allc),'seconds',time.time()-t,flush=True)
 if rank==6:assert not allc,'Need expand rank6 inputs at boundary!'
print('BOUNDARIES_CHECKED')
